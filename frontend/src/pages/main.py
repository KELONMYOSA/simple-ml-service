import flet

from src.pages import dashboard


async def main(page: flet.Page):
    page.title = "KELONMYOSA"
    page.horizontal_alignment = flet.CrossAxisAlignment.CENTER
    page.scroll = flet.ScrollMode.AUTO

    page.appbar = flet.AppBar(
        leading=flet.Icon(flet.icons.COMPUTER),
        leading_width=30,
        title=flet.Text("ML DEV - KELONMYOSA"),
        center_title=False,
        bgcolor=flet.colors.SURFACE_VARIANT,
    )

    await dashboard.main(page)
