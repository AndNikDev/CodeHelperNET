#!/usr/bin/env python3
"""
Script de prueba para verificar que Ollama funciona con CodeHelperNET
"""

import requests
import time

def test_ollama_connection():
    """Probar conexión con Ollama"""
    print("🔍 Probando conexión con Ollama...")
    
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ Ollama está ejecutándose")
            return True
        else:
            print(f"❌ Ollama responde con código: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ No se puede conectar a Ollama: {e}")
        return False

def test_ollama_generation():
    """Probar generación de texto con Ollama"""
    print("🧪 Probando generación de texto...")
    
    try:
        payload = {
            "model": "llama2",
            "prompt": "Eres un experto en C#. Explica brevemente qué es un bucle for.",
            "stream": False,
            "options": {
                "temperature": 0.7,
                "num_predict": 100
            }
        }
        
        response = requests.post(
            "http://localhost:11434/api/generate",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            response_text = result.get("response", "")
            if response_text:
                print("✅ Ollama genera texto correctamente")
                print(f"📝 Respuesta de prueba: {response_text[:100]}...")
                return True
            else:
                print("❌ Ollama no generó texto")
                return False
        else:
            print(f"❌ Error en generación: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error probando generación: {e}")
        return False

def test_chatbot():
    """Probar el chatbot completo"""
    print("🤖 Probando chatbot completo...")
    
    try:
        from rag_chatbot import RAGChatbot
        
        chatbot = RAGChatbot()
        print("✅ Chatbot inicializado correctamente")
        
        # Probar una pregunta simple
        question = "¿Cómo crear un bucle for en C#?"
        print(f"❓ Pregunta de prueba: {question}")
        
        response = chatbot.chat(question)
        
        if response and len(response) > 20:
            print("✅ Chatbot responde correctamente")
            print(f"📝 Respuesta: {response[:200]}...")
            return True
        else:
            print("❌ Chatbot no generó respuesta válida")
            return False
            
    except Exception as e:
        print(f"❌ Error probando chatbot: {e}")
        return False

def main():
    """Función principal de pruebas"""
    print("🧪 Pruebas de CodeHelperNET con Ollama")
    print("=" * 50)
    
    # Prueba 1: Conexión con Ollama
    if not test_ollama_connection():
        print("\n💡 Para solucionar:")
        print("1. Instala Ollama: https://ollama.ai")
        print("2. Ejecuta: ollama serve")
        print("3. Ejecuta: ollama pull llama2")
        return False
    
    # Prueba 2: Generación de texto
    if not test_ollama_generation():
        print("\n💡 Para solucionar:")
        print("1. Verifica que el modelo llama2 esté descargado")
        print("2. Ejecuta: ollama pull llama2")
        return False
    
    # Prueba 3: Chatbot completo
    if not test_chatbot():
        print("\n💡 Para solucionar:")
        print("1. Verifica las dependencias: pip install -r requirements_complete.txt")
        print("2. Asegúrate de que la base de datos vectorial esté disponible")
        return False
    
    print("\n🎉 ¡Todas las pruebas pasaron!")
    print("✅ CodeHelperNET está listo para usar")
    print("\n💡 Para usar el chatbot:")
    print("python3 start_chatbot.py")
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 