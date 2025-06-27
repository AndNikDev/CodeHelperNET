import os
import re
from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer, CrossEncoder
from chromadb import PersistentClient
import requests
from bs4 import BeautifulSoup
import urllib.parse
import time
import json

class RAGChatbot:
    def __init__(self, db_path: str = "./vector_db"):
        """Inicializar el chatbot RAG completo con Ollama"""
        # Ajustar ruta para la nueva estructura
        if not os.path.isabs(db_path):
            db_path = os.path.join(os.path.dirname(__file__), db_path)
        
        self.db_path = db_path
        self.client = PersistentClient(path=db_path)
        
        # Conectar a la colección mejorada
        self.collection = self.client.get_collection("codehelper_csharp_improved")
        
        # Modelo de embeddings para recuperación
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
        
        # Cross-encoder para re-ranking (mejora la calidad de resultados)
        self.cross_encoder = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
        
        # Inicializar Ollama
        self.ollama = OllamaLLM()
        
        # Inicializar buscador web
        self.web_searcher = WebSearcher()
        
    def classify_question(self, question: str) -> str:
        """Clasificar el tipo de pregunta para usar el prompt apropiado"""
        question_lower = question.lower()
        
        # Palabras clave para ejemplos de código
        code_keywords = [
            'ejemplo', 'código', 'implementar', 'cómo hacer', 'muestra', 'muéstrame',
            'dame', 'déjame', 'quiero ver', 'necesito', 'ayúdame con', 'cómo crear',
            'programa', 'aplicación', 'proyecto', 'sample', 'demo', 'tutorial',
            'ver', 'mostrar', 'enseñar', 'enseñame', 'ejemplifica', 'ilustra',
            'código de', 'ejemplo de', 'muestra de', 'cómo se hace', 'cómo se crea',
            'cómo implementar', 'cómo usar', 'cómo trabajar con'
        ]
        
        # Palabras clave para ciclos específicos
        loop_keywords = [
            'for', 'while', 'do while', 'foreach', 'bucle', 'ciclo', 'loop',
            'iterar', 'iteración', 'repetir', 'recorrer', 'contador'
        ]
        
        # Palabras clave para bases de datos
        db_keywords = [
            'base de datos', 'database', 'sql', 'conectar', 'conexión', 'entity framework',
            'ado.net', 'linq', 'query', 'consulta', 'tabla', 'registro', 'insertar',
            'actualizar', 'eliminar', 'select', 'insert', 'update', 'delete'
        ]
        
        # Palabras clave para patrones de diseño
        pattern_keywords = [
            'patrón', 'pattern', 'singleton', 'factory', 'observer', 'strategy',
            'command', 'adapter', 'decorator', 'facade', 'proxy', 'template method',
            'builder', 'prototype', 'chain of responsibility', 'mediator', 'memento'
        ]
        
        # Clasificar la pregunta
        if any(word in question_lower for word in loop_keywords):
            return 'loop_specific'
        elif any(word in question_lower for word in db_keywords):
            return 'database_specific'
        elif any(word in question_lower for word in pattern_keywords):
            return 'pattern_specific'
        elif any(word in question_lower for word in code_keywords):
            return 'code_example'
        else:
            return 'general_help'
    
    def retrieve_relevant_chunks(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """Recuperar chunks relevantes de la base de datos vectorial"""
        try:
            # Generar embedding de la consulta
            query_embedding = self.embedding_model.encode(query).tolist()
            
            # Buscar en la base de datos
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results
            )
            
            # Procesar resultados
            chunks = []
            if results['documents'] and results['documents'][0]:
                for i, doc in enumerate(results['documents'][0]):
                    chunk = {
                        'content': doc,
                        'metadata': results['metadatas'][0][i] if results['metadatas'] and results['metadatas'][0] else {},
                        'distance': results['distances'][0][i] if results['distances'] and results['distances'][0] else 0
                    }
                    chunks.append(chunk)
            
            return chunks
            
        except Exception as e:
            print(f"Error recuperando chunks: {e}")
            return []
    
    def clean_context(self, chunks: List[Dict[str, Any]]) -> str:
        """Limpiar y formatear el contexto de los chunks"""
        if not chunks:
            return ""
        
        # Ordenar por relevancia (menor distancia = más relevante)
        chunks.sort(key=lambda x: x.get('distance', 1.0))
        
        # Tomar los 3 chunks más relevantes
        top_chunks = chunks[:3]
        
        context_parts = []
        for chunk in top_chunks:
            content = chunk.get('content', '')
            if content and len(content.strip()) > 50:  # Solo chunks con contenido significativo
                context_parts.append(content.strip())
        
        return "\n\n".join(context_parts)
    
    def chat(self, question: str) -> str:
        """Método principal para chatear con el bot"""
        try:
            print(f"Procesando pregunta: {question}")
            
            # Clasificar la pregunta
            question_type = self.classify_question(question)
            print(f"Tipo de pregunta detectado: {question_type}")
            
            # Buscar información local
            local_chunks = self.retrieve_relevant_chunks(question, n_results=5)
            local_context = self.clean_context(local_chunks)
            
            # Buscar información web si es necesario
            web_context = ""
            if not local_context or len(local_context) < 100:
                print("Buscando información web...")
                web_results = self.web_searcher.search_web(question, max_results=2)
                if web_results:
                    web_context = "\n\n".join([result['content'] for result in web_results])
            
            # Combinar contextos
            full_context = f"{local_context}\n\n{web_context}".strip()
            
            # Generar respuesta con Ollama
            response = self.ollama.generate_response(question, full_context, question_type)
            
            if not response or len(response) < 20:
                # Fallback local
                response = self.generate_local_fallback(question, full_context)
            
            return response
            
        except Exception as e:
            print(f"Error en chat: {e}")
            return f"Lo siento, tuve un problema procesando tu pregunta. Error: {str(e)}"
    
    def generate_local_fallback(self, question: str, context: str = "") -> str:
        """Generar respuesta local cuando Ollama falla"""
        question_lower = question.lower()
        
        # Respuestas específicas para preguntas comunes
        if any(word in question_lower for word in ['hola mundo', 'hello world', 'primer programa']):
            return """**Hola Mundo en C#**

Aquí tienes un ejemplo simple de "Hola Mundo" en C#:

```csharp
using System;

namespace MiPrimerPrograma
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("¡Hola Mundo desde C#!");
        }
    }
}
```

**Para ejecutarlo:**
1. Guarda el código en un archivo `Program.cs`
2. Abre una terminal en la carpeta del archivo
3. Ejecuta: `dotnet run`

¡Es así de simple!"""
        
        elif any(word in question_lower for word in ['for', 'bucle', 'ciclo', 'loop']):
            return """**Bucle FOR en C#**

El bucle `for` es una estructura de control que permite ejecutar código un número específico de veces.

**Sintaxis básica:**
```csharp
for (inicialización; condición; incremento)
{
    // Código a ejecutar
}
```

**Ejemplos prácticos:**
```csharp
// Imprimir números del 1 al 10
for (int i = 1; i <= 10; i++)
{
    Console.WriteLine($"Número: {i}");
}

// Recorrer un array
string[] frutas = {"manzana", "banana", "naranja"};
for (int i = 0; i < frutas.Length; i++)
{
    Console.WriteLine($"Fruta {i + 1}: {frutas[i]}");
}

// Bucle descendente
for (int i = 10; i >= 1; i--)
{
    Console.WriteLine($"Cuenta regresiva: {i}");
}
```

**Cuándo usar FOR:**
- Cuando conoces el número exacto de iteraciones
- Para recorrer arrays o colecciones por índice
- Cuando necesitas control sobre el contador"""
        
        elif any(word in question_lower for word in ['while', 'mientras']):
            return """**Bucle WHILE en C#**

El bucle `while` ejecuta código mientras una condición sea verdadera.

**Sintaxis básica:**
```csharp
while (condición)
{
    // Código a ejecutar
}
```

**Ejemplos prácticos:**
```csharp
// Contador simple
int contador = 0;
while (contador < 5)
{
    Console.WriteLine($"Contador: {contador}");
    contador++;
}

// Leer entrada del usuario hasta que sea válida
string entrada;
do
{
    Console.Write("Ingresa 'salir' para terminar: ");
    entrada = Console.ReadLine();
    Console.WriteLine($"Escribiste: {entrada}");
} while (entrada.ToLower() != "salir");
```

**Cuándo usar WHILE:**
- Cuando no conoces el número exacto de iteraciones
- Para validación de entrada
- Cuando necesitas ejecutar código al menos una vez (do-while)"""
        
        elif any(word in question_lower for word in ['base de datos', 'database', 'sql', 'conectar', 'conexión']):
            return """**Conexión a Base de Datos en C#**

Para conectar a una base de datos SQL Server en C#:

**Usando ADO.NET:**
```csharp
using System.Data.SqlClient;

string connectionString = "Server=miServidor;Database=miBaseDatos;Trusted_Connection=true;";

using (SqlConnection connection = new SqlConnection(connectionString))
{
    connection.Open();
    Console.WriteLine("Conexión exitosa!");
    
    string query = "SELECT * FROM Usuarios";
    using (SqlCommand command = new SqlCommand(query, connection))
    {
        using (SqlDataReader reader = command.ExecuteReader())
        {
            while (reader.Read())
            {
                Console.WriteLine($"ID: {reader["ID"]}, Nombre: {reader["Nombre"]}");
            }
        }
    }
}
```

**Usando Entity Framework Core:**
```csharp
// En appsettings.json
{
  "ConnectionStrings": {
    "DefaultConnection": "Server=miServidor;Database=miBaseDatos;Trusted_Connection=true;"
  }
}

// En Startup.cs
services.AddDbContext<MiContexto>(options =>
    options.UseSqlServer(Configuration.GetConnectionString("DefaultConnection")));
```"""
        
        elif any(word in question_lower for word in ['qué es', 'que es', 'definir', 'explicar']):
            return """**C# y .NET**

**C#** es un lenguaje de programación moderno, orientado a objetos y de propósito general desarrollado por Microsoft como parte de la plataforma .NET.

**Características principales de C#:**
- Tipado estático y seguro
- Orientado a objetos
- Garbage collection automático
- LINQ para consultas de datos
- Soporte para programación asíncrona
- Multiplataforma

**.NET** es una plataforma de desarrollo que incluye:
- Common Language Runtime (CLR)
- Framework Class Library (FCL)
- Herramientas de desarrollo
- Soporte para múltiples lenguajes

**Ventajas:**
- Excelente para desarrollo web con ASP.NET Core
- Gran ecosistema de librerías
- Soporte empresarial de Microsoft
- Multiplataforma (Windows, Linux, macOS)"""
        
        else:
            return f"""Basándome en la información disponible:

{context[:300] if context else "No encontré información específica en mi base de datos local."}

¿Podrías ser más específico? Por ejemplo:
- "¿Cómo crear un bucle for en C#?"
- "¿Qué es Entity Framework?"
- "¿Cómo conectar a una base de datos SQL Server?"
- "¿Sintaxis de async/await en C#?" """
    
    def interactive_chat(self):
        """Modo interactivo para probar el chatbot"""
        print("🤖 CodeHelperNET - Asistente de C# y .NET")
        print("Escribe 'salir' para terminar")
        print("-" * 50)
        
        while True:
            try:
                question = input("\n👤 Tú: ").strip()
                
                if question.lower() in ['salir', 'exit', 'quit']:
                    print("👋 ¡Hasta luego!")
                    break
                
                if not question:
                    continue
                
                print("\n🤖 CodeHelperNET está pensando...")
                response = self.chat(question)
                print(f"\n🤖 CodeHelperNET: {response}")
                
            except KeyboardInterrupt:
                print("\n👋 ¡Hasta luego!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")


class OllamaLLM:
    """Clase para usar Ollama localmente"""
    
    def __init__(self):
        self.ollama_url = "http://localhost:11434"
        self.model = "llama2"  # Puedes cambiar a "mistral", "codellama", etc.
        
    def generate_response(self, question: str, context: str = "", question_type: str = "general") -> str:
        """Generar respuesta usando Ollama"""
        try:
            # Crear prompt específico para C# y .NET
            if context:
                prompt = f"""Eres un experto especializado en C# y .NET. Responde la siguiente pregunta de manera específica, clara y útil.

Contexto disponible:
{context}

Pregunta: {question}

Instrucciones:
- Responde SOLO sobre C# y .NET
- Si la pregunta es sobre sintaxis, proporciona ejemplos de código claros
- Si es sobre conceptos, explica de manera didáctica
- Usa el contexto proporcionado para enriquecer tu respuesta
- Responde en español de manera natural y conversacional
- Sé específico y directo
- Incluye ejemplos prácticos cuando sea útil
- Si es código, usa bloques de código con ```csharp

Respuesta:"""
            else:
                prompt = f"""Eres un experto especializado en C# y .NET. Responde la siguiente pregunta de manera específica, clara y útil.

Pregunta: {question}

Instrucciones:
- Responde SOLO sobre C# y .NET
- Si la pregunta es sobre sintaxis, proporciona ejemplos de código claros
- Si es sobre conceptos, explica de manera didáctica
- Responde en español de manera natural y conversacional
- Sé específico y directo
- Incluye ejemplos prácticos cuando sea útil
- Si es código, usa bloques de código con ```csharp

Respuesta:"""

            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "num_predict": 300,
                    "top_p": 0.9,
                    "top_k": 40
                }
            }
            
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "")
            else:
                print(f"Error de Ollama: {response.status_code} - {response.text}")
                return ""
            
        except Exception as e:
            print(f"Error con Ollama: {e}")
            return ""


class WebSearcher:
    """Clase para búsqueda web"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def is_csharp_related(self, query: str) -> bool:
        """Verificar si la consulta está relacionada con C#"""
        csharp_keywords = [
            'c#', 'csharp', '.net', 'asp.net', 'entity framework', 'linq',
            'visual studio', 'xamarin', 'blazor', 'wpf', 'winforms',
            'console application', 'web api', 'mvc', 'razor'
        ]
        
        query_lower = query.lower()
        return any(keyword in query_lower for keyword in csharp_keywords)
    
    def search_web(self, query: str, max_results: int = 3) -> List[Dict[str, str]]:
        """Buscar información en la web"""
        try:
            if not self.is_csharp_related(query):
                return []
            
            # Usar DuckDuckGo para búsqueda
            search_url = "https://html.duckduckgo.com/html/"
            params = {
                'q': f"{query} C# .NET site:docs.microsoft.com OR site:learn.microsoft.com"
            }
            
            response = self.session.get(search_url, params=params, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            results = []
            
            # Extraer enlaces de resultados
            links = soup.find_all('a', class_='result__a')
            
            for link in links[:max_results]:
                url = link.get('href', '')
                if url and ('docs.microsoft.com' in url or 'learn.microsoft.com' in url):
                    title = link.get_text(strip=True)
                    content = self.extract_content_from_url(url)
                    if content:
                        results.append({
                            'title': title,
                            'url': url,
                            'content': content[:500]  # Limitar contenido
                        })
            
            return results
            
        except Exception as e:
            print(f"Error en búsqueda web: {e}")
            return []
    
    def extract_content_from_url(self, url: str) -> str:
        """Extraer contenido de una URL"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remover elementos no deseados
            for element in soup(['script', 'style', 'nav', 'header', 'footer']):
                element.decompose()
            
            # Extraer texto del contenido principal
            content = soup.get_text()
            
            # Limpiar y formatear
            lines = (line.strip() for line in content.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            return text[:1000]  # Limitar a 1000 caracteres
            
        except Exception as e:
            print(f"Error extrayendo contenido de {url}: {e}")
            return ""


# Función principal para ejecutar el chatbot
def main():
    """Función principal para ejecutar el chatbot"""
    try:
        print("🚀 Iniciando CodeHelperNET...")
        chatbot = RAGChatbot()
        print("✅ CodeHelperNET iniciado correctamente")
        
        # Verificar conexión con Ollama
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            if response.status_code == 200:
                print("✅ Conexión con Ollama establecida")
            else:
                print("⚠️  Ollama no está respondiendo correctamente")
        except:
            print("❌ No se pudo conectar con Ollama. Asegúrate de que esté ejecutándose.")
            print("💡 Para instalar Ollama: https://ollama.ai")
            print("💡 Para ejecutar: ollama run llama2")
        
        chatbot.interactive_chat()
        
    except Exception as e:
        print(f"❌ Error iniciando CodeHelperNET: {e}")


if __name__ == "__main__":
    main() 