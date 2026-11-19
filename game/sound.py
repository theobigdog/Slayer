"""sound: plays the music and sound effects in the game window (the command prompt stays quiet).

The files are made by tools/make_sounds.py: songs in assets/music/, effects in assets/sounds/.
    play('battle')    loop a song (fades the old one out first; the same song again does nothing)
    sting('victory')  a one-off tune over the top (the loop pauses under it)
    effect('hit')     a sound effect
    volume / set_volume(0.5) / toggle()   remembered in settings.txt next to the game
If anything about sound fails (no speakers, a missing file), the game carries on in silence.
"""
from pathlib import Path

import pygame

ROOT = Path(__file__).resolve().parent.parent
MUSIC = ROOT / 'assets' / 'music'
SOUNDS = ROOT / 'assets' / 'sounds'
SETTINGS = ROOT / 'settings.txt'
DEFAULT_VOLUME = 0.35
EFFECT_BOOST = {'type': 0.35, 'select': 0.8}  # the typewriter's tick stays very quiet

_current = None
_cache = {}


def _load_volume() -> float:
    try:
        return min(1.0, max(0.0, float(SETTINGS.read_text().strip())))
    except Exception:
        return DEFAULT_VOLUME


volume = _load_volume()
_unmuted = volume or DEFAULT_VOLUME


def _ready() -> bool:
    try:
        if not pygame.mixer.get_init():
            pygame.mixer.init(22050, -16, 1, 512)
            pygame.mixer.set_num_channels(16)
        return True
    except pygame.error:
        return False


def play(name: str):
    global _current
    if name == _current or not _ready():
        return
    _current = name
    try:
        pygame.mixer.music.fadeout(300)
        pygame.mixer.music.load(str(MUSIC / f'{name}.wav'))
        pygame.mixer.music.set_volume(volume * 0.8)
        pygame.mixer.music.play(-1, fade_ms=600)
    except (pygame.error, FileNotFoundError):
        _current = None


def _sound(path: Path):
    if path not in _cache:
        _cache[path] = pygame.mixer.Sound(str(path))
    return _cache[path]


def sting(name: str):
    global _current
    if not volume or not _ready():
        return
    try:
        pygame.mixer.music.fadeout(200)
        _current = None
        s = _sound(MUSIC / f'{name}.wav')
        s.set_volume(volume)
        s.play()
    except (pygame.error, FileNotFoundError):
        pass


def effect(name: str):
    if not volume or not _ready():
        return
    try:
        s = _sound(SOUNDS / f'{name}.wav')
        s.set_volume(min(1.0, volume * EFFECT_BOOST.get(name, 1.0)))
        s.play()
    except (pygame.error, FileNotFoundError):
        pass


def set_volume(level: float):
    global volume, _unmuted, _current
    volume = min(1.0, max(0.0, level))
    if volume:
        _unmuted = volume
    if _ready():
        pygame.mixer.music.set_volume(volume * 0.8)
    try:
        SETTINGS.write_text(f'{volume:.2f}')
    except Exception:
        pass


def toggle():
    set_volume(0.0 if volume else _unmuted)
