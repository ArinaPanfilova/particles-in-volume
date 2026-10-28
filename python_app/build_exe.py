"""Собирает приложение для текущей ОС (папка dist/).

Windows: ParticlesInVolume.exe, Linux: ParticlesInVolume (один файл),
macOS: ParticlesInVolume.app. Собрать версию для другой ОС отсюда нельзя:
это делает GitHub Actions (.github/workflows/build.yml).

Запуск: python build_exe.py
Нужны: Python 3.9+, numpy, pillow, pyinstaller (pip install -r requirements.txt).
"""
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
subprocess.check_call([sys.executable, str(ROOT / 'make_icon.py')])
# на macOS onefile + windowed не поддерживается, там собираем .app
mode = '--onedir' if sys.platform == 'darwin' else '--onefile'
subprocess.check_call([
    sys.executable, '-m', 'PyInstaller', '--noconfirm', '--clean', mode, '--windowed',
    '--name', 'ParticlesInVolume',
    '--icon', str(ROOT / 'icon.ico'),
    '--add-data', '%s%s.' % (ROOT / 'icon.ico', os.pathsep),
    '--add-data', '%s%sassets' % (ROOT / 'assets', os.pathsep),  # фото авторов и эмблемы
    '--distpath', str(ROOT / 'dist'), '--workpath', str(ROOT / 'build'), '--specpath', str(ROOT / 'build'),
    str(ROOT / 'app.py'),
])
print('OK:', ROOT / 'dist')
