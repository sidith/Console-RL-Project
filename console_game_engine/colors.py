from typing import Tuple
from dataclasses import dataclass

metalic_colors = {
    "gold": (255, 215, 0),
    "silver": (192, 192, 192),
    "copper": (184, 115, 51),
    "bronze": (205, 127, 50),
    "brass": (181, 166, 66),
    "chrome": (255, 255, 255),
    "nickel": (114, 116, 114),
    "aluminum": (169, 172, 182),
    "cobalt": (61, 89, 171),
    "titanium": (135, 134, 130),
    "tungsten": (78, 84, 129),
    "zinc": (183, 183, 182),
    "platinum": (229, 228, 226),
    "mercury": (158, 161, 176),
    "lead": (77, 81, 86),
    "uranium": (138, 155, 15),
}

fruit_colors = {
    "apple": (255, 0, 0),
    "apricot": (251, 206, 177),
    "avocado": (86, 130, 3),
    "banana": (255, 255, 0),
    "blackberry": (139, 0, 0),
    "blueberry": (0, 0, 255),
    "boysenberry": (135, 50, 74),
    "cherry": (222, 49, 99),
    "clementine": (255, 147, 41),
    "cranberry": (0, 0, 139),
    "date": (139, 69, 19),
    "fig": (255, 0, 255),
    "grape": (111, 45, 168),
    "grapefruit": (255, 69, 0),
    "guava": (112, 128, 144),
    "kiwi": (143, 143, 188),
    "lemon": (255, 255, 0),
    "lime": (0, 255, 0),
    "loganberry": (74, 0, 130),
    "lychee": (255, 255, 240),
    "mandarin": (255, 247, 0),
    "mango": (255, 140, 0),
    "nectarine": (255, 218, 185),
    "olive": (128, 128, 0),
    "orange": (255, 165, 0),
    "papaya": (255, 239, 213),
    "peach": (255, 229, 180),
    "pear": (209, 226, 49),
    "persimmon": (255, 107, 83),
    "plantain": (255, 255, 0),
    "plum": (221, 160, 221),
    "pomegranate": (93, 57, 84),
    "pomelo": (255, 119, 255),
    "raisin": (112, 28, 28),
    "strawberry": (255, 20, 147),
}

basic_colors = {
    "black": (0, 0, 0),
    "gray": (135, 135, 135),
    "blue": (135, 135, 175),
    "green": (135, 175, 135),
    "cyan": (135, 175, 175),
    "red": (175, 135, 135),
    "purple": (175, 135, 175),
    "yellow": (175, 175, 135),
    "white": (175, 175, 175),
}

exotic_colors = {
    "amber": (255, 191, 0),
    "beige": (245, 245, 220),
    "bistre": (61, 43, 31),
    "blond": (250, 240, 190),
    "chartreuse": (127, 255, 0),
    "chocolate": (210, 105, 30),
    "coffee": (111, 78, 55),
    "crimson": (220, 20, 60),
    "fuchsia": (255, 0, 255),
    "indigo": (75, 0, 130),
    "ivory": (255, 255, 240),
    "khaki": (240, 230, 140),
    "lavender": (230, 230, 250),
    "magenta": (255, 0, 255),
    "maroon": (176, 48, 96),
    "ochre": (204, 119, 34),
    "olive": (128, 128, 0),
    "orange": (255, 165, 0),
    "pink": (255, 192, 203),
    "raspberry": (135, 38, 87),
    "rose": (255, 0, 127),
    "salmon": (250, 128, 114),
    "scarlet": (255, 36, 0),
    "tan": (210, 180, 140),
    "taupe": (72, 60, 50),
    "tangerine": (255, 204, 0),
    "teal": (0, 128, 128),
    "turquoise": (64, 224, 208),
    "violet": (238, 130, 238),
    "wine": (114, 47, 55),
    "neon blue": (0, 0, 255),
}

colors = {
    **metalic_colors,
    **fruit_colors,
    **basic_colors,
    **exotic_colors,
}


@dataclass
class RGB_Color(Tuple[int, int, int]):
    r: int = 0
    g: int = 0
    b: int = 0


@dataclass
class HSV_Color(Tuple[int, int, int]):
    h: int = 0
    s: int = 0
    v: int = 0


@dataclass
class CMYK_Color(Tuple[int, int, int, int]):
    c: int = 0
    m: int = 0
    y: int = 0
    k: int = 0
