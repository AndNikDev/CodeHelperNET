# Configuración de CodeHelperNET con Ollama

# Configuración de Ollama
OLLAMA_CONFIG = {
    "url": "http://localhost:11434",
    "model": "llama2",  # Cambiar a "mistral", "codellama", "llama2:13b", etc.
    "temperature": 0.7,
    "num_predict": 500,
    "top_p": 0.9,
    "top_k": 40,
    "timeout": 60
}

# Configuración de la base de datos vectorial
VECTOR_DB_CONFIG = {
    "path": "./vector_db",
    "collection_name": "codehelper_csharp_improved",
    "embedding_model": "all-MiniLM-L6-v2",
    "cross_encoder_model": "cross-encoder/ms-marco-MiniLM-L-6-v2",
    "max_results": 5
}

# Configuración de búsqueda web
WEB_SEARCH_CONFIG = {
    "max_results": 3,
    "timeout": 10,
    "preferred_sites": [
        "docs.microsoft.com",
        "learn.microsoft.com",
        "stackoverflow.com"
    ]
}

# Configuración del chatbot
CHATBOT_CONFIG = {
    "language": "es",  # "es" para español, "en" para inglés
    "max_context_length": 1000,
    "fallback_enabled": True,
    "web_search_enabled": True
}

# Modelos recomendados de Ollama para diferentes usos
RECOMMENDED_MODELS = {
    "general": "llama2",           # Bueno para respuestas generales
    "fast": "mistral",             # Más rápido y eficiente
    "code": "codellama",           # Especializado en código
    "quality": "llama2:13b",       # Mejor calidad (más lento)
    "latest": "llama2:latest"      # Última versión
}

# Prompts personalizados para diferentes tipos de preguntas
CUSTOM_PROMPTS = {
    "code_example": """Eres un experto en C# y .NET. El usuario está pidiendo un ejemplo de código. Proporciona una respuesta clara y útil.

Contexto disponible:
{context}

Pregunta del usuario: {question}

Instrucciones:
- Responde SOLO sobre C# y .NET
- Proporciona ejemplos de código claros y funcionales
- Explica brevemente el código
- Usa bloques de código con ```csharp
- Responde en español de manera natural

Respuesta:""",

    "concept_explanation": """Eres un profesor experto en C# y .NET. Explica el concepto solicitado de manera clara y directa.

Contexto disponible:
{context}

Concepto a explicar: {question}

Instrucciones:
- Explica de manera didáctica y fácil de entender
- Incluye ejemplos prácticos cuando sea útil
- Usa el contexto proporcionado para enriquecer tu explicación
- Responde en español de manera natural

Explicación:""",

    "syntax_help": """Eres un asistente de programación especializado en C#. Ayuda con la sintaxis solicitada.

Contexto disponible:
{context}

Pregunta sobre sintaxis: {question}

Instrucciones:
- Proporciona la sintaxis correcta
- Incluye ejemplos de uso claros
- Sé directo y útil
- Usa bloques de código con ```csharp
- Responde en español

Respuesta:"""
}

# Configuración de logging
LOGGING_CONFIG = {
    "level": "INFO",  # DEBUG, INFO, WARNING, ERROR
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": "codehelper.log"
} 