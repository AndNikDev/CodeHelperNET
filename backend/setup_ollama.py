#!/usr/bin/env python3
"""
Script para configurar Ollama automáticamente
"""

import subprocess
import sys
import requests
import time
import os

def check_ollama_installed():
    """Verificar si Ollama está instalado"""
    try:
        result = subprocess.run(['ollama', '--version'], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def install_ollama():
    """Instalar Ollama"""
    print("🔧 Instalando Ollama...")
    
    # Detectar el sistema operativo
    import platform
    system = platform.system().lower()
    
    if system == "linux":
        # Instalar en Linux
        try:
            subprocess.run([
                "curl", "-fsSL", "https://ollama.ai/install.sh", "|", "sh"
            ], shell=True, check=True)
            print("✅ Ollama instalado en Linux")
            return True
        except subprocess.CalledProcessError:
            print("❌ Error instalando Ollama en Linux")
            return False
    
    elif system == "darwin":  # macOS
        try:
            subprocess.run([
                "curl", "-fsSL", "https://ollama.ai/install.sh", "|", "sh"
            ], shell=True, check=True)
            print("✅ Ollama instalado en macOS")
            return True
        except subprocess.CalledProcessError:
            print("❌ Error instalando Ollama en macOS")
            return False
    
    elif system == "windows":
        print("⚠️  Para Windows, instala Ollama manualmente desde: https://ollama.ai")
        return False
    
    else:
        print(f"⚠️  Sistema operativo no soportado: {system}")
        return False

def check_ollama_running():
    """Verificar si Ollama está ejecutándose"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        return response.status_code == 200
    except:
        return False

def start_ollama():
    """Iniciar Ollama"""
    print("🚀 Iniciando Ollama...")
    
    try:
        # Iniciar Ollama en segundo plano
        subprocess.Popen(['ollama', 'serve'], 
                        stdout=subprocess.DEVNULL, 
                        stderr=subprocess.DEVNULL)
        
        # Esperar a que inicie
        for i in range(30):  # Esperar hasta 30 segundos
            if check_ollama_running():
                print("✅ Ollama iniciado correctamente")
                return True
            time.sleep(1)
        
        print("❌ Ollama no pudo iniciarse")
        return False
        
    except Exception as e:
        print(f"❌ Error iniciando Ollama: {e}")
        return False

def download_model(model_name="llama2"):
    """Descargar modelo de Ollama"""
    print(f"📥 Descargando modelo {model_name}...")
    
    try:
        subprocess.run(['ollama', 'pull', model_name], check=True)
        print(f"✅ Modelo {model_name} descargado correctamente")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ Error descargando modelo {model_name}")
        return False

def test_ollama():
    """Probar Ollama"""
    print("🧪 Probando Ollama...")
    
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama2",
                "prompt": "Hola, ¿cómo estás?",
                "stream": False
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get("response"):
                print("✅ Ollama funciona correctamente")
                return True
        
        print("❌ Ollama no responde correctamente")
        return False
        
    except Exception as e:
        print(f"❌ Error probando Ollama: {e}")
        return False

def main():
    """Función principal"""
    print("🤖 Configurando Ollama para CodeHelperNET")
    print("=" * 50)
    
    # Verificar si Ollama está instalado
    if not check_ollama_installed():
        print("📦 Ollama no está instalado")
        if not install_ollama():
            print("\n💡 Instalación manual:")
            print("1. Ve a https://ollama.ai")
            print("2. Descarga e instala Ollama para tu sistema")
            print("3. Ejecuta este script nuevamente")
            return False
    
    print("✅ Ollama está instalado")
    
    # Verificar si Ollama está ejecutándose
    if not check_ollama_running():
        print("🔄 Ollama no está ejecutándose")
        if not start_ollama():
            print("\n💡 Para iniciar Ollama manualmente:")
            print("1. Abre una terminal")
            print("2. Ejecuta: ollama serve")
            print("3. En otra terminal, ejecuta: ollama run llama2")
            return False
    
    print("✅ Ollama está ejecutándose")
    
    # Descargar modelo si es necesario
    try:
        subprocess.run(['ollama', 'list'], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        if not download_model():
            print("\n💡 Para descargar el modelo manualmente:")
            print("ollama pull llama2")
            return False
    
    # Probar Ollama
    if test_ollama():
        print("\n🎉 ¡Ollama está configurado correctamente!")
        print("\n💡 Ahora puedes ejecutar CodeHelperNET:")
        print("python rag_chatbot.py")
        return True
    else:
        print("\n❌ Ollama no está funcionando correctamente")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 