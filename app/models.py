from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class SearchRequest(BaseModel):
    """
    Modelo para las peticiones de búsqueda.
    Define qué datos debe enviar el cliente para buscar una entidad.
    """
    entity_name: str = Field(
        ..., 
        description="Nombre de la entidad a buscar",
        min_length=1,
        max_length=200,
        example="John Doe"
    )
    source: Optional[str] = Field(
        default="all",
        description="Fuente específica para buscar (offshore_leaks, world_bank, ofac, all)",
        example="offshore_leaks"
    )

class EntityResult(BaseModel):
    """
    Modelo para los resultados individuales de entidades encontradas.
    Cada resultado representa una entidad encontrada en las listas de alto riesgo.
    """
    name: str = Field(..., description="Nombre de la entidad")
    source: str = Field(..., description="Fuente donde se encontró (Offshore Leaks, World Bank, OFAC)")
    jurisdiction: Optional[str] = Field(None, description="Jurisdicción de la entidad")
    address: Optional[str] = Field(None, description="Dirección de la entidad")
    entity_type: Optional[str] = Field(None, description="Tipo de entidad")
    linked_to: Optional[str] = Field(None, description="Entidades relacionadas")
    data_from: Optional[str] = Field(None, description="Fecha de los datos")
    country: Optional[str] = Field(None, description="País de la entidad")
    from_date: Optional[str] = Field(None, description="Fecha de inicio de ineligibilidad")
    to_date: Optional[str] = Field(None, description="Fecha de fin de ineligibilidad")
    grounds: Optional[str] = Field(None, description="Motivos de ineligibilidad")
    programs: Optional[str] = Field(None, description="Programas de sanciones")
    list_name: Optional[str] = Field(None, description="Nombre de la lista")
    score: Optional[str] = Field(None, description="Puntuación de coincidencia")
    url: Optional[str] = Field(None, description="URL de la fuente original")

class SearchResponse(BaseModel):
    """
    Modelo para las respuestas de búsqueda.
    Define qué datos devuelve la API cuando se realiza una búsqueda.
    """
    entity_name: str = Field(..., description="Nombre de la entidad buscada")
    total_hits: int = Field(..., description="Número total de coincidencias encontradas")
    search_time: float = Field(..., description="Tiempo de búsqueda en segundos")
    sources_searched: List[str] = Field(..., description="Fuentes que se buscaron")
    results: List[EntityResult] = Field(..., description="Lista de entidades encontradas")
    timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp de la búsqueda")

class ErrorResponse(BaseModel):
    """
    Modelo para las respuestas de error.
    Define cómo se estructuran los mensajes de error de la API.
    """
    error: str = Field(..., description="Descripción del error")
    detail: Optional[str] = Field(None, description="Detalles adicionales del error")
    timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp del error") 