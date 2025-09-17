import flet as ft
import math

def main(page: ft.Page):
    page.title = "Circle Area Calculator"
    r = ft.TextField(label="Radius (r)", value="0")
    out = ft.Text("Result: —")

    def calc(e):
        try:
            val = float(r.value)
            out.value = f"Result: {math.pi * val * val:.6f}"
        except:
            out.value = "Enter a valid number"
        page.update()

    page.add(
        ft.Column([
            ft.Text("Circle Area", size=24, weight="bold"),
            r,
            ft.ElevatedButton("Calculate", on_click=calc),
            out
        ])
    )

# Run in browser on custom port 5000
ft.app(target=main, view=ft.WEB_BROWSER, port=9000)
