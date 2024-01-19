import flet

from src.pages.main import main

flet.app(target=main, port=80, assets_dir="src/assets", view=flet.AppView.WEB_BROWSER)
