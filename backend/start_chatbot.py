#!/usr/bin/env python3
"""
Script de inicio para CodeHelperNET con Ollama
"""

import os
import sys
import subprocess
import requests
import time

def check_ollama():
    """Verificar si Ollama está ejecutándose"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        return response.status_code == 200
    except:
        return False

def start_ollama_if_needed():
    """Iniciar Ollama si no está ejecutándose"""
    if not check_ollama():
        print("🚀 Iniciando Ollama...")
        try:
            # Iniciar Ollama en segundo plano
            subprocess.Popen(['ollama', 'serve'], 
                            stdout=subprocess.DEVNULL, 
                            stderr=subprocess.DEVNULL)
            
            # Esperar a que inicie
            for i in range(30):
                if check_ollama():
                    print("✅ Ollama iniciado")
                    return True
                time.sleep(1)
            
            print("❌ No se pudo iniciar Ollama")
            return False
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    return True

def main():
    """Función principal"""
    print("🤖 CodeHelperNET - Asistente de C# y .NET")
    print("=" * 50)
    
    # Verificar Ollama
    if not start_ollama_if_needed():
        print("\n💡 Para usar CodeHelperNET:")
        print("1. Instala Ollama: https://ollama.ai")
        print("2. Ejecuta: ollama serve")
        print("3. Ejecuta: ollama pull llama2")
        print("4. Vuelve a ejecutar este script")
        return
    
    # Importar y ejecutar el chatbot
    try:
        from rag_chatbot import main as chatbot_main
        chatbot_main()
    except ImportError as e:
        print(f"❌ Error importando el chatbot: {e}")
        print("💡 Asegúrate de tener todas las dependencias instaladas:")
        print("pip install -r requirements_complete.txt")
    except Exception as e:
        print(f"❌ Error ejecutando el chatbot: {e}")

if __name__ == "__main__":
    main() 