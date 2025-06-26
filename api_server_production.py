import os
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from rag_chatbot import RAGChatbot
import traceback

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Habilitar CORS para el frontend

# Variables de entorno para producción
PORT = int(os.environ.get('PORT', 5000))
DEBUG = os.environ.get('FLASK_ENV') == 'development'

# Inicializar chatbot
chatbot = None

@app.before_first_request
def initialize_chatbot():
    """Inicializar el chatbot antes del primer request"""
    global chatbot
    try:
        logger.info("Inicializando CodeHelperNET chatbot...")
        chatbot = RAGChatbot()
        logger.info("Chatbot inicializado exitosamente")
    except Exception as e:
        logger.error(f"Error inicializando chatbot: {e}")
        logger.error(traceback.format_exc())

@app.route('/')
def home():
    """Endpoint de salud"""
    return jsonify({
        "status": "ok",
        "message": "CodeHelperNET API está funcionando",
        "version": "1.0.0"
    })

@app.route('/health')
def health():
    """Endpoint de salud para monitoreo"""
    return jsonify({
        "status": "healthy",
        "chatbot_ready": chatbot is not None
    })

@app.route('/chat', methods=['POST'])
def chat():
    """Endpoint principal del chat"""
    try:
        if chatbot is None:
            return jsonify({
                "error": "Chatbot no inicializado",
                "message": "El chatbot aún se está inicializando. Intenta de nuevo en unos segundos."
            }), 503
        
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({
                "error": "Mensaje requerido",
                "message": "Debes enviar un mensaje en el campo 'message'"
            }), 400
        
        message = data['message'].strip()
        
        if not message:
            return jsonify({
                "error": "Mensaje vacío",
                "message": "El mensaje no puede estar vacío"
            }), 400
        
        logger.info(f"Mensaje recibido: {message[:50]}...")
        
        # Procesar mensaje con el chatbot
        response = chatbot.chat(message)
        
        logger.info(f"Respuesta generada: {len(response)} caracteres")
        
        return jsonify({
            "response": response,
            "status": "success"
        })
        
    except Exception as e:
        logger.error(f"Error procesando mensaje: {e}")
        logger.error(traceback.format_exc())
        
        return jsonify({
            "error": "Error interno del servidor",
            "message": "Ocurrió un error procesando tu mensaje. Por favor, intenta de nuevo."
        }), 500

@app.route('/api/chat', methods=['POST'])
def api_chat():
    """Endpoint alternativo para compatibilidad con frontend"""
    return chat()

if __name__ == '__main__':
    logger.info(f"Iniciando servidor en puerto {PORT}")
    logger.info(f"Modo debug: {DEBUG}")
    
    # Inicializar chatbot inmediatamente
    initialize_chatbot()
    
    app.run(
        host='0.0.0.0',
        port=PORT,
        debug=DEBUG
    ) 