# 🚀 Guía de Despliegue - CodeHelperNET

## Opción 1: Vercel (Frontend) + Railway/Render (Backend) - RECOMENDADO

### Paso 1: Desplegar el Backend en Railway

1. **Crear cuenta en Railway:**
   - Ve a [railway.app](https://railway.app)
   - Regístrate con tu cuenta de GitHub

2. **Conectar repositorio:**
   - Haz fork o push de tu proyecto a GitHub
   - En Railway, haz clic en "New Project" → "Deploy from GitHub repo"
   - Selecciona tu repositorio

3. **Configurar variables de entorno:**
   - En Railway, ve a la pestaña "Variables"
   - Agrega:
     ```
     FLASK_ENV=production
     PORT=5000
     ```

4. **Configurar el build:**
   - Railway detectará automáticamente que es un proyecto Python
   - Usará el archivo `requirements_production.txt`
   - El `Procfile` indicará cómo ejecutar la aplicación

5. **Desplegar:**
   - Railway construirá y desplegará automáticamente
   - Obtendrás una URL como: `https://tu-app.railway.app`

### Paso 2: Desplegar el Frontend en Vercel

1. **Crear cuenta en Vercel:**
   - Ve a [vercel.com](https://vercel.com)
   - Regístrate con tu cuenta de GitHub

2. **Importar proyecto:**
   - Haz clic en "New Project"
   - Importa tu repositorio de GitHub
   - Vercel detectará automáticamente que es un proyecto Next.js

3. **Configurar variables de entorno:**
   - En la configuración del proyecto, ve a "Environment Variables"
   - Agrega:
     ```
     PYTHON_BACKEND_URL=https://tu-app.railway.app
     ```

4. **Configurar el build:**
   - Framework Preset: Next.js
   - Build Command: `cd frontend && npm run build`
   - Output Directory: `frontend/.next`
   - Install Command: `cd frontend && npm install`

5. **Desplegar:**
   - Vercel construirá y desplegará automáticamente
   - Obtendrás una URL como: `https://tu-app.vercel.app`

## Opción 2: Todo en Vercel (Experimental)

### Configuración para Vercel Functions

1. **Crear archivo `vercel.json` en la raíz:**
```json
{
  "version": 2,
  "builds": [
    {
      "src": "frontend/package.json",
      "use": "@vercel/next"
    },
    {
      "src": "api_server_production.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "/api_server_production.py"
    },
    {
      "src": "/(.*)",
      "dest": "/frontend/$1"
    }
  ]
}
```

2. **Crear archivo `api/chat.py` para Vercel Functions:**
```python
from http.server import BaseHTTPRequestHandler
import json
import sys
import os

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from rag_chatbot import RAGChatbot

# Inicializar chatbot globalmente
chatbot = None

def get_chatbot():
    global chatbot
    if chatbot is None:
        chatbot = RAGChatbot()
    return chatbot

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            message = data.get('message', '').strip()
            
            if not message:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    "error": "Mensaje vacío"
                }).encode())
                return
            
            # Procesar con chatbot
            chatbot = get_chatbot()
            response = chatbot.chat(message)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            
            self.wfile.write(json.dumps({
                "response": response,
                "status": "success"
            }).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                "error": str(e)
            }).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
```

## Opción 3: Render (Todo junto)

### Desplegar en Render

1. **Crear cuenta en Render:**
   - Ve a [render.com](https://render.com)
   - Regístrate con tu cuenta de GitHub

2. **Crear nuevo Web Service:**
   - Conecta tu repositorio
   - Tipo: Web Service
   - Runtime: Python 3
   - Build Command: `pip install -r requirements_production.txt`
   - Start Command: `gunicorn api_server_production:app`

3. **Configurar variables de entorno:**
   ```
   FLASK_ENV=production
   PORT=10000
   ```

4. **Configurar el frontend:**
   - Crear un segundo servicio para el frontend
   - Tipo: Static Site
   - Build Command: `cd frontend && npm install && npm run build`
   - Publish Directory: `frontend/out`

## Opción 4: Heroku

### Desplegar en Heroku

1. **Instalar Heroku CLI:**
```bash
# En macOS
brew install heroku/brew/heroku

# En Windows
# Descargar desde https://devcenter.heroku.com/articles/heroku-cli
```

2. **Login y crear app:**
```bash
heroku login
heroku create tu-app-name
```

3. **Configurar variables de entorno:**
```bash
heroku config:set FLASK_ENV=production
heroku config:set PYTHON_BACKEND_URL=https://tu-app-name.herokuapp.com
```

4. **Desplegar:**
```bash
git add .
git commit -m "Preparar para Heroku"
git push heroku main
```

## Configuración de Dominio Personalizado

### Vercel
1. Ve a la configuración del proyecto
2. Pestaña "Domains"
3. Agrega tu dominio personalizado
4. Configura los registros DNS según las instrucciones

### Railway
1. En la configuración del proyecto
2. Pestaña "Settings" → "Custom Domain"
3. Agrega tu dominio
4. Configura los registros DNS

## Monitoreo y Logs

### Vercel
- Logs en tiempo real en el dashboard
- Analytics integrados
- Performance monitoring

### Railway
- Logs en tiempo real
- Métricas de uso
- Health checks automáticos

### Render
- Logs detallados
- Métricas de rendimiento
- Alertas configurables

## Troubleshooting

### Problemas Comunes

1. **Error de CORS:**
   - Verificar que `flask-cors` esté instalado
   - Configurar correctamente los orígenes permitidos

2. **Error de memoria:**
   - Los modelos de ML pueden consumir mucha memoria
   - Considerar usar servicios con más RAM (Railway Pro, Render)

3. **Timeout en requests:**
   - La primera carga del modelo puede tardar
   - Implementar health checks
   - Considerar warm-up del modelo

4. **Error de dependencias:**
   - Verificar que `requirements_production.txt` esté actualizado
   - Algunas dependencias pueden no estar disponibles en todos los servicios

### Optimizaciones

1. **Reducir tamaño del modelo:**
   - Usar modelos más pequeños
   - Optimizar embeddings

2. **Caching:**
   - Implementar cache de respuestas
   - Cache de embeddings

3. **CDN:**
   - Usar CDN para archivos estáticos
   - Optimizar imágenes y assets

## Costos Estimados

### Vercel
- **Hobby (Gratis):** 100GB bandwidth, 100 serverless function invocations
- **Pro ($20/mes):** 1TB bandwidth, 1000 function invocations

### Railway
- **Hobby (Gratis):** $5 credit/mes
- **Pro ($20/mes):** $20 credit/mes

### Render
- **Free:** 750 horas/mes
- **Paid:** Desde $7/mes

## Recomendación Final

**Para producción, recomiendo:**
1. **Frontend:** Vercel (excelente para Next.js)
2. **Backend:** Railway (bueno para Python, fácil de configurar)
3. **Base de datos:** Railway PostgreSQL (si necesitas persistencia)

Esta configuración te dará:
- ✅ Excelente rendimiento
- ✅ Escalabilidad automática
- ✅ SSL automático
- ✅ CDN global
- ✅ Monitoreo integrado
- ✅ Costos predecibles 