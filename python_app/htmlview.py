# -*- coding: utf-8 -*-
"""Отображение простой HTML-разметки (теория, авторы) в виджете tk.Text."""
import re
import tkinter as tk
from html import unescape
from html.parser import HTMLParser

FONT = 'Segoe UI'
INK, MUTED, ACCENT, LINE = '#1f2937', '#6b7280', '#1d3557', '#e2e4dc'


def _frac(m):
    """<frac>num\\x01den</frac> → num/den, со скобками при необходимости."""
    num, den = m.group(1), m.group(2)

    def wrap(t):
        plain = re.sub(r'<[^>]+>', '', unescape(t))
        return '(' + t + ')' if re.search(r'[ +−\-·]', plain) else t
    return wrap(num) + '/' + wrap(den)


class DocView(tk.Frame):
    def __init__(self, master, **kw):
        super().__init__(master, bg='#f4f5f0', **kw)
        self.text = tk.Text(self, wrap='word', bd=0, highlightthickness=0, padx=40, pady=24,
                            bg='#f4f5f0', fg=INK, font=(FONT, 12), cursor='arrow',
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
        t.tag_configure('muted', foreground=MUTED)
        t.tag_configure('link', foreground='#2f5d8a', underline=True)
        t.tag_configure('th', font=(FONT, 12, 'bold'), background='#eef3f8')
        t.tag_configure('cell0', font=(FONT, 12, 'bold'), foreground=ACCENT)
        t.tag_configure('cell2', foreground='#2f5d8a', lmargin1=24, lmargin2=24)
        t.tag_configure('cell1', lmargin1=24, lmargin2=24)
        t.tag_configure('avatar', font=(FONT, 16, 'bold'), foreground='#ffffff', background=ACCENT)
        t.tag_configure('card', lmargin1=10, lmargin2=60, spacing1=10, spacing3=6)
        t.tag_bind('link', '<Enter>', lambda e: t.configure(cursor='hand2'))
        t.tag_bind('link', '<Leave>', lambda e: t.configure(cursor='arrow'))
        self.text.bind('<MouseWheel>', lambda e: self.text.yview_scroll(int(-e.delta / 40), 'units'))

    def set_html(self, html):
        html = re.sub(r'<frac>(.*?)\x01(.*?)</frac>', _frac, html, flags=re.S)
        t = self.text
        t.configure(state='normal')
        t.delete('1.0', 'end')
        _Renderer(t).feed(html)
        t.configure(state='disabled')
        t.yview_moveto(0)


class _Renderer(HTMLParser):
    BLOCK = {'p', 'h2', 'h3', 'div', 'tr', 'nav', 'table'}

    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.t = text
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
        if tag == 'br':
            self.t.insert('end', '\n', self._tags())
            return
        if tag in self.BLOCK:
            self._nl(2 if tag in ('h2', 'h3', 'p', 'nav') or cls in ('eq', 'author-card') else 1)
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
        if 'muted' in classes:
            tags.append('muted')
        if 'avatar' in classes:
            tags.append('avatar')
        if 'author-card' in classes:
            tags.append('card')
        if 'td' in names or 'th' in names:
            tags.append('th' if 'th' in names else 'cell%d' % min(self.cell, 2))
        for tag, a in self.stack:
            if tag == 'a':
                tags += ['link', a['_tag']]
        return tuple(tags)

    def handle_data(self, data):
        if not data:
            return
        classes = [s[1].get('class', '') for s in self.stack]
        if 'avatar' in classes:
            data = ' ' + data.strip() + ' '
            self.t.insert('end', data, self._tags())
            self.t.insert('end', '   ')
            return
        self.t.insert('end', data.replace('\xa0', ' '), self._tags())
