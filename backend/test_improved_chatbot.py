#!/usr/bin/env python3
"""
Script de prueba para el chatbot mejorado con búsqueda web y LLM externo
"""

import os
from dotenv import load_dotenv
from rag_chatbot import RAGChatbot, WebSearcher, ExternalLLM

# Cargar variables de entorno
load_dotenv('config.env')

def test_web_search():
    """Probar búsqueda web"""
    print("🔍 Probando búsqueda web...")
    searcher = WebSearcher()
    
    # Probar si detecta consultas relacionadas con C#
    test_queries = [
        "¿Qué es un for en C#?",
        "¿Cómo funciona Entity Framework?",
        "¿Cuál es la diferencia entre value types y reference types?",
        "¿Qué es el tiempo?",
        "¿Cómo cocinar pasta?"
    ]
    
    for query in test_queries:
        is_related = searcher.is_csharp_related(query)
        print(f"Query: '{query}' -> C# relacionado: {is_related}")
        
        if is_related:
            results = searcher.search_web(query)
            print(f"  Resultados encontrados: {len(results)}")
            for i, result in enumerate(results[:2]):
                print(f"    {i+1}. {result['title']}")
                print(f"       {result['snippet'][:100]}...")

def test_external_llm():
    """Probar LLM externo"""
    print("\n🤖 Probando LLM externo...")
    llm = ExternalLLM()
    
    # Verificar configuración
    print(f"API Type: {llm.api_type}")
    print(f"HF API Key configurado: {'Sí' if llm.hf_api_key else 'No'}")
    
    # Probar generación
    test_question = "¿Qué es un bucle for en C# y cómo se usa?"
    response = llm.generate_response(test_question)
    
    if response:
        print(f"Respuesta generada: {response[:200]}...")
    else:
        print("No se pudo generar respuesta (API no configurada)")

def test_chatbot():
    """Probar chatbot completo"""
    print("\n🎯 Probando chatbot completo...")
    
    try:
        chatbot = RAGChatbot()
        print("✅ Chatbot inicializado correctamente")
        
        # Probar preguntas específicas
        test_questions = [
            "¿Qué es un bucle for en C#?",
            "¿Cómo implementar un patrón Singleton?",
            "¿Qué son los delegates y eventos?",
            "¿Cuál es la sintaxis de LINQ?",
            "¿Cómo crear una API REST con ASP.NET Core?"
        ]
        
        for question in test_questions:
            print(f"\n❓ Pregunta: {question}")
            response = chatbot.chat(question)
            print(f"🤖 Respuesta: {response[:300]}...")
            
    except Exception as e:
        print(f"❌ Error inicializando chatbot: {e}")

if __name__ == "__main__":
    print("🚀 Iniciando pruebas del chatbot mejorado...")
    
    test_web_search()
    test_external_llm()
    test_chatbot()
    
    print("\n✅ Pruebas completadas!") 