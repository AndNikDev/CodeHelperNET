#!/bin/bash

# Script de instalación completa para CodeHelperNET con Ollama
# Para Linux/macOS

set -e  # Salir si hay algún error

echo "🤖 Instalando CodeHelperNET con Ollama"
echo "======================================"

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para imprimir con colores
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verificar si Python está instalado
print_status "Verificando Python..."
if ! command -v python3 &> /dev/null; then
    print_error "Python3 no está instalado. Por favor instálalo primero."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
print_success "Python $PYTHON_VERSION encontrado"

# Verificar si pip está instalado
print_status "Verificando pip..."
if ! command -v pip3 &> /dev/null; then
    print_error "pip3 no está instalado. Por favor instálalo primero."
    exit 1
fi

print_success "pip3 encontrado"

# Instalar dependencias de Python
print_status "Instalando dependencias de Python..."
pip3 install -r requirements_complete.txt

if [ $? -eq 0 ]; then
    print_success "Dependencias de Python instaladas correctamente"
else
    print_error "Error instalando dependencias de Python"
    exit 1
fi

# Verificar si Ollama está instalado
print_status "Verificando Ollama..."
if ! command -v ollama &> /dev/null; then
    print_warning "Ollama no está instalado. Instalando..."
    
    # Instalar Ollama
    curl -fsSL https://ollama.ai/install.sh | sh
    
    if [ $? -eq 0 ]; then
        print_success "Ollama instalado correctamente"
    else
        print_error "Error instalando Ollama"
        exit 1
    fi
else
    print_success "Ollama ya está instalado"
fi

# Iniciar Ollama
print_status "Iniciando Ollama..."
ollama serve &
OLLAMA_PID=$!

# Esperar a que Ollama inicie
sleep 5

# Verificar si Ollama está ejecutándose
if curl -s http://localhost:11434/api/tags > /dev/null; then
    print_success "Ollama está ejecutándose"
else
    print_warning "Ollama no responde, intentando iniciar..."
    sleep 10
    
    if curl -s http://localhost:11434/api/tags > /dev/null; then
        print_success "Ollama iniciado correctamente"
    else
        print_error "No se pudo iniciar Ollama"
        exit 1
    fi
fi

# Verificar si el modelo llama2 está descargado
print_status "Verificando modelo llama2..."
if ollama list | grep -q "llama2"; then
    print_success "Modelo llama2 ya está descargado"
else
    print_warning "Descargando modelo llama2..."
    ollama pull llama2
    
    if [ $? -eq 0 ]; then
        print_success "Modelo llama2 descargado correctamente"
    else
        print_error "Error descargando modelo llama2"
        exit 1
    fi
fi

# Probar el chatbot
print_status "Probando el chatbot..."
python3 test_ollama.py

if [ $? -eq 0 ]; then
    print_success "Chatbot funciona correctamente"
else
    print_warning "Chatbot tiene problemas, pero la instalación básica está completa"
fi

# Hacer los scripts ejecutables
chmod +x start_chatbot.py
chmod +x setup_ollama.py
chmod +x test_ollama.py

print_success "Instalación completada"
echo ""
echo "🎉 ¡CodeHelperNET está listo para usar!"
echo ""
echo "💡 Comandos útiles:"
echo "  python3 start_chatbot.py    - Iniciar el chatbot"
echo "  python3 test_ollama.py      - Probar el sistema"
echo "  ollama serve                - Iniciar Ollama manualmente"
echo "  ollama list                 - Ver modelos disponibles"
echo ""
echo "📚 Documentación: README_OLLAMA.md"
echo ""

# Limpiar proceso de Ollama si lo iniciamos
if [ ! -z "$OLLAMA_PID" ]; then
    kill $OLLAMA_PID 2>/dev/null || true
fi 