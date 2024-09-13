"""This config module contains the configuration for the pipeline with prefect"""

# dirección de la data sin procesar y donde voy a guardar la data procesada
PATH_DATA_RAW = "data\data_sin_procesar"
DATA_PATH_PROCESSED = "data\data_procesada_2"
# nombre del archivo de la data sin procesar
FILE_NAME_DATA_INPUT = "tickets_classification_eng"

# version of the data
VERSION = 2
# language for the input parameter for the text processing class
LANGUAGE = "english"

# parameters for the logistic regression model based on the model training with mlflow
PARAMETERS_MODEL = {
    "C": 1.0,
    "class_weight": None,
    "dual": False, 
    "fit_intercept": True,
    "intercept_scaling": 1,
    "l1_ratio": None,
    "max_iter": 100,
    "multi_class": "auto",
    "n_jobs": None,
    "penalty": "l2",
    "random_state": 40,
    "solver": "liblinear",
    "tol": 0.0001,
    "verbose": 0,
    "warm_start": False
}

idx2label = {"0": "Bank Account Services", "1": "Credit Report or Prepaid Card", "2": "Mortgage/Loan"}
label2idx = {v: k for k, v in idx2label.items()} #hace el camino inverso a lo de arriba
# tags for mlflow tracking
DEVELOPER_NAME = "Maria"
MODEL_NAME = "LogisticRegression"