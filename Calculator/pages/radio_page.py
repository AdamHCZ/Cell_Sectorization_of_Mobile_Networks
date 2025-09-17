import flet as ft
from theme import *
from components.controls import SectionTitle, Card, NumberInput, SelectInput, ErrorBanner, calc_button, clear_button

def require_float(field: NumberInput, banner: ErrorBanner, label: str):
    v = field.as_float(); ok = v is not None; field.asterisk.visible = not ok
    if not ok: banner.show(f"{label}: valor inválido"); return None
    return v

def require_int(field: NumberInput, banner: ErrorBanner, label: str):
    v = field.as_int(); ok = v is not None; field.asterisk.visible = not ok
    if not ok: banner.show(f"{label}: entero requerido"); return None
    return v

def build_inputs_card(state, banner: ErrorBanner) -> Card:
    state.r_cov = NumberInput("Radio de cobertura (km)")
    state.k_cells = NumberInput("Número de celdas por cluster (k)")
    state.band = SelectInput("Ancho de banda (MHz)", ["5","10","15","25"], value="10")
    state.n_exp = NumberInput("Valor de n (para la pérdida)")
    state.sectors = SelectInput("Sectores por celda", ["1","3"], value="3")
    state.n_clusters = NumberInput("Número de clusters")
    return Card(ft.Column([
        SectionTitle("PARAMETROS DE ENTRADA"),
        ft.Row([state.r_cov, state.k_cells], spacing=16),
        ft.Row([state.band, state.n_exp], spacing=16),
        ft.Row([state.sectors, state.n_clusters], spacing=16),
    ], spacing=12))

def build_results_card(state, tech: str) -> Card:
    state.res_subcarriers = ft.TextField(read_only=True, value="", bgcolor=INPUT_BG, border_color=BORDER)
    state.res_reuse_distance = ft.TextField(read_only=True, value="", suffix_text="km", bgcolor=INPUT_BG, border_color=BORDER)
    state.res_cluster_area = ft.TextField(read_only=True, value="", suffix_text="km²", bgcolor=INPUT_BG, border_color=BORDER)
    state.res_prot_ratio = ft.TextField(read_only=True, value="", suffix_text="dB", bgcolor=INPUT_BG, border_color=BORDER)
    state.res_freq_per_sector = ft.TextField(read_only=True, value="", bgcolor=INPUT_BG, border_color=BORDER)
    state.res_channels = ft.TextField(read_only=True, value="", bgcolor=INPUT_BG, border_color=BORDER)
    channels_row = ft.Row([ft.Text("Número de canales (solo 2G)", weight=ft.FontWeight.BOLD), state.res_channels])
    channels_row.visible = (tech == "2G")
    state.channels_row = channels_row
    return Card(ft.Column([
        SectionTitle("RESULTADOS"),
        ft.Row([ft.Text("Número de subportadoras:"), state.res_subcarriers], spacing=12),
        ft.Row([ft.Text("Distancia de reutilización:"), state.res_reuse_distance], spacing=12),
        ft.Row([ft.Text("Área del cluster:"), state.res_cluster_area], spacing=12),
        ft.Row([ft.Text("Relación de protección rp:"), state.res_prot_ratio], spacing=12),
        ft.Row([ft.Text("Número de frecuencias por sector:"), state.res_freq_per_sector], spacing=12),
        channels_row,
    ], spacing=10))

def compute(state, banner: ErrorBanner, tech: str, e=None):
    banner.clear()
    r_km = require_float(state.r_cov, banner, "Radio de cobertura")
    k = require_int(state.k_cells, banner, "Celdas por cluster")
    n = require_float(state.n_exp, banner, "Valor de n")
    ncl = require_int(state.n_clusters, banner, "Número de clusters")
    if any(v is None for v in [r_km,k,n,ncl]): e and e.page.update(); return
    try: D = 2 * float(r_km) * (3*float(k)) ** 0.5; state.res_reuse_distance.value = f"{D:.3f}"
    except: state.res_reuse_distance.value = "—"
    try:
        from math import sqrt
        A = (3*sqrt(3)/2) * (float(r_km)**2) * float(k); state.res_cluster_area.value = f"{A:.3f}"
    except: state.res_cluster_area.value = "—"
    try:
        import math
        rp = 10*math.log10(max(float(k),1)) + (float(n)-2)*5; state.res_prot_ratio.value = f"{rp:.2f}"
        if rp < 0: banner.show("Red no viable")
    except: state.res_prot_ratio.value = "—"
    bw_mhz = int(state.band.dropdown.value); sectors = int(state.sectors.dropdown.value)
    state.res_subcarriers.value = str(bw_mhz * 10)
    state.res_freq_per_sector.value = str(max(bw_mhz // sectors, 1))
    if tech == "2G":
        state.res_channels.value = str(bw_mhz * 2); state.channels_row.visible = True
    else:
        state.res_channels.value = ""; state.channels_row.visible = False
    e and e.page.update()

def build_radio_page(page: ft.Page, tech: str):
    class State: pass
    state = State()
    banner = ErrorBanner()
    inputs = build_inputs_card(state, banner)
    results = build_results_card(state, tech)
    def on_clear(e):
        for fld in [state.r_cov.field, state.k_cells.field, state.n_exp.field, state.n_clusters.field]: fld.value = ""
        for a in [state.r_cov.asterisk, state.k_cells.asterisk, state.n_exp.asterisk, state.n_clusters.asterisk]: a.visible = False
        for out in [state.res_subcarriers, state.res_reuse_distance, state.res_cluster_area, state.res_prot_ratio, state.res_freq_per_sector, state.res_channels]: out.value = ""
        banner.clear(); page.update()
    buttons = ft.Row([calc_button("Calcular", lambda e: compute(state, banner, tech, e)),
                      clear_button(on_clear)], spacing=10)
    return ft.Column([banner, inputs, buttons, results], spacing=16)
