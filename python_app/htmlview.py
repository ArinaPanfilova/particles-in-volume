# -*- coding: utf-8 -*-
"""Отображение простой HTML-разметки (теория, авторы) в виджете tk.Text."""
import re
import tkinter as tk
import tkinter.font as tkfont
from html.parser import HTMLParser

FONT = 'Segoe UI'
INK, MUTED, ACCENT, LINE = '#1f2937', '#6b7280', '#1d3557', '#e2e4dc'


BG = '#f4f5f0'
# дробь из i18n.F(); «√» прямо перед ней — корень над всей дробью
FRAC = re.compile(r'(√?)<frac>(.*?)\x01(.*?)</frac>', re.S)


class _Runs(HTMLParser):
    """Числитель или знаменатель → куски текста [(текст, '' | 'sub' | 'sup')]."""

    def __init__(self, html):
        super().__init__(convert_charrefs=True)
        self.runs, self.mode = [], ''
        self.feed(html)
        self.close()

    def handle_starttag(self, tag, attrs):
        if tag in ('sub', 'sup'):
            self.mode = tag

    def handle_endtag(self, tag):
        if tag in ('sub', 'sup'):
            self.mode = ''

    def handle_data(self, data):
        self.runs.append((data.replace('\xa0', ' '), self.mode))


def frac_canvas(master, num, den, root, family, size, wheel):
    """Дробь «этажом» на маленьком холсте: числитель над чертой, знаменатель под ней."""
    fonts = {'': (family, size), 'sub': (family, max(7, round(size * 0.7)))}
    fonts['sup'] = fonts['sub']
    big, small = tkfont.Font(master, font=fonts['']), tkfont.Font(master, font=fonts['sub'])
    asc, lh = big.metrics('ascent'), big.metrics('linespace')
    shift = {'': 0, 'sub': round(asc * 0.25), 'sup': -round(asc * 0.45)}
    parts = [_Runs(num).runs, _Runs(den).runs]

    def width(runs):
        return sum((small if m else big).measure(t) for t, m in runs)
    # обе части одной высоты — тогда черта дроби ровно посередине строки
    up = round(lh * 0.3) if any(m == 'sup' for r in parts for _, m in r) else 0
    down = round(lh * 0.2) if any(m == 'sub' for r in parts for _, m in r) else 0
    hp = up + lh + down
    pad, gap = 4, 2
    w = max(width(r) for r in parts) + 2 * pad
    rw = round(lh * 0.6) if root else 0     # место под знак корня
    top = 3 if root else 0                  # зазор под чертой корня
    H = top + 2 * hp + 2 * gap + 1
    cv = tk.Canvas(master, width=rw + w, height=H, bg=BG, highlightthickness=0, bd=0)
    for k, runs in enumerate(parts):
        x = rw + (w - width(runs)) / 2
        base = top + k * (hp + 2 * gap + 1) + up + asc
        for t, m in runs:
            f = small if m else big
            cv.create_text(x, base + shift[m] - f.metrics('ascent'), text=t, anchor='nw', font=fonts[m],
                           fill=INK)
            x += f.measure(t)
    yb = top + hp + gap
    cv.create_line(rw + 1, yb, rw + w - 1, yb, fill=INK, width=1)
    if root:
        cv.create_line(1, H * 0.62, rw * 0.3, H * 0.52, rw * 0.6, H - 1, rw - 1, 1, rw + w, 1,
                       fill=INK, width=1.3)
    for ev in ('<MouseWheel>', '<Button-4>', '<Button-5>'):
        cv.bind(ev, wheel)
    return cv


class DocView(tk.Frame):
    def __init__(self, master, **kw):
        super().__init__(master, bg=BG, **kw)
        self.text = tk.Text(self, wrap='word', bd=0, highlightthickness=0, padx=40, pady=24,
                            bg=BG, fg=INK, font=(FONT, 12), cursor='arrow',
                            spacing1=2, spacing3=2)
        sb = tk.Scrollbar(self, command=self.text.yview)
        self.text.configure(yscrollcommand=sb.set)
        sb.pack(side='right', fill='y')
        self.text.pack(side='left', fill='both', expand=True)
        t = self.text
        t.tag_configure('h2', font=(FONT, 18, 'bold'), foreground=ACCENT, spacing1=18, spacing3=8)
        t.tag_configure('h3', font=(FONT, 14, 'bold'), foreground=ACCENT, spacing1=12, spacing3=4)
        t.tag_configure('b', font=(FONT, 12, 'bold'))
        t.tag_configure('i', font=(FONT, 12, 'italic'))
        t.tag_configure('bi', font=(FONT, 12, 'bold italic'))
        t.tag_configure('sub', offset=-4, font=(FONT, 9))
        t.tag_configure('sup', offset=6, font=(FONT, 9))
        t.tag_configure('eq', font=('Cambria', 14), lmargin1=40, lmargin2=40,
                        spacing1=6, spacing3=6)
        # индексы и степени внутри формул (настроены после 'eq', чтобы перебить его шрифт)
        t.tag_configure('eqsub', offset=-5, font=('Cambria', 10))
        t.tag_configure('eqsup', offset=7, font=('Cambria', 10))
        t.tag_configure('muted', foreground=MUTED)
        t.tag_configure('link', foreground='#2f5d8a', underline=True)
        t.tag_configure('th', font=(FONT, 12, 'bold'), background='#eef3f8')
        t.tag_configure('cell0', font=(FONT, 12, 'bold'), foreground=ACCENT)
        t.tag_configure('cell2', foreground='#2f5d8a', lmargin1=24, lmargin2=24)
        t.tag_configure('cell1', lmargin1=24, lmargin2=24)
        t.tag_bind('link', '<Enter>', lambda e: t.configure(cursor='hand2'))
        t.tag_bind('link', '<Leave>', lambda e: t.configure(cursor='arrow'))
        self.text.bind('<MouseWheel>', self._wheel)
        self.windows = []    # холсты с дробями внутри текста

    def _wheel(self, e):
        if e.num in (4, 5):
            self.text.yview_scroll(-3 if e.num == 4 else 3, 'units')
        else:
            self.text.yview_scroll(int(-e.delta / 40), 'units')
        return 'break'

    def set_html(self, html):
        fracs = []

        def mark(m):
            fracs.append((m.group(2), m.group(3), bool(m.group(1))))
            return '<img k="%d">' % (len(fracs) - 1)
        html = FRAC.sub(mark, html)
        t = self.text
        t.configure(state='normal')
        t.delete('1.0', 'end')
        for w in self.windows:
            w.destroy()
        r = _Renderer(t, fracs, self._wheel)
        r.feed(html)
        self.windows = r.windows
        t.configure(state='disabled')
        t.yview_moveto(0)


class _Renderer(HTMLParser):
    BLOCK = {'p', 'h2', 'h3', 'div', 'tr', 'nav', 'table'}

    def __init__(self, text, fracs=(), wheel=None):
        super().__init__(convert_charrefs=True)
        self.t = text
        self.fracs, self.wheel, self.windows = fracs, wheel, []
        self.stack = []      # открытые теги с атрибутами
        self.cell = -1
        self.link_no = 0

    def _nl(self, n=1):
        """Перейти на новую строку (не плодя пустых строк)."""
        idx = self.t.index('end-1c')
        if idx == '1.0':
            return
        tail = self.t.get('end-%dc' % (n + 1), 'end-1c')
        need = n - (len(tail) - len(tail.rstrip('\n')))
        if need > 0:
            self.t.insert('end', '\n' * need)

    def _cls(self, attrs):
        return dict(attrs).get('class', '')

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        cls = a.get('class', '')
        if tag == 'img':     # дробь; в формулах — шрифтом формул
            num, den, root = self.fracs[int(a['k'])]
            tags = self._tags()
            eq = 'eq' in tags
            cv = frac_canvas(self.t, num, den, root, 'Cambria' if eq else FONT, 14 if eq else 12, self.wheel)
            self.t.window_create('end', window=cv, align='center', padx=1)
            for tg in tags:  # отступ строки формулы
                self.t.tag_add(tg, 'end-2c')
            self.windows.append(cv)
            return
        if tag == 'br':
            self.t.insert('end', '\n', self._tags())
            return
        if tag in self.BLOCK:
            self._nl(2 if tag in ('h2', 'h3', 'p', 'nav') or cls == 'eq' else 1)
        if tag == 'h2' and a.get('id'):
            self.t.mark_set(a['id'], 'end-1c')
            self.t.mark_gravity(a['id'], 'left')
        if tag == 'tr':
            self.cell = -1
        if tag in ('td', 'th'):
            self.cell += 1
            if self.cell > 0:
                self.t.insert('end', '\n')
        if tag == 'a':
            self.link_no += 1
            name = 'lnk%d' % self.link_no
            target = a.get('href', '').lstrip('#')
            self.t.tag_bind(name, '<Button-1>', lambda e, m=target: self._jump(m))
            a['_tag'] = name
            self.t.insert('end', '  ')
        self.stack.append((tag, a))

    def _jump(self, mark):
        try:
            self.t.yview(mark)
        except tk.TclError:
            pass

    def handle_endtag(self, tag):
        for k in range(len(self.stack) - 1, -1, -1):
            if self.stack[k][0] == tag:
                del self.stack[k:]
                break
        if tag in self.BLOCK:
            self._nl(1)
        if tag == 'tr':
            self.t.insert('end', '\n')

    def _tags(self):
        names = [s[0] for s in self.stack]
        classes = [s[1].get('class', '') for s in self.stack]
        tags = []
        b = 'b' in names or 'th' in names
        i = 'i' in names
        if b and i:
            tags.append('bi')
        elif b:
            tags.append('b')
        elif i:
            tags.append('i')
        for n in ('h2', 'h3', 'sub', 'sup'):
            if n in names:
                tags.append(n)
        if 'eq' in classes:
            tags.append('eq')
            tags += ['eq' + n for n in ('sub', 'sup') if n in names]
        if 'muted' in classes:
            tags.append('muted')
        if 'td' in names or 'th' in names:
            tags.append('th' if 'th' in names else 'cell%d' % min(self.cell, 2))
        for tag, a in self.stack:
            if tag == 'a':
                tags += ['link', a['_tag']]
        return tuple(tags)

    def handle_data(self, data):
        if not data:
            return
        self.t.insert('end', data.replace('\xa0', ' '), self._tags())
