#!/usr/bin/env python3
"""
Script para iniciar CodeHelperNET completo (Backend + Frontend)
"""

import subprocess
import sys
import os
import time
import requests
import threading
from pathlib import Path

def check_ollama():
    """Verificar si Ollama está ejecutándose"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        return response.status_code == 200
    except:
        return False

def start_ollama():
    """Iniciar Ollama si no está ejecutándose"""
    if not check_ollama():
        print("🚀 Iniciando Ollama...")
        try:
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
            print(f"❌ Error iniciando Ollama: {e}")
            return False
    else:
        print("✅ Ollama ya está ejecutándose")
        return True

def start_backend():
    """Iniciar el servidor backend"""
    print("🚀 Iniciando servidor backend...")
    backend_dir = Path(__file__).parent / "backend"
    
    try:
        # Cambiar al directorio del backend
        os.chdir(backend_dir)
        
        # Iniciar el servidor Flask
        process = subprocess.Popen([
            sys.executable, "api_server.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Esperar un poco para que inicie
        time.sleep(3)
        
        # Verificar si está funcionando
        try:
            response = requests.get("http://localhost:5000/health", timeout=5)
            if response.status_code == 200:
                print("✅ Backend iniciado correctamente")
                return process
            else:
                print("❌ Backend no responde correctamente")
                return None
        except:
            print("❌ Backend no está disponible")
            return None
            
    except Exception as e:
        print(f"❌ Error iniciando backend: {e}")
        return None

def start_frontend():
    """Iniciar el servidor frontend"""
    print("🚀 Iniciando servidor frontend...")
    frontend_dir = Path(__file__).parent / "frontend"
    
    try:
        # Cambiar al directorio del frontend
        os.chdir(frontend_dir)
        
        # Verificar si node_modules existe
        if not (frontend_dir / "node_modules").exists():
            print("📦 Instalando dependencias del frontend...")
            subprocess.run(["npm", "install"], check=True)
        
        # Iniciar el servidor de desarrollo
        process = subprocess.Popen([
            "npm", "run", "dev"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Esperar un poco para que inicie
        time.sleep(5)
        
        # Verificar si está funcionando
        try:
            response = requests.get("http://localhost:3000", timeout=5)
            if response.status_code == 200:
                print("✅ Frontend iniciado correctamente")
                return process
            else:
                print("❌ Frontend no responde correctamente")
                return None
        except:
            print("❌ Frontend no está disponible")
            return None
            
    except Exception as e:
        print(f"❌ Error iniciando frontend: {e}")
        return None

def monitor_processes(backend_process, frontend_process):
    """Monitorear los procesos y mostrar logs"""
    print("\n📊 Monitoreando servicios...")
    print("💡 Presiona Ctrl+C para detener todos los servicios")
    
    try:
        while True:
            # Verificar si los procesos siguen ejecutándose
            if backend_process and backend_process.poll() is not None:
                print("❌ Backend se detuvo")
                break
                
            if frontend_process and frontend_process.poll() is not None:
                print("❌ Frontend se detuvo")
                break
                
            time.sleep(5)
            
    except KeyboardInterrupt:
        print("\n🛑 Deteniendo servicios...")
        
        # Detener procesos
        if backend_process:
            backend_process.terminate()
            print("✅ Backend detenido")
            
        if frontend_process:
            frontend_process.terminate()
            print("✅ Frontend detenido")

def main():
    """Función principal"""
    print("🤖 CodeHelperNET - Iniciando Stack Completo")
    print("=" * 50)
    
    # Verificar Ollama
    if not start_ollama():
        print("❌ No se pudo iniciar Ollama. Saliendo...")
        return False
    
    # Iniciar backend
    backend_process = start_backend()
    if not backend_process:
        print("❌ No se pudo iniciar el backend. Saliendo...")
        return False
    
    # Iniciar frontend
    frontend_process = start_frontend()
    if not frontend_process:
        print("❌ No se pudo iniciar el frontend. Saliendo...")
        backend_process.terminate()
        return False
    
    print("\n🎉 ¡CodeHelperNET está listo!")
    print("📱 Frontend: http://localhost:3000")
    print("🔧 Backend: http://localhost:5000")
    print("🤖 Ollama: http://localhost:11434")
    
    # Monitorear procesos
    monitor_processes(backend_process, frontend_process)
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 