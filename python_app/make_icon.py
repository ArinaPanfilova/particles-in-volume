"""Рисует значок приложения icon.ico: сосуд с закрашенной областью и молекулами."""
from pathlib import Path

from PIL import Image, ImageDraw

S = 256
img = Image.new('RGBA', (S, S), (0, 0, 0, 0))
d = ImageDraw.Draw(img)
d.rounded_rectangle([8, 28, S - 8, S - 28], radius=18, fill=(251, 251, 247), outline=(43, 43, 43), width=10)
d.rectangle([13, 33, 110, 140], fill=(207, 230, 189))
d.line([110, 33, 110, 140], fill=(80, 130, 60), width=5)
d.line([13, 140, 110, 140], fill=(80, 130, 60), width=5)
for x, y, inside in ((45, 70, 1), (80, 105, 1), (55, 118, 1), (160, 70, 0), (200, 120, 0),
                     (150, 180, 0), (70, 185, 0), (210, 190, 0)):
    r = 13
    col = (29, 53, 87)
    d.ellipse([x - r, y - r, x + r, y + r], fill=col if inside else (255, 255, 255), outline=col, width=5)
out = Path(__file__).with_name('icon.ico')
img.save(out, sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
print('OK', out)
