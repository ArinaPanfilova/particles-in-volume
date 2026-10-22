# -*- coding: utf-8 -*-
"""Частицы в выделенном объёме — интерактивная демонстрация (Python / tkinter).

Запуск:  python app.py                 — главное меню
         python app.py --demo hole     — сразу открыть готовый опыт
         python app.py --theory | --authors
"""
import math
import os
import sys
import time
import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageDraw, ImageTk

import charts
from htmlview import DocView
from i18n import I18N, LANGS
from sim import Simulation

BG, PANEL, INK, MUTED, LINE = '#f4f5f0', '#ffffff', '#1f2937', '#6b7280', '#e2e4dc'
ACCENT, ACCENT2, REGION = '#1d3557', '#2f5d8a', '#cfe6bd'
FONT = 'Segoe UI'

BASE = dict(W=600.0, N=100, r=4.0, u=2.0, frac=0.3, shape='strip', wall=False, hole=0.25,
            impN=0, impR=10.0, diatomic=False, count='main', init='uniform')
# готовые опыты: параметры модели, показываемые кривые, скорость моделирования
PRESETS = [
    ('few', 'presetFew', dict(N=6, r=6, frac=0.25, shape='corner'), dict(binom=True), 6),
    ('p112', 'preset112', dict(N=2, r=4, frac=0.1), dict(binom=True), 6),
    ('corner', 'presetCorner', dict(N=60, r=4, frac=0.2, shape='corner'), dict(binom=True, gauss=True), 3),
    ('binom', 'presetBinom', dict(N=20, r=5, frac=0.5), dict(binom=True, gauss=True), 4),
    ('poisson', 'presetPoisson', dict(N=300, r=2.5, frac=0.02), dict(binom=True, pois=True), 4),
    ('bigV', 'presetBigV', dict(W=1000.0, N=100, r=4, frac=0.18), dict(binom=True), 3),
    ('p33', 'preset33', dict(N=60, r=4, frac=0.95), dict(binom=True, pois=True), 4),
    ('hole', 'presetHole', dict(N=150, r=3, frac=0.3, wall=True, hole=0.15, init='outside'), dict(binom=True), 4),
    ('dense', 'presetDense', dict(N=340, r=8, frac=0.3, u=1.5), dict(binom=True), 2),
    ('bigAtoms', 'presetBigAtoms', dict(N=40, r=12, frac=0.25, shape='corner'), dict(binom=True), 3),
    ('diatomic', 'presetDiatomic', dict(N=120, r=4, frac=0.3, diatomic=True), dict(binom=True), 3),
    ('imp', 'presetImp', dict(N=150, r=3, frac=0.3, impN=15, impR=18), dict(binom=True), 2),
]
PRESET_BY_ID = {p[0]: p for p in PRESETS}


def btn(master, primary=False, big=False, **kw):
    b = tk.Button(master, relief='flat', bd=0, cursor='hand2',
                  font=(FONT, 13 if big else 10), padx=18 if big else 12, pady=10 if big else 5,
                  bg=ACCENT if primary else PANEL, fg='#ffffff' if primary else INK,
                  activebackground=ACCENT2 if primary else '#eef3f8',
                  activeforeground='#ffffff' if primary else INK,
                  highlightthickness=1, highlightbackground=ACCENT if primary else LINE,
                  anchor='w' if big else 'center', **kw)
    return b


class VesselView:
    """Отрисовка сосуда: кадр рисуется в памяти (Pillow, со сглаживанием)
    и выводится на tk.Canvas одним изображением; подписи — элементы холста."""
    SS = 2  # коэффициент суперсэмплинга

    def __init__(self, canvas, sim, labels=True):
        self.cv, self.sim, self.labels = canvas, sim, labels
        self.photo = None
        self.size = None
        self.img_item = canvas.create_image(0, 0, anchor='nw')
        self.text_key = None

    def _hex(self, c):
        return tuple(int(c[i:i + 2], 16) for i in (1, 3, 5))

    def draw(self, tagged=True, closed_text=''):
        cv, s = self.cv, self.sim
        w, h = cv.winfo_width(), cv.winfo_height()
        if w < 20 or h < 20:
            return
        pad = 6
        k = min((w - 2 * pad) / s.W, (h - 2 * pad) / s.H)
        ox, oy = round((w - s.W * k) / 2), round((h - s.H * k) / 2)
        iw, ih = max(1, round(s.W * k)), max(1, round(s.H * k))
        if self.size != (iw, ih):
            self.size = (iw, ih)
            self.photo = ImageTk.PhotoImage('RGB', (iw, ih))
            cv.itemconfigure(self.img_item, image=self.photo)
            self.text_key = None
        cv.coords(self.img_item, ox, oy)
        S = self.SS
        K = k * S
        img = Image.new('RGB', (iw * S, ih * S), (251, 251, 247))
        d = ImageDraw.Draw(img)

        def X(x):
            return x * K

        def Y(y):
            return y * K
        a, b = s.region()
        d.rectangle([X(0), Y(0), X(a), Y(b)], fill=self._hex(REGION))
        if s.p['wall']:
            for x0, y0, x1, y1 in s.segments():
                d.line([X(x0), Y(y0), X(x1), Y(y1)], fill=(43, 43, 43), width=int(4 * S))
        else:
            for x0, y0, x1, y1 in s.boundary():
                L = math.hypot(X(x1) - X(x0), Y(y1) - Y(y0))
                ux, uy = (X(x1) - X(x0)) / L, (Y(y1) - Y(y0)) / L
                t = 0.0
                while t < L:  # пунктир
                    e = min(L, t + 6 * S)
                    d.line([X(x0) + ux * t, Y(y0) + uy * t, X(x0) + ux * e, Y(y0) + uy * e],
                           fill=(80, 130, 60), width=max(1, int(1.5 * S)))
                    t += 11 * S
        xs = X(0) + s.x * K
        ys = Y(0) + s.y * K
        rs = s.r * K
        ins = s.inside_mask() if len(s.x) else []
        I, J = s.bonds
        for i, j in zip(I, J):
            d.line([xs[i], ys[i], xs[j], ys[j]], fill=self._hex(ACCENT), width=max(1, int(s.r[i] * K * 0.6)))
        t_idx = s.tagged if tagged else -1
        main_c, imp_c = self._hex(ACCENT), (200, 85, 61)
        for i in range(len(s.x)):
            if i == t_idx:
                continue
            col = main_c if s.s[i] == 0 else imp_c
            fill = col if ins[i] else ((255, 255, 255) if s.s[i] == 0 else (251, 227, 220))
            r = rs[i]
            d.ellipse([xs[i] - r, ys[i] - r, xs[i] + r, ys[i] + r], fill=fill, outline=col,
                      width=max(S, int(r * 0.25)))
        if 0 <= t_idx < len(s.x):
            x, y, r = xs[t_idx], ys[t_idx], rs[t_idx]
            g = 5 * S
            d.ellipse([x - r - g, y - r - g, x + r + g, y + r + g], fill=(245, 201, 201))
            d.ellipse([x - r, y - r, x + r, y + r], fill=(214, 40, 40) if ins[t_idx] else (255, 255, 255),
                      outline=(214, 40, 40), width=max(int(1.5 * S), int(r * 0.3)))
        d.rectangle([0, 0, iw * S - 1, ih * S - 1], outline=(43, 43, 43), width=3 * S)
        self.photo.paste(img.reduce(S))

        key = (w, h, ox, oy, closed_text, self.labels)
        if key != self.text_key:
            self.text_key = key
            cv.delete('label')
            if self.labels:
                cv.create_text(ox + 10, oy + 8, text='v', anchor='nw', fill='#28501e',
                               font=(FONT, 13, 'italic'), tags='label')
                cv.create_text(ox + s.W * k - 10, oy + 8, text='V', anchor='ne', fill=MUTED,
                               font=(FONT, 13, 'italic'), tags='label')
            if closed_text:
                t = cv.create_text(w / 2, oy + s.H * k - 14, text=closed_text, anchor='s', width=w * 0.8,
                                   fill='#7a2e1d', font=(FONT, 10), tags='label')
                bb = cv.bbox(t)
                r = cv.create_rectangle(bb[0] - 8, bb[1] - 5, bb[2] + 8, bb[3] + 5, fill='#fff4e5',
                                        outline='#e9b872', tags='label')
                cv.tag_raise(t, r)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.lang = 'ru'
        self.title(self.t('appTitle'))
        self.configure(bg=BG)
        # значок окна: рядом со скриптом или внутри собранного exe
        base = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        try:
            self.iconbitmap(os.path.join(base, 'icon.ico'))
        except tk.TclError:
            pass
        self.geometry('1400x880')
        self.minsize(1040, 680)
        try:
            self.state('zoomed')
        except tk.TclError:
            pass
        self.scale_ui = self.winfo_fpixels('1i') / 96
        charts.SCALE = self.scale_ui
        self.loc = []          # (виджет, ключ) для смены языка
        self.loc_combos = []   # (combobox, [ключи])
        self.lang_combos = []

        self.sim = Simulation()
        self.running = False
        self.sim_speed = 2.0
        self.view = dict(tagged=True, binom=True, pois=False, gauss=False)
        self.menu_sim = Simulation()
        self.menu_sim.p.update(N=70, r=5, u=0.8, frac=0.2, shape='corner')
        self.menu_sim.reset()

        style = ttk.Style(self)
        style.configure('TCombobox', padding=4)

        self.container = tk.Frame(self, bg=BG)
        self.container.pack(fill='both', expand=True)
        self.container.rowconfigure(0, weight=1)
        self.container.columnconfigure(0, weight=1)
        self.screens = {}
        self._build_menu()
        self._build_demo()
        self._build_doc('theory', 'menuTheory', 'theoryHtml')
        self._build_doc('authors', 'menuAuthors', 'authorsHtml')
        self.screen = None
        self.go('menu')
        self.sync_controls()
        self.apply_lang()
        self.bind('<space>', self._space)
        self.last = time.perf_counter()
        self.frame_no = 0
        self.after(16, self.loop)

    # ---------------- язык ----------------
    def t(self, k):
        d = I18N.get(self.lang, {})
        return d.get(k, I18N['ru'].get(k, k))

    def L(self, widget, key):
        self.loc.append((widget, key))
        return widget

    def apply_lang(self):
        self.title(self.t('appTitle'))
        for w, k in self.loc:
            w.configure(text=self.t(k))
        for cb, keys in self.loc_combos:
            i = cb.current()
            cb.configure(values=[self.t(k) for k in keys])
            cb.current(max(0, i))
        names = [I18N[l]['langName'] for l in LANGS]
        for cb in self.lang_combos:
            cb.configure(values=names)
            cb.current(LANGS.index(self.lang))
        self.lang_btn.configure(text='%s: %s' % (self.t('menuLanguage'), self.t('langName')))
        for name, (view, key) in self.docs.items():
            html = self.t(key)
            if key == 'theoryHtml':
                html = self._theory_html()
            view.set_html(html)
        self.update_play()
        self.draw_legends()
        self.draw_all(force=True)

    def _theory_html(self):
        html = self.t('theoryHtml')
        extra = self.t('theoryExtra')
        # новый раздел 11 — перед таблицей задач и ссылка на него в оглавлении
        i = html.find('<h2 id="t10">')
        if i >= 0:
            html = html[:i] + extra + html[i:]
        html = html.replace('</nav>', '<a href="#t11">%s</a></nav>' % self.t('tocExtra'), 1)
        return html

    def set_lang(self, l):
        self.lang = l
        self.apply_lang()

    def _lang_combo(self, master):
        cb = ttk.Combobox(master, state='readonly', width=10, font=(FONT, 10))
        cb.bind('<<ComboboxSelected>>', lambda e: self.set_lang(LANGS[cb.current()]))
        self.lang_combos.append(cb)
        return cb

    # ---------------- экраны ----------------
    def go(self, name):
        self.screen = name
        self.screens[name].tkraise()
        self.after(30, lambda: self.draw_all(force=True))

    def _topbar(self, parent, title_key):
        bar = tk.Frame(parent, bg=PANEL, highlightthickness=1, highlightbackground=LINE)
        bar.pack(fill='x')
        self.L(btn(bar, command=lambda: self.go('menu')), 'back').pack(side='left', padx=(10, 6), pady=8)
        self.L(tk.Label(bar, bg=PANEL, fg=ACCENT, font=(FONT, 14, 'bold')), title_key).pack(side='left', padx=8)
        self._lang_combo(bar).pack(side='right', padx=10)
        return bar

    def _build_menu(self):
        f = tk.Frame(self.container, bg=BG)
        f.grid(row=0, column=0, sticky='nsew')
        self.screens['menu'] = f
        self.menu_cv = tk.Canvas(f, bg=BG, highlightthickness=0)
        self.menu_cv.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.menu_view = VesselView(self.menu_cv, self.menu_sim, labels=False)
        card = tk.Frame(f, bg=PANEL, highlightthickness=1, highlightbackground=LINE, padx=34, pady=28)
        card.place(relx=0.5, rely=0.5, anchor='center')
        self.L(tk.Label(card, bg=PANEL, fg=ACCENT2, font=(FONT, 9)), 'kicker').pack(anchor='w')
        self.L(tk.Label(card, bg=PANEL, fg=ACCENT, font=(FONT, 24, 'bold'), justify='left'),
               'appTitle').pack(anchor='w', pady=(6, 8))
        self.L(tk.Label(card, bg=PANEL, fg=MUTED, font=(FONT, 11), wraplength=470, justify='left'),
               'appSubtitle').pack(anchor='w', pady=(0, 18))
        for key, target, prim in (('menuDemo', 'demo', True), ('menuTheory', 'theory', False),
                                  ('menuAuthors', 'authors', False)):
            self.L(btn(card, primary=prim, big=True, command=lambda g=target: self.go(g)),
                   key).pack(fill='x', pady=4)
        self.lang_btn = tk.Menubutton(card, relief='flat', bd=0, font=(FONT, 13), bg=PANEL, fg=INK,
                                      anchor='w', padx=18, pady=10, cursor='hand2',
                                      highlightthickness=1, highlightbackground=LINE,
                                      activebackground='#eef3f8')
        m = tk.Menu(self.lang_btn, tearoff=0, font=(FONT, 12))
        for l in LANGS:
            m.add_command(label=I18N[l]['langName'], command=lambda l=l: self.set_lang(l))
        self.lang_btn.configure(menu=m)
        self.lang_btn.pack(fill='x', pady=4)

    def _build_doc(self, name, title_key, html_key):
        f = tk.Frame(self.container, bg=BG)
        f.grid(row=0, column=0, sticky='nsew')
        self.screens[name] = f
        bar = self._topbar(f, title_key)
        if name == 'theory':
            self.L(btn(bar, primary=True, command=lambda: self.go('demo')), 'menuDemo').pack(side='right', padx=4)
        view = DocView(f)
        view.pack(fill='both', expand=True)
        if not hasattr(self, 'docs'):
            self.docs = {}
        self.docs[name] = (view, html_key)

    # ---------------- демонстрация ----------------
    def _panel(self, parent, title_key=None):
        p = tk.Frame(parent, bg=PANEL, highlightthickness=1, highlightbackground=LINE, padx=12, pady=8)
        p.pack(fill='x', pady=(0, 8))
        if title_key:
            self.L(tk.Label(p, bg=PANEL, fg=ACCENT, font=(FONT, 11, 'bold')), title_key).pack(anchor='w', pady=(0, 4))
        return p

    def _build_demo(self):
        f = tk.Frame(self.container, bg=BG)
        f.grid(row=0, column=0, sticky='nsew')
        self.screens['demo'] = f
        bar = self._topbar(f, 'appTitle')
        self.L(btn(bar, command=self.clear_stats), 'clearStats').pack(side='right', padx=4)
        self.L(btn(bar, command=self.restart), 'reset').pack(side='right', padx=4)
        self.play_btn = btn(bar, primary=True, command=self.toggle_play)
        self.play_btn.pack(side='right', padx=4)

        body = tk.Frame(f, bg=BG)
        body.pack(fill='both', expand=True, padx=10, pady=10)
        side_outer = tk.Frame(body, bg=BG, width=int(380 * self.scale_ui))
        side_outer.pack(side='right', fill='y', padx=(10, 0))
        side_outer.pack_propagate(False)
        main = tk.Frame(body, bg=BG)
        main.pack(side='left', fill='both', expand=True)

        vp = tk.Frame(main, bg=PANEL, highlightthickness=1, highlightbackground=LINE)
        vp.pack(fill='both', expand=True)
        self.vessel_cv = tk.Canvas(vp, bg=PANEL, highlightthickness=0)
        self.vessel_cv.pack(fill='both', expand=True, padx=4, pady=4)
        self.vessel = VesselView(self.vessel_cv, self.sim)

        ch = tk.Frame(main, bg=BG)
        ch.pack(fill='both', expand=True, pady=(10, 0))
        ch.columnconfigure(0, weight=1, uniform='c')
        ch.columnconfigure(1, weight=1, uniform='c')
        ch.rowconfigure(0, weight=1)
        hp = tk.Frame(ch, bg=PANEL, highlightthickness=1, highlightbackground=LINE, padx=8, pady=6)
        hp.grid(row=0, column=0, sticky='nsew', padx=(0, 5))
        sp = tk.Frame(ch, bg=PANEL, highlightthickness=1, highlightbackground=LINE, padx=8, pady=6)
        sp.grid(row=0, column=1, sticky='nsew', padx=(5, 0))
        self.L(tk.Label(hp, bg=PANEL, fg=ACCENT, font=(FONT, 11, 'bold')), 'histTitle').pack(anchor='w')
        tg = tk.Frame(hp, bg=PANEL)
        tg.pack(side='bottom', fill='x')
        self.hist_leg = tk.Canvas(hp, bg=PANEL, height=int(20 * self.scale_ui), highlightthickness=0)
        self.hist_leg.pack(side='bottom', fill='x')
        self.hist_cv = tk.Canvas(hp, bg=PANEL, highlightthickness=0)
        self.hist_cv.pack(fill='both', expand=True)
        self.show_vars = {}
        for k, key in (('binom', 'showBinom'), ('pois', 'showPois'), ('gauss', 'showGauss')):
            v = tk.BooleanVar(value=self.view[k])
            self.show_vars[k] = v
            self.L(tk.Checkbutton(tg, variable=v, bg=PANEL, font=(FONT, 10), activebackground=PANEL,
                                  command=lambda k=k: self._toggle_curve(k)), key).pack(side='left', padx=(0, 10))
        self.L(tk.Label(sp, bg=PANEL, fg=ACCENT, font=(FONT, 11, 'bold')), 'timeTitle').pack(anchor='w')
        self.series_leg = tk.Canvas(sp, bg=PANEL, height=int(20 * self.scale_ui), highlightthickness=0)
        self.series_leg.pack(side='bottom', fill='x')
        self.series_cv = tk.Canvas(sp, bg=PANEL, highlightthickness=0)
        self.series_cv.pack(fill='both', expand=True)

        # прокручиваемая правая панель
        scv = tk.Canvas(side_outer, bg=BG, highlightthickness=0)
        ssb = tk.Scrollbar(side_outer, command=scv.yview)
        scv.configure(yscrollcommand=ssb.set)
        ssb.pack(side='right', fill='y')
        scv.pack(side='left', fill='both', expand=True)
        side = tk.Frame(scv, bg=BG)
        win = scv.create_window(0, 0, window=side, anchor='nw')
        side.bind('<Configure>', lambda e: scv.configure(scrollregion=scv.bbox('all')))
        scv.bind('<Configure>', lambda e: scv.itemconfigure(win, width=e.width))

        def wheel(e):
            scv.yview_scroll(int(-e.delta / 60), 'units')
        side_outer.bind('<Enter>', lambda e: self.bind_all('<MouseWheel>', wheel))
        side_outer.bind('<Leave>', lambda e: self.unbind_all('<MouseWheel>'))
        self._build_side(side)

        for cv in (self.vessel_cv, self.hist_cv, self.series_cv):
            cv.bind('<Configure>', lambda e: self.after_idle(self.draw_all))

    def _build_side(self, side):
        # статистика
        p = self._panel(side, 'secStats')
        tb = tk.Frame(p, bg=PANEL)
        tb.pack(fill='x')
        tb.columnconfigure(0, weight=1)
        self.L(tk.Label(tb, bg=PANEL, fg=MUTED, font=(FONT, 9, 'bold')), 'colExp').grid(row=0, column=1, sticky='e', padx=4)
        self.L(tk.Label(tb, bg=PANEL, fg=MUTED, font=(FONT, 9, 'bold')), 'colTheory').grid(row=0, column=2, sticky='e', padx=4)
        self.st = {}
        rows = [('stN', 'n', True), ('stSamples', 'samples', True), ('stP', 'p', False), ('stMean', 'mean', False),
                ('stVar', 'var', False), ('stRel', 'rel', False), ('stTag', 'tag', False)]
        self.tag_row = []
        for i, (key, name, span) in enumerate(rows, start=1):
            lab = self.L(tk.Label(tb, bg=PANEL, fg=INK, font=(FONT, 9), anchor='w', justify='left',
                                  wraplength=int(170 * self.scale_ui)), key)
            lab.grid(row=i, column=0, sticky='w', pady=1)
            if span:
                e = tk.Label(tb, bg=PANEL, font=('Consolas', 10))
                e.grid(row=i, column=1, columnspan=2, sticky='e', padx=4)
                self.st[name] = (e, None)
                cells = [lab, e]
            else:
                e = tk.Label(tb, bg=PANEL, font=('Consolas', 10))
                th = tk.Label(tb, bg=PANEL, font=('Consolas', 10), fg=ACCENT2)
                e.grid(row=i, column=1, sticky='e', padx=4)
                th.grid(row=i, column=2, sticky='e', padx=4)
                self.st[name] = (e, th)
                cells = [lab, e, th]
            if name == 'tag':
                self.tag_row = cells
        self.pairs_note = self.L(tk.Label(p, bg=PANEL, fg=MUTED, font=(FONT, 8), wraplength=int(330 * self.scale_ui),
                                          justify='left'), 'pairsNote')

        # готовые опыты
        p = self._panel(side, 'secPresets')
        keys = ['presetNone'] + [x[1] for x in PRESETS]
        self.preset_cb = ttk.Combobox(p, state='readonly', font=(FONT, 10), height=len(keys))
        self.preset_cb.pack(fill='x')
        self.loc_combos.append((self.preset_cb, keys))
        self.preset_cb.configure(values=[self.t(k) for k in keys])
        self.preset_cb.current(0)
        self.preset_cb.bind('<<ComboboxSelected>>', lambda e: self.apply_preset(self.preset_cb.current()))

        self.sliders = {}
        self.checks = {}
        self.combos = {}

        p = self._panel(side, 'secParticles')
        self._slider(p, 'N', 'N', 1, 500, 1, reinit=True, fmt='%d')
        self._slider(p, 'r', 'r', 1.5, 12, 0.5, reinit=True, fmt='%.1f')
        self._slider(p, 'u', 'u', 0.3, 5, 0.1, live=self.sim.set_speed, fmt='%.1f')
        self._check(p, 'tagged', 'tagged', self._on_tagged)
        self._check(p, 'diatomic', 'diatomic', self._on_diatomic)

        p = self._panel(side, 'secVessel')
        self._slider(p, 'W', 'Wv', 300, 1000, 10, fmt='%d', on_release=self._on_width)
        self._slider(p, 'frac', 'frac', 0.02, 0.98, 0.01, live=self._on_frac, reinit=lambda: self.sim.p['wall'], fmt='%.2f')
        self._combo(p, 'shape', 'shape', ['strip', 'corner'], ['shapeStrip', 'shapeCorner'], self._on_shape)
        self._combo(p, 'count', 'count', ['main', 'imp', 'all'], ['countMain', 'countImp', 'countAll'], self._on_count)

        p = self._panel(side, 'secWall')
        self._check(p, 'wall', 'wall', self._on_wall)
        self._slider(p, 'hole', 'hole', 0, 1, 0.01, live=lambda v: self.sim.p.__setitem__('hole', v), fmt='%.2f')

        p = self._panel(side, 'secImp')
        self._slider(p, 'impN', 'impN', 0, 100, 1, reinit=True, fmt='%d')
        self._slider(p, 'impR', 'impR', 2, 25, 0.5, reinit=True, fmt='%.1f')

        p = self._panel(side, 'secSim')
        self._slider(p, 'speed', 'speed', 0.25, 10, 0.25, live=self._on_speed, fmt='×%.2f')
        self._combo(p, 'init', 'init', ['uniform', 'outside', 'inside'],
                    ['initUniform', 'initOutside', 'initInside'], self._on_init)

    def _slider(self, parent, name, key, lo, hi, res, live=None, reinit=False, fmt='%s', on_release=None):
        row = tk.Frame(parent, bg=PANEL)
        row.pack(fill='x', pady=(4, 0))
        self.L(tk.Label(row, bg=PANEL, fg=INK, font=(FONT, 9)), key).pack(side='left')
        out = tk.Label(row, bg=PANEL, fg=ACCENT, font=('Consolas', 10, 'bold'))
        out.pack(side='right')
        sc = tk.Scale(parent, from_=lo, to=hi, resolution=res, orient='horizontal', showvalue=False,
                      bg=PANEL, highlightthickness=0, troughcolor='#e6ebf2', bd=0, sliderlength=18,
                      activebackground=ACCENT2)
        sc.pack(fill='x')
        info = dict(scale=sc, out=out, fmt=fmt, live=live, reinit=reinit, on_release=on_release)
        self.sliders[name] = info

        def on_move(val):
            v = float(val)
            out.configure(text=fmt % v)
            if self._syncing:
                return
            # tk.Scale вызывает command и после программной установки значения —
            # такие вызовы (значение уже совпадает с моделью) пропускаем
            cur = self.sim_speed if name == 'speed' else self.sim.p.get(name)
            if cur is not None and abs(float(cur) - v) < 1e-9:
                return
            if live:
                live(v)
            elif name in self.sim.p and not on_release:
                self.sim.p[name] = int(v) if fmt == '%d' else v
            self.preset_cb.current(0)

        def on_release_(e):
            v = float(sc.get())
            if on_release:
                on_release(v)
                return
            re = reinit() if callable(reinit) else reinit
            if re:
                self.sim.reset()
            self.refresh()
        sc.configure(command=on_move)
        sc.bind('<ButtonRelease-1>', on_release_)
        sc.bind('<KeyRelease>', on_release_)

    def _check(self, parent, name, key, cmd):
        v = tk.BooleanVar()
        cb = self.L(tk.Checkbutton(parent, variable=v, bg=PANEL, activebackground=PANEL, font=(FONT, 9),
                                   anchor='w', justify='left', wraplength=int(320 * self.scale_ui),
                                   command=lambda: cmd(v.get())), key)
        cb.pack(fill='x', pady=(4, 0))
        self.checks[name] = v

    def _combo(self, parent, name, key, values, keys, cmd):
        self.L(tk.Label(parent, bg=PANEL, fg=INK, font=(FONT, 9)), key).pack(anchor='w', pady=(6, 0))
        cb = ttk.Combobox(parent, state='readonly', font=(FONT, 10), values=[self.t(k) for k in keys])
        cb.pack(fill='x')
        cb.bind('<<ComboboxSelected>>', lambda e: (cmd(values[cb.current()]), self.preset_cb.current(0)))
        self.loc_combos.append((cb, keys))
        self.combos[name] = (cb, values)

    _syncing = False

    def sync_controls(self):
        self._syncing = True
        try:
            p = self.sim.p
            for name, info in self.sliders.items():
                v = self.sim_speed if name == 'speed' else p[name]
                info['scale'].set(v)
                info['out'].configure(text=info['fmt'] % v)
            self.checks['tagged'].set(self.view['tagged'])
            self.checks['wall'].set(p['wall'])
            self.checks['diatomic'].set(p['diatomic'])
            for name, (cb, values) in self.combos.items():
                cb.current(values.index(p[name]))
            for k, v in self.show_vars.items():
                v.set(self.view[k])
            self.sliders['hole']['scale'].configure(state='normal' if p['wall'] else 'disabled')
        finally:
            self._syncing = False

    # обработчики элементов управления
    def _on_tagged(self, v):
        self.view['tagged'] = v
        self.refresh()

    def _on_diatomic(self, v):
        self.sim.p['diatomic'] = v
        self.preset_cb.current(0)
        self.sim.reset()
        self.refresh()

    def _on_wall(self, v):
        self.sim.p['wall'] = v
        self.preset_cb.current(0)
        self.sim.reset()
        self.sync_controls()
        self.refresh()

    def _on_frac(self, v):
        self.sim.p['frac'] = v
        if not self.sim.p['wall']:
            self.sim.clear_stats()

    def _on_width(self, v):
        self.sim.set_width(v)
        self.sim.reset()
        self.sync_controls()
        self.refresh()

    def _on_shape(self, v):
        self.sim.p['shape'] = v
        if self.sim.p['wall']:
            self.sim.reset()
        else:
            self.sim.clear_stats()
        self.refresh()

    def _on_count(self, v):
        self.sim.p['count'] = v
        self.sim.clear_stats()
        self.refresh()

    def _on_init(self, v):
        self.sim.p['init'] = v
        self.sim.reset()
        self.refresh()

    def _on_speed(self, v):
        self.sim_speed = v

    def _toggle_curve(self, k):
        self.view[k] = self.show_vars[k].get()
        self.draw_legends()
        self.draw_all(force=True)

    def apply_preset(self, idx):
        if idx <= 0:
            return
        pid, _, params, curves, speed = PRESETS[idx - 1]
        self.sim.p.update(BASE)
        self.sim.p.update(params)
        self.view.update(tagged=True, binom=False, pois=False, gauss=False)
        self.view.update(curves)
        self.sim_speed = speed
        self.sim.reset()
        self.running = True
        self.sync_controls()
        self.update_play()
        self.refresh()

    def toggle_play(self):
        self.running = not self.running
        self.update_play()

    def _space(self, e):
        if self.screen == 'demo' and not isinstance(e.widget, (ttk.Combobox, tk.Button, tk.Checkbutton)):
            self.toggle_play()

    def update_play(self):
        self.play_btn.configure(text=self.t('pause') if self.running else self.t('play'))

    def restart(self):
        self.sim.reset()
        self.refresh()

    def clear_stats(self):
        self.sim.clear_stats()
        self.refresh()

    def refresh(self):
        self.sliders['hole']['scale'].configure(state='normal' if self.sim.p['wall'] else 'disabled')
        self.draw_legends()
        self.draw_all(force=True)

    # ---------------- легенды и статистика ----------------
    def _legend(self, cv, items):
        cv.delete('all')
        x = 4
        h = int(cv['height'])
        y = h / 2
        for kind, color, text in items:
            if kind == 'box':
                cv.create_rectangle(x, y - 5, x + 12, y + 5, fill=color, outline=charts.C['barEdge'])
            elif kind == 'band':
                cv.create_rectangle(x, y - 5, x + 12, y + 5, fill=charts.C['band'], outline=charts.C['binom'], dash=(2, 2))
            elif kind == 'dash':
                cv.create_line(x, y, x + 14, y, fill=color, width=2, dash=(4, 2))
            else:
                cv.create_line(x, y, x + 14, y, fill=color, width=3)
            t = cv.create_text(x + 18, y, text=text, anchor='w', fill=MUTED, font=(FONT, 9))
            x = cv.bbox(t)[2] + 14

    def draw_legends(self):
        C = charts.C
        items = [('box', C['bar'], self.t('legExp'))]
        if self.view['binom']:
            items.append(('line', C['binom'], self.t('legBinom')))
        if self.view['pois']:
            items.append(('dash', C['pois'], self.t('legPoisMirror') if self.sim.theory_p() > 0.5 else self.t('legPois')))
        if self.view['gauss']:
            items.append(('line', C['gauss'], self.t('legGauss')))
        self._legend(self.hist_leg, items)
        self._legend(self.series_leg, [('line', C['line'], 'n(t)'), ('band', None, self.t('legMean'))])

    @staticmethod
    def f(v, d):
        return '—' if v is None or not math.isfinite(v) else '%.*f' % (d, v)

    def update_stats(self):
        s = self.sim
        N, p, closed = s.counted_n(), s.theory_p(), s.is_closed()
        pairs = s.pairs_counted()
        S = s.samples
        mean = s.sum / S if S else float('nan')
        vr = max(0.0, s.sum2 / S - mean * mean) if S > 1 else float('nan')
        mT = s.n0 if closed else N * p
        vT = 0 if closed else (2 if pairs else 1) * N * p * (1 - p)
        f = self.f
        st = self.st
        st['n'][0].configure(text='%d / %d' % (s.count_inside(), N))
        st['samples'][0].configure(text=str(S))
        st['p'][1].configure(text=f(p, 4))
        st['p'][0].configure(text='')
        st['mean'][0].configure(text=f(mean, 3))
        st['mean'][1].configure(text=f(mT, 3))
        st['var'][0].configure(text=f(vr, 3))
        st['var'][1].configure(text=f(vT, 3))
        st['rel'][0].configure(text=f(math.sqrt(vr) / mean, 3) if S > 1 and mean > 0 else '—')
        st['rel'][1].configure(text=f(math.sqrt(vT) / mT, 3) if mT > 0 else '—')
        show_tag = self.view['tagged'] and s.tagged >= 0
        for i, w in enumerate(self.tag_row):
            if show_tag:
                w.grid()
            else:
                w.grid_remove()
        if show_tag:
            st['tag'][0].configure(text=f(s.tagged_in / S, 3) if S else '—')
            st['tag'][1].configure(text=f(s.p_for_radius(s.p['r']), 3))
        if pairs:
            self.pairs_note.pack(anchor='w', pady=(4, 0))
        else:
            self.pairs_note.pack_forget()

    def draw_charts(self):
        s = self.sim
        N, p, closed = s.counted_n(), s.theory_p(), s.is_closed()
        pairs = s.pairs_counted()
        charts.hist(self.hist_cv, dict(N=N, p=p, closed=closed, n0=s.n0, hist=s.hist, samples=s.samples,
                                       pairs=pairs, show=dict(binom=self.view['binom'], pois=self.view['pois'],
                                                              gauss=self.view['gauss']),
                                       xLabel=self.t('axisN'), yLabel=self.t('axisP'), empty=self.t('noData')))
        charts.series(self.series_cv, dict(series=s.series, N=N, p=p, closed=closed, n0=s.n0, pairs=pairs,
                                           xLabel=self.t('axisT'), yLabel=self.t('axisNt')))

    def draw_vessel(self):
        self.vessel.draw(self.view['tagged'], self.t('closedNote') if self.sim.is_closed() else '')

    def draw_all(self, force=False):
        if self.screen == 'demo':
            self.draw_vessel()
            self.draw_charts()
            self.update_stats()
        elif self.screen == 'menu':
            self.menu_view.draw(True)

    # ---------------- главный цикл ----------------
    def loop(self):
        now = time.perf_counter()
        dt = min(0.05, now - self.last)
        self.last = now
        self.frame_no += 1
        try:
            if self.screen == 'demo':
                if self.running:
                    self.sim.advance(self.sim_speed * dt * 30)
                if self.running or self.frame_no % 10 == 0:
                    self.draw_vessel()
                    if self.frame_no % 3 == 0:
                        self.draw_charts()
                    if self.frame_no % 6 == 0:
                        self.update_stats()
            elif self.screen == 'menu':
                self.menu_sim.advance(dt * 30)
                self.menu_view.draw(True)
        finally:
            spent = time.perf_counter() - now
            self.loop_id = self.after(max(1, int(16 - spent * 1000)), self.loop)

    def destroy(self):
        if getattr(self, 'loop_id', None):
            self.after_cancel(self.loop_id)
        super().destroy()


def main():
    try:
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass
    app = App()
    args = sys.argv[1:]
    if args and args[0] in ('--demo', '--theory', '--authors'):
        app.go(args[0][2:])
        if args[0] == '--demo' and len(args) > 1 and args[1] in PRESET_BY_ID:
            idx = [p[0] for p in PRESETS].index(args[1]) + 1
            app.preset_cb.current(idx)
            app.apply_preset(idx)
    app.mainloop()


if __name__ == '__main__':
    main()
