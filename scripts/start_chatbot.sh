#!/bin/bash

echo "========================================"
echo "   CodeHelperNET - Chatbot C# y .NET"
echo "========================================"
echo

echo "Iniciando CodeHelperNET..."
echo

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 no está instalado"
    echo "Por favor instala Python 3.8+ desde https://python.org"
    exit 1
fi

# Verificar si Node.js está instalado
if ! command -v node &> /dev/null; then
    echo "ERROR: Node.js no está instalado"
    echo "Por favor instala Node.js 18+ desde https://nodejs.org"
    exit 1
fi

# Verificar si el entorno virtual existe
if [ ! -f "codehelper_env/bin/activate" ]; then
    echo "Creando entorno virtual..."
    python3 -m venv codehelper_env
    if [ $? -ne 0 ]; then
        echo "ERROR: No se pudo crear el entorno virtual"
        exit 1
    fi
fi

# Verificar si las dependencias están instaladas
if [ ! -d "codehelper_env/lib/python3.10/site-packages/flask" ]; then
    echo "Instalando dependencias de Python..."
    source codehelper_env/bin/activate
    pip install -r backend/requirements.txt
    if [ $? -ne 0 ]; then
        echo "ERROR: No se pudieron instalar las dependencias"
        exit 1
    fi
fi

# Verificar si la base de datos vectorial existe
if [ ! -d "backend/vector_db" ]; then
    echo "Generando base de datos vectorial..."
source codehelper_env/bin/activate
    cd backend
    python improved_vector_db.py
    if [ $? -ne 0 ]; then
        echo "ERROR: No se pudo generar la base de datos vectorial"
    exit 1
fi
    cd ..
fi

# Verificar si las dependencias del frontend están instaladas
if [ ! -d "frontend/node_modules" ]; then
    echo "Instalando dependencias del frontend..."
cd frontend
    npm install
    if [ $? -ne 0 ]; then
        echo "ERROR: No se pudieron instalar las dependencias del frontend"
        exit 1
    fi
    cd ..
fi

echo
echo "========================================"
echo "    Iniciando servicios..."
echo "========================================"
echo

# Iniciar el backend en una nueva terminal
echo "Iniciando backend (puerto 5000)..."
gnome-terminal -- bash -c "source codehelper_env/bin/activate && cd backend && python api_server.py; exec bash" 2>/dev/null || \
xterm -e "source codehelper_env/bin/activate && cd backend && python api_server.py; exec bash" 2>/dev/null || \
konsole -e "source codehelper_env/bin/activate && cd backend && python api_server.py; exec bash" 2>/dev/null || \
echo "No se pudo abrir una nueva terminal. Ejecuta manualmente: source codehelper_env/bin/activate && cd backend && python api_server.py"

# Esperar un momento para que el backend se inicie
sleep 3

# Iniciar el frontend en una nueva terminal
echo "Iniciando frontend (puerto 3000)..."
gnome-terminal -- bash -c "cd frontend && npm run dev; exec bash" 2>/dev/null || \
xterm -e "cd frontend && npm run dev; exec bash" 2>/dev/null || \
konsole -e "cd frontend && npm run dev; exec bash" 2>/dev/null || \
echo "No se pudo abrir una nueva terminal. Ejecuta manualmente: cd frontend && npm run dev"

echo
echo "========================================"
echo "    Servicios iniciados correctamente"
echo "========================================"
echo
echo "Backend:  http://localhost:5000"
echo "Frontend: http://localhost:3000"
echo
echo "Presiona cualquier tecla para abrir el frontend en tu navegador..."
read -n 1

# Abrir el navegador
xdg-open http://localhost:3000 2>/dev/null || \
open http://localhost:3000 2>/dev/null || \
start http://localhost:3000 2>/dev/null || \
echo "No se pudo abrir el navegador automáticamente. Abre manualmente: http://localhost:3000"

echo
echo "¡CodeHelperNET está listo para usar!"
echo
echo "Para detener los servicios, cierra las ventanas de terminal"
echo "o presiona Ctrl+C en cada una."
echo
read -p "Presiona Enter para salir..." 