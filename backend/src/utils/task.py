from fastapi import HTTPException, status

from src.contracts import InputData, TaskCreate, TaskInfo
from src.database.db import get_db
from src.database.models.celery import CeleryTask
from src.database.models.model import Model
from src.database.models.task import UserTask
from src.database.models.user import User
from src.utils.balance import get_user_balance, make_deposit
from src.utils.celery_config import celery_app, get_task_result


def get_model_by_id(model_id: int) -> Model:
    with get_db() as db:
        model = db.query(Model).filter(Model.id == model_id).first()
    if model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Model not found")

    return model


def get_all_models() -> list[Model]:
    with get_db() as db:
        return db.query(Model).all()


def _send_task_to_celery(model_id: int, input_data: InputData) -> str:
    if model_id == 1:
        task = celery_app.send_task("predict.lr", kwargs={"input_data": input_data.model_dump()})
    elif model_id == 2:
        task = celery_app.send_task("predict.rf", kwargs={"input_data": input_data.model_dump()})
    elif model_id == 3:
        task = celery_app.send_task("predict.nn", kwargs={"input_data": input_data.model_dump()})

    task_id = task.id

    return task_id


def _create_celery_task(model_id: int, input_data: InputData) -> int:
    celery_task = _send_task_to_celery(model_id, input_data)
    with get_db() as db:
        task = CeleryTask(
            celery_task=celery_task, model_id=model_id, input_data=input_data.model_dump(), task_result="In Progress"
        )
        db.add(task)
        db.commit()
        db.refresh(task)
        return task.id


def _set_user_to_task(user_id: int, celery_task_id: int):
    with get_db() as db:
        task = UserTask(user_id=user_id, task_id=celery_task_id)
        db.add(task)
        db.commit()


def _get_task_info_by_id(task_id: int) -> TaskInfo:
    with get_db() as db:
        task = db.query(CeleryTask).filter(CeleryTask.id == task_id).first()
        model = task.model

        task_info = TaskInfo(
            id=task.id,
            model_name=model.name,
            cost=model.cost,
            input_data=task.input_data,
            prediction=task.prediction,
            task_result=task.task_result,
        )

        return task_info


def create_new_task(task_data: TaskCreate, current_user: User) -> TaskInfo:
    model = get_model_by_id(task_data.model_id)
    balance = get_user_balance(current_user)

    if balance < model.cost:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient funds")

    celery_task_id = _create_celery_task(model.id, task_data.input_data)
    _set_user_to_task(current_user.id, celery_task_id)

    return _get_task_info_by_id(celery_task_id)


def _update_in_progress_tasks(current_user: User):
    with get_db() as db:
        in_progress_tasks = (
            db.query(CeleryTask)
            .join(UserTask)
            .filter(CeleryTask.task_result == "In Progress", UserTask.user_id == current_user.id)
            .all()
        )

        for task in in_progress_tasks:
            task_status = get_task_result(task.celery_task)
            if task_status["status"] == "SUCCESS":
                task.prediction = bool(task_status["result"]["score"])
                task.task_result = "Done"
            elif task_status["status"] == "FAILURE":
                task.task_result = "Error"
                make_deposit(current_user, task.model.cost)
        db.commit()


def get_user_tasks(current_user: User) -> list[TaskInfo]:
    _update_in_progress_tasks(current_user)
    with get_db() as db:
        user_tasks = db.query(UserTask).filter(UserTask.user_id == current_user.id).all()
        results = []

        for user_task in user_tasks:
            task = user_task.tasks
            model = task.model
            task_info = TaskInfo(
                id=task.id,
                model_name=model.name,
                cost=model.cost,
                input_data=task.input_data,
                prediction=task.prediction,
                task_result=task.task_result,
            )
            results.append(task_info)

        return results
