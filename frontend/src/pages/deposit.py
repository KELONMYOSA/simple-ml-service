import flet

from src.pages import dashboard
from src.utils.balance import make_deposit


async def main(page: flet.Page):
    text_value = flet.TextField(
        label="Enter the amount",
        text_align=flet.TextAlign.CENTER,
        width=300,
        input_filter=flet.NumbersOnlyInputFilter(),
    )
    text_warning = flet.Text(text_align=flet.TextAlign.CENTER, color=flet.colors.RED_500, width=300)
    button_submit = flet.ElevatedButton("Deposit", disabled=True, width=300)
    button_cancel = flet.IconButton(flet.icons.ARROW_BACK)

    async def validate(e: flet.ControlEvent) -> None:
        if text_value.value:
            if float(text_value.value) > 0:
                button_submit.disabled = False
            else:
                text_value.value = None
        else:
            button_submit.disabled = True
        await page.update_async()

    async def submit(e: flet.ControlEvent) -> None:
        deposit_resp = await make_deposit(page, float(text_value.value))
        if deposit_resp["result"]:
            await dashboard.main(page)
            page.snack_bar = flet.SnackBar(
                flet.Text(
                    "Successful Replenishment",
                    text_align=flet.TextAlign.CENTER,
                    color=flet.colors.GREEN_500,
                    style=flet.TextThemeStyle.HEADLINE_SMALL,
                )
            )
            page.snack_bar.bgcolor = flet.colors.SURFACE_VARIANT
            page.snack_bar.open = True
            await page.update_async()
        else:
            text_warning.value = deposit_resp["message"]
            text_value.value = None
            await page.update_async()

    async def cancel(e: flet.ControlEvent) -> None:
        await dashboard.main(page)

    text_value.on_change = validate
    button_submit.on_click = submit
    button_cancel.on_click = cancel

    await page.clean_async()
    await page.add_async(
        flet.Column(
            controls=[
                flet.Column(height=200),
                flet.Row(controls=[button_cancel], width=300),
                flet.Column(controls=[text_value, button_submit, text_warning], height=300),
            ]
        )
    )
