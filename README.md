# SLAYER (the classic)

*The original 2021 Slayer, back from the dead on a glowing green screen.* One hero, three dragons, a Magic
Coin, and a man-bun that might just save your life. It swears.

Walk into the Dragon Cliffs and pick a tunnel. Fight Trogdor The Burninator (still drunk) and Skippy (reads
your mind), loot their hoards, and find the hidden way down to The Ancient. Or take the money and go home a
hero. You will probably die either way. Every way of dying has its own ending.

## Playing it

```
pip install pygame-ce
python main.py                 # the game window
python play_in_terminal.py     # the original command-prompt way (nothing to install)
```

**No Python?** `python tools/build_exe.py` (after `pip install pyinstaller`) makes `dist/Slayer.exe`, one file that
runs on any Windows PC. Windows may warn about it the first time ("More info" → "Run anyway"), since it isn't signed.

In the window: click or press Enter to keep reading, click a choice or press its number, mouse wheel to scroll
back. **M** mutes; click the bar at the top right to set the volume.

## What's new since 2021 (Nov 2026)

- **A game window** that looks like an old green-screen computer, booting up BUBBA-DOS, with Ted's own dragon drawings as glowing lines,
  health bars, floating damage numbers, and the screen shaking and flashing when things hurt.
- **Its own 8-bit soundtrack and sound effects**, all original: a march for the title, a drunk waltz in
  Trogdor's cave, a bouncy creep for Skippy, a slow rumble for The Ancient, and fight music.
- **One run through the Dragon Cliffs:** beat a dragon, grab one thing from her hoard, get tougher, then choose:
  home (Ted's original endings) or deeper. Both tunnels, then the hidden Lower path to The Ancient.
  "Kool-Aid" still opens the Lower path straight away, for the brave.
- **Dragons with tricks:** Trogdor hiccups and winds up a BURNINATE; Skippy reads your mind if you swing the same
  weapon twice and puffs up at half health; The Ancient's scales shrug off light hits (the Halberd finds the
  gaps), she charges an INFERNO, and gets FURIOUS near the end.
- **Duck and cover**, drinks (Trogdor's Mead gets you drunk), and statuses: on fire, drunk, terrified, damp.
- In the window, dither too long over your weapon and the dragon closes in. You know what happens then.
- The dragons keep Ted's 2021 numbers; `SCALE` in `game/fighters.py` tunes them for the run (about 4 in 5
  sensible players beat the first dragon, about 1 in 5 beat all three).

## What's where

- `game/story.py`: **every word of the story**. Ted's file. The bottom section is Claude's drafts for the new
  parts (marked), for Ted to rewrite.
- `game/fighters.py`: the hero, the dragons' stats and tricks, the loot.
- `game/battle.py`: how a fight works. `game/play.py`: the run from start to finish.
- `game/ui.py`: the one place the game prints and asks things. `game/window.py` is the game window,
  `game/sound.py` plays the music, `game/art.py` holds the ASCII art (edit freely).
- `tools/bot_test.py`: plays thousands of games with a random bot and a sensible one, checks nothing breaks, and
  prints win rates.
- `tools/make_dragons.py`: turns Ted's dragon drawings (`assets/drawings/`) into the glowing line art the window
  shows (`assets/dragons/`). Draw on light paper, save as trogdor/skippy/ancient .png or .jpg, run it. A dragon
  with no drawing falls back to the ASCII art.
- `tools/build_exe.py`: packs the whole game into `dist/Slayer.exe`.
- `tools/make_sounds.py`: writes the music and sound effects (`pip install numpy` first). The songs are written
  as notes in that file, so they're easy to change.

The original single-file version is still in `python_homework/Slayer_v1/` and in this repo's history (along
with the old Flask version).

## Fixes to the 2021 code

- Weapons rolled their damage once per game (your Sword did the same damage every swing all game), and so did
  the dragons' claws and fire. They roll fresh every time now.
- Dying from the Magic Coin's tails fireball didn't end the game, and health could go negative.
- Runs on Mac and Linux too; you can type a number instead of the exact name.
- Typos: "a peed" → "peed", "obsenities" → "obscenities", "succomb" → "succumb", "irridescent" → "iridescent",
  "a boys name" → "a boy's name". "Cajones", "fiercestest" and "readyness" were left alone on purpose.

## License

Same as Slayer_Next_Gen: free and non-commercial. Code under PolyForm Noncommercial 1.0.0, creative work (story,
music, sounds, art) under CC BY-NC-SA 4.0; see `LICENSES/`. The font is DejaVu Sans Mono (its license is in
`assets/fonts/`).
