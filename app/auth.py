import os
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configurar el esquema de autenticación
security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Verifica el token de autenticación.
    
    Args:
        credentials: Credenciales HTTP Bearer token
        
    Returns:
        str: El token verificado
        
    Raises:
        HTTPException: Si el token es inválido o no está presente
    """
    # Obtener el token del archivo .env o usar un valor por defecto
    valid_token = os.getenv("API_TOKEN", "test_token_123")
    
    if not credentials:
        raise HTTPException(
            status_code=401,
            detail="Token de autenticación requerido"
        )
    
    if credentials.credentials != valid_token:
        raise HTTPException(
            status_code=401,
            detail="Token de autenticación inválido"
        )
    
    return credentials.credentials

def get_api_token():
    """
    Obtiene el token de la API desde las variables de entorno.
    
    Returns:
        str: El token de la API
    """
    return os.getenv("API_TOKEN", "test_token_123") 