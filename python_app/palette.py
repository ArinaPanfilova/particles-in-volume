# -*- coding: utf-8 -*-
"""ВСЕ ЦВЕТА СОСУДА И ГРАФИКОВ: три схемы (обычная, контрастная, чёрно-белая).
Текущая схема — словарь C; её меняет set_palette(), и все рисунки сразу берут новые цвета.

КАРТА ФАЙЛА
===========
PALETTES      — схемы 'color' (обычная), 'contrast' (проектор), 'bw' (печать). Ключи в каждой:
                  vbg — фон сосуда;  wall — стенки;  region, regionEdge, regionText — выделенная область
                  mol, imp, impLight — молекулы, примесь;  tag, tagHalo — выделенная молекула
                  startIn, startOut, speed — раскраска «по начальному положению» и «по скорости»
                  axis, grid, text — оси, сетка, цифры;  bar, barEdge — столбики;  sig1–sig3 — столбики «по σ»
                  binom, pois, gauss — кривые;  band — коридор ⟨n⟩ ± σ;  line — линия n(t)
                  lw — толщина линий;  …Dash — пунктир кривых
SCHEMES       — порядок схем в меню «Вид»
C             — ТЕКУЩАЯ СХЕМА (при запуске — 'color')
set_palette() — переключить схему;  rgb() — цвет '#rrggbb' → (r, g, b);  speed_rgb() — цвет по скорости

ЧАСТЫЕ ПРАВКИ → ГДЕ
  поменять цвет → нужный ключ в PALETTES['color'] (формат '#rrggbb');   схема при запуске → строка C = …
"""

PALETTES = {
    # обычная: как на рисунке к задаче
    'color': dict(
        vbg='#fbfbf7', wall='#222222', region='#bfe3a5', regionEdge='#3f7a2a', regionText='#1f4a12',
        mol='#16325c', imp='#d2452b', impLight='#fbe0d8', tag='#e01b1b', tagHalo='#f7c2c2',
        startIn='#f07c10', startOut='#16325c', speed=['#2160c4', '#9a30b0', '#ef4f12'],
        axis='#4b5563', grid='#e2e5ea', text='#1f2937', bar='#6aaae8', barEdge='#1f63ad',
        sig1='#7cc97c', sig2='#f5bd5a', sig3='#f07a6e',
        binom='#e01b1b', pois='#0f9a8a', gauss='#f28a1c', band='#fbd6d6', line='#16325c',
        lw=1.3, binomDash=(), poisDash=(5, 4), gaussDash=(), meanDash=(6, 4)),
    # контрастная: насыщенные цвета и толстые линии, чтобы было видно на проекторе
    'contrast': dict(
        vbg='#ffffff', wall='#000000', region='#a8d98a', regionEdge='#2e6b16', regionText='#1b4a0c',
        mol='#0a1a33', imp='#b33000', impLight='#ffd2bf', tag='#e00000', tagHalo='#ffb3b3',
        startIn='#ff7b00', startOut='#0a1a33', speed=['#0047d6', '#9c00b8', '#ff3c00'],
        axis='#111111', grid='#cfd3da', text='#111111', bar='#4a90d9', barEdge='#123e73',
        sig1='#3fae49', sig2='#ffb000', sig3='#e8433a',
        binom='#d00000', pois='#008577', gauss='#ff8c00', band='#ffd0d0', line='#000000',
        lw=1.8, binomDash=(), poisDash=(6, 4), gaussDash=(), meanDash=(8, 4)),
    # чёрно-белая: для печати и цитирования; кривые различаются типом линии
    'bw': dict(
        vbg='#ffffff', wall='#000000', region='#e2e2e2', regionEdge='#000000', regionText='#000000',
        mol='#000000', imp='#000000', impLight='#bdbdbd', tag='#000000', tagHalo='#c4c4c4',
        startIn='#000000', startOut='#8c8c8c', speed=['#b0b0b0', '#5a5a5a', '#000000'],
        axis='#000000', grid='#e0e0e0', text='#000000', bar='#d0d0d0', barEdge='#000000',
        sig1='#7a7a7a', sig2='#bdbdbd', sig3='#efefef',
        binom='#000000', pois='#000000', gauss='#000000', band='#ececec', line='#000000',
        lw=1.3, binomDash=(), poisDash=(6, 4), gaussDash=(2, 3), meanDash=(6, 4)),
}
SCHEMES = ['color', 'contrast', 'bw']

C = dict(PALETTES['color'])


def set_palette(name):
    C.clear()
    C.update(PALETTES[name])


def rgb(c):
    return tuple(int(c[i:i + 2], 16) for i in (1, 3, 5))


def speed_rgb(t):
    """Цвет молекулы по скорости: t от 0 (медленная) до 1 (быстрая)."""
    stops = [rgb(c) for c in C['speed']]
    t = min(1.0, max(0.0, t)) * (len(stops) - 1)
    i = min(int(t), len(stops) - 2)
    f = t - i
    return tuple(round(a + (b - a) * f) for a, b in zip(stops[i], stops[i + 1]))
