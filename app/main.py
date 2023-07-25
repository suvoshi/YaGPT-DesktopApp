import pystray
from PIL import Image
from app.app import app_setup

image = Image.open("yagpticon.png")


def exit():
    icon.stop()


menu = pystray.Menu(
    pystray.MenuItem(text="Open", action=app_setup, default=True),
    pystray.MenuItem(text="Exit", action=exit),
)

icon = pystray.Icon("YaGPT", image, menu=menu)

icon.run()
