# main.py — app entry: navbar + page switch + theming
import flet as ft
from theme import *
from pages.area_page import build_area_page

def main(page: ft.Page):
    page.title = "Area Calculator — Local"
    page.bgcolor = BG
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0

    # Top nav bar (blue like calculator.net)
    navbar = ft.Container(
        content=ft.Row([
            ft.Text("CALCULADORA PARA PLANIFICACION DE RED MOVIL", color="white", size=22, weight=ft.FontWeight.BOLD),
            ft.Row([ft.TextButton("FINANCIAL"), ft.TextButton("FITNESS & HEALTH"), ft.TextButton("MATH", style=ft.ButtonStyle(color=ft.Colors.BLACK87, bgcolor=ft.Colors.AMBER_200)), ft.TextButton("OTHER")], spacing=16)
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        bgcolor=NAVY, padding=ft.padding.symmetric(20, 10)
    )

    body = ft.Container(
        content=ft.Column(
        [
            ft.Text("Area Calculator", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK87),
            ft.Text("Evaluate the area of common shapes. Modify the values and click Calculate.", size=14, color=MUTED),
            ft.Container(
                content=build_area_page(page),
                padding=ft.padding.symmetric(0, 10)
            ),
        ], 
        spacing=14, 
        scroll=ft.ScrollMode.AUTO,
        expand=True),
        padding=ft.padding.symmetric(20, 20),
        expand=True
    )

    page.add(navbar, body)

if __name__ == "__main__":
    # Run in browser on custom port
    ft.app(target=main, view=ft.WEB_BROWSER, port=5001)
