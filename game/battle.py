"""The fight: the hero against one dragon, a round at a time, until somebody's dead (or runs away)."""
import random

import story
import ui
from fighters import BARE_HANDS, MAGIC_COIN, MENU, WEAPONS, d10, d20, hitpoints


def fill(text: str, hero=None, dragon=None, **extra) -> str:
    """Swaps {hero}, {dragon} and any extras (like {weapon} or {damage}) into a line of the story."""
    words = dict(extra)
    if hero:
        words['hero'] = hero.name
    if dragon:
        words['dragon'] = dragon.name
    for key, value in words.items():
        text = text.replace('{' + key + '}', str(value))
    return text


async def tell(beats: list, hero=None, dragon=None, **extra):
    """Tells a story: each beat's lines, then a wait for Enter, with a blank line between beats."""
    for i, beat in enumerate(beats):
        if i:
            await ui.say()
        for line in beat:
            if isinstance(line, (int, float)):
                await ui.wait(line)
            else:
                await ui.say(fill(line, hero, dragon, **extra))
        await ui.pause()


async def lines(texts: list, hero=None, dragon=None, **extra):
    for text in texts:
        await ui.say(fill(text, hero, dragon, **extra))


# ---------- the health bar at the top of each round --------------------------------------------------------------

def health(fighter) -> str:
    color = 'red' if fighter.hp <= 0.25 * fighter.max_hp else 'white'
    return f"[{color}]Health:  {fighter.hp}/{fighter.max_hp}[/]"

async def show_health(hero, dragon):
    await ui.clear()
    await ui.say()
    width = max(len(hero.name), 20) + 6  # the dragon's column starts here
    gap = ' ' * (width - len(f'Health:  {hero.hp}/{hero.max_hp}'))
    await ui.say(f"    [white]{hero.name:<{width}}{dragon.name}[/]")
    await ui.say(f"    {health(hero)}{gap}{health(dragon)}")
    await ui.say()


# ---------- the hero's turn ---------------------------------------------------------------------------------------

def match(answer: str, choices: list):
    """What the player meant: a number from the menu, or a name (any capitals). None if neither."""
    answer = answer.strip()
    if answer.isdigit() and 1 <= int(answer) <= len(choices):
        return choices[int(answer) - 1]
    for choice in choices:
        if answer.lower() == choice.lower():
            return choice
    return None

async def choose_weapon(hero, dragon) -> str:
    await ui.say(story.CHOOSE_WEAPON)
    await ui.say()
    for number, item in enumerate(hero.inventory, 1):
        await ui.say(f"  {number}. {MENU[item]}")
    await ui.say()
    answer = await ui.ask_text(story.ASK_WEAPON)
    for tries in range(3):
        weapon = match(answer, hero.inventory)
        if weapon:
            return weapon
        gone = match(answer, [MAGIC_COIN] + list(WEAPONS))  # something she had, but doesn't any more
        if gone == MAGIC_COIN:
            await ui.say()
            await ui.say(story.COIN_USED_UP)
        elif gone:
            await ui.say()
            await ui.say(story.WEAPON_BROKEN)
        if tries == 2:
            break
        await ui.say()
        answer = await ui.ask_text(story.STALLING[tries])
    # Three bad answers: she freezes up, drops everything, and goes for the man-bun.
    await ui.say()
    await tell(story.FROZE, hero, dragon)
    return BARE_HANDS


async def swing(hero, dragon, weapon: str):
    if d10() > dragon.dodge:
        await ui.say(story.HERO_MISSES)
        return
    damage = hero.swing(weapon)
    crit = d20() > hero.crit_chance
    if crit:
        damage = int(damage * hero.crit_multiplier)
    damage = min(damage, dragon.hp)
    dragon.take(damage)
    await ui.say()
    await ui.say(fill(story.HERO_HITS, hero, dragon, weapon=weapon, damage=hitpoints(damage)))
    if crit:
        await ui.say(story.CRIT)


async def flip_coin(hero, dragon):
    """The Magic Coin: heads, she runs for it; tails, it burns her and a fireball hits her in the face.
    Returns how the game ended, or None if the fight goes on (the coin's gone either way)."""
    await ui.say()
    await tell([story.COIN_TOSS], hero, dragon)
    hero.inventory.remove(MAGIC_COIN)
    if random.choice(['Heads', 'Tails']) == 'Heads':
        await ui.say()
        await tell([story.COIN_HEADS], hero, dragon)
        if dragon.name != 'The Ancient':
            return 'ran_away'
        # The Ancient already blew up the exit. Oops.
        damage = dragon.fireball() * 3
        hero.take(damage)
        await ui.say()
        await tell(story.COIN_HEADS_ANCIENT, hero, dragon, damage=hitpoints(damage))
        return None if hero.alive else 'coin_killed_you_ancient'
    damage = dragon.fireball() * 2
    hero.take(damage)
    await ui.say()
    await tell([story.COIN_TAILS], hero, dragon, damage=hitpoints(damage))
    return None if hero.alive else 'coin_killed_you'


async def strangle(hero, dragon) -> str:
    await ui.wait(1)
    await ui.say()
    await tell([story.BARE_HANDS], hero, dragon)
    await ui.say()
    if hero.grip > dragon.strangle:
        dragon.hp = 0
        await tell(story.STRANGLED_HER, hero, dragon)
        await ui.say()
        return 'won'
    return 'bucked_off'


# ---------- the dragon's turn -------------------------------------------------------------------------------------

async def dragon_attacks(hero, dragon, weapon: str):
    breath = d10() > dragon.breath
    if d10() > hero.dodge:
        await ui.say()
        await ui.say(story.HERO_DODGES)
        return
    damage = dragon.fireball() if breath else random.randint(*dragon.claws)
    crit = d20() > dragon.crit_chance
    if crit:
        damage = int(damage * dragon.crit_multiplier)
    damage = min(damage, hero.hp)
    hero.take(damage)
    await ui.say(fill(story.DRAGON_BREATHES if breath else story.DRAGON_CLAWS, hero, dragon, damage=hitpoints(damage)))
    if crit:
        await ui.say(story.CRIT)
    if d20() > dragon.weapon_break and weapon in hero.inventory:
        await ui.wait(0.5)
        await ui.say()
        await lines(story.WEAPON_SHATTERS, hero, dragon, weapon=weapon)
        hero.inventory.remove(weapon)


# ---------- the whole fight ---------------------------------------------------------------------------------------

async def fight(hero, dragon) -> str:
    """Returns how it ended: 'won', or one of the losing endings in story.ENDINGS."""
    while hero.alive and dragon.alive:
        await show_health(hero, dragon)
        weapon = await choose_weapon(hero, dragon)
        if weapon == MAGIC_COIN:
            ending = await flip_coin(hero, dragon)
            if ending:
                return ending
        elif weapon == BARE_HANDS:
            return await strangle(hero, dragon)
        else:
            await swing(hero, dragon, weapon)
            await ui.pause()
            if dragon.alive:
                await dragon_attacks(hero, dragon, weapon)
                await ui.pause()
    return 'won' if hero.alive else 'slain'
