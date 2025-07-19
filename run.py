#!/usr/bin/env python3
"""
Script para ejecutar la API de búsqueda en listas de alto riesgo.
"""

import uvicorn
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

if __name__ == "__main__":
    # Configuración del servidor
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    
    print(f"🚀 Iniciando API de Búsqueda en Listas de Alto Riesgo")
    print(f"📍 Servidor: http://{host}:{port}")
    print(f"📚 Documentación: http://{host}:{port}/docs")
    print(f"🔍 Health check: http://{host}:{port}/health")
    print(f"⏹️  Para detener: Ctrl+C")
    print("-" * 50)
    
    # Ejecutar el servidor
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=True,  # Recargar automáticamente en desarrollo
        log_level="info"
    ) 