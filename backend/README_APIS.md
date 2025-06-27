# 🚀 Configuración de APIs Externas para CodeHelperNET

## 📋 Resumen de Mejoras

El chatbot ahora incluye:
- ✅ **Búsqueda web automática** cuando no encuentra información local
- ✅ **LLM externo** para respuestas más específicas y naturales
- ✅ **Detección inteligente** de consultas relacionadas con C# y .NET
- ✅ **Respuestas más precisas** y contextuales

## 🔧 Configuración de APIs

### Opción 1: Hugging Face Inference API (Recomendada - Gratuita)

1. **Crear cuenta en Hugging Face:**
   - Ve a https://huggingface.co/join
   - Crea una cuenta gratuita

2. **Obtener API Key:**
   - Ve a https://huggingface.co/settings/tokens
   - Haz clic en "New token"
   - Dale un nombre (ej: "CodeHelperNET")
   - Selecciona "Read" como rol
   - Copia el token generado

3. **Configurar el archivo:**
   - Edita `config.env`
   - Reemplaza `your_huggingface_api_key_here` con tu API key real

```bash
HF_API_KEY=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Opción 2: Ollama (Local - Gratuita)

1. **Instalar Ollama:**
   ```bash
   # En Ubuntu/Debian
   curl -fsSL https://ollama.ai/install.sh | sh
   
   # En macOS
   brew install ollama
   ```

2. **Descargar modelo:**
   ```bash
   ollama pull llama2
   # o
   ollama pull codellama
   ```

3. **Iniciar Ollama:**
   ```bash
   ollama serve
   ```

4. **Configurar el archivo:**
   - Edita `config.env`
   - Cambia `api_type = "ollama"` en `rag_chatbot.py`

## 🎯 Cómo Funciona

### Flujo de Respuestas:

1. **Búsqueda Local:** Primero busca en la base de datos vectorial local
2. **Búsqueda Web:** Si no encuentra información, busca en internet
3. **LLM Externo:** Si aún no hay respuesta, usa la API externa
4. **Respuesta Genérica:** Como último recurso, da información básica

### Ejemplos de Uso:

```bash
# Pregunta específica sobre sintaxis
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "¿Qué es un bucle for en C#?"}'

# Pregunta sobre patrones de diseño
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "¿Cómo implementar un patrón Singleton?"}'

# Pregunta sobre conceptos avanzados
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "¿Qué son los delegates y eventos?"}'
```

## 🔍 Tipos de Preguntas que Funcionan Mejor

### ✅ **SÍ preguntar:**
- **Sintaxis específica:** "¿Cómo usar LINQ?", "¿Sintaxis de async/await?"
- **Conceptos:** "¿Qué es Entity Framework?", "¿Qué son los generics?"
- **Ejemplos de código:** "Dame un ejemplo de clase en C#"
- **Patrones:** "¿Cómo implementar Singleton?", "¿Qué es el patrón Observer?"
- **Frameworks:** "¿Cómo crear API REST con ASP.NET Core?"

### ❌ **NO preguntar:**
- Preguntas no relacionadas con C# o .NET
- Consultas sobre otros lenguajes de programación
- Preguntas personales o de opinión

## 🚀 Iniciar el Servidor

```bash
cd backend
python3 api_server.py
```

El servidor estará disponible en `http://localhost:5000`

## 🧪 Probar la Funcionalidad

```bash
# Ejecutar pruebas
python3 test_improved_chatbot.py

# Probar endpoint de salud
curl http://localhost:5000/health

# Probar chat
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "¿Qué es un bucle for en C#?"}'
```

## 🔧 Solución de Problemas

### Error: "HF API Key no configurado"
- Verifica que el archivo `config.env` existe
- Asegúrate de que la API key esté correctamente configurada

### Error: "Ollama no disponible"
- Verifica que Ollama esté instalado y ejecutándose
- Ejecuta `ollama serve` en otra terminal

### Respuestas genéricas
- Verifica que la pregunta esté relacionada con C# o .NET
- Intenta ser más específico en la pregunta

## 📊 Rendimiento

- **Búsqueda local:** ~100ms
- **Búsqueda web:** ~2-5 segundos
- **LLM externo:** ~3-10 segundos
- **Respuesta total:** ~1-15 segundos

## 🎉 ¡Listo!

Tu chatbot ahora puede responder preguntas específicas sobre C# y .NET de manera mucho más precisa y natural. ¡Disfruta programando! 🚀 