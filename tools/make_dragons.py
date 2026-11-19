"""Turns Ted's dragon drawings into the glowing line art the game window shows.

    python tools/make_dragons.py        (needs numpy: pip install numpy)

Put a drawing in assets/drawings/ named trogdor.png, skippy.png or ancient.png (a .jpg works too). Any dark pen or
pencil on light paper works; light blue notebook lines are ignored. It finds the dark lines, crops to them, turns the
dragon to face left (toward the hero) and saves assets/dragons/<name>.png. The game tints it the dragon's color.

FACING says which way each drawing faces. ERASE blanks out parts of a drawing (like a title written beside it), as
(left, top, right, bottom) boxes in the drawing's own pixels.
"""
from pathlib import Path
import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import numpy as np
import pygame

ROOT = Path(__file__).resolve().parent.parent
DRAWINGS = ROOT / 'assets' / 'drawings'
OUT = ROOT / 'assets' / 'dragons'
HEIGHT = 540            # saved twice the size it's shown, so it stays sharp
FACING = {'trogdor': 'right', 'skippy': 'left', 'ancient': 'left'}
ERASE = {}


def ink(path: Path, erase) -> np.ndarray:
    """How strongly each pixel is a pen line, 0 to 1."""
    rgb = pygame.surfarray.array3d(pygame.image.load(str(path))).astype(float)  # (x, y, 3)
    lum = rgb.mean(axis=2)
    paper = np.percentile(lum, 90)                     # the paper's brightness, whatever the photo's lighting
    blueish = rgb[..., 2] - rgb[..., 0]                # notebook lines are much bluer than pencil
    strength = np.clip((paper - lum - 45) / 70, 0, 1)
    strength[blueish > 35] = 0
    for left, top, right, bottom in erase:
        strength[left:right, top:bottom] = 0
    return strength


def convert(name: str, path: Path):
    a = ink(path, ERASE.get(name, []))
    xs, ys = np.nonzero(a > 0.3)
    if not len(xs):
        print(f'  {path.name}: found no lines!')
        return
    pad = 4
    a = a[max(0, xs.min() - pad):xs.max() + pad, max(0, ys.min() - pad):ys.max() + pad]
    if FACING.get(name, 'right') == 'right':
        a = a[::-1, :]
    surf = pygame.Surface(a.shape, pygame.SRCALPHA)
    surf.fill((255, 255, 255, 255))
    pygame.surfarray.pixels_alpha(surf)[:] = (a * 255).astype(np.uint8)
    w, h = surf.get_size()
    surf = pygame.transform.smoothscale(surf, (round(w * HEIGHT / h), HEIGHT))
    OUT.mkdir(parents=True, exist_ok=True)
    pygame.image.save(surf, str(OUT / f'{name}.png'))
    print(f'  {path.name} -> assets/dragons/{name}.png ({surf.get_width()}x{HEIGHT})')


def main():
    pygame.init()
    for path in sorted(DRAWINGS.iterdir()):
        if path.suffix.lower() in ('.png', '.jpg', '.jpeg'):
            convert(path.stem.lower(), path)


if __name__ == '__main__':
    main()
