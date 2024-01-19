import flet


async def main(page: flet.Page):
    page.title = "KELONMYOSA"
    page.horizontal_alignment = flet.CrossAxisAlignment.CENTER
    page.scroll = flet.ScrollMode.AUTO

    main_page_controls = [
        flet.Container(
            content=flet.Text(
                value="KELONMYOSA", style=flet.TextThemeStyle.HEADLINE_MEDIUM, color=flet.colors.BLUE_600
            ),
            alignment=flet.alignment.center,
            height=80,
        ),
    ]
    view = flet.Column(width=page.width * 0.6, controls=main_page_controls)

    await page.add_async(view)
