# CodeHelperNET con Ollama

CodeHelperNET es un asistente especializado en C# y .NET que utiliza Ollama para generar respuestas inteligentes y específicas.

## 🚀 Características

- **Base de datos vectorial local** con información especializada en C# y .NET
- **Generación de respuestas con Ollama** (modelo local)
- **Búsqueda web** para información actualizada
- **Respuestas específicas** para preguntas sobre:
  - Sintaxis de C#
  - Ejemplos de código
  - Conceptos de .NET
  - Patrones de diseño
  - Conexiones a bases de datos
  - Y mucho más

## 📋 Requisitos

- Python 3.8+
- Ollama instalado y ejecutándose
- Modelo Llama2 descargado

## 🔧 Instalación

### 1. Instalar dependencias de Python

```bash
pip install -r requirements_complete.txt
```

### 2. Instalar Ollama

#### Linux/macOS:
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

#### Windows:
Descarga desde: https://ollama.ai

### 3. Configurar Ollama automáticamente

```bash
python setup_ollama.py
```

O manualmente:

```bash
# Iniciar Ollama
ollama serve

# En otra terminal, descargar el modelo
ollama pull llama2
```

## 🎯 Uso

### Inicio rápido

```bash
python start_chatbot.py
```

### Inicio manual

```bash
python rag_chatbot.py
```

## 💬 Ejemplos de preguntas

El chatbot puede responder preguntas como:

- **"¿Cómo crear un bucle for en C#?"**
- **"Muéstrame un ejemplo de hola mundo"**
- **"¿Qué es Entity Framework?"**
- **"¿Cómo conectar a una base de datos SQL Server?"**
- **"Explica el patrón Singleton"**
- **"¿Sintaxis de async/await en C#?"**
- **"¿Cómo usar LINQ?"**
- **"¿Qué son los delegates en C#?"**

## 🔧 Configuración

### Cambiar modelo de Ollama

En `rag_chatbot.py`, línea 385:

```python
self.model = "llama2"  # Cambiar a "mistral", "codellama", etc.
```

### Modelos recomendados

- **llama2**: Bueno para respuestas generales
- **mistral**: Más rápido y eficiente
- **codellama**: Especializado en código
- **llama2:13b**: Mejor calidad (más lento)

### Descargar otros modelos

```bash
ollama pull mistral
ollama pull codellama
ollama pull llama2:13b
```

## 🛠️ Solución de problemas

### Ollama no responde

```bash
# Verificar si está ejecutándose
curl http://localhost:11434/api/tags

# Reiniciar Ollama
pkill ollama
ollama serve
```

### Error de modelo no encontrado

```bash
# Listar modelos disponibles
ollama list

# Descargar modelo específico
ollama pull llama2
```

### Dependencias faltantes

```bash
# Reinstalar dependencias
pip install -r requirements_complete.txt
```

## 📁 Estructura del proyecto

```
backend/
├── rag_chatbot.py          # Chatbot principal
├── setup_ollama.py         # Configuración automática
├── start_chatbot.py        # Script de inicio
├── requirements_complete.txt # Dependencias
├── data/                   # Base de datos de conocimiento
└── vector_db/             # Base de datos vectorial
```

## 🔄 Actualización

Para actualizar el sistema:

```bash
# Actualizar dependencias
pip install -r requirements_complete.txt --upgrade

# Actualizar Ollama
ollama pull llama2:latest
```

## 📞 Soporte

Si tienes problemas:

1. Verifica que Ollama esté ejecutándose
2. Asegúrate de tener el modelo descargado
3. Revisa los logs de error
4. Ejecuta `python setup_ollama.py` para diagnóstico

## 🎉 ¡Listo!

Ahora tienes un asistente inteligente especializado en C# y .NET que puede:

- Responder preguntas específicas sobre sintaxis
- Generar ejemplos de código
- Explicar conceptos de .NET
- Ayudar con patrones de diseño
- Proporcionar información sobre bases de datos

¡Disfruta programando con C# y .NET! 🚀 