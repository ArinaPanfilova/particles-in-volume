# -*- coding: utf-8 -*-
"""Молекулярно-динамическая модель двумерного газа из твёрдых дисков
в прямоугольном сосуде с выделенной областью (полоса у левой стенки или
прямоугольник в углу), необязательной перегородкой с отверстием, примесью
молекул другого размера и возможностью объединять атомы в двухатомные молекулы."""
import math
import random

import numpy as np

# ln(k!) для k = 0..2000
LOG_FACT = np.concatenate(([0.0], np.cumsum(np.log(np.arange(1, 2001)))))


class Dist:
    @staticmethod
    def binom(n, N, p):
        if n < 0 or n > N:
            return 0.0
        if p <= 0:
            return 1.0 if n == 0 else 0.0
        if p >= 1:
            return 1.0 if n == N else 0.0
        return math.exp(LOG_FACT[N] - LOG_FACT[n] - LOG_FACT[N - n]
                        + n * math.log(p) + (N - n) * math.log(1 - p))

    @staticmethod
    def poisson(n, lam):
        if n < 0:
            return 0.0
        if lam <= 0:
            return 1.0 if n == 0 else 0.0
        return math.exp(n * math.log(lam) - lam - LOG_FACT[n])

    @staticmethod
    def gauss(x, mu, s2):
        if s2 <= 0:
            return 0.0
        return math.exp(-(x - mu) ** 2 / (2 * s2)) / math.sqrt(2 * math.pi * s2)


class Simulation:
    SKIN = 12.0  # запас для списка соседей (список Верле)
    H = 400.0    # высота сосуда; ширина задаётся параметром W

    def __init__(self, W=600):
        self.p = dict(
            W=float(W),       # ширина сосуда (объём V = W·H)
            N=100,            # число атомов основной компоненты
            r=4.0,            # радиус атома
            u=2.0,            # тепловая скорость (σ проекции скорости) основной компоненты
            frac=0.3,         # доля площади сосуда, занятая выделенной областью, v/V
            shape='strip',    # форма области: strip (полоса) | corner (угол сосуда)
            wall=False,       # непроницаемая перегородка на границе области
            hole=0.25,        # размер отверстия (доля длины стороны области)
            impN=0,           # число молекул примеси
            impR=10.0,        # радиус молекул примеси
            diatomic=False,   # атомы основной компоненты объединены попарно в молекулы
            count='main',     # кого считаем: main | imp | all
            init='uniform',   # начальное состояние: uniform | outside | inside
        )
        self.sample_dt = 2.0
        self.series_len = 12000  # история n(t) для самого мелкого масштаба графика (charts.WIN · 2^3)
        self.reset()

    # ---------------- геометрия ----------------
    @property
    def W(self):
        return self.p['W']

    def region(self):
        """Размеры выделенной области a × b (левый верхний угол сосуда)."""
        f = self.p['frac']
        if self.p['shape'] == 'corner':
            k = math.sqrt(f)
            return self.W * k, self.H * k
        return self.W * f, self.H

    def inside(self, x, y):
        a, b = self.region()
        if self.p['shape'] == 'corner':
            return (x < a) & (y < b)
        return x < a

    def hole_range(self):
        """Отверстие — в середине вертикальной стороны области x = a."""
        _, b = self.region()
        h = self.p['hole'] * b
        return (b - h) / 2, (b + h) / 2

    def boundary(self):
        """Граница области в виде отрезков (x0, y0, x1, y1) без отверстия."""
        a, b = self.region()
        s = [(a, 0.0, a, b)]
        if self.p['shape'] == 'corner':
            s.append((0.0, b, a, b))
        return s

    def segments(self):
        """Отрезки непроницаемой перегородки с учётом отверстия."""
        if not self.p['wall']:
            return []
        a, b = self.region()
        ha, hb = self.hole_range()
        s = []
        if ha > 0:
            s.append((a, 0.0, a, ha))
        if hb < b:
            s.append((a, hb, a, b))
        if self.p['shape'] == 'corner':
            s.append((0.0, b, a, b))
        return s

    def counted_radius(self):
        return self.p['impR'] if self.p['count'] == 'imp' else self.p['r']

    def main_n(self):
        N = int(self.p['N'])
        return N - N % 2 if self.p['diatomic'] else N

    def counted_n(self):
        c = self.p['count']
        if c == 'main':
            return self.main_n()
        if c == 'imp':
            return int(self.p['impN'])
        return self.main_n() + int(self.p['impN'])

    def counted_mask(self):
        c = self.p['count']
        if c == 'all':
            return np.ones(len(self.x), bool)
        return self.s == (0 if c == 'main' else 1)

    def pairs_counted(self):
        """Считаем атомы, объединённые в пары (двухатомные молекулы)."""
        return self.p['diatomic'] and self.p['count'] == 'main'

    def is_closed(self):
        """Отверстие меньше диаметра молекулы — частицы не проходят."""
        _, b = self.region()
        return self.p['wall'] and self.p['hole'] * b <= 2 * self.counted_radius()

    def p_for_radius(self, r):
        """Вероятность нахождения центра молекулы в выделенной области с учётом
        того, что центр не подходит к стенкам и перегородке ближе r."""
        W, H = self.W, self.H
        a, b = self.region()
        wall = self.p['wall']
        if self.p['shape'] == 'corner':
            total = (W - 2 * r) * (H - 2 * r)
            if wall:
                pin = max(0.0, a - 2 * r) * max(0.0, b - 2 * r)
                pout = total - a * b
                p = pin / (pin + pout) if pin + pout > 0 else 0.0
            else:
                p = max(0.0, a - r) * max(0.0, b - r) / total
        else:
            p = (a - 2 * r) / (W - 4 * r) if wall else (a - r) / (W - 2 * r)
        return min(1.0, max(0.0, p))

    def theory_p(self):
        return self.p_for_radius(self.counted_radius())

    # ---------------- инициализация ----------------
    def _too_close_to_wall(self, x, y, r):
        for x0, y0, x1, y1 in self.segments():
            cx = min(max(x, x0), x1)
            cy = min(max(y, y0), y1)
            if (x - cx) ** 2 + (y - cy) ** 2 < (r + 0.5) ** 2:
                return True
        return False

    def _mode_ok(self, x, y, mode):
        if mode == 'uniform':
            return True
        ins = bool(self.inside(x, y))
        return ins if mode == 'inside' else not ins

    def reset(self):
        p, W, H = self.p, self.W, self.H
        m0 = p['r'] ** 2
        n_imp, n_main = int(p['impN']), self.main_n()
        # одна «единица» размещения — атом или пара атомов
        units = [((p['impR'],), 1)] * n_imp
        if p['diatomic']:
            units += [((p['r'], p['r']), 0)] * (n_main // 2)
        else:
            units += [((p['r'],), 0)] * n_main
        n = n_imp + n_main
        X, Y, R = np.zeros(n), np.zeros(n), np.zeros(n)
        S = np.zeros(n, int)
        bonds = []
        k = 0
        for radii, s in units:
            mode = p['init'] if s == 0 else 'uniform'
            r = radii[0]
            best = None
            for attempt in range(300):
                x = r + random.random() * (W - 2 * r)
                y = r + random.random() * (H - 2 * r)
                pts = [(x, y)]
                if len(radii) == 2:
                    ang = random.random() * 2 * math.pi
                    pts.append((x + 2 * r * math.cos(ang), y + 2 * r * math.sin(ang)))
                if any(not (r <= qx <= W - r and r <= qy <= H - r) for qx, qy in pts):
                    continue
                if any(self._too_close_to_wall(qx, qy, r) for qx, qy in pts):
                    continue
                best = pts
                if attempt < 200 and not all(self._mode_ok(qx, qy, mode) for qx, qy in pts):
                    continue
                if k and any(np.any((X[:k] - qx) ** 2 + (Y[:k] - qy) ** 2 < (R[:k] + r) ** 2)
                             for qx, qy in pts):
                    continue
                break
            if best is None:
                best = [(r + random.random() * (W - 2 * r), r + random.random() * (H - 2 * r))
                        for _ in radii]
            for qx, qy in best:
                X[k], Y[k], R[k], S[k] = qx, qy, r, s
                k += 1
            if len(radii) == 2:
                bonds.append((k - 2, k - 1))
        self.x, self.y, self.r, self.s = X, Y, R, S
        self.m = R ** 2
        sv = p['u'] * np.sqrt(m0 / self.m) if n else np.zeros(0)
        self.vx = np.random.randn(n) * sv
        self.vy = np.random.randn(n) * sv
        self.bonds = (np.array([b[0] for b in bonds], int), np.array([b[1] for b in bonds], int))
        if bonds:
            self.apply_bonds()
        self.px, self.py = X.copy(), Y.copy()
        self.start_in = self.inside_mask()  # где молекула была при старте — для раскраски
        # «температура» поддерживается постоянной: энергия, заданная при старте
        self.energy = float(np.sum(self.m * (self.vx ** 2 + self.vy ** 2))) if n else 0.0
        self.tagged = n_imp if n_main > 0 else -1
        self.pairs = None
        self.time = 0.0
        self.next_sample = 0.0
        self.last_n = 0
        self.clear_stats()

    def clear_stats(self):
        self.hist = np.zeros(self.counted_n() + 1)
        self.samples = 0
        self.sum = 0.0
        self.sum2 = 0.0
        self.series = []
        self.tagged_in = 0
        self.n0 = self.count_inside()

    def set_speed(self, u):
        """Изменение температуры без перезапуска: масштабируем скорости."""
        k = u / self.p['u'] if self.p['u'] else 0
        if k > 0 and math.isfinite(k):
            self.vx *= k
            self.vy *= k
            self.energy *= k * k
        self.p['u'] = u

    def set_width(self, W):
        """Изменение объёма сосуда V при неизменном объёме выделенной области v."""
        a_old = self.p['frac'] * self.p['W']
        self.p['W'] = float(W)
        self.p['frac'] = min(0.98, max(0.02, a_old / self.p['W']))

    # ---------------- статистика ----------------
    def inside_mask(self):
        return self.inside(self.x, self.y)

    def count_inside(self):
        if not len(self.x):
            return 0
        return int(np.count_nonzero(self.inside_mask() & self.counted_mask()))

    def sample(self):
        n = self.count_inside()
        if n < len(self.hist):
            self.hist[n] += 1
        self.samples += 1
        self.sum += n
        self.sum2 += n * n
        self.series.append((self.time, n))
        if len(self.series) > self.series_len:
            del self.series[0]
        t = self.tagged
        if t >= 0 and self.inside(self.x[t], self.y[t]):
            self.tagged_in += 1
        self.last_n = n

    # ---------------- столкновения ----------------
    def build_pairs(self):
        """Список пар-кандидатов, находящихся ближе R + SKIN (список Верле)."""
        n = len(self.x)
        if n < 2:
            self.pairs = (np.zeros(0, int), np.zeros(0, int))
        else:
            # сортируем по x и для каждой частицы берём соседей справа в пределах lmax
            order = np.argsort(self.x)
            xs = self.x[order]
            lmax = 2 * float(self.r.max()) + self.SKIN
            hi = np.searchsorted(xs, xs + lmax, side='right')
            first = np.arange(1, n + 1)
            counts = np.maximum(hi - first, 0)
            total = int(counts.sum())
            si = np.repeat(np.arange(n), counts)
            sj = np.arange(total) - np.repeat(np.cumsum(counts) - counts, counts) + np.repeat(first, counts)
            I, J = order[si], order[sj]
            dx = self.x[J] - self.x[I]
            dy = self.y[J] - self.y[I]
            lim = self.r[I] + self.r[J] + self.SKIN
            keep = dx * dx + dy * dy < lim * lim
            I, J = I[keep], J[keep]
            bi, bj = self.bonds
            if len(bi):
                # атомы одной молекулы связаны жёстко и не сталкиваются друг с другом
                key = np.minimum(I, J) * n + np.maximum(I, J)
                keep = ~np.isin(key, np.minimum(bi, bj) * n + np.maximum(bi, bj))
                I, J = I[keep], J[keep]
            self.pairs = (I, J)
        self.ref_x = self.x.copy()
        self.ref_y = self.y.copy()

    def collide(self):
        I, J = self.pairs
        if not len(I):
            return
        x, y = self.x, self.y
        dx = x[J] - x[I]
        dy = y[J] - y[I]
        R = self.r[I] + self.r[J]
        d2 = dx * dx + dy * dy
        hit = d2 < R * R
        if not hit.any():
            return
        I, J, dx, dy, R, d2 = I[hit], J[hit], dx[hit], dy[hit], R[hit], d2[hit]
        d = np.sqrt(d2)
        tiny = d < 1e-9
        d_safe = np.where(tiny, 1.0, d)
        nx = np.where(tiny, 1.0, dx / d_safe)
        ny = np.where(tiny, 0.0, dy / d_safe)
        d = np.where(tiny, 0.0, d)
        ia = 1 / self.m[I]
        ib = 1 / self.m[J]
        vrel = (self.vx[I] - self.vx[J]) * nx + (self.vy[I] - self.vy[J]) * ny
        imp = np.where(vrel > 0, 2 * vrel / (ia + ib), 0.0)  # упругий удар
        k = (R - d) / (ia + ib)                               # раздвигаем перекрытие
        n = len(x)
        bc = np.bincount
        self.vx += bc(J, imp * ib * nx, n) - bc(I, imp * ia * nx, n)
        self.vy += bc(J, imp * ib * ny, n) - bc(I, imp * ia * ny, n)
        self.x += bc(J, k * ib * nx, n) - bc(I, k * ia * nx, n)
        self.y += bc(J, k * ib * ny, n) - bc(I, k * ia * ny, n)

    def apply_bonds(self):
        """Начальная расстановка молекулы: расстояние между центрами атомов
        ровно 2r, относительная скорость вдоль связи гасится."""
        I, J = self.bonds
        if not len(I):
            return
        dx = self.x[J] - self.x[I]
        dy = self.y[J] - self.y[I]
        d = np.maximum(np.sqrt(dx * dx + dy * dy), 1e-9)
        nx, ny = dx / d, dy / d
        corr = (d - 2 * self.r[I]) / 2
        self.x[I] += nx * corr
        self.y[I] += ny * corr
        self.x[J] -= nx * corr
        self.y[J] -= ny * corr
        vrel = (self.vx[J] - self.vx[I]) * nx + (self.vy[J] - self.vy[I]) * ny
        self.vx[I] += nx * vrel / 2
        self.vy[I] += ny * vrel / 2
        self.vx[J] -= nx * vrel / 2
        self.vy[J] -= ny * vrel / 2

    def bond_forces(self, dt):
        """Атомы молекулы связаны жёсткой пружиной с длиной покоя 2r
        (жёсткость подобрана так, чтобы при тепловом движении связь
        растягивалась лишь на ~10–20 %). В отличие от жёсткой связи
        пружина сохраняет энергию при ударах молекулы о стенки."""
        I, J = self.bonds
        if not len(I):
            return
        dx = self.x[J] - self.x[I]
        dy = self.y[J] - self.y[I]
        d = np.maximum(np.sqrt(dx * dx + dy * dy), 1e-9)
        r = self.r[I]
        m = self.m[I]
        kspring = m * (self.p['u'] / (0.2 * r)) ** 2
        f = kspring * (d - 2 * r) * dt / m  # изменение скорости за шаг
        fx, fy = f * dx / d, f * dy / d
        self.vx[I] += fx
        self.vy[I] += fy
        self.vx[J] -= fx
        self.vy[J] -= fy

    def step(self, dt):
        W, H = self.W, self.H
        x, y, vx, vy, r = self.x, self.y, self.vx, self.vy, self.r
        self.px[:] = x
        self.py[:] = y
        x += vx * dt
        y += vy * dt
        self.bond_forces(dt)
        self.collide()
        # стенки сосуда
        np.copyto(vx, np.abs(vx), where=x < r)
        np.copyto(vx, -np.abs(vx), where=x > W - r)
        np.copyto(vy, np.abs(vy), where=y < r)
        np.copyto(vy, -np.abs(vy), where=y > H - r)
        np.clip(x, r, W - r, out=x)
        np.clip(y, r, H - r, out=y)
        if self.p['wall']:
            for x0, y0, x1, y1 in self.segments():
                cx = np.clip(x, x0, x1)
                cy = np.clip(y, y0, y1)
                ddx = x - cx
                ddy = y - cy
                d2 = ddx * ddx + ddy * ddy
                hit = d2 < r * r
                if not hit.any():
                    continue
                idx = np.nonzero(hit)[0]
                d = np.sqrt(d2[idx])
                ex, ey = ddx[idx], ddy[idx]
                tiny = d < 1e-9
                if tiny.any():
                    # центр точно на отрезке — выталкиваем туда, откуда пришёл
                    vert = x0 == x1
                    side = np.where((self.px[idx] if vert else self.py[idx]) < (x0 if vert else y0), -1.0, 1.0)
                    ex = np.where(tiny, side if vert else 0.0, ex)
                    ey = np.where(tiny, 0.0 if vert else side, ey)
                    d = np.where(tiny, 1.0, d)
                nx, ny = ex / d, ey / d
                vn = vx[idx] * nx + vy[idx] * ny
                refl = np.minimum(vn, 0.0)
                vx[idx] -= 2 * refl * nx
                vy[idx] -= 2 * refl * ny
                x[idx] = cx[idx] + nx * r[idx]
                y[idx] = cy[idx] + ny * r[idx]
            # защита от «туннелирования» сквозь перегородку
            ha, hb = self.hole_range()
            was = self.inside(self.px, self.py)
            bad = (was != self.inside(x, y)) & ~((y > ha) & (y < hb))
            if bad.any():
                x[bad] = self.px[bad]
                y[bad] = self.py[bad]
                vx[bad] = -vx[bad]
                vy[bad] = -vy[bad]
        self.time += dt
        while self.time >= self.next_sample:
            self.sample()
            self.next_sample += self.sample_dt

    def advance(self, T):
        """Продвинуть модель на интервал времени T, разбив его на устойчивые шаги."""
        if not len(self.x):
            self.time += T
            while self.time >= self.next_sample:
                self.sample()
                self.next_sample += self.sample_dt
            return
        vmax = max(1e-6, float(np.max(np.abs(self.vx) + np.abs(self.vy))))
        dt = min(1.0, max(0.01, 0.3 * float(self.r.min()) / vmax))
        steps = min(600, math.ceil(T / dt))
        h = T / steps
        if self.pairs is None:
            self.build_pairs()
        for _ in range(steps):
            disp = np.max((self.x - self.ref_x) ** 2 + (self.y - self.ref_y) ** 2)
            if 4 * disp > self.SKIN * self.SKIN:
                self.build_pairs()
            self.step(h)
        # одновременная обработка столкновений и связей слегка нарушает закон
        # сохранения энергии — возвращаем кинетическую энергию к заданной (термостат)
        e = float(np.sum(self.m * (self.vx ** 2 + self.vy ** 2)))
        if e > 0 and self.energy > 0:
            k = math.sqrt(self.energy / e)
            self.vx *= k
            self.vy *= k
