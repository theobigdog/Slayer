# SLAYER (the classic)

*The original 2021 Slayer, cleaned up.* One hero, three tunnels, three dragons, a Magic Coin, and a man-bun
that might just save your life. It swears.

Pick a path, meet Trogdor The Burninator (Easy), Skippy (Regular) or, if you know the code, The Ancient (Hard),
and try not to die. You will probably die. Every way of dying has its own ending.

## Playing it

```
python main.py
```

Works in the command prompt on Windows, Mac or Linux. Nothing to install.
Type a number or a name to pick (`2`, `sword`, `Sword` all work). Press Enter to keep reading.

## What's where

- `game/story.py`: **every word of the story**. Ted's file. Edit text here without touching any code.
- `game/fighters.py`: the hero, the three dragons' stats (Ted's original numbers and notes), and the dice.
- `game/battle.py`: how a fight works.
- `game/play.py`: the game from start to finish.
- `game/ui.py`: the one place the game prints and asks things (same idea as `Slayer_UI` in Slayer_Next_Gen,
  so a game window can be added later without touching the game).
- `tools/bot_test.py`: plays thousands of random games and checks nothing breaks (`python tools/bot_test.py`).

The original single-file version is still in `python_homework/Slayer_v1/` and in this repo's history.

## What changed from the 2021 version (Nov 19, 2026)

Same game, same story, same numbers. The code was rewritten from one 630-line file into the pieces above.
Fixes along the way:

- **Weapons rolled their damage once per game.** Your Sword did the same damage every swing all game long, and
  so did each dragon's claws and fire. They now roll fresh every time.
- **Dying from the Magic Coin's tails fireball didn't end the game.** You'd keep fighting at 0 or negative HP.
- **Health could go negative** (the coin's fireballs).
- Runs on Mac and Linux now (it used to need Windows' `msvcrt`), and needs no colorama.
- You can type a number instead of the exact name, and capitals don't matter. Bad answers still get yelled at,
  and three bad answers still end in the man-bun.
- Typos: "a peed" → "peed", "obsenities" → "obscenities", "succomb" → "succumb", "irridescent" → "iridescent",
  "a boys name" → "a boy's name". "Cajones", "fiercestest" and "readyness" were left alone on purpose.
