#!/bin/bash

echo "🚀 Preparando CodeHelperNET para despliegue..."

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para mostrar mensajes
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

# Verificar que estamos en el directorio correcto
if [ ! -f "rag_chatbot.py" ]; then
    print_error "No se encontró rag_chatbot.py. Asegúrate de estar en el directorio raíz del proyecto."
    exit 1
fi

print_status "Verificando estructura del proyecto..."

# Verificar archivos necesarios
required_files=(
    "rag_chatbot.py"
    "api_server_production.py"
    "requirements_production.txt"
    "Procfile"
    "runtime.txt"
    "frontend/package.json"
    "frontend/next.config.js"
)

for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        print_error "Archivo requerido no encontrado: $file"
        exit 1
    fi
done

print_success "Estructura del proyecto verificada"

# Verificar que la base de datos vectorial existe
if [ ! -d "vector_db" ]; then
    print_warning "Base de datos vectorial no encontrada. Generando..."
    source codehelper_env/bin/activate
    python improved_vector_db.py
    if [ $? -ne 0 ]; then
        print_error "Error generando la base de datos vectorial"
        exit 1
    fi
    print_success "Base de datos vectorial generada"
fi

# Verificar dependencias del frontend
print_status "Verificando dependencias del frontend..."
cd frontend
if [ ! -d "node_modules" ]; then
    print_warning "Instalando dependencias del frontend..."
    npm install
    if [ $? -ne 0 ]; then
        print_error "Error instalando dependencias del frontend"
        exit 1
    fi
fi

# Construir el frontend
print_status "Construyendo el frontend..."
npm run build
if [ $? -ne 0 ]; then
    print_error "Error construyendo el frontend"
    exit 1
fi
cd ..

print_success "Frontend construido correctamente"

# Crear archivo .env.example para referencia
print_status "Creando archivo .env.example..."
cat > .env.example << EOF
# Variables de entorno para producción
FLASK_ENV=production
PORT=5000
PYTHON_BACKEND_URL=https://tu-backend-url.railway.app

# Variables para el frontend
NEXT_PUBLIC_API_URL=/api
EOF

print_success "Archivo .env.example creado"

# Crear archivo de configuración para Vercel
print_status "Creando configuración para Vercel..."
cat > vercel.json << EOF
{
  "version": 2,
  "builds": [
    {
      "src": "frontend/package.json",
      "use": "@vercel/next"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "https://tu-backend-url.railway.app/api/\$1"
    },
    {
      "src": "/(.*)",
      "dest": "/frontend/\$1"
    }
  ],
  "env": {
    "PYTHON_BACKEND_URL": "https://tu-backend-url.railway.app"
  }
}
EOF

print_success "Configuración de Vercel creada"

# Crear README de despliegue
print_status "Creando README de despliegue..."
cat > DEPLOYMENT_README.md << EOF
# 🚀 Despliegue de CodeHelperNET

## Configuración Rápida

### 1. Backend (Railway)
1. Ve a [railway.app](https://railway.app)
2. Conecta tu repositorio de GitHub
3. Configura variables de entorno:
   - \`FLASK_ENV=production\`
   - \`PORT=5000\`
4. Railway usará automáticamente:
   - \`requirements_production.txt\`
   - \`Procfile\`
   - \`api_server_production.py\`

### 2. Frontend (Vercel)
1. Ve a [vercel.com](https://vercel.com)
2. Importa tu repositorio
3. Configura variables de entorno:
   - \`PYTHON_BACKEND_URL=https://tu-backend-url.railway.app\`
4. Vercel detectará automáticamente que es Next.js

### 3. Actualizar URLs
1. Reemplaza \`tu-backend-url.railway.app\` en \`vercel.json\` con tu URL real
2. Actualiza \`PYTHON_BACKEND_URL\` en Vercel con tu URL real

## Estructura del Proyecto
\`\`\`
CodeHelperNET/
├── api_server_production.py    # Servidor para producción
├── rag_chatbot.py             # Lógica del chatbot
├── requirements_production.txt # Dependencias Python
├── Procfile                   # Configuración para Railway/Heroku
├── runtime.txt                # Versión de Python
├── vercel.json                # Configuración para Vercel
├── frontend/                  # Aplicación Next.js
│   ├── package.json
│   ├── next.config.js
│   └── src/
└── vector_db/                 # Base de datos vectorial
\`\`\`

## URLs Finales
- **Frontend:** https://tu-app.vercel.app
- **Backend:** https://tu-backend-url.railway.app

## Monitoreo
- **Vercel:** Dashboard con analytics y logs
- **Railway:** Logs en tiempo real y métricas
EOF

print_success "README de despliegue creado"

# Mostrar resumen
echo ""
print_success "🎉 Proyecto preparado para despliegue!"
echo ""
echo "📋 Próximos pasos:"
echo "1. Sube tu código a GitHub"
echo "2. Despliega el backend en Railway"
echo "3. Despliega el frontend en Vercel"
echo "4. Actualiza las URLs en la configuración"
echo ""
echo "📚 Documentación completa: DEPLOYMENT_GUIDE.md"
echo "📖 Guía rápida: DEPLOYMENT_README.md"
echo ""
print_warning "⚠️  Recuerda actualizar las URLs en vercel.json con tu backend real"
echo "" 