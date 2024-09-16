### Task y WorkFlow

Un Workflow (flujo de trabajo) es un conjunto de actividades (tareas o task) relacionadas, que son completadas en un determinado orden y de forma automática para alcanzar un objetivo.

Un ejemplo de un Workflow:

    *Atender a una persona en un restaurante*
    
    Disparador: Llegada de una persona

    Workflow:
        - Recibir a la persona
        - Asignar mesa
        - Tomar pedido
        - Llevarle la comida
        - Cobrar el servicio
        - Despedir a la persona

Cada task de este workflow estará conformada por una seria de acciones propias de esa tarea. Por ejemplo, "asignar mesa" tendrá los pasos de verificar mesas disponibles, prepararla, llevar a la persona a la mesa. 

Incluso tareas, como llevar comida, sean un workflow en si (refiriendo a la confección del plato), al ser una tarea demasiado compleja para ser una simple task


### Prefect

La librería utilizada para la definición de las Task y los WorkFlow es `Prefect`. Para definir una task en prefect se utiliza el decorador `@task` y debajo el método que realizara la lógica de la task. Por ejemplo (tomado de [Iris Clasificacion](\introduction\run_iris.py)  ):

```python
@task(
    name="Load Iris Dataset",
    tags=["data_loading"],
    description="Load Iris dataset from sklearn",
)
def get_data_from_sklearn() -> dict:
    """This function loads the iris dataset from sklearn and returns it as a dictionary."""
    data = load_iris()
    return {"data": data.data, "target": data.target}
```

Los parámetros definidos en la task del ejemplo: `name`, `tags` y `description` son identificación y pueden ser omitidos

Las task deben ser colocadas dentro de un flow para que sean útiles. Su definición, es similar a definir una task: se utiliza el decorador `@flow` y debajo el método que realizara la lógica del flow. Por ejemplo:

```python
@flow(retries=3, retry_delay_seconds=5, log_prints=True)
def iris_classification():
    """This function orchestrates the whole flow"""
    dataset = get_data_from_sklearn()
    X_train, X_test, y_train, y_test = split_data(dataset)
    train_model(X_train, X_test, y_train, y_test)
```
<sub> 
Nota: `split_data` y `train_model` son task que también fueron definidas
</sub>

Los parámetros definidos en el flow del ejemplo: `retries`, `retry_delay_seconds` y `log_prints` definen el comportamiento del flow, para este caso que lo intente ejecutar 3 veces, que espere 5 segundos entre intento y printee los log. Si no se definieran usaría los valores por defecto. 

Al final del archivo, para que pueda ser ejecutado, se coloca el método del flow: 

```python
iris_classification():
```


#### Visualización de Workflow

En consola de comando inicio el servidor de prefect: 

`prefect server start`

Se tendría que ver de la siguiente manera, con la dirección del servidor:

![prefect Start](imagenes/prefect%20start.png)

y en el navegador:

![prefect Navegador](imagenes/prefect%20navegador.png)

Ahora en otra terminal ejecuto el archivo. En la terminal veremos:

![Terminal run iris](imagenes/terminal%20run_iris.png)

Identificados como "Task run" veremos las task corridas del workflow (los "tireless-seal" son los print indicados en la lógica)

En el navegador, en la pestaña de flow runs veremos los runs ejecutados

![navegador flow runs run_iris](imagenes/navegador%20flow%20runs%20run_iris.png)

y al hacer click en la corrida, tendremos los detalles de las corridas "iris-classification"

![detalle flow runs run_iris](imagenes/detalle%20flow%20runs%20run_iris.png)

y al hacer nuevamente click en una corrida en particular, tendremos los detalles de la misma

![mas detalle flow runs run_iris](imagenes/mas%20detalle%20flow%20run_iris.png)

Las task que se realizaron (con su orden) y cuanto tiempo ha llevado el flow en ejecutarse. También podremos consultar otros detalles de la corrida como los log o los artefactos generados(data procesada por ejemplo)

Los flow pueden integrase con programas externos, como los tipo Cron, lo que me permite controlar, por ejemplo, cada cuanto se despliega el flow, tener acceso a las salidas generadas por el flow, etc.