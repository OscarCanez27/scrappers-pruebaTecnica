from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import os
from dotenv import load_dotenv
from datetime import datetime

# Importar nuestros módulos
from .scraping import search_entity
from .models import SearchRequest, SearchResponse, EntityResult, ErrorResponse
from .auth import verify_token, get_api_token
from .rate_limit import limiter, get_rate_limit_info, create_rate_limit_exceeded_response

# Cargar variables de entorno
load_dotenv()

# Crear la aplicación FastAPI
app = FastAPI(
    title="API de Búsqueda en Listas de Alto Riesgo",
    description="""
    API REST para buscar entidades en listas de alto riesgo usando web scraping.
    
    ## Características
    * 🔍 Búsqueda en múltiples fuentes (Offshore Leaks, World Bank, OFAC)
    * 🔐 Autenticación con Bearer Token
    * ⏱️ Rate limiting (20 llamadas por minuto)
    * 📊 Resultados estructurados con metadatos
    
    ## Fuentes disponibles
    * **Offshore Leaks Database**: Entidades offshore y jurisdicciones
    * **World Bank Debarred Firms**: Firmas ineligibles para contratos
    * **OFAC Sanctions**: Lista de sanciones de EE.UU.
    """,
    version="1.0.0",
    contact={
        "name": "API Support",
        "email": "support@example.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# Configurar rate limiting en la app
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Configurar autenticación
security = HTTPBearer()

@app.get("/", tags=["Información"])
async def root():
    """
    Endpoint raíz que proporciona información básica sobre la API.
    """
    return {
        "message": "API de Búsqueda en Listas de Alto Riesgo",
        "version": "1.0.0",
        "status": "activo",
        "timestamp": datetime.now().isoformat(),
        "endpoints": {
            "search": "/search",
            "health": "/health",
            "docs": "/docs",
            "rate_limit_info": "/rate-limit-info"
        }
    }

@app.get("/health", tags=["Monitoreo"])
async def health_check():
    """
    Endpoint de verificación de salud de la API.
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

@app.get("/rate-limit-info", tags=["Información"])
async def rate_limit_info():
    """
    Endpoint que proporciona información sobre los límites de velocidad.
    """
    return get_rate_limit_info()

@app.post("/search", 
          response_model=SearchResponse,
          tags=["Búsqueda"],
          summary="Buscar entidad en listas de alto riesgo",
          description="""
          Busca una entidad en las listas de alto riesgo especificadas.
          
          **Requerimientos:**
          * Autenticación con Bearer Token
          * Rate limiting: máximo 20 llamadas por minuto
          
          **Fuentes disponibles:**
          * `all`: Busca en todas las fuentes
          * `offshore_leaks`: Solo Offshore Leaks Database
          * `world_bank`: Solo World Bank Debarred Firms
          * `ofac`: Solo OFAC Sanctions
          """)
@limiter.limit("20/minute")
async def search_entity_endpoint(
    request: Request,
    search_request: SearchRequest,
    token: str = Depends(verify_token)
):
    """
    Endpoint principal para buscar entidades en listas de alto riesgo.
    
    Args:
        request: Petición HTTP
        search_request: Datos de la búsqueda (nombre de entidad y fuente)
        token: Token de autenticación
        
    Returns:
        SearchResponse: Resultados de la búsqueda
        
    Raises:
        HTTPException: Si hay errores en la búsqueda
    """
    try:
        # Validar el nombre de la entidad
        if not search_request.entity_name.strip():
            raise HTTPException(
                status_code=400,
                detail="El nombre de la entidad no puede estar vacío"
            )
        
        # Validar la fuente especificada
        valid_sources = ["all", "offshore_leaks", "world_bank", "ofac"]
        if search_request.source not in valid_sources:
            raise HTTPException(
                status_code=400,
                detail=f"Fuente inválida. Fuentes válidas: {', '.join(valid_sources)}"
            )
        
        # Realizar la búsqueda
        result = search_entity(
            entity_name=search_request.entity_name,
            source=search_request.source
        )
        
        return result
        
    except HTTPException:
        # Re-lanzar las excepciones HTTP que ya hemos creado
        raise
    except Exception as e:
        # Manejar errores inesperados
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor: {str(e)}"
        )

@app.get("/sources", tags=["Información"])
async def get_available_sources():
    """
    Endpoint que lista las fuentes disponibles para búsqueda.
    """
    return {
        "sources": [
            {
                "id": "offshore_leaks",
                "name": "Offshore Leaks Database",
                "url": "https://offshoreleaks.icij.org",
                "description": "Base de datos de entidades offshore y jurisdicciones",
                "attributes": ["Entity", "Jurisdiction", "Linked To", "Data From"]
            },
            {
                "id": "world_bank",
                "name": "World Bank Debarred Firms",
                "url": "https://projects.worldbank.org/en/projects-operations/procurement/debarred-firms",
                "description": "Lista de firmas ineligibles para contratos del Banco Mundial",
                "attributes": ["Firm Name", "Address", "Country", "From Date", "To Date", "Grounds"]
            },
            {
                "id": "ofac",
                "name": "OFAC Sanctions",
                "url": "https://sanctionssearch.ofac.treas.gov",
                "description": "Lista de sanciones de la Oficina de Control de Activos Extranjeros",
                "attributes": ["Name", "Address", "Type", "Program(s)", "List", "Score"]
            }
        ]
    }

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """
    Manejador personalizado para excepciones HTTP.
    """
    return ErrorResponse(
        error=exc.detail,
        detail=f"Error {exc.status_code}: {exc.detail}",
        timestamp=datetime.now()
    )

@app.exception_handler(RateLimitExceeded)
async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    """
    Manejador personalizado para excepciones de rate limiting.
    """
    return create_rate_limit_exceeded_response(request, exc)

# Configurar CORS para permitir peticiones desde diferentes orígenes
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica los orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
) 