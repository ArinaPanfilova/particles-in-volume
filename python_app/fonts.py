# -*- coding: utf-8 -*-
"""Шрифты интерфейса. Все виджеты и рисунки берут шрифты отсюда, поэтому размер всего текста
задаётся одним числом SCALE и меняется на лету (Вид → крупнее / мельче, Ctrl + / Ctrl −)."""
import tkinter.font as tkfont

FAMILY, MONO = 'Segoe UI', 'Consolas'
DEFAULT = 1.3   # масштаб при запуске: крупнее обычного, чтобы читалось с проектора
SCALE = DEFAULT
_cache = {}


def font(size, *style, family=FAMILY):
    """Именованный шрифт Tk размером size · SCALE пунктов; style — 'bold', 'italic'.
    При смене масштаба все виджеты с этим шрифтом обновляются сами."""
    key = (family, size) + style
    if key not in _cache:
        _cache[key] = tkfont.Font(family=family, size=round(size * SCALE),
                                  weight='bold' if 'bold' in style else 'normal',
                                  slant='italic' if 'italic' in style else 'roman')
    return _cache[key]


def mono(size, *style):
    return font(size, *style, family=MONO)


def set_scale(k):
    global SCALE
    SCALE = k
    for (family, size, *style), f in _cache.items():
        f.configure(size=round(size * SCALE))
