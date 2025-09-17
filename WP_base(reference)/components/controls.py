# components/controls.py — reusable Flet controls
import flet as ft
from theme import *
from utils.units import UNITS, AREA_UNITS

class SectionTitle(ft.Text):
    def __init__(self, text: str):
        super().__init__(text, size=20, weight=ft.FontWeight.BOLD, color=NAVY)

class Card(ft.Container):
    def __init__(self, content: ft.Control):
        super().__init__(
            content=content,
            bgcolor=CARD_BG,
            padding=PADDING,
            border_radius=RADIUS,
            border=ft.border.all(1, BORDER),
        )

class LabeledNumberInput(ft.Column):
    def __init__(self, label: str, value: float | None = None):
        self.field = ft.TextField(
            value=str(value) if value is not None else "",
            bgcolor=INPUT_BG, border_color=BORDER, dense=True, text_size=14,
            content_padding=ft.Padding(10,8,10,8), keyboard_type=ft.KeyboardType.NUMBER,
            width=150,
        )
        self.units = ft.Dropdown(
            options=[ft.dropdown.Option(u) for u in UNITS.keys()],
            value="meters", dense=True, width=120, border_color=BORDER, bgcolor=INPUT_BG,
        )
        super().__init__([
            ft.Text(label, weight=ft.FontWeight.BOLD, size=14),
            ft.Row([self.field, self.units], spacing=10, vertical_alignment=ft.CrossAxisAlignment.CENTER)
        ], spacing=6)

    def numeric_value(self) -> float:
        try:
            return float(self.field.value or 0)
        except Exception:
            return 0.0

class OutputArea(ft.Column):
    def __init__(self, label: str = "Result"):
        self.output = ft.Text("—", size=18, weight=ft.FontWeight.BOLD)
        self.unit_out = ft.Dropdown(
            options=[ft.dropdown.Option(u) for u in AREA_UNITS.keys()],
            value="m²", dense=True, width=100, border_color=BORDER, bgcolor=INPUT_BG,
        )
        super().__init__([
            ft.Text(label, weight=ft.FontWeight.BOLD, size=14),
            ft.Row([self.output, self.unit_out], spacing=10, vertical_alignment=ft.CrossAxisAlignment.CENTER)
        ], spacing=6)

    def set_value(self, value: float):
        self.output.value = f"{value:.6f}"

def calc_button(text: str, on_click):
    return ft.ElevatedButton(
        text, on_click=on_click,
        bgcolor=GREEN, color=ft.Colors.WHITE, style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=RADIUS),
            overlay_color=ft.Colors.with_opacity(0.08, ft.Colors.WHITE),
        ),
    )

def clear_button(on_click):
    return ft.ElevatedButton(
        "Clear", on_click=on_click, bgcolor=GRAY_BTN, color=TEXT,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=RADIUS))
    )
