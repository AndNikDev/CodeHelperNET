#!/usr/bin/env python3
"""
Servidor API para CodeHelperNET con Ollama
Expone el chatbot RAG como una API REST
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os
import logging
from datetime import datetime
from dotenv import load_dotenv
import requests

# Cargar variables de entorno
load_dotenv('config.env')

# Agregar el directorio actual al path para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importar el chatbot
from rag_chatbot import RAGChatbot

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Habilitar CORS para el frontend

# Inicializar el chatbot
chatbot = None

def check_ollama_status():
    """Verificar el estado de Ollama"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get('models', [])
            return {
                'status': 'running',
                'models': [model['name'] for model in models],
                'model_count': len(models)
            }
        else:
            return {'status': 'error', 'message': f'HTTP {response.status_code}'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

def initialize_chatbot():
    """Inicializar el chatbot RAG"""
    global chatbot
    try:
        logger.info("Inicializando CodeHelperNET chatbot...")
        chatbot = RAGChatbot()
        logger.info("Chatbot inicializado exitosamente")
        return True
    except Exception as e:
        logger.error(f"Error inicializando chatbot: {e}")
        return False

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint de salud del servidor"""
    ollama_status = check_ollama_status()
    
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'chatbot_ready': chatbot is not None,
        'ollama': ollama_status,
        'version': '2.0.0',
        'backend': 'Ollama + RAG'
    })

@app.route('/chat', methods=['POST'])
def chat():
    """Endpoint principal para el chat"""
    try:
        # Verificar que el chatbot esté inicializado
        if chatbot is None:
            return jsonify({
                'error': 'Chatbot no inicializado',
                'message': 'El servidor está iniciando, por favor espera un momento.'
            }), 503

        # Obtener el mensaje del request
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({
                'error': 'Mensaje requerido',
                'message': 'Debes enviar un mensaje en el campo "message"'
            }), 400

        user_message = data['message'].strip()
        if not user_message:
            return jsonify({
                'error': 'Mensaje vacío',
                'message': 'El mensaje no puede estar vacío'
            }), 400

        logger.info(f"Mensaje recibido: {user_message[:100]}...")

        # Procesar el mensaje con el chatbot
        response = chatbot.chat(user_message)
        
        logger.info(f"Respuesta generada: {len(response)} caracteres")

        return jsonify({
            'response': response,
            'timestamp': datetime.now().isoformat(),
            'backend': 'Ollama + RAG'
        })

    except Exception as e:
        logger.error(f"Error procesando mensaje: {e}")
        return jsonify({
            'error': 'Error interno del servidor',
            'message': 'Ocurrió un error procesando tu mensaje. Por favor, intenta de nuevo.',
            'details': str(e)
        }), 500

@app.route('/ollama/status', methods=['GET'])
def ollama_status():
    """Endpoint para verificar el estado de Ollama"""
    status = check_ollama_status()
    return jsonify(status)

@app.route('/ollama/models', methods=['GET'])
def ollama_models():
    """Endpoint para listar modelos disponibles"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get('models', [])
            return jsonify({
                'models': models,
                'count': len(models)
            })
        else:
            return jsonify({
                'error': 'No se pudo obtener la lista de modelos',
                'status_code': response.status_code
            }), 500
    except Exception as e:
        return jsonify({
            'error': 'Error conectando con Ollama',
            'message': str(e)
        }), 500

@app.route('/info', methods=['GET'])
def get_info():
    """Endpoint para obtener información del chatbot"""
    if chatbot is None:
        return jsonify({
            'error': 'Chatbot no inicializado'
        }), 503

    ollama_status = check_ollama_status()

    return jsonify({
        'name': 'CodeHelperNET',
        'description': 'Asistente especializado en C# y .NET con Ollama',
        'version': '2.0.0',
        'backend': 'Ollama + RAG',
        'ollama_status': ollama_status,
        'topics': [
            'C# Fundamentals',
            'ASP.NET Core',
            'Entity Framework',
            'Design Patterns',
            'Testing',
            'Security',
            'Performance',
            'Cloud Development',
            'Microservices',
            'DevOps'
        ],
        'documents_count': len(chatbot.collection.get()['documents']) if hasattr(chatbot, 'collection') else 0
    })

@app.route('/test', methods=['POST'])
def test_chat():
    """Endpoint de prueba para verificar el funcionamiento"""
    try:
        test_message = "¿Cómo crear un bucle for en C#?"
        logger.info("Ejecutando prueba con mensaje de ejemplo...")
        
        if chatbot is None:
            return jsonify({
                'error': 'Chatbot no inicializado'
            }), 503

        response = chatbot.chat(test_message)
        
        return jsonify({
            'test_message': test_message,
            'response': response,
            'response_length': len(response),
            'success': True,
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"Error en prueba: {e}")
        return jsonify({
            'error': 'Error en prueba',
            'message': str(e),
            'success': False
        }), 500

@app.errorhandler(404)
def not_found(error):
    """Manejar rutas no encontradas"""
    return jsonify({
        'error': 'Endpoint no encontrado',
        'message': 'La ruta solicitada no existe'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Manejar errores internos"""
    return jsonify({
        'error': 'Error interno del servidor',
        'message': 'Ocurrió un error inesperado'
    }), 500

if __name__ == '__main__':
    # Inicializar el chatbot al arrancar
    if not initialize_chatbot():
        logger.error("No se pudo inicializar el chatbot. Saliendo...")
        sys.exit(1)

    # Verificar Ollama
    ollama_status = check_ollama_status()
    if ollama_status['status'] == 'running':
        logger.info(f"Ollama está ejecutándose con {ollama_status['model_count']} modelos")
    else:
        logger.warning(f"Ollama no está disponible: {ollama_status['message']}")

    # Configurar el servidor
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    logger.info(f"Iniciando servidor en puerto {port}")
    logger.info(f"Modo debug: {debug}")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug,
        threaded=True
    ) 