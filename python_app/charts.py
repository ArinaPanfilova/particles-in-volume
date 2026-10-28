# -*- coding: utf-8 -*-
"""Графики на tk.Canvas: гистограмма P(n) и временной ряд n(t)."""
import math

from palette import C
from sim import Dist

FONT = ('Segoe UI', 9)
SCALE = 1.0  # масштаб интерфейса (DPI), задаётся приложением
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


def frame(cv, L, T, R, B, xlo, xhi, ylo, yhi, xstep, ystep, xlabel, ylabel, integer_x):
    def X(x):
        return L + (x - xlo) / (xhi - xlo) * (R - L)

    def Y(y):
        return B - (y - ylo) / (yhi - ylo) * (B - T)
    for y in frange(math.ceil(ylo / ystep) * ystep, yhi, ystep):
        cv.create_line(L, Y(y), R, Y(y), fill=C['grid'])
        cv.create_text(L - 4, Y(y), text=fmt(y), anchor='e', fill=C['text'], font=FONT)
    for x in frange(math.ceil(xlo / xstep) * xstep, xhi, xstep):
        xv = round(x) if integer_x else x
        cv.create_text(X(xv), B + 4, text=fmt(xv), anchor='n', fill=C['text'], font=FONT)
    cv.create_line(L, T, L, B, R, B, fill=C['axis'])
    cv.create_text(R, B - 3, text=xlabel, anchor='se', fill=C['axis'], font=FONT)
    cv.create_text(L + 4, T, text=ylabel, anchor='nw', fill=C['axis'], font=FONT)
    return X, Y


def hist(cv, st):
    """st: N, p, closed, n0, hist, samples, pairs, show{binom,pois,gauss}, xLabel, yLabel, empty,
    sigma — раскрасить столбики по отклонению от ⟨n⟩: до σ, до 2σ, дальше"""
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
    L, T, R, B = 46 * SCALE, 14 * SCALE, w - 10 * SCALE, h - 22 * SCALE
    xstep = max(1, round(nice_step(hi - lo, 10)))
    X, Y = frame(cv, L, T, R, B, lo - 0.6, hi + 0.6, 0, ymax, xstep, nice_step(ymax, 4),
                 st['xLabel'], st['yLabel'], True)
    bw = max(1, (X(1) - X(0)) * 0.8)
    by_sigma = st.get('sigma') and not st['closed'] and sig > 0
    lw = C['lw']
    for n in range(lo, hi + 1):
        v = expP(n)
        if v <= 0:
            continue
        x = X(n) - bw / 2
        col = C['bar']
        if by_sigma:
            dev = abs(n - mu)
            col = C['sig1'] if dev <= sig else C['sig2'] if dev <= 2 * sig else C['sig3']
        cv.create_rectangle(x, Y(v), x + bw, B, fill=col, outline=C['barEdge'] if bw > 3 else '')
    if st['show']['gauss'] and not st['closed'] and s2 > 0:
        pts = []
        K = 200
        scale = 2 if pairs else 1   # у пар вероятность сосредоточена на чётных n
        for i in range(K + 1):
            x = lo - 0.6 + (hi - lo + 1.2) * i / K
            pts += [X(x), Y(min(scale * Dist.gauss(x, mu, s2), ymax))]
        cv.create_line(*pts, fill=C['gauss'], width=2 * lw, smooth=True, dash=C['gaussDash'])
    ns = [n for n in range(lo, hi + 1) if not pairs or n % 2 == 0]
    if st['show']['pois'] and not st['closed'] and len(ns) > 1:
        pts = []
        for n in ns:
            pts += [X(n), Y(poisP(n))]
        cv.create_line(*pts, fill=C['pois'], width=1.5 * lw, dash=C['poisDash'])
        if bw > 4:
            for n in ns:
                q = 2.5 * lw
                cv.create_rectangle(X(n) - q, Y(poisP(n)) - q, X(n) + q, Y(poisP(n)) + q,
                                    fill=C['pois'], outline='')
    if st['show']['binom']:
        pts = []
        for n in ns:
            pts += [X(n), Y(binP(n))]
        if len(pts) >= 4:
            cv.create_line(*pts, fill=C['binom'], width=1.5 * lw, dash=C['binomDash'])
        if bw > 3:
            for n in ns:
                y = Y(binP(n))
                q = 3 * lw
                cv.create_oval(X(n) - q, y - q, X(n) + q, y + q, fill=C['binom'], outline='')
    if tot == 0 and st.get('empty'):
        cv.create_text((L + R) / 2, (T + B) / 2, text=st['empty'], fill=C['axis'], font=('Segoe UI', 10))


def series(cv, st):
    """st: series [(t, n)], N, p, closed, n0, pairs, xLabel, yLabel, zoom (0 … ZOOMS − 1)"""
    cv.delete('all')
    w, h = cv.winfo_width(), cv.winfo_height()
    if w < 50 or h < 50:
        return
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
    t0 = d[0][0] if d else 0
    t1 = d[-1][0] if d else 1
    if t1 - t0 < 1:
        t1 = t0 + 1
    L, T, R, B = 46 * SCALE, 14 * SCALE, w - 10 * SCALE, h - 22 * SCALE
    X, Y = frame(cv, L, T, R, B, t0, t1, ymin, ymax, nice_step(t1 - t0, 6),
                 max(1, round(nice_step(ymax - ymin, 4))), st['xLabel'], st['yLabel'], False)

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
