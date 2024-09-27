## Despliegue de modelo (Deploy)

En esta rama realizaremos toda la lógica para desplegar la aplicación que utilizara el modelo, utilizando Docker y FastAPI. Esta rama tendrá la función de utilizarse para los testing, mientras que la rama `deploy_prod` busca simular un ambiente de production conectándonos a un cliente, en este caso AWS.

- **app/** : API para la realización de una predicción [Detalle](app\README.md)

### Dockerfile y docker-compose

**Dockerfile:** El encargado de generar el contenedor. Simplemente carga el Python a utilizar, setea el  directorio de trabajo (Workdir), variables de entorno y carga los paquetes que utilizaremos.

**docker-compose:** Permite definir y orquestar múltiples contenedores para crear un entorno de desarrollo completo. 

En el defino varios servicios, que utilizan diferentes contenedores, para este caso se definen 4 servicios: 

- `web`: desplegar el servicio web con Uvicorn y FastAPI

- `db`: gestiona la base de datos postgres

- `adminer`: Es un auxiliar para la base de datos

- `grafana`: permite visualizar y monitorear el servicio

`db`, `adminer` y `grafana` utilizan imágenes publica de dockers

Por ultimo, definimos los volúmenes (lugares donde Docker guardara datos)

```yaml
volumes:
  postgres_data:
  grafana_data: {}
```
Con esto tendré acceso a los datos de la base de datos y a los de monitoreo

---
#### Analizando cada servicio definido

- **Servicio `web`:**


```yaml
web:
    build: .
```
Primero define el servicio y luego con `build: .` le indico que lo construya a partir de la imagen de que se encuentra en el directorio actual

```yaml
    command: bash -c 'while !</dev/tcp/db/5432; do sleep 1; done; uvicorn app.main:app --reload --host 0.0.0.0'
    volumes:
      - .:/app
```
Luego se indica que ejecute el comando para la generación del servicio web con uvicorn y que mapee el directorio actual (`.`) a la carpeta `/app` del contenedor

```yaml
   ports:
      - "5004:8000"
```
Continuo habilitando los puertos de comunicación. Los puertos indicados son el `HOST_PORT` y el `CONTAINER_PORT`, con la forma `HOST_PORT:CONTAINER_PORT`. 

El `HOST_PORT` es para la comunicación externa mientras que el `CONTAINER_PORT` es para la comunicación interna, es decir, entre contenedores. Para este caso, el puerto **5004** es para acceder al servicio desde afuera (se podría realizar como **: //{DOCKER_IP}:5004**) mientras que el puerto 8000 lo utilizaria otro contenedor para acceder a este.

```yaml
    environment:
      - DATABASE_URL=postgresql://fastapi_traefik:fastapi_traefik@db:5432/fastapi_traefik
    depends_on:
      - db
```

Por ultimo defino como variable de entorno `DATABASE_URL` el acceso a la base de datos y, por ultimo, que va a utilizar de dependencia, para este caso, el servicio db. Esto indica un orden de prioridades al crear los servicios, para este caso, esperar que el servicio db sea creado correctamente para crear el servicio web

<sub>
Nota: observe que DATABASE_URL posee la forma [POSTGRES_USER : POSTGRES_PASSWORD @db : CONTAINER_PORT / POSTGRES_DB ] ya que es la forma de acceder a la base de datos postgres y son las variables que luego define el servicio `db`
</sub>

---
**Servicio `db`**

```yaml
  db:
    image: postgres:15-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    ports:
      - "5433:5432"
    expose:
      - 5432
    environment:
      - POSTGRES_USER=fastapi_traefik
      - POSTGRES_PASSWORD=fastapi_traefik
      - POSTGRES_DB=fastapi_traefik
```
A diferencia del servicio `web` que se utilizo el `build` para construirlo a partid de la imagen, aca se utiliza el `image` para que utilice la imagen publica de postgres para generar el contenedor.

Luego mapea el directorio `postgres_data` a la carpeta del contenedor `/var/lib/postgresql/data/`, esto significa que cuando pida acceder a `postgres_data`, en realidad voy a estar accediendo a `/var/lib/postgresql/data/`.

Continuo habilitando los puertos (`HOST_PORT:CONTAINER_PORT`) y con `expose` le indico que el puerto **5432** es solo accesible dentro de la red de docker (aunque al ya estar definido como ``CONTAINER_PORT`` el uso del expose seria una redundancia)

Y por ultimo defino las variables de entorno (user, password y nombre de la base de datos) para el acceso

---
Para los servicios `adminer` y `grafana` no se explicara en detalle, ya que, con lo expuesto anteriormente se puede comprender su configuración. 

Solo se indicara dos instrucciones: 
- `restart: always` indica que, si llega a detenerse, siempre se reinicie el servicio.
-  `user: "472"`, que aparece en el servicio de grafana, es una configuración propia de grafana