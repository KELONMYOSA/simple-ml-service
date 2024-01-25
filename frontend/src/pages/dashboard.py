import flet

from src.pages import deposit, login
from src.utils.auth import get_user_info, logout
from src.utils.balance import get_user_balance


async def main(page: flet.Page):
    user = await get_user_info(page)
    balance = await get_user_balance(page)
    if user:
        page.appbar.actions = [
            flet.Row(
                controls=[
                    flet.TextButton(
                        text=f"{balance} cu",
                        icon=flet.icons.ACCOUNT_BALANCE_WALLET,
                        on_click=to_deposit,
                    ),
                    flet.Text(
                        value=user["email"],
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


async def to_deposit(e: flet.ControlEvent):
    page = e.page
    await deposit.main(page)
