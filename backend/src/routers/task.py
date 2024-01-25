from fastapi import APIRouter, Depends

from src.contracts import ModelResponse, TaskCreate, TaskInfo
from src.database.models.user import User
from src.utils.auth import get_current_user
from src.utils.task import create_new_task, get_all_models, get_user_tasks

router = APIRouter(
    prefix="/task",
    tags=["Celery tasks"],
)


# Информация о моделях для предсказания
@router.get("/models", response_model=list[ModelResponse])
def get_models_info():
    return get_all_models()


# Метод для создания задачи
@router.post("/", response_model=TaskInfo)
def create_task(task_data: TaskCreate, current_user: User = Depends(get_current_user)):
    return create_new_task(task_data, current_user)


# Получить все мои задачи
@router.get("/", response_model=list[TaskInfo])
def get_tasks(current_user: User = Depends(get_current_user)):
    return get_user_tasks(current_user)
