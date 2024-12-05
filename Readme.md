Que se busca:

Clasificar los ticket de solicitudes que llegan a un banco, utilizando técnicas de NLP (procesamiento de lenguaje natural)

El dataset se obtuvo de: https://www.kaggle.com/datasets/abhishek14398/automatic-ticket-classification-dataset/data


Que se realizo:

En la rama main -> teoría y practica:

1. Introducción al tracking: las 3 formas de trackear con MLflow → [Notebook](Introduccion_tracking/introduccion_al_tracking.ipynb)

2. Utils: funciones para el procesamiento del texto → [Descripción](utils/readme.md)

3. Tracking: ejemplo de trackeo usando MLflow →
[Notebook](tracking/tracking_data_tickets_baseline.ipynb)

4. Orquestación / Introducción: Introducción a los flow, task y uso de prefect → [Descripción](orquestacion/introduction/readme.md)

5. Orquestación : Ejemplo de generación y aplicación de un flow con prefect → [Descripción](orquestacion/readme.md)

En la rama deploy-serving: se desarrolla la lógica para desplegar la aplicación que utilizara el modelo utilizando Docker y FastAPI.

No se desarrolla la implementacion en AWS debido a que hubo inconvenientes con la cuenta y que el curso hace una explicacion muy vaga de la misma 

