import flet

from src.pages import login
from src.utils.auth import get_user_info, logout


async def main(page: flet.Page):
    user = await get_user_info(page)
    if user:
        page.appbar.actions = [
            flet.Row(
                controls=[
                    flet.Text(
                        value=user["email"],
                        color=flet.colors.BLUE_600,
                        style=flet.TextThemeStyle.BODY_LARGE,
                    ),
                    flet.IconButton(icon=flet.icons.LOGOUT, tooltip="Logout", on_click=logout),
                ],
                spacing=10,
            ),
        ]
    else:
        await login.main(page)
        return

    await page.clean_async()
    await page.add_async(
        flet.Column(
            controls=[
                flet.Container(
                    content=flet.Text(
                        value="KELONMYOSA", style=flet.TextThemeStyle.HEADLINE_SMALL, color=flet.colors.BLUE_600
                    ),
                    alignment=flet.alignment.center,
                    height=80,
                ),
            ],
            width=page.width * 0.6,
        )
    )
