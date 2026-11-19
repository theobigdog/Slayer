"""Makes Slayer Classic's music and sound effects: 8-bit, old-computer style, all original.

    python tools/make_sounds.py        (needs numpy: pip install numpy)

Writes assets/music/*.wav and assets/sounds/*.wav. Players don't need numpy: the .wav files are in the repo.

How a song is written: each part is a string of steps, one per 16th note, separated by spaces.
    C4  a note (C, C#, Db ... B, then the octave)        .  keep holding the note before
    -   silence                                           |  ignored (just to mark bars)
Drum parts use K (kick), S (snare), H (hi-hat), - (nothing).
Each part has an instrument: 'pulse' (the classic beepy lead; duty 0.125 / 0.25 / 0.5 changes its color),
'triangle' (soft bass), or 'drums'.
"""
import os
import wave

import numpy as np

RATE = 22050
HERE = os.path.dirname(os.path.abspath(__file__))
MUSIC = os.path.join(HERE, '..', 'assets', 'music')
SOUNDS = os.path.join(HERE, '..', 'assets', 'sounds')
NOTES = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
rng = np.random.default_rng(1982)


def freq(name: str) -> float:
    pitch = NOTES[name[0]]
    rest = name[1:]
    while rest and rest[0] in '#b':
        pitch += 1 if rest[0] == '#' else -1
        rest = rest[1:]
    midi = 12 * (int(rest) + 1) + pitch
    return 440.0 * 2 ** ((midi - 69) / 12)


def t(seconds: float):
    return np.arange(int(RATE * seconds)) / RATE


# ---------- the instruments --------------------------------------------------------------------------------------

def pulse(f, seconds, duty=0.5, vibrato=0.0, wobble=0.0):
    x = t(seconds)
    bend = 1 + vibrato * np.sin(2 * np.pi * 5.5 * x) + wobble * np.sin(2 * np.pi * 0.7 * x)  # wobble: drunk
    phase = np.cumsum(f * bend) / RATE
    return np.where((phase % 1) < duty, 1.0, -1.0)

def triangle(f, seconds, **_):
    phase = (t(seconds) * f) % 1
    return 4 * np.abs(phase - 0.5) - 1  # (stepped a little, like the old chips)

def noise(seconds):
    n = int(RATE * seconds)
    hold = 2  # each random value held for a couple of samples: crunchier, more 8-bit
    return np.repeat(rng.uniform(-1, 1, n // hold + 1), hold)[:n]

def envelope(n, attack=0.004, decay=0.08, sustain=0.6, release=0.03):
    env = np.full(n, sustain)
    a, d, r = int(attack * RATE), int(decay * RATE), int(release * RATE)
    a, d, r = min(a, n), min(d, max(0, n - a)), min(r, n)
    env[:a] = np.linspace(0, 1, a, endpoint=False)
    env[a:a + d] = np.linspace(1, sustain, d, endpoint=False)
    if r:
        env[n - r:] *= np.linspace(1, 0, r)
    return env

def drum(kind, seconds):
    x = t(min(seconds, 0.3))
    if kind == 'K':
        sweep = 150 * np.exp(-x * 25) + 45
        out = np.sin(2 * np.pi * np.cumsum(sweep) / RATE) * np.exp(-x * 18)
    elif kind == 'S':
        out = noise(len(x) / RATE) * np.exp(-x * 22) * 0.8
    else:  # H
        n = noise(len(x) / RATE)
        out = np.diff(n, prepend=0) * np.exp(-x * 70) * 0.35
    full = np.zeros(int(RATE * seconds))
    full[:len(out)] = out[:len(full)]
    return full


# ---------- songs -------------------------------------------------------------------------------------------------

def render(song: dict) -> np.ndarray:
    step = 60 / song['bpm'] / 4
    mix = None
    for part in song['parts']:
        kind, pattern, volume = part[0], part[1], part[2]
        options = part[3] if len(part) > 3 else {}
        steps = [s for s in pattern.split() if s != '|']
        out = np.zeros(int(RATE * step * len(steps)) + RATE)
        i = 0
        while i < len(steps):
            token = steps[i]
            length = 1
            while i + length < len(steps) and steps[i + length] == '.':
                length += 1
            start = int(RATE * step * i)
            if token not in ('-', '.'):
                seconds = step * length
                if kind == 'drums':
                    sound = drum(token, seconds)
                else:
                    wave_fn = pulse if kind == 'pulse' else triangle
                    sound = wave_fn(freq(token), seconds, **options)
                    sound = sound * envelope(len(sound), **song.get('env', {}))
                out[start:start + len(sound)] += sound * volume
            i += length
        out = out[:int(RATE * step * len(steps))]
        mix = out if mix is None else mix[:len(out)] + out[:len(mix)]
    return mix


def bars(*chunks, times=1):
    return ' | '.join(chunks * times)


SONGS = {
    # The title: a proud little march in A minor that thinks it's more heroic than it is.
    'title': dict(bpm=132, parts=[
        ('pulse', bars('A4 . . E4 A4 . C5 . B4 . A4 . G4 . E4 .', 'F4 . . A4 C5 . F5 . E5 . D5 . C5 . B4 .',
                       'A4 . . E4 A4 . C5 . E5 . . D5 C5 . B4 .', 'A4 . E4 . A4 . . . - - A5 . A5 . - -'), 0.22, {'duty': 0.25}),
        ('pulse', bars('E4 . - - E4 . - - E4 . - - E4 . - -', 'C4 . - - C4 . - - C4 . - - D4 . - -',
                       'E4 . - - E4 . - - G4 . - - G4 . - -', 'E4 . - - E4 . - - - - E5 . E5 . - -'), 0.12, {'duty': 0.125}),
        ('triangle', bars('A2 . A3 . A2 . A3 . A2 . A3 . E2 . E3 .', 'F2 . F3 . F2 . F3 . G2 . G3 . G2 . B2 .',
                          'A2 . A3 . A2 . A3 . C3 . C3 . E2 . E3 .', 'A2 . E2 . A2 . . . - - A2 . A2 . - -'), 0.5),
        ('drums', bars('K - H - S - H - K - K - S - H H', 'K - H - S - H - K - K - S - H H',
                       'K - H - S - H - K - K - S - H H', 'K - S - K - - - - - S S S S S S'), 0.6),
    ]),
    # Down the tunnel: slow, drippy, minor. Something is in here with you.
    'tunnel': dict(bpm=76, env={'decay': 0.3, 'sustain': 0.25, 'release': 0.2}, parts=[
        ('pulse', bars('E4 - G4 - B4 - G4 - E4 - G4 - B4 - C5 -', 'D4 - F4 - A4 - F4 - D4 - F4 - A4 - B4 -',
                       'C4 - E4 - G4 - E4 - C4 - E4 - G4 - A4 -', 'B3 - D#4 - F#4 - B4 - F#4 - D#4 - B3 - - -'), 0.14, {'duty': 0.125}),
        ('triangle', bars('E2 . . . . . . . . . . . . . . .', 'D2 . . . . . . . . . . . . . . .',
                          'C2 . . . . . . . . . . . . . . .', 'B1 . . . . . . . . . . . . . . .'), 0.55),
        ('pulse', bars('- - - - - - - - - - - - - - B5 -', '- - - - - - - - - - - - - - - -',
                       '- - - - - - - - - - - - G5 - - -', '- - - - - - - - - - - - - - - -'), 0.05, {'duty': 0.5, 'vibrato': 0.01}),
    ]),
    # Trogdor's cave: an oom-pah waltz that's had a few. Everything wobbles.
    'drunk': dict(bpm=150, env={'decay': 0.1, 'sustain': 0.5}, parts=[
        ('pulse', bars('G4 . . . . . B4 . D5 . . . E5 . D5 . B4 . ', 'A4 . . . . . C5 . E5 . . . D5 . C5 . A4 . ',
                       'G4 . . . B4 . D5 . G5 . . . F#5 . E5 . D5 . ', 'C5 . . . A4 . F#4 . . . . . G4 . . . . . '),
         0.2, {'duty': 0.25, 'wobble': 0.018}),
        ('triangle', bars('G2 . - - D3 - B2 - - - D3 - G2 . - - D3 - ', 'D2 . - - A2 - F#2 - - - A2 - D2 . - - A2 - ',
                          'G2 . - - D3 - B2 - - - D3 - E2 . - - B2 - ', 'C3 . - - A2 - D2 . - - F#2 - G2 . - - - - '), 0.5, {}),
        ('drums', bars('K - - - H - - - H - - - K - - - H - ', 'K - - - H - - - H - - - K - - - H - ',
                       'K - - - H - - - H - - - K - - - H - ', 'K - - - H - - - H - - - K - S - S S'), 0.5),
    ]),
    # Skippy's cave: a kid playing with bones. Bouncy, sneaky, a little nuts.
    'skippy': dict(bpm=120, env={'decay': 0.05, 'sustain': 0.3}, parts=[
        ('pulse', bars('D5 - D5 F5 - A5 - G5 F5 - E5 - D5 - C#5 -', 'D5 - A4 - D5 - F5 - E5 - C#5 - A4 - - -',
                       'Bb4 - Bb4 D5 - F5 - E5 D5 - C5 - Bb4 - A4 -', 'G4 - Bb4 - D5 - C#5 - D5 - - - D6 - - -'), 0.18, {'duty': 0.125}),
        ('triangle', bars('D2 - D3 - D2 - D3 - D2 - D3 - A2 - C#3 -', 'D2 - D3 - D2 - D3 - A1 - A2 - A1 - A2 -',
                          'Bb1 - Bb2 - Bb1 - Bb2 - F2 - F3 - F2 - F3 -', 'G2 - G3 - A2 - A3 - D2 - - - D2 - - -'), 0.5),
        ('drums', bars('K - H H S - H - K K H - S - H H', 'K - H H S - H - K K H - S - H H',
                       'K - H H S - H - K K H - S - H H', 'K - H H S - H - K - S S S - - -'), 0.5),
    ]),
    # The Ancient's cave: old, huge, slow. The floor shakes.
    'ancient': dict(bpm=64, env={'attack': 0.05, 'decay': 0.4, 'sustain': 0.5, 'release': 0.3}, parts=[
        ('triangle', bars('C2 . . . . . . . Db2 . . . . . . .', 'C2 . . . . . . . G1 . . . . . . .'), 0.7),
        ('pulse', bars('- - - - C4 . . . - - - - Db4 . . .', '- - - - Eb4 . . . D4 . . . B3 . . .'), 0.1, {'duty': 0.5, 'vibrato': 0.006}),
        ('pulse', bars('G3 . . . . . . . Ab3 . . . . . . .', 'G3 . . . . . . . F3 . . . . . . .'), 0.07, {'duty': 0.125}),
        ('drums', bars('K - - - - - - - K - - - - - - -', 'K - - - - - - - K - - - S - - -'), 0.8),
    ]),
    # Every fight: fast, driving, minor. (The Ancient gets 'inferno' instead.)
    'battle': dict(bpm=168, env={'decay': 0.06, 'sustain': 0.55}, parts=[
        ('pulse', bars('E5 . E5 . D5 . E5 . G5 . E5 . D5 . B4 .', 'C5 . C5 . B4 . C5 . E5 . D5 . C5 . A4 .',
                       'E5 . E5 . D5 . E5 . G5 . A5 . B5 . G5 .', 'F#5 . . . D#5 . . . B4 . . . B5 . . .'), 0.18, {'duty': 0.25}),
        ('pulse', bars('B4 - B4 - A4 - B4 - D5 - B4 - A4 - G4 -', 'A4 - A4 - G4 - A4 - C5 - B4 - A4 - E4 -',
                       'B4 - B4 - A4 - B4 - D5 - E5 - F#5 - D5 -', 'D#5 - - - B4 - - - F#4 - - - D#5 - - -'), 0.08, {'duty': 0.125}),
        ('triangle', bars('E2 E3 E2 E3 E2 E3 E2 E3 E2 E3 E2 E3 E2 E3 D3 E3', 'A2 A3 A2 A3 A2 A3 A2 A3 A2 A3 A2 A3 C3 B2 A2 G2',
                          'E2 E3 E2 E3 E2 E3 E2 E3 G2 G3 A2 A3 B2 B3 G2 G3', 'B1 B2 B1 B2 B1 B2 B1 B2 B1 B2 B1 B2 B1 B2 D#3 F#3'), 0.5),
        ('drums', bars('K - H - S - H K K - H - S - H H', 'K - H - S - H K K - H - S - H H',
                       'K - H - S - H K K - H - S - H H', 'K - S - K - S - K S K S S S S S'), 0.55),
    ]),
    # The Ancient's fight: the battle's big, mean, slower cousin.
    'inferno': dict(bpm=140, env={'decay': 0.08, 'sustain': 0.6}, parts=[
        ('pulse', bars('C5 . . . G4 . . . Ab4 . . . G4 . F4 .', 'Eb4 . . . F4 . G4 . Ab4 . . . Bb4 . B4 .',
                       'C5 . . . G4 . . . Db5 . . . C5 . Bb4 .', 'Ab4 . G4 . F4 . Eb4 . D4 . . . B3 . . .'), 0.2, {'duty': 0.5}),
        ('triangle', bars('C2 C2 C3 C2 C2 C2 C3 C2 Ab1 Ab1 Ab2 Ab1 G1 G1 G2 G1', 'C2 C2 C3 C2 C2 C2 C3 C2 Ab1 Ab1 Ab2 Ab1 G1 G1 G2 G1',
                          'Db2 Db2 Db3 Db2 Db2 Db2 Db3 Db2 C2 C2 C3 C2 C2 C2 C3 C2', 'F1 F1 F2 F1 Eb2 Eb2 Eb3 Eb2 G1 G1 G2 G1 G1 G2 G1 G2'), 0.55),
        ('drums', bars('K K - - S - - - K K - - S - H H', 'K K - - S - - - K K - - S - H H',
                       'K K - - S - - - K K - - S - H H', 'K - K - S - K - K S K S S S S S'), 0.65),
    ]),
    # Loot! A bright, bleepy treasure jingle that loops.
    'loot': dict(bpm=144, env={'decay': 0.05, 'sustain': 0.4}, parts=[
        ('pulse', bars('C5 E5 G5 C6 - G5 E5 - F5 A5 C6 F6 - C6 A5 -', 'G5 B5 D6 G6 - D6 B5 - C6 . E6 . C6 . - -'), 0.16, {'duty': 0.25}),
        ('triangle', bars('C3 . G2 . C3 . G2 . F2 . C3 . F2 . C3 .', 'G2 . D3 . G2 . D3 . C3 . G2 . C3 . - -'), 0.5),
        ('drums', bars('K - H - S - H - K - H - S - H -', 'K - H - S - H - K - S - K S S -'), 0.45),
    ]),
}

STINGS = {  # one-offs: they play once
    'victory': dict(bpm=150, parts=[
        ('pulse', 'G4 C5 E5 G5 - E5 G5 . . . . . - - - -', 0.22, {'duty': 0.25}),
        ('triangle', 'C3 - C3 - - C3 C3 . . . . . - - - -', 0.5)]),
    'defeat': dict(bpm=90, env={'decay': 0.2, 'sustain': 0.7}, parts=[
        ('pulse', 'G4 . . F#4 . . F4 . . E4 . . . . . . . .', 0.2, {'duty': 0.5, 'vibrato': 0.02}),
        ('triangle', 'C3 . . B2 . . Bb2 . . A2 . . . . . . . .', 0.5)]),
    'level_up': dict(bpm=200, parts=[('pulse', 'C5 E5 G5 C6 E6 G6 C7 . . -', 0.18, {'duty': 0.125})]),
}


# ---------- sound effects -----------------------------------------------------------------------------------------

def sweep(f0, f1, seconds, duty=0.5, kind='pulse'):
    x = t(seconds)
    f = f0 * (f1 / f0) ** (x / seconds)
    phase = np.cumsum(f) / RATE
    if kind == 'pulse':
        return np.where((phase % 1) < duty, 1.0, -1.0)
    return 4 * np.abs((phase % 1) - 0.5) - 1

def fade(x, power=1.5):
    return x * np.linspace(1, 0, len(x)) ** power

def lowpass(x, amount):
    """A very rough smoothing: bigger amount = duller."""
    k = np.ones(amount) / amount
    return np.convolve(x, k, mode='same')

def blips(names, each=0.05, duty=0.25):
    return np.concatenate([fade(pulse(freq(n), each, duty), 0.5) for n in names])

SFX = {
    'type': lambda: fade(noise(0.012), 3) * 0.25,                                     # the typewriter's tick
    'select': lambda: blips(['E5', 'B5'], 0.035) * 0.35,                              # a menu pick
    'swing': lambda: fade(sweep(900, 300, 0.12, 0.125), 1) * 0.35,                     # a weapon swung
    'hit': lambda: fade(noise(0.18), 2) * 0.6 + fade(sweep(220, 60, 0.18), 2) * 0.4,   # landing a hit
    'crit': lambda: np.concatenate([blips(['C6', 'G6', 'C7'], 0.04, 0.125) * 0.3, fade(noise(0.25), 1.5) * 0.7]),
    'miss': lambda: lowpass(fade(noise(0.3), 1) * np.sin(np.linspace(0, np.pi, int(RATE * 0.3))), 6) * 0.7,
    'claws': lambda: np.concatenate([fade(noise(0.07), 1) for _ in range(3)]) * 0.6,
    'fire': lambda: lowpass(fade(noise(1.0), 0.8), 9) * 1.6 + fade(sweep(120, 50, 1.0, kind='tri'), 1) * 0.4,
    'inferno': lambda: lowpass(fade(noise(2.0), 0.6), 14) * 2.2 + fade(sweep(80, 30, 2.0, kind='tri'), 0.8) * 0.6,
    'inhale': lambda: lowpass(noise(1.0) * np.linspace(0, 1, RATE), 20) * 1.6,
    'hurt': lambda: fade(sweep(500, 150, 0.22, 0.25), 1) * 0.4,
    'die': lambda: fade(sweep(600, 40, 1.4, 0.5), 0.7) * 0.35,
    'roar': lambda: lowpass(fade(noise(0.9), 1), 5) * 0.9 + fade(sweep(110, 70, 0.9, 0.3), 1) * 0.35,
    'shatter': lambda: np.concatenate([fade(noise(0.15), 2) * 0.8] + [fade(pulse(rng.uniform(1800, 3200), 0.04, 0.5), 2) * 0.2 for _ in range(6)]),
    'coin': lambda: blips(['B5', 'E6', 'G#6', 'B6', 'E7'], 0.06, 0.125) * 0.3,
    'zap': lambda: np.concatenate([fade(sweep(rng.uniform(400, 1200), 3000, 0.05, 0.5), 1) for _ in range(6)]) * 0.3,
    'burn': lambda: lowpass(fade(noise(0.4), 1.2), 6) * 0.9,
    'hiccup': lambda: np.concatenate([fade(sweep(300, 700, 0.08, 0.25), 1) * 0.4, np.zeros(int(RATE * 0.05))]),
    'gulp': lambda: np.concatenate([fade(sweep(200, 500, 0.09, 0.5, 'tri'), 1) for _ in range(3)]) * 0.6,
    'heal': lambda: blips(['C5', 'E5', 'G5', 'C6', 'E6'], 0.07, 0.5) * 0.25,
    'fart': lambda: lowpass(pulse(70, 0.9, 0.3, vibrato=0.25) * np.linspace(1, 0.2, int(RATE * 0.9)), 4) * 0.5,
    'duck': lambda: fade(sweep(700, 250, 0.1, 0.5, 'tri'), 1) * 0.5,
    'scream': lambda: fade(sweep(900, 1300, 0.5, 0.125) * (1 + 0.3 * np.sin(np.linspace(0, 60, int(RATE * 0.5)))), 1) * 0.25,
    'gag': lambda: np.concatenate([lowpass(fade(noise(0.15), 1), 8) * 0.8 + fade(sweep(160, 90, 0.15, 0.4), 1) * 0.3 for _ in range(2)]),
    'cackle': lambda: np.concatenate([fade(sweep(700, 500, 0.07, 0.25), 1) for _ in range(5)]) * 0.35,
}


def write(path: str, samples: np.ndarray):
    peak = np.max(np.abs(samples)) or 1
    if peak > 0.95:
        samples = samples * (0.95 / peak)
    data = (np.clip(samples, -1, 1) * 32000).astype('<i2')
    with wave.open(path, 'wb') as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(RATE)
        f.writeframes(data.tobytes())


def main():
    os.makedirs(MUSIC, exist_ok=True)
    os.makedirs(SOUNDS, exist_ok=True)
    for name, song in {**SONGS, **STINGS}.items():
        loop = render(song)  # (songs loop seamlessly in the game; stings play once)
        write(os.path.join(MUSIC, f'{name}.wav'), loop)
    for name, make in SFX.items():
        write(os.path.join(SOUNDS, f'{name}.wav'), make())
    print(f'{len(SONGS) + len(STINGS)} songs and {len(SFX)} sounds written.')


if __name__ == '__main__':
    main()
