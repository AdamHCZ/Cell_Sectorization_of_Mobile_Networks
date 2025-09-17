# pages/area_page.py — the main calculators page (rectangle, triangle, trapezoid)
import math
import flet as ft
from theme import *
from utils.units import to_meters, area_from_m2
from components.controls import SectionTitle, Card, LabeledNumberInput, OutputArea, calc_button, clear_button

def rectangle_card():
    l = LabeledNumberInput("Length (l)", 30)
    w = LabeledNumberInput("Width (w)", 20)
    out = OutputArea("Area")

    def do_calc(e=None):
        lm = to_meters(l.numeric_value(), l.units.value)
        wm = to_meters(w.numeric_value(), w.units.value)
        area_m2 = lm * wm
        out.set_value(area_from_m2(area_m2, out.unit_out.value))
        e and e.page.update()

    def do_clear(e=None):
        l.field.value = ""; w.field.value = ""; out.set_value(float("nan"))
        e and e.page.update()

    return Card(ft.Column([
        SectionTitle("Rectangle"),
        ft.Row([l, w, ft.Container(width=40)], alignment=ft.MainAxisAlignment.START, spacing=16),
        ft.Row([calc_button("Calculate", do_calc), clear_button(do_clear)], spacing=8),
        out
    ], spacing=12))

def triangle_card():
    a = LabeledNumberInput("Edge 1 (a)", 30)
    b = LabeledNumberInput("Edge 2 (b)", 45)
    c = LabeledNumberInput("Edge 3 (c)", 50)
    out = OutputArea("Area")

    def do_calc(e=None):
        am, bm, cm = to_meters(a.numeric_value(), a.units.value), to_meters(b.numeric_value(), b.units.value), to_meters(c.numeric_value(), c.units.value)
        # Triangle inequality
        if am + bm <= cm or am + cm <= bm or bm + cm <= am:
            out.output.value = "Invalid sides"
        else:
            s = (am + bm + cm) / 2.0
            area_m2 = math.sqrt(s*(s-am)*(s-bm)*(s-cm))
            out.set_value(area_from_m2(area_m2, out.unit_out.value))
        e and e.page.update()

    def do_clear(e=None):
        for x in (a,b,c): x.field.value = ""
        out.set_value(float("nan"))
        e and e.page.update()

    return Card(ft.Column([
        SectionTitle("Triangle"),
        ft.Row([a, b, c], spacing=16),
        ft.Row([calc_button("Calculate", do_calc), clear_button(do_clear)], spacing=8),
        out
    ], spacing=12))

def trapezoid_card():
    b1 = LabeledNumberInput("Base 1 (b₁)", 30)
    b2 = LabeledNumberInput("Base 2 (b₂)", 45)
    h = LabeledNumberInput("Height (h)", 20)
    out = OutputArea("Area")

    def do_calc(e=None):
        b1m = to_meters(b1.numeric_value(), b1.units.value)
        b2m = to_meters(b2.numeric_value(), b2.units.value)
        hm  = to_meters(h.numeric_value(),  h.units.value)
        area_m2 = (b1m + b2m) * 0.5 * hm
        out.set_value(area_from_m2(area_m2, out.unit_out.value))
        e and e.page.update()

    def do_clear(e=None):
        for x in (b1,b2,h): x.field.value = ""
        out.set_value(float("nan"))
        e and e.page.update()

    return Card(ft.Column([
        SectionTitle("Trapezoid"),
        ft.Row([b1, b2, h], spacing=16),
        ft.Row([calc_button("Calculate", do_calc), clear_button(do_clear)], spacing=8),
        out
    ], spacing=12))

def build_area_page(page: ft.Page) -> ft.Control:
    # Left main calculators; right sidebar like calculator.net
    left = ft.Column([rectangle_card(), triangle_card(), trapezoid_card()], spacing=20, expand=True)

    sidebar = Card(ft.Column([
        ft.Text("Math Calculators", weight=ft.FontWeight.BOLD, size=16, color=ft.Colors.WHITE),
        ft.Divider(),
        ft.TextButton("Scientific"), ft.TextButton("Percentage"), ft.TextButton("Volume"),
        ft.TextButton("Random Number Generator"), ft.TextButton("Fraction"),
        ft.TextButton("Triangle"), ft.TextButton("Standard Deviation"),
        ft.TextButton("More Math Calculators"),
    ], spacing=6))
    sidebar.bgcolor = NAVY
    sidebar.border = None

    content = ft.ResponsiveRow([
        ft.Container(left, col={"xs":12, "md":8}),
        ft.Container(sidebar, col={"xs":12, "md":4})
    ], columns=12, run_spacing=20)

    return content
