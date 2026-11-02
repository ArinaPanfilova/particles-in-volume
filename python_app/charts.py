# -*- coding: utf-8 -*-
"""Графики на tk.Canvas: гистограмма P(n) и временной ряд n(t).

КАРТА ФАЙЛА
===========
TICK                — размер цифр на осях (пт, умножается на общий масштаб шрифта fonts.SCALE)
ZOOMS, WIN          — число уровней масштаба n(t) и сколько последних отсчётов видно на масштабе 1:1
nice_step(), fmt()  — «круглый» шаг делений и запись чисел на осях
ticks(), margins(), nticks(), ny_ticks() — подписи делений, поля графика под цифры, сколько делений
                      помещается (чтобы цифры не слипались)
frame()             — оси, сетка, цифры и подписи осей (общая для обоих графиков)
hist()              — ГИСТОГРАММА P(n): диапазон n (4.5σ), столбики опыта (раскраска по σ),
                      кривые Гаусса, Пуассона и бинома; режим rotate — повёрнутая на 90°
series_range()      — какой кусок истории и какой диапазон n показывать на графике n(t)
series()            — ГРАФИК n(t): коридор ⟨n⟩ ± σ, линия среднего, ступенчатая линия n(t)

ЧАСТЫЕ ПРАВКИ → ГДЕ
  крупнее цифры на осях → TICK;   ширина столбиков → «* 0.8» в hist();   толщина линий и цвета → palette.py
  какой диапазон n у гистограммы → «4.5 * sig» в hist();   у n(t) → «3.5 * sig» в series_range()
"""
import math

import fonts
from palette import C
from sim import Dist

TICK = 11  # размер цифр и подписей на осях графиков, пт (умножается на общий масштаб fonts.SCALE)
# масштаб графика n(t): уровень 0 — крупно (⟨n⟩ ± 3.5σ, последние WIN отсчётов),
# каждый следующий вдвое шире по n и вдвое длиннее по времени, последний — вся шкала 0…N
ZOOMS = 4
WIN = 1500


def nice_step(rng, target):
    if rng <= 0:
        return 1
    raw = rng / target
    mag = 10 ** math.floor(math.log10(raw))
    f = raw / mag
    return (1 if f < 1.5 else 2 if f < 3 else 5 if f < 7 else 10) * mag


def fmt(v):
    if abs(v) >= 1000:
        return '%.0f' % v
    s = ('%.3f' % v).rstrip('0').rstrip('.')
    return '0' if s in ('-0', '') else s


def frange(start, stop, step):
    v = start
    while v <= stop + 1e-9:
        yield v
        v += step


def ticks(lo, hi, step):
    return [fmt(v) for v in frange(math.ceil(lo / step) * step, hi, step)]


def margins(w, h, ylabels):
    """Поля графика (L, T, R, B) под цифры осей — растут вместе с размером цифр."""
    f = fonts.font(TICK)
    u = f.metrics('linespace')
    return max([f.measure(t) for t in ylabels] + [u]) + 0.6 * u, 0.9 * u, w - 0.8 * u, h - 1.4 * u


def nticks(span, sample, most):
    """Сколько делений поместится на горизонтальной оси длиной span пикселей, чтобы цифры не слипались."""
    return max(2, min(most, int(span / (fonts.font(TICK).measure(sample) * 1.8))))


def ny_ticks(h):
    """Сколько делений по вертикали; зависит только от высоты графика, поэтому у повёрнутой
    гистограммы и у n(t) деления совпадают."""
    u = fonts.font(TICK).metrics('linespace')
    return max(2, min(5, int((h - 2.3 * u) / (1.8 * u))))


def frame(cv, L, T, R, B, xlo, xhi, ylo, yhi, xstep, ystep, xlabel, ylabel, integer_x):
    def X(x):
        return L + (x - xlo) / (xhi - xlo) * (R - L)

    def Y(y):
        return B - (y - ylo) / (yhi - ylo) * (B - T)
    for y in frange(math.ceil(ylo / ystep) * ystep, yhi, ystep):
        cv.create_line(L, Y(y), R, Y(y), fill=C['grid'])
        cv.create_text(L - 4, Y(y), text=fmt(y), anchor='e', fill=C['text'], font=fonts.font(TICK))
    for x in frange(math.ceil(xlo / xstep) * xstep, xhi, xstep):
        xv = round(x) if integer_x else x
        cv.create_text(X(xv), B + 4, text=fmt(xv), anchor='n', fill=C['text'], font=fonts.font(TICK))
    cv.create_line(L, T, L, B, R, B, fill=C['axis'])
    cv.create_text(R, B - 3, text=xlabel, anchor='se', fill=C['axis'], font=fonts.font(TICK))
    cv.create_text(L + 4, T, text=ylabel, anchor='nw', fill=C['axis'], font=fonts.font(TICK))
    return X, Y


def hist(cv, st):
    """st: N, p, closed, n0, hist, samples, pairs, show{binom,pois,gauss}, xLabel, yLabel, empty,
    sigma — раскрасить столбики по отклонению от ⟨n⟩: до σ, до 2σ, дальше;
    rotate — повернуть на 90°: n по вертикали в диапазоне nrange (тот же, что у графика n(t))"""
    cv.delete('all')
    w, h = cv.winfo_width(), cv.winfo_height()
    if w < 50 or h < 50:
        return
    N, p = st['N'], st['p']
    pairs = st.get('pairs', False)
    M = N // 2
    mu = N * p
    s2 = (2 if pairs else 1) * N * p * (1 - p)
    sig = math.sqrt(s2)
    if st['closed']:
        lo, hi = st['n0'] - 3, st['n0'] + 3
    else:
        lo, hi = math.floor(mu - 4.5 * sig - 1), math.ceil(mu + 4.5 * sig + 1)
    H = st['hist']
    nz = [n for n in range(len(H)) if H[n] > 0]
    if nz:
        lo, hi = min(lo, nz[0]), max(hi, nz[-1])
    lo, hi = max(0, lo), min(N, hi)
    while hi - lo < 6 and (lo > 0 or hi < N):
        if lo > 0:
            lo -= 1
        if hi < N:
            hi += 1

    tot = st['samples']

    def expP(n):
        return H[n] / tot if tot > 0 and n < len(H) else 0.0
    mirror = p > 0.5
    lam = N * (1 - p) if mirror else N * p

    def poisP(n):
        if pairs:
            if n % 2:
                return 0.0
            k = n // 2
            return Dist.poisson(M - k, M * (1 - p)) if mirror else Dist.poisson(k, M * p)
        return Dist.poisson(N - n, lam) if mirror else Dist.poisson(n, lam)

    def binP(n):
        if st['closed']:
            return 1.0 if n == st['n0'] else 0.0
        if pairs:
            return Dist.binom(n // 2, M, p) if n % 2 == 0 else 0.0
        return Dist.binom(n, N, p)

    ymax = 0.05
    for n in range(lo, hi + 1):
        ymax = max(ymax, expP(n))
        if st['show']['binom']:
            ymax = max(ymax, binP(n))
        if st['show']['pois'] and not st['closed']:
            ymax = max(ymax, poisP(n))
    ymax *= 1.1
    rot = st.get('rotate')
    if rot:
        # n — по вертикали, в тех же границах и с теми же делениями, что у графика n(t):
        # панели одной высоты, поэтому одинаковые n оказываются на одной высоте экрана
        lo, hi = st['nrange']
        nlo, nhi = lo, hi
        nstep = max(1, round(nice_step(hi - lo, ny_ticks(h))))
        L, T, R, B = margins(w, h, ticks(lo, hi, nstep))
        Xp, Yn = frame(cv, L, T, R, B, 0, ymax, nlo, nhi, nice_step(ymax, nticks(R - L, '0.00', 4)),
                       nstep, st['yLabel'], st['xLabel'], False)

        def pt(n, v):
            return Xp(v), Yn(n)
        bw = max(1, (Yn(0) - Yn(1)) * 0.8)
    else:
        nlo, nhi = lo - 0.6, hi + 0.6
        pstep = nice_step(ymax, ny_ticks(h))
        L, T, R, B = margins(w, h, ticks(0, ymax, pstep))
        Xn, Yp = frame(cv, L, T, R, B, nlo, nhi, 0, ymax,
                       max(1, round(nice_step(hi - lo, nticks(R - L, fmt(hi) + '0', 10)))),
                       pstep, st['xLabel'], st['yLabel'], True)

        def pt(n, v):
            return Xn(n), Yp(v)
        bw = max(1, (Xn(1) - Xn(0)) * 0.8)
    by_sigma = st.get('sigma') and not st['closed'] and sig > 0
    lw = C['lw']
    for n in range(lo, hi + 1):
        v = expP(n)
        if v <= 0:
            continue
        col = C['bar']
        if by_sigma:
            dev = abs(n - mu)
            col = C['sig1'] if dev <= sig else C['sig2'] if dev <= 2 * sig else C['sig3']
        (x0, y0), (x1, y1) = pt(n, 0), pt(n, v)
        edge = C['barEdge'] if bw > 3 else ''
        if rot:
            cv.create_rectangle(x0, y0 - bw / 2, x1, y0 + bw / 2, fill=col, outline=edge)
        else:
            cv.create_rectangle(x0 - bw / 2, y1, x0 + bw / 2, y0, fill=col, outline=edge)
    if st['show']['gauss'] and not st['closed'] and s2 > 0:
        pts = []
        K = 200
        scale = 2 if pairs else 1   # у пар вероятность сосредоточена на чётных n
        for i in range(K + 1):
            x = nlo + (nhi - nlo) * i / K
            pts += pt(x, min(scale * Dist.gauss(x, mu, s2), ymax))
        cv.create_line(*pts, fill=C['gauss'], width=2 * lw, smooth=True, dash=C['gaussDash'])
    ns = [n for n in range(lo, hi + 1) if not pairs or n % 2 == 0]
    if st['show']['pois'] and not st['closed'] and len(ns) > 1:
        pts = []
        for n in ns:
            pts += pt(n, poisP(n))
        cv.create_line(*pts, fill=C['pois'], width=1.5 * lw, dash=C['poisDash'])
        if bw > 4:
            q = 2.5 * lw
            for n in ns:
                x, y = pt(n, poisP(n))
                cv.create_rectangle(x - q, y - q, x + q, y + q, fill=C['pois'], outline='')
    if st['show']['binom']:
        pts = []
        for n in ns:
            pts += pt(n, binP(n))
        if len(pts) >= 4:
            cv.create_line(*pts, fill=C['binom'], width=1.5 * lw, dash=C['binomDash'])
        if bw > 3:
            q = 3 * lw
            for n in ns:
                x, y = pt(n, binP(n))
                cv.create_oval(x - q, y - q, x + q, y + q, fill=C['binom'], outline='')
    if tot == 0 and st.get('empty'):
        cv.create_text((L + R) / 2, (T + B) / 2, text=st['empty'], fill=C['axis'], font=fonts.font(10))


def series_range(st):
    """Окно истории и шкала n графика n(t): (отсчёты, n_min, n_max, ⟨n⟩, σ).
    Ту же шкалу берёт повёрнутая гистограмма."""
    z = st.get('zoom', 0)
    d, N, p = st['series'][-WIN * 2 ** z:], st['N'], st['p']
    mu = st['n0'] if st['closed'] else N * p
    sig = 0 if st['closed'] else math.sqrt((2 if st.get('pairs') else 1) * N * p * (1 - p))
    if z == ZOOMS - 1:
        ymin, ymax = 0, N
    else:
        half = (3.5 * sig + 1) * 2 ** z
        ymin, ymax = mu - half, mu + half
        for _, n in d:
            ymin, ymax = min(ymin, n), max(ymax, n)
    ymin = max(0, math.floor(ymin))
    ymax = min(max(N, 1), math.ceil(ymax))
    if ymax - ymin < 2:
        ymax = ymin + 2
    return d, ymin, ymax, mu, sig


def series(cv, st):
    """st: series [(t, n)], N, p, closed, n0, pairs, xLabel, yLabel, zoom (0 … ZOOMS − 1)"""
    cv.delete('all')
    w, h = cv.winfo_width(), cv.winfo_height()
    if w < 50 or h < 50:
        return
    d, ymin, ymax, mu, sig = series_range(st)
    t0 = d[0][0] if d else 0
    t1 = d[-1][0] if d else 1
    if t1 - t0 < 1:
        t1 = t0 + 1
    ystep = max(1, round(nice_step(ymax - ymin, ny_ticks(h))))
    L, T, R, B = margins(w, h, ticks(ymin, ymax, ystep))
    X, Y = frame(cv, L, T, R, B, t0, t1, ymin, ymax, nice_step(t1 - t0, nticks(R - L, fmt(t1) + '0', 6)),
                 ystep, st['xLabel'], st['yLabel'], False)

    def clipY(v):
        return min(B + 2, max(T - 2, Y(v)))
    if sig > 0:
        cv.create_rectangle(L, clipY(mu + sig), R, clipY(mu - sig), fill=C['band'], outline='')
    cv.create_line(L, clipY(mu), R, clipY(mu), fill=C['binom'], dash=C['meanDash'], width=1.2 * C['lw'])
    if len(d) > 2 * (R - L):  # точек больше, чем пикселей: в каждом столбце пикселей — от min до max
        cols = {}
        for t, n in d:
            c = int(X(t))
            lo, hi = cols.get(c, (n, n))
            cols[c] = (min(lo, n), max(hi, n))
        pts = []
        for c in sorted(cols):
            lo, hi = cols[c]
            pts += [c, Y(hi), c, Y(lo)]
        cv.create_line(*pts, fill=C['line'], width=1.4 * C['lw'])
    elif len(d) > 1:
        pts = [X(d[0][0]), Y(d[0][1])]
        for i in range(1, len(d)):  # ступенчатая линия
            x = X(d[i][0])
            pts += [x, Y(d[i - 1][1]), x, Y(d[i][1])]
        cv.create_line(*pts, fill=C['line'], width=1.4 * C['lw'])
    cv.tag_raise('all')
