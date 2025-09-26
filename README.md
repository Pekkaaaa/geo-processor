# Geo Processor (FastAPI + Poetry + Docker)

Servicio que recibe una lista de coordenadas y devuelve:

- **centroid** (promedio lat/lng)
- **bounds** (north/south/east/west)

Incluye:

- **Poetry** para dependencias
- **Ruff + mypy + pytest**
- **Middleware** que exige `x-api-key`
- **.env** con `pydantic-settings` y `decouple`
- **Dockerfile** multietapa (imagen ligera)

---

## Estructura del proyecto

```
geo-processor/
├── app/
│   ├── __init__.py
│   ├── config.py        # Config desde .env (pydantic-settings). Lee las variables
│   ├── main.py          # Crea la app con FastAPI, añade middleware e incluye router
│   ├── middleware.py    # Valida header x-api-key para endpoints protegidos
│   ├── models.py        # Pydantic models (request/response)
│   └── router.py        # Rutas: /api/health (GET), /api/process (POST)
├── tests/
│   ├── test_api.py      # Genera los tests de api
│   └── test_auth.py     # Genera los tests de autorización con el api key
├── .env.rename          # Variables de entorno de ejemplo
├── Dockerfile           # Build multietapa con Poetry
├── pyproject.toml       # Poetry + linters + mypy
└── README.md            # Este archivo
```

### Notas de diseño

- `config.py` lee `.env` con **pydantic-settings** y **decouple** y maneja:
  - `APP_NAME`
  - `DEBUG`
  - `API_KEY`
  - `PUBLIC_PATHS`
- `middleware.py` protege todo **salvo** rutas en `PUBLIC_PATHS`.
- `router.py` expone:
  - `GET /api/health` (público)
  - `POST /api/process` (requiere `x-api-key`)

---

## Requisitos

- Python **3.10+** (probado con 3.10 y 3.13)
- Poetry **≥ 1.6**
- Docker (opcional)

---

## Configuración de entorno (.env)

Copia el ejemplo y ajusta valores:

```bash
cp .env.rename .env
```

Contenido recomendado:

```env
APP_NAME=Geo Processor
DEBUG=false
API_KEY=api-key
PUBLIC_PATHS=/api/health,/openapi.json,/docs,/redoc
```

---

## Ejecución **sin Docker** (Poetry)

Instala dependencias (incluyendo dev):

```bash
poetry install --with dev
```

Activa el ambiente

```bash
eval $(poetry env activate)
```

Corre el servidor:

```bash
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Abre:

- Swagger: http://localhost:8000/docs  
- Health: http://localhost:8000/health

---

## Ejecución **con Docker**

**Build:**

```bash
docker build -t geo-processor:latest .
```

**Run** (leyendo variables desde tu `.env`):

```bash
docker run --rm -p 8000:8000 --env-file .env geo-processor:latest
```

_O_ pasando variables explícitas:

```bash
docker run --rm -p 8000:8000   -e APP_NAME="Geo Processor"   -e DEBUG=false   -e API_KEY="tu-super-api-key"   -e PUBLIC_PATHS="/health,/openapi.json,/docs,/redoc"   geo-processor:latest
```

---

## Correr pruebas

### Con Poetry (recomendado)

```bash
poetry run pytest
```

o

```bash
poetry run pytest -v
```

---

## Ejemplos **curl** de todos los endpoints

La API Key se envía en el header **`x-api-key`**.  


### 1) Health (público)

```bash
curl -s http://localhost:8000/api/health
# {"status":"ok"}
```

### 2) Process (protegido: requiere `x-api-key`)

```bash
curl -s -X POST http://localhost:8000/api/process   -H "Content-Type: application/json"   -H "x-api-key: nLBmh4RfVEuEzhUwcXTMipzEWt7595NH"   -d '{"points":[{"lat":40.7128,"lng":-74.0060},{"lat":34.0522,"lng":-118.2437},{"lat":41.8781,"lng":-87.6298}]}'
```

**Respuesta 200 (ejemplo):**

```json
{
  "centroid": { "lat": 38.21436666666667, "lng": -93.2929 },
  "bounds": { "north": 41.8781, "south": 34.0522, "east": -74.006, "west": -118.2437 }
}
```

**Errores típicos:**

- `401` sin API key:

  ```json
  {"error":"Unauthorized: invalid or missing x-api-key"}
  ```

- `400` por validación (p. ej., lat fuera de rango):

  ```json
  {"error":"points.0.lat: Input should be greater than or equal to -90"}
  ```

---

