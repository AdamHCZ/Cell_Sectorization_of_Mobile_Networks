import flet as ft
from theme import *


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

class ErrorBanner(ft.Container):
    def __init__(self):
        self.text = ft.Text("", color=ft.Colors.WHITE, size=14)
        super().__init__(
            content=ft.Row([ft.Icon(ft.Icons.ERROR_OUTLINE, color=ft.Colors.WHITE), self.text], spacing=8),
            visible=False, bgcolor=ERROR, padding=ft.padding.all(10), border_radius=RADIUS,
        )
    def show(self, msg: str): self.text.value = msg; self.visible = True
    def clear(self): self.text.value = ""; self.visible = False

class Asterisk(ft.Text): # Asterisk for required fields defined
    def __init__(self, visible: bool=False):
        super().__init__("*", color=ERROR, size=18, visible=visible, weight=ft.FontWeight.BOLD)

class LabeledField(ft.Column): # Text for inputs with asterisk or not and the inputs section
    def __init__(self, label: str, control: ft.Control):
        self.asterisk = Asterisk(False)
        title_row = ft.Row([ft.Text(label, weight=ft.FontWeight.BOLD, size=14), self.asterisk], spacing=6)
        super().__init__([title_row, control], spacing=6)

class NumberInput(LabeledField): # Number Input for numeric inputs
    def __init__(self, label: str, placeholder: str = "", width: int = 180, value: str | None=None):
        self.field = ft.TextField(value=value or "", hint_text=placeholder, width=width,
                                  bgcolor=INPUT_BG, border_color=BORDER, dense=True, text_size=14,
                                  content_padding=ft.Padding(10,8,10,8), keyboard_type=ft.KeyboardType.NUMBER) # Search about padding
        super().__init__(label, self.field)
    def as_float(self):
        try: return float(self.field.value)
        except: return None
    def as_int(self):
        try: return int(float(self.field.value))
        except: return None

class SelectInput(LabeledField): # Selecting Input for dropdowns
    def __init__(self, label: str, options: list[str], value: str | None=None, width: int = 180):
        self.dropdown = ft.Dropdown(options=[ft.dropdown.Option(o) for o in options],
                                    value=value or (options[0] if options else None),
                                    width=width, dense=True, border_color=BORDER, bgcolor=INPUT_BG)
        super().__init__(label, self.dropdown)

def calc_button(text: str, on_click):
    return ft.ElevatedButton(text, on_click=on_click, bgcolor=GREEN, color=ft.Colors.WHITE,
                             style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=RADIUS),
                                                  overlay_color=ft.Colors.with_opacity(0.08, ft.Colors.WHITE)))
def clear_button(on_click):
    return ft.ElevatedButton("Clear", on_click=on_click, bgcolor=GRAY_BTN, color=TEXT,
                             style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=RADIUS)))
