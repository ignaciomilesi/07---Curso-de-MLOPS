import joblib
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel
from app.db import engine, create_db_and_tables, PredictionsTickets
from app.utils import preprocessing_fn
from sqlmodel import Session, select
from enum import Enum


global label_mapping

label_mapping = {
    "0": "Bank Account Services",
    "1": "Credit Report or Prepaid Card",
    "2": "Mortgage/Loan"}

# define data structure for each input 
class Sentence(BaseModel):
    client_name: str
    text: str 

# define data structure for request 
class ProcessTextRequestModel(BaseModel):
    sentences: list[Sentence]

app = FastAPI(title="FastAPI, Docker, and Traefik")

#entrypoint
@app.post("/predict")
async def read_root(data: ProcessTextRequestModel):

    # Inicial sesión en la base de datos
    session = Session(engine)
    
    # Carga el modelo
    model = joblib.load("model.pkl")

    preds_list = []

    for sentence in data.sentences: 

        # Procesa el texto pasado Tokenización, Lematización, etc
        processed_data_vectorized = preprocessing_fn(sentence.text)
        X_dense = [sparse_matrix.toarray() for sparse_matrix in processed_data_vectorized]
        X_dense = np.vstack(X_dense) 

        # Realizo la predicción y la decodifico ()
        preds = model.predict(X_dense)
        decoded_predictions = label_mapping[str(preds[0])]

        # Creo el objeto predicción (definido en db)
        prediction_ticket = PredictionsTickets(
            client_name=sentence.client_name,
            prediction=decoded_predictions
        )
        
        print(prediction_ticket)

        # agrego la perdición a la lista
        preds_list.append({
            "client_name": sentence.client_name,
            "prediction": decoded_predictions
        })
        
        # Agrego el objeto predicción a la base de datos
        session.add(prediction_ticket)

    # Busca confirma las operaciones, asi me evito cerrar la base de datos aun estando en procesamiento
    session.commit() 
    session.close() # cierro la base de datos

    # Contesto las predicciones
    return {"predictions": preds_list}


# Asegura crea la base de datos cuando al API este creada
@app.on_event("startup")
async def startup():
    create_db_and_tables()
