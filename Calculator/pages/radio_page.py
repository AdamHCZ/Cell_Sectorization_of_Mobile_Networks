import flet as ft
from theme import *
from components.controls import SectionTitle, Card, NumberInput, SelectInput, ErrorBanner, calc_button, clear_button
from utils.DATA import CELLS, ABC
import math

def require_float(field: NumberInput, banner: ErrorBanner, label: str):
    v = field.as_float(); ok = v is not None and v > 0; field.asterisk.visible = not ok
    if not ok: banner.show(f"{label}: valor inválido"); return None
    return v

def require_int(field: NumberInput, banner: ErrorBanner, label: str):
    v = field.as_int(); ok = v is not None and v > 0; field.asterisk.visible = not ok
    if not ok: banner.show(f"{label}: entero positivo requerido"); return None
    return v

def require_from_list(field: NumberInput, allowed: list[int], banner: ErrorBanner, label: str) -> int | None:
    v = field.as_int()
    ok = (v is not None) and (v in allowed)
    field.asterisk.visible = not ok
    if not ok:
        banner.show(f"{label}: debe ser un numero rómbico válido")
        return None
    return v

def require_btn_range(field: NumberInput, range: list[int], banner: ErrorBanner, label: str) -> int | None:
    v = field.as_float()
    ok = (v is not None) and (v >= range[0]) and (v <= range[1])
    field.asterisk.visible = not ok
    if not ok:
        banner.show(f"{label}: debe ser un número dentro del rango {range[0]} - {range[1]}")
        return None
    return v

def build_inputs_card(state, banner: ErrorBanner, tech: str) -> Card: # For Square of inputs
    state.r_cov = NumberInput("Radio de cobertura (km)")
    state.k_cells = NumberInput("Número de celdas por cluster (k)")
    if tech == "1G":
        state.band = SelectInput("Ancho de banda (MHz)", ["5","10"], value="10")
    else: # 2G
        state.band = SelectInput("Ancho de banda (MHz)", ["10","15","25"], value="10")
    state.n_exp = NumberInput("Valor de n (para la pérdida)")
    state.sectors = SelectInput("Sectores por celda", ["1","3"], value="3")
    state.n_clusters = NumberInput("Número de clusters")
    return Card(ft.Column([
        SectionTitle("PARAMETROS DE ENTRADA"),
        ft.Row([state.r_cov, state.k_cells], spacing=16),
        ft.Row([state.band, state.n_exp], spacing=16),
        ft.Row([state.sectors, state.n_clusters], spacing=16),
    ], spacing=12))

def build_results_card(state, tech: str) -> Card: # For Square of results
    state.res_subcarriers = ft.TextField(read_only=True, value="", bgcolor=INPUT_BG, border_color=BORDER)
    state.res_reuse_distance = ft.TextField(read_only=True, value="", suffix_text="km", bgcolor=INPUT_BG, border_color=BORDER)
    state.res_cluster_area = ft.TextField(read_only=True, value="", suffix_text="km²", bgcolor=INPUT_BG, border_color=BORDER)
    state.res_prot_ratio = ft.TextField(read_only=True, value="", suffix_text="dB", bgcolor=INPUT_BG, border_color=BORDER)
    state.res_freq_per_cluster = [ft.TextField(read_only=True, value="", bgcolor=INPUT_BG, border_color=BORDER),
                                  ft.TextField(read_only=True, value="", bgcolor=INPUT_BG, border_color=BORDER)]
    state.res_freq_per_cell = [ft.TextField(read_only=True, value="", bgcolor=INPUT_BG, border_color=BORDER),
                               ft.TextField(read_only=True, value="", bgcolor=INPUT_BG, border_color=BORDER)]
    state.res_freq_per_sector = [ft.TextField(read_only=True, value="", bgcolor=INPUT_BG, border_color=BORDER),
                                 ft.TextField(read_only=True, value="", bgcolor=INPUT_BG, border_color=BORDER)]
    state.res_freq_per_SA = [ft.TextField(read_only=True, value="", bgcolor=INPUT_BG, border_color=BORDER),
                                 ft.TextField(read_only=True, value="", bgcolor=INPUT_BG, border_color=BORDER)]
    state.res_channels = [ft.TextField(read_only=True, value="", bgcolor=INPUT_BG, border_color=BORDER), 
                          ft.TextField(read_only=True, value="", bgcolor=INPUT_BG, border_color=BORDER)]
    channels_row = ft.Row([ft.Text("Número de canales por sector:", weight=ft.FontWeight.NORMAL), 
                            ft.Column([ft.Text("Mínimo:"), state.res_channels[0]], spacing=10),
                            ft.Column([ft.Text("Máximo:"), state.res_channels[1]], spacing=10)], spacing=12) # Change FontWeight.NORMAL or BOLD
    channels_row.visible = (tech == "2G")
    state.channels_row = channels_row
    return Card(ft.Column([
        SectionTitle("RESULTADOS"),
        ft.Row([ft.Text("Número de subportadoras:"), state.res_subcarriers], spacing=12),
        ft.Row([ft.Text("Distancia de reutilización:"), state.res_reuse_distance], spacing=12),
        ft.Row([ft.Text("Área del cluster:"), state.res_cluster_area], spacing=12),
        ft.Row([ft.Text("Relación de protección rp:"), state.res_prot_ratio], spacing=12),
        ft.Row([
            ft.Text(
                "Número de frecuencias por sector:"
            ),
            ft.Column([ft.Text("Mínimo:"), state.res_freq_per_sector[0]], spacing=10),
            ft.Column([ft.Text("Máximo:"), state.res_freq_per_sector[1]], spacing=10)
        ], spacing=12),
        channels_row,
        ft.Row([
            ft.Text(
                "Número de canales por celda:" if tech == "2G" else "Número de subportadoras por celda:"
            ),
            ft.Column([ft.Text("Mínimo:"), state.res_freq_per_cell[0]], spacing=10),
            ft.Column([ft.Text("Máximo:"), state.res_freq_per_cell[1]], spacing=10)
        ], spacing=12),
        ft.Row([
            ft.Text(
                "Número de canales por cluster:" if tech == "2G" else "Número de subportadoras por cluster:"
            ),
            ft.Column([ft.Text("Mínimo:"), state.res_freq_per_cluster[0]], spacing=10),
            ft.Column([ft.Text("Máximo:"), state.res_freq_per_cluster[1]], spacing=10)
        ], spacing=12),
        ft.Row([
            ft.Text(
                "Número de canales por Area de Servicio Movil:" if tech == "2G" else "Número de subportadoras por Area de Servicio Movil:"
            ),
            ft.Column([ft.Text("Mínimo:"), state.res_freq_per_SA[0]], spacing=10),
            ft.Column([ft.Text("Máximo:"), state.res_freq_per_SA[1]], spacing=10)
        ], spacing=12)], spacing=10,))


def build_empty_freq_table_placeholder() -> ft.Control: # Placeholder table when no data
    columns = [ft.DataColumn(ft.Text(f"{i+1}(A)")) for i in range(4)]
    rows = []
    for _ in range(4):
        cells = [ft.DataCell(ft.Text("-")) for _ in range(4)]
        rows.append(ft.DataRow(cells=cells))

    table = ft.DataTable(
        columns=columns,
        rows=rows,
        heading_row_color=ft.Colors.with_opacity(0.05, ft.Colors.BLACK),
        data_row_min_height=40,
        border=ft.border.all(1, BORDER),
        divider_thickness=0.5,
    )
    return Card(ft.Column([SectionTitle("RESUMEN DE FRECUENCIAS"), table], spacing=12))


def build_frequency_grid_card(total: int, k: int, sectors: int, title: str) -> ft.Control:

    if total is None or total <= 0 or k <= 0 or sectors <= 0:
        total = 0

    if k is None or sectors is None:
        k, sectors = 0, 0

    num_cols = int(k) * int(sectors) if (k and sectors) else 0  

    headers: list[ft.DataColumn]
    if num_cols > 0:
        headers = []
        for s in range(sectors):
            for j in range(1, k + 1):
                sector_label = ABC[s] if s < len(ABC) else f"A{s+1}"
                headers.append(ft.DataColumn(ft.Text(f"{j} ({sector_label})")))
    else:
        headers = [ft.DataColumn(ft.Text("—"))]  # fallback 1-col header

    rows: list[ft.DataRow] = []

    # Build content vector: 1..total as strings
    if num_cols <= 0:
            # No valid columns: show a single 1x1 cell with "-"
            rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text("-"))]))
    else:
        # Valid columns
        total = int(total) if (total is not None and total > 0) else 0

        if total == 0:
            # Show exactly one row filled with "-" to match num_cols
            cells = [ft.DataCell(ft.Text("-")) for _ in range(num_cols)]
            rows.append(ft.DataRow(cells=cells))
        else:
            # Fill 1..total, pad to rectangle
            data = [str(i) for i in range(1, total + 1)]
            num_rows = math.ceil(total / num_cols)

            pad = num_rows * num_cols - len(data)
            if pad > 0:
                data.extend(["-"] * pad)

            for r in range(num_rows):
                start = r * num_cols
                end = start + num_cols
                row_slice = data[start:end]  # length == num_cols
                cells = [ft.DataCell(ft.Text(val)) for val in row_slice]
                rows.append(ft.DataRow(cells=cells))

    # Creating the table
    table = ft.DataTable(
        columns=headers if num_cols > 0 else [ft.DataColumn(ft.Text("—"))],
        rows=rows,
        heading_row_color=ft.Colors.with_opacity(0.05, ft.Colors.BLACK),
        data_row_min_height=40,
        border=ft.border.all(1, BORDER),
        divider_thickness=0.5,
    )
    h_scroller = ft.Row([table], scroll=ft.ScrollMode.AUTO, expand=True)

    return Card(ft.Column([SectionTitle(title), h_scroller], spacing=12))

def compute(state, banner: ErrorBanner, tech: str, e=None): # Operaciones para los resultados
    banner.clear()
    r_km = require_float(state.r_cov, banner, "Radio de cobertura")
    k = require_from_list(state.k_cells, CELLS, banner, "Celdas por cluster")
    n = require_btn_range(state.n_exp,[2.7, 5] , banner, "Valor de n") # Range between 2.7 and 5
    ncl = require_int(state.n_clusters, banner, "Número de clusters")
    if any(v is None for v in [r_km,k,n,ncl]): e and e.page.update(); return
    try: D = float(r_km) * ((3*float(k)) ** 0.5); state.res_reuse_distance.value = f"{D:.3f}" # Reuse Distance
    except: state.res_reuse_distance.value = "—"
    try: # Cluster Area
        from math import sqrt
        A = (3*sqrt(3)/2) * (float(r_km)**2) * float(k); state.res_cluster_area.value = f"{A:.3f}"
    except: state.res_cluster_area.value = "—"
    try: # Protection Ratio
        import math
        rp = 10*math.log10((((D/r_km) - 1)**n)/6); state.res_prot_ratio.value = f"{rp:.2f}"
        if rp < 8 or rp > 12: banner.show("Red no viable")
    except: state.res_prot_ratio.value = "—"

    bw_mhz = int(state.band.dropdown.value); sectors = int(state.sectors.dropdown.value) # Bandwidth and sectors
    if tech == "2G":
        state.res_subcarriers.value = f"{(float(bw_mhz) / 0.2) - 1:.0f}" # Subcarriers for 2G
        state.res_freq_per_sector[0].value = str(max(float(state.res_subcarriers.value) // (sectors * k), 1))
        state.res_freq_per_sector[1].value = str(float(state.res_freq_per_sector[0].value) + 1)
        state.res_channels[0].value = str(float(state.res_freq_per_sector[0].value) * 8)
        state.res_channels[1].value = str(float(state.res_freq_per_sector[1].value) * 8); state.channels_row.visible = True
        state.res_freq_per_cell[0].value = str(float(state.res_channels[0].value) * sectors)
        state.res_freq_per_cell[1].value = str(float(state.res_channels[1].value) * sectors)

    else:
        state.res_subcarriers.value = f"{float(bw_mhz) / 0.03:.0f}" # Subcarriers for 1G
        state.res_freq_per_sector[0].value = str(max(float(state.res_subcarriers.value) // (sectors * k), 1))
        state.res_freq_per_sector[1].value = str(float(state.res_freq_per_sector[0].value))
        state.res_channels[0].value = ""; state.res_channels[1].value = ""; state.channels_row.visible = False

        state.res_freq_per_cell[0].value = str(float(state.res_freq_per_sector[0].value) * sectors)
        state.res_freq_per_cell[1].value = str(float(state.res_freq_per_sector[1].value) * sectors)

    try:
        state.res_freq_per_cluster[0].value = str(float(state.res_freq_per_cell[0].value) * k)
        state.res_freq_per_cluster[1].value = str(float(state.res_freq_per_cell[1].value) * k)
        state.res_freq_per_SA[0].value = str(float(state.res_freq_per_cluster[0].value) * ncl)
        state.res_freq_per_SA[1].value = str(float(state.res_freq_per_cluster[1].value) * ncl)
    except:
        state.res_freq_per_cluster[0].value = "—"
        state.res_freq_per_cluster[1].value = "—"
        state.res_freq_per_SA[0].value = "—"
        state.res_freq_per_SA[1].value = "—"

    try:
        k = int(state.k_cells.field.value) if hasattr(state.k_cells, "field") else int(state.k_cells.dropdown.value)
    except Exception:
        # If you used SelectInput for k, use dropdown; if NumberInput, use field.
        # Fallback to parsing from your validated value 'k' if you already have it as int.
        pass

    try:
        sectors = int(state.sectors.dropdown.value)
    except Exception:
        sectors = 1

    def safe_int(s, default=0):
        try:
            return int(float(s))
        except Exception:
            return default

    total_min = safe_int(state.res_freq_per_cluster[0].value, 0)
    total_max = safe_int(state.res_freq_per_cluster[1].value, 0)

    # Rebuild the table and replace host content
    if tech == "2G":
        state.table_host_min.content = build_frequency_grid_card(
            total=total_min // 8,  # Convert channels to frequencies
            k=int(state.k_cells.dropdown.value) if hasattr(state.k_cells, "dropdown") else k,
            sectors=sectors,
            title="RESUMEN DE FRECUENCIAS (Mínimo)",
        )

        state.table_host_max.content = build_frequency_grid_card(
            total=total_max // 8,
            k=int(state.k_cells.dropdown.value) if hasattr(state.k_cells, "dropdown") else k,
            sectors=sectors,
            title="RESUMEN DE FRECUENCIAS (Máximo)",
        )
    else:  # 1G
        state.table_host.content = build_frequency_grid_card(
            total=total_min,
            k=int(state.k_cells.dropdown.value) if hasattr(state.k_cells, "dropdown") else k,
            sectors=sectors,
            title="RESUMEN DE FRECUENCIAS",
        )

    e and e.page.update()

def build_radio_page(page: ft.Page, tech: str):
    class State: pass
    state = State()
    banner = ErrorBanner()
    inputs = build_inputs_card(state, banner, tech)
    results = build_results_card(state, tech)
    if tech == "1G":
        state.table_host = ft.Container(content=build_empty_freq_table_placeholder())
        table_section = state.table_host
    else:
        state.table_host_min = ft.Container(content=build_empty_freq_table_placeholder())
        state.table_host_max = ft.Container(content=build_empty_freq_table_placeholder())
        table_section = ft.Row([state.table_host_min, state.table_host_max], spacing=16, scroll=ft.ScrollMode.AUTO, expand=True)

    def on_clear(e):
        for fld in [state.r_cov.field, state.k_cells.field, state.n_exp.field, state.n_clusters.field]: fld.value = ""
        for a in [state.r_cov.asterisk, state.k_cells.asterisk, state.n_exp.asterisk, state.n_clusters.asterisk]: a.visible = False
        for out in [state.res_subcarriers, state.res_reuse_distance, state.res_cluster_area, state.res_prot_ratio, state.res_freq_per_sector, 
                    state.res_channels, state.res_freq_per_cell, state.res_freq_per_cluster, state.res_freq_per_SA]: out.value = ""
        if tech == "1G":
            state.table_host.content = build_empty_freq_table_placeholder()
        else:
            state.table_host_min.content = build_empty_freq_table_placeholder()
            state.table_host_max.content = build_empty_freq_table_placeholder()
        banner.clear(); page.update()
    buttons = ft.Row([calc_button("Calcular", lambda e: compute(state, banner, tech, e)),
                      clear_button(on_clear)], spacing=10)
    form_section = ft.Column(
        [banner, inputs, buttons, results],
        spacing=16,
        expand=True,
    )
    return form_section, table_section, state
