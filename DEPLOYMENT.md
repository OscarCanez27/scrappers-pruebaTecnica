# Guía de Despliegue - API de Búsqueda en Listas de Alto Riesgo

Esta guía te ayudará a desplegar la API en diferentes entornos, desde desarrollo local hasta producción.

## 🚀 Despliegue Local (Desarrollo)

### Prerrequisitos
- Python 3.8+
- pip
- Git

### Pasos

1. **Clonar el repositorio**
   ```bash
   git clone <url-del-repositorio>
   cd scrappers-pruebaTecnica
   ```

2. **Crear entorno virtual**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno**
   ```bash
   cp env.example .env
   # Editar .env según necesites
   ```

5. **Ejecutar la aplicación**
   ```bash
   python run.py
   ```

6. **Verificar que funciona**
   - API: http://localhost:8000
   - Documentación: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

## 🐳 Despliegue con Docker

### Crear Dockerfile

```dockerfile
FROM python:3.9-slim

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivo de dependencias
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY . .

# Exponer puerto
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Construir y ejecutar con Docker

```bash
# Construir imagen
docker build -t api-risk-lists .

# Ejecutar contenedor
docker run -p 8000:8000 --env-file .env api-risk-lists
```

### Docker Compose (recomendado)

Crear `docker-compose.yml`:

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - API_TOKEN=test_token_123
      - HOST=0.0.0.0
      - PORT=8000
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped
```

Ejecutar:
```bash
docker-compose up -d
```

## ☁️ Despliegue en la Nube

### AWS (EC2)

1. **Crear instancia EC2**
   - Tipo: t2.micro (gratis) o t3.small
   - Sistema operativo: Ubuntu 20.04 LTS
   - Configurar Security Group para puerto 8000

2. **Conectar y configurar**
   ```bash
   # Conectar via SSH
   ssh -i tu-key.pem ubuntu@tu-ip-ec2
   
   # Actualizar sistema
   sudo apt update && sudo apt upgrade -y
   
   # Instalar Python y dependencias
   sudo apt install python3 python3-pip python3-venv -y
   
   # Clonar repositorio
   git clone <url-del-repositorio>
   cd scrappers-pruebaTecnica
   
   # Crear entorno virtual
   python3 -m venv venv
   source venv/bin/activate
   
   # Instalar dependencias
   pip install -r requirements.txt
   
   # Configurar variables de entorno
   cp env.example .env
   # Editar .env con valores de producción
   ```

3. **Configurar como servicio**
   ```bash
   # Crear archivo de servicio
   sudo nano /etc/systemd/system/api-risk-lists.service
   ```

   Contenido del archivo:
   ```ini
   [Unit]
   Description=API de Búsqueda en Listas de Alto Riesgo
   After=network.target
   
   [Service]
   Type=simple
   User=ubuntu
   WorkingDirectory=/home/ubuntu/scrappers-pruebaTecnica
   Environment=PATH=/home/ubuntu/scrappers-pruebaTecnica/venv/bin
   ExecStart=/home/ubuntu/scrappers-pruebaTecnica/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
   Restart=always
   
   [Install]
   WantedBy=multi-user.target
   ```

4. **Iniciar servicio**
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable api-risk-lists
   sudo systemctl start api-risk-lists
   sudo systemctl status api-risk-lists
   ```

### Azure (App Service)

1. **Crear App Service**
   - Plataforma: Python 3.9
   - Plan: B1 (básico) o superior

2. **Configurar variables de entorno**
   - Ir a Configuration > Application settings
   - Agregar:
     - `API_TOKEN`: tu_token_secreto
     - `HOST`: 0.0.0.0
     - `PORT`: 8000

3. **Desplegar código**
   ```bash
   # Instalar Azure CLI
   az login
   az webapp up --name tu-app-name --resource-group tu-resource-group --runtime "PYTHON:3.9"
   ```

### Google Cloud Platform (App Engine)

1. **Crear app.yaml**
   ```yaml
   runtime: python39
   
   env_variables:
     API_TOKEN: "tu_token_secreto"
     HOST: "0.0.0.0"
     PORT: "8080"
   
   handlers:
   - url: /.*
     script: auto
   ```

2. **Desplegar**
   ```bash
   gcloud app deploy
   ```

## 🔧 Configuración de Producción

### Variables de entorno recomendadas

```env
# Token de autenticación (CAMBIAR EN PRODUCCIÓN)
API_TOKEN=tu_token_super_secreto_aqui

# Configuración del servidor
HOST=0.0.0.0
PORT=8000

# Logging
LOG_LEVEL=WARNING

# Rate limiting
MAX_REQUESTS_PER_MINUTE=20

# Configuración adicional para producción
ENVIRONMENT=production
DEBUG=false
```

### Configuración de seguridad

1. **Cambiar token por defecto**
   ```bash
   # Generar token seguro
   openssl rand -hex 32
   ```

2. **Configurar firewall**
   ```bash
   # Solo permitir puerto 8000
   sudo ufw allow 8000
   sudo ufw enable
   ```

3. **Configurar HTTPS (recomendado)**
   - Usar Nginx como proxy reverso
   - Configurar certificados SSL con Let's Encrypt

### Configuración de Nginx (opcional)

```nginx
server {
    listen 80;
    server_name tu-dominio.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 📊 Monitoreo

### Health Check
```bash
curl http://tu-servidor:8000/health
```

### Logs
```bash
# Ver logs del servicio
sudo journalctl -u api-risk-lists -f

# Ver logs de la aplicación
tail -f logs/app.log
```

### Métricas básicas
- Uptime: `uptime`
- Uso de memoria: `free -h`
- Uso de CPU: `top`
- Espacio en disco: `df -h`

## 🔄 Actualizaciones

### Actualizar código
```bash
# Detener servicio
sudo systemctl stop api-risk-lists

# Actualizar código
git pull origin main

# Instalar nuevas dependencias
source venv/bin/activate
pip install -r requirements.txt

# Reiniciar servicio
sudo systemctl start api-risk-lists
```

### Rollback
```bash
# Volver a versión anterior
git checkout <commit-anterior>

# Reiniciar servicio
sudo systemctl restart api-risk-lists
```

## 🚨 Troubleshooting

### Problemas comunes

1. **Puerto ya en uso**
   ```bash
   # Ver qué proceso usa el puerto
   sudo netstat -tlnp | grep :8000
   
   # Matar proceso
   sudo kill -9 <PID>
   ```

2. **Error de permisos**
   ```bash
   # Cambiar permisos
   sudo chown -R ubuntu:ubuntu /home/ubuntu/scrappers-pruebaTecnica
   ```

3. **Error de dependencias**
   ```bash
   # Reinstalar entorno virtual
   rm -rf venv
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Error de memoria**
   ```bash
   # Ver uso de memoria
   free -h
   
   # Reiniciar servicio
   sudo systemctl restart api-risk-lists
   ```

## 📞 Soporte

Para problemas de despliegue:
1. Revisar logs: `sudo journalctl -u api-risk-lists -f`
2. Verificar estado: `sudo systemctl status api-risk-lists`
3. Probar endpoint: `curl http://localhost:8000/health`
4. Crear issue en el repositorio con logs y configuración 