import os

import joblib
import numpy as np

from celery import Celery

from torch_model import nn_predict, load_nn_model

RMQ_URL = os.getenv("RMQ_URL")
REDIS_URL = os.getenv("REDIS_URL")

celery_app = Celery("tasks", broker=RMQ_URL, backend=REDIS_URL)

model_lr = joblib.load("models/LR.pkl")
model_rf = joblib.load("models/RF.pkl")
model_nn = load_nn_model()


@celery_app.task(name="predict.lr")
def predict_lr(input_data: dict) -> dict:
    data = np.array(
        [
            input_data["temperature"],
            input_data["humidity"],
            input_data["CO2CosIRValue"],
            input_data["CO2MG811Value"],
            input_data["MOX1"],
            input_data["MOX2"],
            input_data["MOX3"],
            input_data["MOX4"],
            input_data["COValue"],
        ]
    )

    result = model_lr.predict(data.reshape(1, -1)).tolist()

    return {"score": result[0]}


@celery_app.task(name="predict.rf")
def predict_rf(input_data: dict) -> dict:
    data = np.array(
        [
            input_data["temperature"],
            input_data["humidity"],
            input_data["CO2CosIRValue"],
            input_data["CO2MG811Value"],
            input_data["MOX1"],
            input_data["MOX2"],
            input_data["MOX3"],
            input_data["MOX4"],
            input_data["COValue"],
        ]
    )

    result = model_rf.predict(data.reshape(1, -1)).tolist()

    return {"score": result[0]}


@celery_app.task(name="predict.nn")
def predict_nn(input_data: dict) -> dict:
    data = np.array(
        [
            input_data["temperature"],
            input_data["humidity"],
            input_data["CO2CosIRValue"],
            input_data["CO2MG811Value"],
            input_data["MOX1"],
            input_data["MOX2"],
            input_data["MOX3"],
            input_data["MOX4"],
            input_data["COValue"],
        ]
    )
    data = data.reshape(1, -1)

    return nn_predict(model_nn, data)
