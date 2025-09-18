import flet as ft
from theme import *
from pages.radio_page import build_radio_page

def main(page: ft.Page):
    page.title = "Planificador de Red Movil — 1G / 2G Calculator"
    page.bgcolor = BG
    page.padding = 0
    page.theme_mode = ft.ThemeMode.LIGHT

    selected = {"tech": "2G"}

    def render():
        def nav_button(label):
            is_active = (label == selected["tech"])
            return ft.TextButton(
                label,
                style=ft.ButtonStyle(
                    color=ft.Colors.BLACK87 if is_active else ft.Colors.WHITE,
                    bgcolor=ft.Colors.AMBER_200 if is_active else None,
                ),
                on_click=lambda e, l=label: switch(l),
            )

        navbar = ft.Container(
            content=ft.Row([
                ft.Text("Calculator.net", color="white", size=22, weight=ft.FontWeight.BOLD),
                ft.Row([nav_button("1G"), nav_button("2G")], spacing=12)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            bgcolor=NAVY, padding=ft.padding.symmetric(20, 10)
        )

        body = ft.Container(
            content=ft.Column([
                ft.Text("Name", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK87),
                ft.Text(f"Parámetros de entrada y resultados — {selected['tech']}", size=14, color=MUTED),
                build_radio_page(page, selected["tech"]),
            ], spacing=12, scroll=ft.ScrollMode.AUTO, expand=True),
            padding=ft.padding.symmetric(20, 20),
            expand=True,
        )

        page.controls.clear(); page.add(navbar, body); page.update()

    def switch(tech):
        selected["tech"] = tech
        render()

    render()

if __name__ == "__main__":
    ft.app(target=main, view=ft.WEB_BROWSER, port=5000)
