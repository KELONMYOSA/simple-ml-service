import aiohttp
import flet

from src.config import settings
from src.utils.auth import refresh_token


async def get_user_balance(page: flet.Page) -> float | None:
    async with aiohttp.ClientSession() as session:
        token = await page.client_storage.get_async("access_token")
        if not token:
            return None

        url = settings.FASTAPI_URL + "/balance"
        headers = {"Authorization": f"bearer {token}"}
        async with session.get(url, headers=headers) as resp:
            if resp.status == 200:
                resp_json = await resp.json()
                return resp_json["balance"]

        await refresh_token(page)
        token = await page.client_storage.get_async("access_token")
        if not token:
            return None

        headers = {"Authorization": f"bearer {token}"}
        async with session.get(url, headers=headers) as resp:
            if resp.status == 200:
                resp_json = await resp.json()
                return resp_json["balance"]

        return None


async def make_deposit(page: flet.Page, amount: float) -> dict:
    async with aiohttp.ClientSession() as session:
        url = settings.FASTAPI_URL + "/balance/deposit"
        token = await page.client_storage.get_async("access_token")
        headers = {"Authorization": f"bearer {token}"}
        body = {"amount": amount}
        async with session.post(url, params=body, headers=headers) as resp:
            data = await resp.json()
            if resp.status == 200:
                return {"result": True}
            else:
                return {"result": False, "message": data["detail"]}


async def do_withdraw(page: flet.Page, amount: float) -> dict:
    async with aiohttp.ClientSession() as session:
        url = settings.FASTAPI_URL + "/balance/withdraw"
        token = await page.client_storage.get_async("access_token")
        headers = {"Authorization": f"bearer {token}"}
        body = {"amount": amount}
        async with session.post(url, params=body, headers=headers) as resp:
            data = await resp.json()
            if resp.status == 200:
                return {"result": True}
            else:
                return {"result": False, "message": data["detail"]}
