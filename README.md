# API de Búsqueda en Listas de Alto Riesgo

API REST para buscar entidades en listas de alto riesgo usando web scraping. Desarrollada como prueba técnica para una institución financiera.

## 🎯 Características

- 🔍 **Búsqueda en múltiples fuentes**: Offshore Leaks, World Bank, OFAC
- 🔐 **Autenticación**: Bearer Token para proteger la API
- ⏱️ **Rate Limiting**: Máximo 20 llamadas por minuto
- 📊 **Resultados estructurados**: JSON con metadatos completos
- 📚 **Documentación automática**: Swagger UI integrado
- 🛡️ **Validaciones**: Manejo robusto de errores

## 🚀 Instalación

### Prerrequisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de instalación

1. **Clonar el repositorio**
   ```bash
   git clone <url-del-repositorio>
   cd scrappers-pruebaTecnica
   ```

2. **Crear entorno virtual (recomendado)**
   ```bash
   python -m venv venv
   
   # En Windows
   venv\Scripts\activate
   
   # En macOS/Linux
   source venv/bin/activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno**
   ```bash
   # Copiar el archivo de ejemplo
   cp env.example .env
   
   # Editar el archivo .env con tus configuraciones
   # El token por defecto es: test_token_123
   ```

## 🏃‍♂️ Ejecución

### Desarrollo local

```bash
python run.py
```

O directamente con uvicorn:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Acceso a la API

- **API Base**: http://localhost:8000
- **Documentación**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 📖 Uso de la API

### Autenticación

Todas las peticiones requieren autenticación con Bearer Token:

```bash
Authorization: Bearer test_token_123
```

### Endpoints principales

#### 1. Buscar entidad

```bash
POST /search
Content-Type: application/json
Authorization: Bearer test_token_123

{
  "entity_name": "John Doe",
  "source": "all"
}
```

**Parámetros:**
- `entity_name` (requerido): Nombre de la entidad a buscar
- `source` (opcional): Fuente específica (`all`, `offshore_leaks`, `world_bank`, `ofac`)

#### 2. Información de la API

```bash
GET /
```

#### 3. Health Check

```bash
GET /health
```

#### 4. Fuentes disponibles

```bash
GET /sources
```

#### 5. Información de rate limiting

```bash
GET /rate-limit-info
```

### Ejemplos de uso

#### Con curl

```bash
# Buscar en todas las fuentes
curl -X POST "http://localhost:8000/search" \
  -H "Authorization: Bearer test_token_123" \
  -H "Content-Type: application/json" \
  -d '{"entity_name": "John Doe", "source": "all"}'

# Buscar solo en Offshore Leaks
curl -X POST "http://localhost:8000/search" \
  -H "Authorization: Bearer test_token_123" \
  -H "Content-Type: application/json" \
  -d '{"entity_name": "John Doe", "source": "offshore_leaks"}'
```

#### Con Python requests

```python
import requests

url = "http://localhost:8000/search"
headers = {
    "Authorization": "Bearer test_token_123",
    "Content-Type": "application/json"
}
data = {
    "entity_name": "John Doe",
    "source": "all"
}

response = requests.post(url, headers=headers, json=data)
print(response.json())
```

## 🔧 Configuración

### Variables de entorno

Crea un archivo `.env` basado en `env.example`:

```env
# Token de autenticación
API_TOKEN=tu_token_secreto

# Configuración del servidor
HOST=0.0.0.0
PORT=8000

# Logging
LOG_LEVEL=INFO

# Rate limiting
MAX_REQUESTS_PER_MINUTE=20
```

## 📁 Estructura del proyecto

```
scrappers-pruebaTecnica/
├── app/
│   ├── __init__.py
│   ├── main.py           # Punto de entrada de la API
│   ├── models.py         # Modelos de datos (Pydantic)
│   ├── auth.py           # Autenticación
│   ├── rate_limit.py     # Rate limiting
│   └── scraping.py       # Lógica de web scraping
├── requirements.txt      # Dependencias
├── run.py               # Script de ejecución
├── env.example          # Variables de entorno de ejemplo
└── README.md           # Este archivo
```

## 🧪 Testing

### Probar la API

1. **Iniciar el servidor**
   ```bash
   python run.py
   ```

2. **Abrir la documentación**
   - Ve a http://localhost:8000/docs
   - Haz clic en "Authorize" e ingresa: `test_token_123`
   - Prueba los endpoints desde la interfaz

3. **Probar con Postman**
   - Importa la colección de Postman (ver sección Postman)
   - Configura el token de autenticación
   - Ejecuta las peticiones

## 📊 Fuentes de datos

### Offshore Leaks Database
- **URL**: https://offshoreleaks.icij.org
- **Atributos**: Entity, Jurisdiction, Linked To, Data From

### World Bank Debarred Firms
- **URL**: https://projects.worldbank.org/en/projects-operations/procurement/debarred-firms
- **Atributos**: Firm Name, Address, Country, From Date, To Date, Grounds

### OFAC Sanctions
- **URL**: https://sanctionssearch.ofac.treas.gov
- **Atributos**: Name, Address, Type, Program(s), List, Score

## 🚨 Limitaciones

- **Web Scraping**: Las implementaciones actuales son ejemplos simplificados
- **Rate Limiting**: Las fuentes externas pueden tener sus propios límites
- **Disponibilidad**: Las fuentes externas pueden no estar siempre disponibles

## 🔒 Seguridad

- **Autenticación**: Bearer Token requerido para todos los endpoints
- **Rate Limiting**: Protección contra abuso (20 llamadas/minuto)
- **Validación**: Validación de entrada en todos los endpoints
- **CORS**: Configurado para desarrollo (ajustar en producción)

## 📈 Monitoreo

### Health Check
```bash
GET /health
```

### Logs
Los logs se muestran en la consola con nivel INFO por defecto.

## 🚀 Despliegue

### Desarrollo
```bash
python run.py
```

### Producción
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Docker (opcional)
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 📝 Notas importantes

1. **Token por defecto**: `test_token_123` (cambiar en producción)
2. **Rate limiting**: 20 llamadas por minuto por IP
3. **Web scraping**: Implementación educativa, ajustar según necesidades reales
4. **Fuentes**: Las URLs y estructuras pueden cambiar, actualizar según sea necesario

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 📞 Soporte

Para soporte técnico o preguntas sobre la implementación, contacta a través de los issues del repositorio.