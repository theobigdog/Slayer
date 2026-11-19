"""The game from start to finish: name the hero, pick a path, then fight your way through the Dragon Cliffs.

The run: whichever of Trogdor (Left) or Skippy (Right) you pick first, then the other one, then The Ancient
down the hidden Lower path. After each win you loot the hoard, get tougher, and choose: go home a hero
(Ted's original ending) or press on. The Kool-Aid code (beat Skippy and go home to get it) lets you take the
Lower path right away, straight to The Ancient.
"""
import random

import story
import ui
from battle import fight, line, match, tell
from fighters import HOARDS, PATHS, Dragon, Hero

TROGDOR, SKIPPY, ANCIENT = 'Trogdor The Burninator', 'Skippy', 'The Ancient'


async def name_the_hero() -> Hero:
    hero = Hero((await ui.ask_text(story.ASK_NAME)).strip() or 'Nobody')
    for text in story.RENAME:
        await ui.say(text)
    await ui.wait(2)
    hero.rename()
    await ui.say()
    await tell([story.NEW_NAME], hero)
    await ui.say()
    return hero


async def pick_a_path(hero: Hero, hard_mode: bool, intro: bool) -> str:
    paths = list(PATHS) if hard_mode else ['Left', 'Right']
    if intro:
        ui.music('tunnel')
        await ui.clear()
        beats = story.INTRO + ([story.INTRO_HARD_MODE] if hard_mode else [])
        await tell(beats, hero)
        await ui.say()
        await ui.say(story.PICK_A_PATH)
        answer = await ui.choose_or_stall(story.ASK_PATH, paths, patience=None)
    else:
        await ui.say()
        await ui.say(story.NO_INTRO)
        answer = await ui.choose_or_stall(story.ASK_PATH_NO_INTRO, paths, patience=None, hidden=True)
    path = paths[answer] if isinstance(answer, int) else match(answer, paths)
    while not path:
        await ui.say()
        if answer.strip().lower() == 'lower':  # nice try
            await ui.say(story.NO_LOWER_PATH)
        else:
            await ui.say(story.NOT_A_PATH)
        answer = await ui.choose_or_stall(story.ASK_PATH_AGAIN, paths, patience=None)
        path = paths[answer] if isinstance(answer, int) else match(answer, paths)
    if hard_mode and path != 'Lower':
        await ui.say()
        await ui.say(story.CHICKEN)
        if not await ui.yes_no(story.ASK_CHICKEN):
            path = 'Lower'
    return path


async def loot(hero: Hero, dragon: Dragon):
    pool = HOARDS[dragon.name]
    if not pool:
        return
    ui.music('loot')
    await ui.say()
    await tell([[story.HOARD[0], story.HOARD[1]]], hero, dragon)
    offered = random.sample(pool, 3)
    pick = await ui.choose(story.PICK_LOOT, [story.LOOT_LABELS[item] for item in offered])
    hero.take_loot(offered[pick])
    ui.sound('coin')
    await line(story.TOOK_LOOT, hero, dragon, item=offered[pick])


async def the_end(hero: Hero, dragon: Dragon, ending: str):
    """Ted's endings. 'won' is beating The Ancient; 'went_home' is leaving a hero after Trogdor or Skippy."""
    if ending == 'won':
        await tell(story.VICTORY, hero, dragon)
        await ui.say()
        await tell(story.VICTORY_ANCIENT, hero, dragon)
    elif ending == 'went_home':
        await tell(story.VICTORY[1:], hero, dragon)
        await ui.say()
        await tell(story.VICTORY_GO_HOME, hero, dragon)
    else:
        await ui.say()
        await tell(story.ENDINGS[ending], hero, dragon)
    await ui.say()
    await ui.say(story.THE_END)
    await ui.say()
    if ending == 'went_home' and dragon.name == SKIPPY:
        for text in story.HARD_MODE_UNLOCKED:
            await ui.say(text)
        await ui.say()
    await ui.the_end()


async def play() -> str:
    """One whole game. Returns '<the last dragon>: <how it ended>' (the test bot counts these)."""
    await ui.title_screen()
    await ui.clear()
    hero = await name_the_hero()
    hard_mode = (await ui.ask_text(story.ASK_READY.replace('{hero}', hero.name))).strip().lower() == story.HARD_MODE_CODE.lower()
    if hard_mode:
        ui.sting('level_up')
    await ui.say(story.HARD_MODE_ON if hard_mode else story.NOT_READY)
    await ui.say()
    intro = await ui.yes_no(story.ASK_INTRO)
    first = PATHS[await pick_a_path(hero, hard_mode, intro)]
    run = [ANCIENT] if first == ANCIENT else [first, SKIPPY if first == TROGDOR else TROGDOR, ANCIENT]

    for name in run:
        dragon = Dragon(name)
        if intro:
            ui.music(dragon.song)
            await ui.say()
            await tell(story.DRAGON_INTROS[name], hero, dragon)
        ui.music(dragon.fight_song)
        ending = await fight(hero, dragon)
        await ui.show_battle(hero, dragon, final=True)
        if ending != 'won':
            ui.sting('defeat')
            await the_end(hero, dragon, ending)
            return f'{name}: {ending}'
        ui.sting('victory')
        if name == ANCIENT:
            await the_end(hero, dragon, 'won')
            return f'{name}: won'

        # Won, with more dragons to go.
        await line(story.YOU_WON, hero, dragon)
        if hero.dropped_weapons:
            hero.dropped_weapons = False
            await ui.say(story.PICK_UP_WEAPONS)
        gain = hero.grow()
        await ui.wait(1)
        ui.sting('level_up')
        await line(story.GROW, hero, gain=gain)
        await ui.pause()
        await loot(hero, dragon)
        await ui.say()
        if await ui.choose(story.ONWARD, story.HOME_OR_DEEPER) == 0:
            await ui.say()
            await the_end(hero, dragon, 'went_home')
            return f'{name}: went_home'
        ui.music('tunnel')
        await ui.clear()
        next_one = run[run.index(name) + 1]
        bridge = (story.BRIDGE_TO_ANCIENT if next_one == ANCIENT
                  else story.BRIDGE_TO_SKIPPY if next_one == SKIPPY else story.BRIDGE_TO_TROGDOR)
        await tell(bridge, hero)
