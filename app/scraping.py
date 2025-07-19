import requests
from bs4 import BeautifulSoup
import time
from typing import List, Dict, Optional
from .models import EntityResult, SearchResponse
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WebScraper:
    """
    Clase principal para realizar web scraping en listas de alto riesgo.
    """
    
    def __init__(self):
        """
        Inicializa el scraper con configuraciones básicas.
        """
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def search_offshore_leaks(self, entity_name: str) -> List[EntityResult]:
        """
        Busca una entidad en la Offshore Leaks Database.
        
        Args:
            entity_name: Nombre de la entidad a buscar
            
        Returns:
            List[EntityResult]: Lista de entidades encontradas
        """
        try:
            logger.info(f"Buscando '{entity_name}' en Offshore Leaks Database")
            
            # URL de búsqueda de Offshore Leaks
            search_url = "https://offshoreleaks.icij.org/search"
            
            # Parámetros de búsqueda
            params = {
                'q': entity_name,
                'cat': '1',  # Buscar en entidades
                'from': '0',
                'size': '20'
            }
            
            # Realizar la petición
            response = self.session.get(search_url, params=params, timeout=30)
            response.raise_for_status()
            
            # Parsear el HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            results = []
            
            # Buscar resultados en la página (esto es un ejemplo simplificado)
            # En una implementación real, necesitarías analizar la estructura específica de la página
            search_results = soup.find_all('div', class_='search-result')
            
            for result in search_results:
                try:
                    # Extraer información del resultado
                    name_elem = result.find('h3', class_='entity-name')
                    name = name_elem.get_text(strip=True) if name_elem else "N/A"
                    
                    jurisdiction_elem = result.find('span', class_='jurisdiction')
                    jurisdiction = jurisdiction_elem.get_text(strip=True) if jurisdiction_elem else None
                    
                    linked_to_elem = result.find('span', class_='linked-to')
                    linked_to = linked_to_elem.get_text(strip=True) if linked_to_elem else None
                    
                    data_from_elem = result.find('span', class_='data-from')
                    data_from = data_from_elem.get_text(strip=True) if data_from_elem else None
                    
                    # Crear el resultado
                    entity_result = EntityResult(
                        name=name,
                        source="Offshore Leaks Database",
                        jurisdiction=jurisdiction,
                        linked_to=linked_to,
                        data_from=data_from,
                        url=search_url
                    )
                    
                    results.append(entity_result)
                    
                except Exception as e:
                    logger.error(f"Error procesando resultado de Offshore Leaks: {e}")
                    continue
            
            logger.info(f"Encontrados {len(results)} resultados en Offshore Leaks Database")
            return results
            
        except requests.RequestException as e:
            logger.error(f"Error de red al buscar en Offshore Leaks: {e}")
            return []
        except Exception as e:
            logger.error(f"Error inesperado al buscar en Offshore Leaks: {e}")
            return []
    
    def search_world_bank(self, entity_name: str) -> List[EntityResult]:
        """
        Busca una entidad en la lista de firmas debarred del World Bank.
        
        Args:
            entity_name: Nombre de la entidad a buscar
            
        Returns:
            List[EntityResult]: Lista de entidades encontradas
        """
        try:
            logger.info(f"Buscando '{entity_name}' en World Bank Debarred Firms")
            
            # URL de búsqueda del World Bank
            search_url = "https://projects.worldbank.org/en/projects-operations/procurement/debarred-firms"
            
            # Parámetros de búsqueda
            params = {
                'search': entity_name
            }
            
            # Realizar la petición
            response = self.session.get(search_url, params=params, timeout=30)
            response.raise_for_status()
            
            # Parsear el HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            results = []
            
            # Buscar resultados en la página (ejemplo simplificado)
            search_results = soup.find_all('tr', class_='debarred-firm')
            
            for result in search_results:
                try:
                    # Extraer información del resultado
                    cells = result.find_all('td')
                    if len(cells) >= 4:
                        firm_name = cells[0].get_text(strip=True) if cells[0] else "N/A"
                        address = cells[1].get_text(strip=True) if len(cells) > 1 and cells[1] else None
                        country = cells[2].get_text(strip=True) if len(cells) > 2 and cells[2] else None
                        from_date = cells[3].get_text(strip=True) if len(cells) > 3 and cells[3] else None
                        to_date = cells[4].get_text(strip=True) if len(cells) > 4 and cells[4] else None
                        grounds = cells[5].get_text(strip=True) if len(cells) > 5 and cells[5] else None
                        
                        # Crear el resultado
                        entity_result = EntityResult(
                            name=firm_name,
                            source="World Bank Debarred Firms",
                            address=address,
                            country=country,
                            from_date=from_date,
                            to_date=to_date,
                            grounds=grounds,
                            url=search_url
                        )
                        
                        results.append(entity_result)
                        
                except Exception as e:
                    logger.error(f"Error procesando resultado del World Bank: {e}")
                    continue
            
            logger.info(f"Encontrados {len(results)} resultados en World Bank")
            return results
            
        except requests.RequestException as e:
            logger.error(f"Error de red al buscar en World Bank: {e}")
            return []
        except Exception as e:
            logger.error(f"Error inesperado al buscar en World Bank: {e}")
            return []
    
    def search_ofac(self, entity_name: str) -> List[EntityResult]:
        """
        Busca una entidad en la lista de sanciones de OFAC.
        
        Args:
            entity_name: Nombre de la entidad a buscar
            
        Returns:
            List[EntityResult]: Lista de entidades encontradas
        """
        try:
            logger.info(f"Buscando '{entity_name}' en OFAC Sanctions")
            
            # URL de búsqueda de OFAC
            search_url = "https://sanctionssearch.ofac.treas.gov"
            
            # Parámetros de búsqueda
            params = {
                'name': entity_name
            }
            
            # Realizar la petición
            response = self.session.get(search_url, params=params, timeout=30)
            response.raise_for_status()
            
            # Parsear el HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            results = []
            
            # Buscar resultados en la página (ejemplo simplificado)
            search_results = soup.find_all('div', class_='sanctioned-entity')
            
            for result in search_results:
                try:
                    # Extraer información del resultado
                    name_elem = result.find('span', class_='entity-name')
                    name = name_elem.get_text(strip=True) if name_elem else "N/A"
                    
                    address_elem = result.find('span', class_='address')
                    address = address_elem.get_text(strip=True) if address_elem else None
                    
                    entity_type_elem = result.find('span', class_='entity-type')
                    entity_type = entity_type_elem.get_text(strip=True) if entity_type_elem else None
                    
                    programs_elem = result.find('span', class_='programs')
                    programs = programs_elem.get_text(strip=True) if programs_elem else None
                    
                    list_name_elem = result.find('span', class_='list-name')
                    list_name = list_name_elem.get_text(strip=True) if list_name_elem else None
                    
                    score_elem = result.find('span', class_='score')
                    score = score_elem.get_text(strip=True) if score_elem else None
                    
                    # Crear el resultado
                    entity_result = EntityResult(
                        name=name,
                        source="OFAC Sanctions",
                        address=address,
                        entity_type=entity_type,
                        programs=programs,
                        list_name=list_name,
                        score=score,
                        url=search_url
                    )
                    
                    results.append(entity_result)
                    
                except Exception as e:
                    logger.error(f"Error procesando resultado de OFAC: {e}")
                    continue
            
            logger.info(f"Encontrados {len(results)} resultados en OFAC")
            return results
            
        except requests.RequestException as e:
            logger.error(f"Error de red al buscar en OFAC: {e}")
            return []
        except Exception as e:
            logger.error(f"Error inesperado al buscar en OFAC: {e}")
            return []

def search_entity(entity_name: str, source: str = "all") -> SearchResponse:
    """
    Función principal para buscar una entidad en las listas de alto riesgo.
    
    Args:
        entity_name: Nombre de la entidad a buscar
        source: Fuente específica para buscar ("offshore_leaks", "world_bank", "ofac", "all")
        
    Returns:
        SearchResponse: Respuesta con los resultados de la búsqueda
    """
    start_time = time.time()
    scraper = WebScraper()
    all_results = []
    sources_searched = []
    
    try:
        # Determinar qué fuentes buscar
        if source == "all" or source == "offshore_leaks":
            results = scraper.search_offshore_leaks(entity_name)
            all_results.extend(results)
            sources_searched.append("Offshore Leaks Database")
        
        if source == "all" or source == "world_bank":
            results = scraper.search_world_bank(entity_name)
            all_results.extend(results)
            sources_searched.append("World Bank Debarred Firms")
        
        if source == "all" or source == "ofac":
            results = scraper.search_ofac(entity_name)
            all_results.extend(results)
            sources_searched.append("OFAC Sanctions")
        
        search_time = time.time() - start_time
        
        return SearchResponse(
            entity_name=entity_name,
            total_hits=len(all_results),
            search_time=search_time,
            sources_searched=sources_searched,
            results=all_results
        )
        
    except Exception as e:
        logger.error(f"Error general en la búsqueda: {e}")
        search_time = time.time() - start_time
        
        return SearchResponse(
            entity_name=entity_name,
            total_hits=0,
            search_time=search_time,
            sources_searched=sources_searched,
            results=[]
        ) 