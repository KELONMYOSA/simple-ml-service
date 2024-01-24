import aiohttp
import flet

from src.config import settings
from src.pages import main


async def refresh_token(page: flet.Page):
    async with aiohttp.ClientSession() as session:
        refresh = await page.client_storage.get_async("refresh_token")
        if not refresh:
            return

        url = settings.FASTAPI_URL + "/auth/refresh"
        params = {"token": refresh}
        async with session.post(url, params=params) as resp:
            if resp.status == 200:
                data = await resp.json()
                await page.client_storage.set_async("access_token", data["access_token"])
                await page.client_storage.set_async("refresh_token", data["refresh_token"])


async def get_user_info(page: flet.Page) -> dict | None:
    async with aiohttp.ClientSession() as session:
        token = await page.client_storage.get_async("access_token")
        if not token:
            return None

        url = settings.FASTAPI_URL + "/auth/info"
        headers = {"Authorization": f"bearer {token}"}
        async with session.get(url, headers=headers) as resp:
            if resp.status == 200:
                return await resp.json()

        await refresh_token(page)

        async with session.get(url, headers=headers) as resp:
            if resp.status == 200:
                return await resp.json()

        return None


async def login(page: flet.Page, username: str, password: str) -> dict:
    async with aiohttp.ClientSession() as session:
        url = settings.FASTAPI_URL + "/auth/token"
        body = {"username": username, "password": password}
        async with session.post(url, data=body) as resp:
            data = await resp.json()
            if resp.status == 200:
                await page.client_storage.set_async("access_token", data["access_token"])
                await page.client_storage.set_async("refresh_token", data["refresh_token"])
                return {"result": True}
            else:
                return {"result": False, "message": data["detail"]}


async def logout(e: flet.ControlEvent):
    page = e.page
    await page.client_storage.remove_async("access_token")
    await page.client_storage.remove_async("refresh_token")
    await page.update_async()
    await main.main(page)


async def register(username: str, password: str) -> dict:
    async with aiohttp.ClientSession() as session:
        url = settings.FASTAPI_URL + "/auth/register"
        body = {"email": username, "password": password}
        async with session.post(url, params=body) as resp:
            data = await resp.json()
            if resp.status == 200:
                return {"result": True}
            else:
                return {"result": False, "message": data["detail"]}
