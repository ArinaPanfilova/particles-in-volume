# -*- coding: utf-8 -*-
"""Цветовые схемы сосуда и графиков. Текущая схема — словарь C;
её меняет set_palette(), и все рисунки сразу берут новые цвета."""

PALETTES = {
    # обычная: как на рисунке к задаче
    'color': dict(
        vbg='#fbfbf7', wall='#2b2b2b', region='#cfe6bd', regionEdge='#50823c', regionText='#28501e',
        mol='#1d3557', imp='#c8553d', impLight='#fbe3dc', tag='#d62828', tagHalo='#f5c9c9',
        startIn='#e07a1f', startOut='#1d3557', speed=['#2c62b4', '#9a3fa8', '#e2541c'],
        axis='#6b7280', grid='#e5e7eb', text='#374151', bar='#8ab8e6', barEdge='#3f7fbf',
        sig1='#8cc98c', sig2='#f2c27a', sig3='#ee8a80',
        binom='#d62828', pois='#2a9d8f', gauss='#f4a261', band='#f6dede', line='#1d3557',
        lw=1.0, binomDash=(), poisDash=(5, 4), gaussDash=(), meanDash=(6, 4)),
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
