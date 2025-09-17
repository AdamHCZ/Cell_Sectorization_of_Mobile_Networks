# utils/units.py — simple metric/imperial conversions
UNITS = {
    "meters": 1.0,
    "centimeters": 0.01,
    "millimeters": 0.001,
    "feet": 0.3048,
    "inches": 0.0254,
    "yards": 0.9144,
}

def to_meters(value: float, unit: str) -> float:
    return float(value) * UNITS[unit]

def from_meters(value_m: float, unit: str) -> float:
    return float(value_m) / UNITS[unit]

AREA_UNITS = {
    "m²": 1.0,
    "cm²": 0.0001,
    "mm²": 0.000001,
    "ft²": 0.09290304,
    "in²": 0.00064516,
    "yd²": 0.83612736,
}

def area_from_m2(value_m2: float, unit: str) -> float:
    return float(value_m2) / AREA_UNITS[unit]
