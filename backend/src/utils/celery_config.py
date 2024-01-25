import json

from celery import Celery

from src.config import settings

celery_app = Celery("tasks", broker=settings.RMQ_URL, backend=settings.REDIS_URL)


def get_task_result(task_id: str) -> dict:
    task = celery_app.AsyncResult(task_id)

    if task.state == "SUCCESS":
        response = {"status": task.state, "result": task.get()}
    elif task.state == "FAILURE":
        response = json.loads(task.backend.get(task.backend.get_key_for_task(task.id)).decode("utf-8"))
        response["status"] = "FAILURE"
        del response["children"]
        del response["traceback"]
    else:
        response = {"status": task.state, "result": task.info}

    return response
