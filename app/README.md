## Implementación de la API

Se genera un api que permite realizar una predicción al modelo generado. La misma es implementada con FastAPI.

### Archivo `main.py`

En el archivo `main.py` se genera la app para el manejo de las solicitudes.

- Se definen las label, para la decodificación de la predicción:

```python
label_mapping = {
    "0": "Bank Account Services",
    "1": "Credit Report or Prepaid Card",
    "2": "Mortgage/Loan"}
```

- Se crean las clases para manejar y validar los valores de entrada. 

```python
class Sentence(BaseModel):
    client_name: str
    text: str 

class ProcessTextRequestModel(BaseModel):
    sentences: list[Sentence]
```

Los datos de entrada deben ser del tipo `ProcessTextRequestModel` el cual es una lista objetos `Sentence` que contiene quien lo solicita (client_name) y el texto a clasificar (text). Ambas clases se realizan con pydantic, esta librería es el que se encarga de la validación de los datos y la creación del objeto, las clases son heredadas de la clase BaseModel.

- Se genera la app y el entrypoint, en este caso del tipo POST, para realizar la predicción

```python
app = FastAPI(title="FastAPI, Docker, and Traefik")

@app.post("/predict")
async def read_root(data: ProcessTextRequestModel):
```

Esta app, no solo devolverá la predicción de la Clasificacion del texto pasado, sino que también lo guardara para mejorar el modelo. Dentro del archivo se comenta el paso a paso del funcionamiento

### Archivo `db.py`

El archivo `db.py` se encarga de manejar la base de datos. Se crea la clases para ingresar los datos a la base

```python
class PredictionsTickets(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    client_name: str 
    prediction: str
```
y la función para crear la tabla

### Archivo `util.py`

El archivo `util.py` se encarga del procesamiento del texto: Tokenización, Lematización, etc

### Archivo `config.py`

El archivo `config.py` va a guarda la dirección de la base de datos. Lo va a tomar del contenedor, definido en el docker-compose:

```yaml
environment:
      - DATABASE_URL=postgresql://fastapi_traefik:fastapi_traefik@db:5432/fastapi_traefik
```

### Archivo `prestart.sh`

El archivo `prestart.sh` se encarga de inicializar la base de datos