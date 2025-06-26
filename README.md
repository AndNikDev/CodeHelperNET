# CodeHelperNET - Chatbot Especializado en C# y .NET

Un chatbot inteligente especializado en C# y .NET, desarrollado con tecnologías de Deep Learning y RAG (Retrieval-Augmented Generation). El proyecto incluye un backend en Python con embeddings y un frontend moderno en Next.js.

## 🚀 Características

- **Chatbot especializado** en C# y .NET con 76 documentos de conocimiento
- **RAG (Retrieval-Augmented Generation)** para respuestas precisas y contextuales
- **Frontend moderno** con interfaz tipo ChatGPT y tema oscuro
- **Backend robusto** con embeddings y cross-encoder para mejor calidad
- **API REST** para integración fácil
- **Base de conocimientos** con 3,073 chunks de información especializada
- **Multiplataforma** - Compatible con Windows, Linux y macOS
- **Despliegue fácil** - Configurado para Vercel, Railway, Render y más
- **Estructura limpia** - Organización modular y profesional

## 📁 Estructura del Proyecto

```
CodeHelperNET/
├── backend/                    # Backend Python
│   ├── api_server.py          # Servidor de desarrollo
│   ├── api_server_production.py # Servidor para producción
│   ├── rag_chatbot.py         # Lógica principal del chatbot
│   ├── improved_vector_db.py  # Generador de base vectorial
│   ├── requirements.txt       # Dependencias de desarrollo
│   ├── requirements_production.txt # Dependencias de producción
│   ├── Procfile              # Configuración para Railway/Heroku
│   ├── runtime.txt           # Versión de Python
│   ├── data/                 # Documentos de conocimiento (76 archivos)
│   └── vector_db/            # Base de datos vectorial (3,073 chunks)
├── frontend/                  # Frontend Next.js
│   ├── package.json
│   ├── next.config.js
│   ├── src/
│   │   ├── app/              # App Router de Next.js
│   │   ├── components/       # Componentes React
│   │   └── services/         # Servicios de API
│   └── public/               # Archivos estáticos
├── scripts/                   # Scripts de inicio y despliegue
│   ├── start_chatbot.sh      # Inicio en Linux/macOS
│   ├── start_chatbot.bat     # Inicio en Windows
│   └── deploy.sh             # Preparación para despliegue
├── docs/                      # Documentación
│   ├── DEPLOYMENT_GUIDE.md   # Guía completa de despliegue
│   └── Proyecto Final IF7103 2025 Sis.Expertos.pdf
├── codehelper_env/           # Entorno virtual Python
├── vercel.json              # Configuración para Vercel
└── README.md                # Este archivo
```

## 🛠️ Tecnologías

### Backend (Python)
- **Sentence Transformers** - Embeddings para recuperación semántica
- **ChromaDB** - Base de datos vectorial
- **Flask** - API REST
- **Transformers** - Modelos de lenguaje
- **LangChain** - Framework para RAG

### Frontend (Next.js)
- **Next.js 14** - Framework de React
- **TypeScript** - Tipado estático
- **Tailwind CSS** - Framework de CSS
- **Lucide React** - Iconos

## 📦 Instalación y Configuración

### Prerrequisitos
- Python 3.8+
- Node.js 18+
- npm o yarn

### 1. Clonar el repositorio
```bash
git clone <tu-repositorio>
cd CodeHelperNET
```

### 2. Configurar el Backend (Python)

#### Crear entorno virtual

**En Linux/macOS:**
```bash
python3 -m venv codehelper_env
source codehelper_env/bin/activate
```

**En Windows:**
```cmd
python -m venv codehelper_env
codehelper_env\Scripts\activate
```

#### Instalar dependencias
```bash
pip install -r backend/requirements.txt
```

#### Generar la base de datos vectorial
```bash
cd backend
python improved_vector_db.py
cd ..
```

#### Iniciar el servidor backend
```bash
cd backend
python api_server.py
```

El backend estará disponible en: http://localhost:5000

### 3. Configurar el Frontend (Next.js)

#### Instalar dependencias
```bash
cd frontend
npm install
```

#### Configurar variables de entorno
Crear archivo `.env.local` en la carpeta `frontend/`:
```env
PYTHON_BACKEND_URL=http://localhost:5000
NEXT_PUBLIC_API_URL=/api
```

#### Iniciar el servidor frontend
```bash
npm run dev
```

El frontend estará disponible en: http://localhost:3000

## 🚀 Inicio Rápido

### Opción 1: Script de inicio automático

**En Linux/macOS:**
```bash
chmod +x scripts/start_chatbot.sh
./scripts/start_chatbot.sh
```

**En Windows:**
```cmd
scripts\start_chatbot.bat
```

### Opción 2: Inicio manual

1. **Terminal 1 - Backend:**
   ```bash
   # Linux/macOS
   source codehelper_env/bin/activate
   cd backend
   python api_server.py
   
   # Windows
   codehelper_env\Scripts\activate
   cd backend
   python api_server.py
   ```

2. **Terminal 2 - Frontend:**
   ```bash
   cd frontend
   npm run dev
   ```

3. **Abrir navegador:** http://localhost:3000

## 🌐 Despliegue en Producción

### Despliegue Automático
```bash
# Preparar proyecto para despliegue
chmod +x scripts/deploy.sh
./scripts/deploy.sh
```

### Opciones de Despliegue

#### 🎯 **Recomendado: Vercel + Railway**
- **Frontend:** Vercel (excelente para Next.js)
- **Backend:** Railway (bueno para Python)
- **Ventajas:** Escalabilidad automática, SSL, CDN global

#### 📋 **Pasos Rápidos:**

1. **Backend en Railway:**
   - Ve a [railway.app](https://railway.app)
   - Conecta tu repositorio de GitHub
   - Railway detectará automáticamente la configuración

2. **Frontend en Vercel:**
   - Ve a [vercel.com](https://vercel.com)
   - Importa tu repositorio
   - Configura `PYTHON_BACKEND_URL` con tu URL de Railway

3. **Configurar URLs:**
   - Actualiza `vercel.json` con tu URL de Railway
   - Configura variables de entorno en Vercel

#### 🔧 **Otras Opciones:**
- **Render:** Todo en un solo servicio
- **Heroku:** Plataforma tradicional
- **AWS/GCP/Azure:** Servicios en la nube

### Documentación Completa
- 📚 **Guía detallada:** [docs/DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md)
- 📖 **Configuración rápida:** [docs/DEPLOYMENT_README.md](docs/DEPLOYMENT_README.md)

## 🎯 Uso del Chatbot

### Interfaz Web
1. Abre http://localhost:3000 en tu navegador
2. Escribe tu pregunta sobre C# o .NET
3. El chatbot responderá con información especializada

### Ejemplos de preguntas
- "¿Qué es async/await en C#?"
- "¿Cómo crear una API REST con ASP.NET Core?"
- "¿Qué son los patrones de diseño más comunes?"
- "¿Cómo implementar Entity Framework Core?"
- "¿Cuáles son las mejores prácticas de seguridad en .NET?"
- "dame un ejemplo de código de .NET"
- "muéstrame un ejemplo de LINQ"

### API REST
También puedes usar el chatbot programáticamente:

**En Linux/macOS:**
```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "¿Qué es LINQ en C#?"}'
```

**En Windows (PowerShell):**
```powershell
Invoke-RestMethod -Uri "http://localhost:5000/chat" -Method POST -ContentType "application/json" -Body '{"message": "¿Qué es LINQ en C#?"}'
```

## 📚 Base de Conocimientos

El chatbot tiene acceso a información sobre:

- **C# Fundamentals** - Conceptos básicos y avanzados
- **ASP.NET Core** - Desarrollo web moderno
- **Entity Framework** - ORM y acceso a datos
- **Design Patterns** - Patrones de diseño
- **Testing** - Pruebas unitarias e integración
- **Security** - Mejores prácticas de seguridad
- **Performance** - Optimización y rendimiento
- **Cloud Development** - Azure, AWS, GCP
- **Microservices** - Arquitectura de microservicios
- **DevOps** - CI/CD y automatización

## 🔧 Configuración Avanzada

### Variables de Entorno del Backend

**En Linux/macOS:**
```bash
export FLASK_ENV=development  # Modo desarrollo
export PORT=5000              # Puerto del servidor
```

**En Windows:**
```cmd
set FLASK_ENV=development
set PORT=5000
```

### Variables de Entorno del Frontend
```env
PYTHON_BACKEND_URL=http://localhost:5000  # URL del backend
NEXT_PUBLIC_API_URL=/api                  # URL de la API del frontend
```

### Personalización del Chatbot
Puedes modificar:
- `backend/rag_chatbot.py` - Lógica del chatbot
- `backend/improved_vector_db.py` - Generación de embeddings
- `frontend/src/components/ChatInterface.tsx` - Interfaz del chat

## 🐛 Solución de Problemas

### Error: "Chatbot no inicializado"
- Verifica que el backend esté ejecutándose
- Revisa los logs del servidor Flask

### Error: "No se pudo conectar con el servidor"
- Confirma que la URL del backend sea correcta
- Verifica que no haya problemas de CORS

### Error: "Base de datos vectorial no encontrada"
- Ejecuta `cd backend && python improved_vector_db.py` para regenerar la base

### Error: "Dependencias faltantes"
- Ejecuta `pip install -r backend/requirements.txt`
- Verifica que el entorno virtual esté activado

### Problemas específicos de Windows
- **Error de permisos:** Ejecuta PowerShell como administrador
- **Error de encoding:** Usa `chcp 65001` para UTF-8
- **Error de path:** Usa rutas con backslashes `\` en lugar de `/`

### Problemas específicos de Linux
- **Error de permisos:** Usa `sudo` si es necesario
- **Error de dependencias:** Instala `python3-dev` y `build-essential`
- **Error de encoding:** Configura `export LANG=en_US.UTF-8`

### Problemas de Despliegue
- **Error de memoria:** Los modelos de ML requieren RAM suficiente
- **Timeout:** La primera carga puede tardar, implementa health checks
- **CORS:** Verifica que `flask-cors` esté configurado correctamente

## 📊 Rendimiento

- **Tiempo de respuesta**: ~1-3 segundos por pregunta
- **Precisión**: Alta gracias al RAG y cross-encoder
- **Base de datos**: 3,073 chunks de información
- **Documentos**: 76 archivos de conocimiento especializado

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👨‍💻 Autor

Desarrollado como proyecto universitario para el curso IF7103 Sistemas Expertos.

## 🙏 Agradecimientos

- Sentence Transformers por los modelos de embeddings
- ChromaDB por la base de datos vectorial
- Next.js por el framework frontend
- La comunidad de C# y .NET por el conocimiento compartido 