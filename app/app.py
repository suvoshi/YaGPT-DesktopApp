import flet as ft
from app.yagpt import Chat

PALETTE = {
    "light": "#9ECAFF",
    "normal": "#001C3D",
    "dark": "#001229",
    "normal-light": "#235FA9",
}


def main(page):
    # page settings
    page.padding = 0
    page.spacing = 0
    page.bgcolor = PALETTE["normal"]

    page.window_title_bar_hidden = True
    page.window_title_bar_buttons_hidden = True

    page.window_width = 400
    page.window_height = 650
    page.window_top = 70
    page.window_left = 1050
    page.window_resizable = False

    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def minimize():
        page.window_minimized = True
        page.update()

    def send_click(e):
        message = send_textfield.value
        if message != "":
            send_textfield.value = ""

            send_panel.disabled = True
            page.update()

            # send - front
            message_container = ft.Container(
                content=ft.Text(
                    message, size=15, font_family="RobotoSlab", selectable=True
                ),
                bgcolor=PALETTE["normal-light"],
                border_radius=10,
                padding=10,
            )

            chat_listview.controls.append(message_container)

            page.update()

            # send - back
            yagptchat.send_message(message)
            ans = yagptchat.get_answer()

            # get answer - front
            message_container = ft.Container(
                content=ft.Text(
                    ans, size=15, font_family="RobotoSlab", selectable=True
                ),
                bgcolor=PALETTE["normal"],
                border_radius=10,
                padding=10,
            )

            chat_listview.controls.append(message_container)
            send_panel.disabled = False
            page.update()

    def close():
        page.window_close()
        yagptchat.close()

    # window tools
    tools = ft.Container(
        content=ft.Row(
            [
                ft.WindowDragArea(
                    ft.Container(bgcolor=PALETTE["normal"], padding=20),
                    expand=True,
                    maximizable=False,
                ),
                ft.IconButton(
                    ft.icons.MINIMIZE_ROUNDED,
                    on_click=lambda _: minimize(),
                    icon_color=ft.colors.WHITE,
                ),
                ft.IconButton(
                    ft.icons.CLOSE,
                    on_click=lambda _: close(),
                    icon_color=ft.colors.WHITE,
                ),
            ],
            spacing=0,
        ),
        bgcolor=PALETTE["normal"],
    )

    # primary controls
    chat_text = ft.Text("YandexGPT", size=20, font_family="RobotoSlab")
    chat_icon = ft.Icon(name=ft.icons.ACCOUNT_CIRCLE, size=30)

    chat_listview = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)

    send_textfield = ft.TextField(label="Send message", height=60, width=300)
    send_iconbutton = ft.IconButton(
        icon=ft.icons.ARROW_CIRCLE_RIGHT,
        icon_color=PALETTE["light"],
        icon_size=59,
        on_click=send_click,
    )

    # chat panel
    chat_text_container = ft.Container(
        content=chat_text,
        bgcolor=PALETTE["dark"],
        alignment=ft.alignment.center,
        border=ft.border.symmetric(vertical=ft.border.BorderSide(1, PALETTE["light"])),
    )

    chat_icon_container = ft.Container(
        content=chat_icon, alignment=ft.alignment.center_left, margin=10
    )

    chat_panel = ft.Stack(
        [chat_text_container, chat_icon_container], width=400, height=60
    )

    # chat area
    chat_area = ft.Container(content=chat_listview, bgcolor=PALETTE["dark"], height=460)

    # send panel
    send_textfield_container = ft.Container(
        content=send_textfield, margin=ft.margin.only(top=14, left=10, bottom=10)
    )

    send_panel = ft.Row([send_textfield_container, send_iconbutton], spacing=0)

    # adding
    page.add(tools, chat_panel, chat_area, send_panel)

    # setup yagptchat
    send_panel.disabled = True
    page.update()

    yagpt_setup()

    send_panel.disabled = False
    page.update()


def yagpt_setup():
    global yagptchat
    yagptchat = Chat()


def app_setup():
    ft.app(target=main)
