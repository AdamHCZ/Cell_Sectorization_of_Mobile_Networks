import flet as ft

def build_kv_row(label: str, value: str) -> ft.Row:
    return ft.Row(
        controls=[
            ft.Text(f"{label}:", weight=ft.FontWeight.BOLD),
            ft.Text(value),
        ],
        spacing=8,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

def build_paragraph(text: str) -> ft.Text:
    return ft.Text(
        text,
        size=14,
        selectable=True,
        color=ft.Colors.BLACK87
    )

def build_section_card(title: str, paragraph: str, defaults: list[tuple[str, str]]) -> ft.Card:
    return ft.Card(
        ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(title, size=20, weight=ft.FontWeight.BOLD),
                    build_paragraph(paragraph),
                    ft.Divider(),
                    ft.Text("Parámetros por defecto", size=16, weight=ft.FontWeight.W_600),
                    ft.Column([build_kv_row(k, v) for k, v in defaults], spacing=6),
                ],
                spacing=10,
                tight=True,
            ),
            padding=16
        ),
        elevation=2,
        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
    )

def build_tech_info(tech: str) -> ft.Column:
    # Contenidos
    p_1g = (
        "La primera generación de telefonía móvil (1G) se basó en la técnica de acceso múltiple "
        "por división de frecuencia (FDMA), donde cada usuario disponía de un canal exclusivo "
        "durante toda la llamada. Estos sistemas eran analógicos, con un ancho de banda típico "
        "de 5 a 10 MHz, y un espaciamiento de canales de 30 kHz. Su calidad de voz era limitada, "
        "con alta susceptibilidad a interferencias y sin ningún tipo de encriptación, lo que hacía "
        "las comunicaciones poco seguras. Además, la capacidad del sistema era reducida, ya que el "
        "espectro no se aprovechaba de manera eficiente."
    )
    d_1g = [
        ("Ancho de banda total", "5 – 10 MHz"),
        ("Ancho de canal", "30 kHz"),
        ("Acceso múltiple", "FDMA"),
        ("Tipo de señal", "Analógica"),
        ("Seguridad", "Sin encriptación"),
        ("Capacidad", "Limitada, baja eficiencia"),
    ]

    p_2g = (
        "La segunda generación (2G) representó un salto hacia la digitalización de la telefonía móvil. "
        "Combinó FDMA con TDMA, permitiendo que múltiples usuarios compartieran la misma portadora "
        "mediante división en ranuras de tiempo. Los sistemas 2G ofrecían mejor calidad de voz, capacidad "
        "aumentada y soporte para servicios de datos básicos como SMS. El ancho de banda empleado podía ser "
        "de 10, 15 o 25 MHz, con un espaciamiento de 200 kHz por canal, restando una subportadora de protección "
        "en cada bloque. Además, incorporó mecanismos de encriptación, lo que mejoró la seguridad frente a la "
        "primera generación."
    )
    d_2g = [
        ("Ancho de banda total", "10 – 25 MHz"),
        ("Ancho de canal", "200 kHz (–1 portadora de protección)"),
        ("Acceso múltiple", "FDMA + TDMA"),
        ("Tipo de señal", "Digital"),
        ("Seguridad", "Con encriptación"),
        ("Capacidad", "Mayor capacidad y eficiencia"),
    ]

    # Render según selección
    if tech == "1G":
        cards = [build_section_card("Primera Generación (1G)", p_1g, d_1g)]
    elif tech == "2G":
        cards = [build_section_card("Segunda Generación (2G)", p_2g, d_2g)]
    else:
        # Si algún día agregas más tecnologías, muestra ambas como fallback
        cards = [
            build_section_card("Primera Generación (1G)", p_1g, d_1g),
            build_section_card("Segunda Generación (2G)", p_2g, d_2g),
        ]

    return ft.Column(cards, spacing=12)