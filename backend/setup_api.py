#!/usr/bin/env python3
"""
Script para configurar APIs externas para CodeHelperNET
"""

import os
import requests
from dotenv import load_dotenv

def setup_huggingface():
    """Configurar Hugging Face API"""
    print("🔧 Configurando Hugging Face API...")
    print("\nPara obtener una API key gratuita:")
    print("1. Ve a https://huggingface.co/join")
    print("2. Crea una cuenta gratuita")
    print("3. Ve a https://huggingface.co/settings/tokens")
    print("4. Haz clic en 'New token'")
    print("5. Dale un nombre (ej: 'CodeHelperNET')")
    print("6. Selecciona 'Read' como rol")
    print("7. Copia el token generado")
    
    api_key = input("\nPega tu API key aquí (o presiona Enter para saltar): ").strip()
    
    if api_key:
        # Probar la API key
        headers = {"Authorization": f"Bearer {api_key}"}
        try:
            response = requests.get(
                "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                print("✅ API key válida!")
                
                # Guardar en config.env
                config_content = f"""# Configuración de APIs externas para CodeHelperNET

# Hugging Face Inference API (gratuita)
HF_API_KEY={api_key}

# Configuración de Ollama (opcional, local)
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama2

# Configuración del servidor
PORT=5000
FLASK_ENV=production"""
                
                with open('config.env', 'w') as f:
                    f.write(config_content)
                
                print("✅ Configuración guardada en config.env")
                return True
            else:
                print("❌ API key inválida o error en la API")
                return False
                
        except Exception as e:
            print(f"❌ Error probando API key: {e}")
            return False
    else:
        print("⏭️ Saltando configuración de Hugging Face")
        return False

def test_apis():
    """Probar las APIs configuradas"""
    print("\n🧪 Probando APIs configuradas...")
    
    load_dotenv('config.env')
    hf_api_key = os.environ.get("HF_API_KEY", "")
    
    if hf_api_key:
        print("✅ Hugging Face API configurada")
        
        # Probar con una pregunta simple
        headers = {"Authorization": f"Bearer {hf_api_key}"}
        payload = {
            "inputs": "¿Qué es C#?",
            "parameters": {
                "max_length": 50,
                "temperature": 0.7
            }
        }
        
        try:
            response = requests.post(
                "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                print("✅ API funcionando correctamente")
            else:
                print(f"❌ Error en API: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error probando API: {e}")
    else:
        print("❌ Hugging Face API no configurada")

def main():
    print("🚀 Configuración de APIs para CodeHelperNET")
    print("=" * 50)
    
    # Verificar si ya existe config.env
    if os.path.exists('config.env'):
        print("📁 Archivo config.env encontrado")
        response = input("¿Quieres reconfigurar las APIs? (s/n): ").lower()
        if response != 's':
            test_apis()
            return
    
    # Configurar APIs
    setup_huggingface()
    test_apis()
    
    print("\n🎉 Configuración completada!")
    print("\nPara usar el chatbot mejorado:")
    print("1. Ejecuta: python3 api_server.py")
    print("2. Prueba con: curl -X POST http://localhost:5000/chat -H 'Content-Type: application/json' -d '{\"message\": \"¿Qué es un bucle for en C#?\"}'")

if __name__ == "__main__":
    main() 