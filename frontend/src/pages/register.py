import flet

from src.pages import login
from src.utils.auth import register


async def main(page: flet.Page):
    text_username = flet.TextField(label="Email", text_align=flet.TextAlign.LEFT, width=300)
    text_password = flet.TextField(label="Password", text_align=flet.TextAlign.LEFT, password=True, width=300)
    text_password_2 = flet.TextField(
        label="Re-enter password", text_align=flet.TextAlign.LEFT, password=True, width=300
    )
    text_warning = flet.Text(text_align=flet.TextAlign.CENTER, color=flet.colors.RED_500, width=300)
    button_submit = flet.ElevatedButton("Submit", disabled=True, width=300)

    sign_in_button = flet.ElevatedButton(
        text="Sign in",
        expand=True,
        style=flet.ButtonStyle(
            shape=flet.RoundedRectangleBorder(
                radius=flet.BorderRadius(top_left=10, bottom_left=10, top_right=0, bottom_right=0)
            )
        ),
    )

    sign_up_button = flet.ElevatedButton(
        text="Sign up",
        disabled=True,
        expand=True,
        style=flet.ButtonStyle(
            shape=flet.RoundedRectangleBorder(
                radius=flet.BorderRadius(top_left=0, bottom_left=0, top_right=10, bottom_right=10)
            )
        ),
    )

    async def validate(e: flet.ControlEvent) -> None:
        if all([text_username.value, text_password.value, text_password_2.value]):
            button_submit.disabled = False
        else:
            button_submit.disabled = True
        await page.update_async()

    async def submit(e: flet.ControlEvent) -> None:
        if text_password.value != text_password_2.value:
            text_warning.value = "Passwords do not match"
            text_password.value = None
            text_password_2.value = None
            await page.update_async()
            return

        register_resp = await register(text_username.value, text_password.value)
        if register_resp["result"]:
            await login.main(page)
            page.snack_bar = flet.SnackBar(
                flet.Text(
                    "Successfully Registered",
                    text_align=flet.TextAlign.CENTER,
                    color=flet.colors.GREEN_500,
                    style=flet.TextThemeStyle.HEADLINE_SMALL,
                )
            )
            page.snack_bar.bgcolor = flet.colors.SURFACE_VARIANT
            page.snack_bar.open = True
            await page.update_async()
        else:
            text_warning.value = register_resp["message"]
            text_username.value = None
            text_password.value = None
            text_password_2.value = None
            await page.update_async()

    async def to_login(e: flet.ControlEvent) -> None:
        await login.main(page)

    text_username.on_change = validate
    text_password.on_change = validate
    text_password_2.on_change = validate
    button_submit.on_click = submit
    sign_in_button.on_click = to_login

    await page.clean_async()
    await page.add_async(
        flet.Column(
            controls=[
                flet.Column(height=200),
                flet.Row(controls=[sign_in_button, sign_up_button], spacing=0, width=300),
                flet.Column(
                    controls=[text_username, text_password, text_password_2, button_submit, text_warning], height=300
                ),
            ]
        )
    )
