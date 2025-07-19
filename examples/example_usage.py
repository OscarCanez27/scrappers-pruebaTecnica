#!/usr/bin/env python3
"""
Ejemplo de uso de la API de Búsqueda en Listas de Alto Riesgo
"""

import requests
import json
import time
from typing import Dict, Any

class RiskListsAPI:
    """
    Cliente para interactuar con la API de búsqueda en listas de alto riesgo.
    """
    
    def __init__(self, base_url: str = "http://localhost:8000", api_token: str = "test_token_123"):
        """
        Inicializa el cliente de la API.
        
        Args:
            base_url: URL base de la API
            api_token: Token de autenticación
        """
        self.base_url = base_url.rstrip('/')
        self.api_token = api_token
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }
    
    def health_check(self) -> Dict[str, Any]:
        """
        Verifica el estado de salud de la API.
        
        Returns:
            Dict con información del estado de la API
        """
        try:
            response = requests.get(f"{self.base_url}/health", timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": f"Error de conexión: {str(e)}"}
    
    def get_sources(self) -> Dict[str, Any]:
        """
        Obtiene la lista de fuentes disponibles.
        
        Returns:
            Dict con información de las fuentes disponibles
        """
        try:
            response = requests.get(f"{self.base_url}/sources", timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": f"Error de conexión: {str(e)}"}
    
    def search_entity(self, entity_name: str, source: str = "all") -> Dict[str, Any]:
        """
        Busca una entidad en las listas de alto riesgo.
        
        Args:
            entity_name: Nombre de la entidad a buscar
            source: Fuente específica ("all", "offshore_leaks", "world_bank", "ofac")
            
        Returns:
            Dict con los resultados de la búsqueda
        """
        try:
            data = {
                "entity_name": entity_name,
                "source": source
            }
            
            response = requests.post(
                f"{self.base_url}/search",
                headers=self.headers,
                json=data,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                return {"error": "Token de autenticación inválido"}
            elif e.response.status_code == 429:
                return {"error": "Rate limit excedido. Intenta de nuevo en unos minutos"}
            else:
                return {"error": f"Error HTTP {e.response.status_code}: {e.response.text}"}
        except requests.RequestException as e:
            return {"error": f"Error de conexión: {str(e)}"}

def main():
    """
    Función principal con ejemplos de uso de la API.
    """
    print("🔍 API de Búsqueda en Listas de Alto Riesgo - Ejemplos de Uso")
    print("=" * 60)
    
    # Inicializar cliente
    api = RiskListsAPI()
    
    # 1. Verificar estado de la API
    print("\n1. Verificando estado de la API...")
    health = api.health_check()
    if "error" in health:
        print(f"❌ Error: {health['error']}")
        print("Asegúrate de que la API esté ejecutándose en http://localhost:8000")
        return
    else:
        print(f"✅ API funcionando correctamente")
        print(f"   Status: {health.get('status', 'N/A')}")
        print(f"   Versión: {health.get('version', 'N/A')}")
    
    # 2. Obtener fuentes disponibles
    print("\n2. Obteniendo fuentes disponibles...")
    sources = api.get_sources()
    if "error" in sources:
        print(f"❌ Error: {sources['error']}")
    else:
        print("📊 Fuentes disponibles:")
        for source in sources.get("sources", []):
            print(f"   • {source['name']} ({source['id']})")
            print(f"     {source['description']}")
    
    # 3. Ejemplos de búsqueda
    print("\n3. Ejemplos de búsqueda...")
    
    # Ejemplo 1: Búsqueda en todas las fuentes
    print("\n   🔍 Buscando 'John Doe' en todas las fuentes...")
    result1 = api.search_entity("John Doe", "all")
    if "error" in result1:
        print(f"   ❌ Error: {result1['error']}")
    else:
        print(f"   ✅ Encontrados {result1.get('total_hits', 0)} resultados")
        print(f"   ⏱️  Tiempo de búsqueda: {result1.get('search_time', 0):.2f} segundos")
        print(f"   📍 Fuentes buscadas: {', '.join(result1.get('sources_searched', []))}")
    
    # Ejemplo 2: Búsqueda específica en OFAC
    print("\n   🔍 Buscando 'Vladimir Putin' en OFAC...")
    result2 = api.search_entity("Vladimir Putin", "ofac")
    if "error" in result2:
        print(f"   ❌ Error: {result2['error']}")
    else:
        print(f"   ✅ Encontrados {result2.get('total_hits', 0)} resultados")
        for i, entity in enumerate(result2.get('results', [])[:3], 1):
            print(f"   {i}. {entity.get('name', 'N/A')} - {entity.get('source', 'N/A')}")
    
    # Ejemplo 3: Búsqueda de empresa
    print("\n   🔍 Buscando 'Apple Inc' en todas las fuentes...")
    result3 = api.search_entity("Apple Inc", "all")
    if "error" in result3:
        print(f"   ❌ Error: {result3['error']}")
    else:
        print(f"   ✅ Encontrados {result3.get('total_hits', 0)} resultados")
        for i, entity in enumerate(result3.get('results', [])[:3], 1):
            print(f"   {i}. {entity.get('name', 'N/A')} - {entity.get('source', 'N/A')}")
    
    # 4. Ejemplo de manejo de errores
    print("\n4. Probando manejo de errores...")
    
    # Error: Nombre vacío
    print("\n   🚫 Probando con nombre vacío...")
    error_result = api.search_entity("", "all")
    if "error" in error_result:
        print(f"   ✅ Error capturado correctamente: {error_result['error']}")
    
    # Error: Fuente inválida
    print("\n   🚫 Probando con fuente inválida...")
    error_result2 = api.search_entity("John Doe", "invalid_source")
    if "error" in error_result2:
        print(f"   ✅ Error capturado correctamente: {error_result2['error']}")
    
    print("\n" + "=" * 60)
    print("✅ Ejemplos completados. Revisa los resultados arriba.")

def test_rate_limiting():
    """
    Función para probar el rate limiting de la API.
    """
    print("\n🧪 Probando rate limiting...")
    api = RiskListsAPI()
    
    # Hacer múltiples peticiones rápidas
    for i in range(25):
        print(f"   Petición {i+1}/25...")
        result = api.search_entity("Test Entity")
        
        if "error" in result and "Rate limit" in result["error"]:
            print(f"   ✅ Rate limiting funcionando: {result['error']}")
            break
        elif "error" in result:
            print(f"   ❌ Error inesperado: {result['error']}")
            break
        
        time.sleep(0.1)  # Pequeña pausa entre peticiones
    
    print("   ✅ Prueba de rate limiting completada")

if __name__ == "__main__":
    # Ejecutar ejemplos principales
    main()
    
    # Preguntar si quiere probar rate limiting
    print("\n¿Quieres probar el rate limiting? (s/n): ", end="")
    try:
        response = input().lower().strip()
        if response in ['s', 'si', 'sí', 'y', 'yes']:
            test_rate_limiting()
    except KeyboardInterrupt:
        print("\n\n👋 ¡Hasta luego!")
    except EOFError:
        print("\n\n👋 ¡Hasta luego!") 