import aiohttp
import flet

from src.config import settings
from src.pages import dashboard
from src.utils.auth import refresh_token
from src.utils.balance import do_withdraw


async def get_user_tasks(page: flet.Page) -> list[dict] | None:
    async with aiohttp.ClientSession() as session:
        token = await page.client_storage.get_async("access_token")
        if not token:
            return None

        url = settings.FASTAPI_URL + "/task"
        headers = {"Authorization": f"bearer {token}"}
        async with session.get(url, headers=headers) as resp:
            if resp.status == 200:
                resp_json = await resp.json()
                return resp_json

        await refresh_token(page)
        token = await page.client_storage.get_async("access_token")
        if not token:
            return None

        headers = {"Authorization": f"bearer {token}"}
        async with session.get(url, headers=headers) as resp:
            if resp.status == 200:
                resp_json = await resp.json()
                return resp_json

        return None


async def create_task(page: flet.Page, data: dict):
    async with aiohttp.ClientSession() as session:
        url = settings.FASTAPI_URL + "/task"
        token = await page.client_storage.get_async("access_token")
        headers = {"Authorization": f"bearer {token}"}
        async with session.post(url, json=data, headers=headers) as resp:
            if resp.status == 200:
                await do_withdraw(page, modelId2cost[data["model_id"]])
        await dashboard.main(page)


async def refresh_table(e: flet.ControlEvent):
    page = e.page
    await dashboard.main(page)


modelLabel2id = {
    "Linear Regression (5 cu)": 1,
    "Random Forest (15 cu)": 2,
    "Neural Network (30 cu)": 3,
}

modelId2cost = {
    1: 5,
    2: 15,
    3: 30,
}
