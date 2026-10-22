"""Собирает приложение в один исполняемый файл ParticlesInVolume.exe (папка dist/).

Запуск: python build_exe.py
Нужны: Python 3.9+, numpy, pillow, pyinstaller (pip install numpy pillow pyinstaller).
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
subprocess.check_call([sys.executable, str(ROOT / 'make_icon.py')])
subprocess.check_call([
    sys.executable, '-m', 'PyInstaller', '--noconfirm', '--clean', '--onefile', '--windowed',
    '--name', 'ParticlesInVolume',
    '--icon', str(ROOT / 'icon.ico'),
    '--add-data', '%s;.' % (ROOT / 'icon.ico'),
    '--distpath', str(ROOT / 'dist'), '--workpath', str(ROOT / 'build'), '--specpath', str(ROOT / 'build'),
    str(ROOT / 'app.py'),
])
print('OK:', ROOT / 'dist' / 'ParticlesInVolume.exe')
