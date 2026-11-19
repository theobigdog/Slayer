"""Builds Slayer.exe: one file that runs on any Windows PC, no Python needed.

    pip install pyinstaller
    python tools/build_exe.py

The exe lands in dist/Slayer.exe (about 30 MB). It keeps its volume setting (and any crash_log.txt) in the
folder it's run from. assets/drawings/ (the originals) aren't needed inside it, only what the game uses.
"""
from pathlib import Path
import os
import struct
import subprocess
import sys

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame

ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / 'build'
PACKED = ['assets/music', 'assets/sounds', 'assets/fonts', 'assets/dragons']


def make_icon(path: Path):
    """Trogdor, glowing green on the dark screen, as a Windows .ico (a PNG wrapped in an icon header)."""
    size = 256
    icon = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.rect(icon, (5, 13, 7, 255), icon.get_rect(), border_radius=40)
    pygame.draw.rect(icon, (36, 130, 64, 255), icon.get_rect(), 6, border_radius=40)
    dragon = pygame.image.load(str(ROOT / 'assets' / 'dragons' / 'trogdor.png'))
    w, h = dragon.get_size()
    fit = (size - 30) / max(w, h)
    dragon = pygame.transform.smoothscale(dragon, (round(w * fit), round(h * fit)))
    dragon.fill((150, 255, 90, 255), special_flags=pygame.BLEND_RGBA_MULT)
    icon.blit(dragon, dragon.get_rect(center=(size // 2, size // 2)))
    png = BUILD / 'icon.png'
    pygame.image.save(icon, str(png))
    data = png.read_bytes()
    path.write_bytes(struct.pack('<HHH', 0, 1, 1) + struct.pack('<BBBBHHII', 0, 0, 0, 0, 1, 32, len(data), 22) + data)


def main():
    pygame.init()
    BUILD.mkdir(exist_ok=True)
    icon = BUILD / 'slayer.ico'
    make_icon(icon)
    sep = ';' if os.name == 'nt' else ':'
    command = [sys.executable, '-m', 'PyInstaller', '--noconfirm', '--onefile', '--windowed',
               '--name', 'Slayer', '--icon', str(icon), '--paths', str(ROOT / 'game'),
               '--workpath', str(BUILD), '--specpath', str(BUILD), '--distpath', str(ROOT / 'dist')]
    for folder in PACKED:
        command += ['--add-data', f'{ROOT / folder}{sep}{folder}']
    command.append(str(ROOT / 'main.py'))
    subprocess.run(command, check=True)
    exe = ROOT / 'dist' / ('Slayer.exe' if os.name == 'nt' else 'Slayer')
    print(f'\nDone: {exe}  ({exe.stat().st_size / 1e6:.0f} MB)')


if __name__ == '__main__':
    main()
