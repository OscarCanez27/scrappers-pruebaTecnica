from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request

# Configurar el limitador de velocidad
limiter = Limiter(key_func=get_remote_address)

def get_rate_limit_info():
    """
    Obtiene información sobre los límites de velocidad configurados.
    
    Returns:
        dict: Información sobre los límites de velocidad
    """
    return {
        "max_requests_per_minute": 20,
        "description": "Máximo 20 llamadas por minuto por IP"
    }

def create_rate_limit_exceeded_response(request: Request, exc: RateLimitExceeded):
    """
    Crea una respuesta personalizada cuando se excede el límite de velocidad.
    
    Args:
        request: La petición HTTP
        exc: La excepción de límite excedido
        
    Returns:
        dict: Respuesta de error personalizada
    """
    return {
        "error": "Rate limit exceeded",
        "detail": f"Has excedido el límite de {get_rate_limit_info()['max_requests_per_minute']} llamadas por minuto",
        "retry_after": exc.retry_after,
        "limit": exc.retry_after
    } 