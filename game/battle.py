"""The fight: the hero against one dragon, a round at a time, until somebody's dead (or runs away)."""
import random

import story
import ui
from fighters import BARE_HANDS, DRINKS, DUCK, MAGIC_COIN, WEAPONS, d10, d20, hitpoints


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


async def line(text: str, hero=None, dragon=None, **extra):
    await ui.say(fill(text, hero, dragon, **extra))


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

async def choose_action(hero, dragon) -> str:
    """What she does this turn. Dither too long (or keep typing nonsense) and she freezes up: Bare-Hands."""
    options = hero.menu()
    names = [what for what, _ in options]
    labels = [label for _, label in options]
    await ui.say(story.CHOOSE_WEAPON)
    answer = await ui.choose_or_stall(story.ASK_WEAPON, labels)
    for tries in range(3):
        if isinstance(answer, int):
            return names[answer]
        picked = match(answer, names)
        if picked:
            return picked
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
        answer = await ui.choose_or_stall(story.STALLING[tries], labels, quiet=True)
    # Too slow, or three bad answers: she freezes up, drops everything, and goes for the man-bun.
    ui.sound('scream')
    await ui.say()
    await tell(story.FROZE, hero, dragon)
    hero.statuses['damp'] = 1
    return BARE_HANDS


async def swing(hero, dragon, weapon: str):
    ui.sound('swing')
    await ui.wait(0.25)
    dodge = dragon.dodge - (1 if 'drunk' in hero.statuses else 0)
    read_her_mind = dragon.mind_reader and weapon == hero.last_weapon
    if read_her_mind:
        dodge -= dragon.mind_reader
    hero.last_weapon = weapon
    if d10() > dodge:
        ui.sound('miss')
        await ui.say()
        await line(story.MIND_READ if read_her_mind else story.HERO_MISSES, hero, dragon)
        return
    damage = hero.swing(weapon)
    hero.tick('terrified')
    crit = d20() > hero.crit_chance
    if crit:
        damage = int(damage * hero.crit_multiplier)
    pierce = WEAPONS[weapon].get('pierce')
    if dragon.armor and not pierce:
        damage = max(1, damage - dragon.armor)
    damage = min(damage, dragon.hp)
    dragon.take(damage)
    ui.sound('crit' if crit else 'hit')
    await ui.effect('flash_white' if crit else 'shake', dragon)
    await ui.say()
    await line(story.HERO_HITS, hero, dragon, weapon=weapon, damage=hitpoints(damage))
    if crit:
        await ui.say(story.CRIT)
    if dragon.armor:
        await line(story.PIERCE if pierce else story.ARMOR, hero, dragon, weapon=weapon)


async def drink(hero, what: str):
    hero.drinks[what] -= 1
    if not hero.drinks[what]:
        del hero.drinks[what]
    ui.sound('gulp')
    await ui.wait(0.4)
    healed = hero.heal(random.randint(*DRINKS[what]['heal']))
    ui.sound('heal')
    await ui.say()
    await line(story.DRINK_MEAD if 'drunk' in DRINKS[what] else story.DRINK_DRAUGHT, hero, heal=hitpoints(healed))
    if 'drunk' in DRINKS[what]:
        hero.statuses['drunk'] = DRINKS[what]['drunk']


async def flip_coin(hero, dragon):
    """The Magic Coin: heads, she runs for it; tails, it burns her and a fireball hits her in the face.
    Returns how the game ended, or None if the fight goes on (the coin's gone either way)."""
    ui.sound('coin')
    await ui.say()
    await tell([story.COIN_TOSS], hero, dragon)
    hero.inventory.remove(MAGIC_COIN)
    ui.sound('zap')
    if random.choice(['Heads', 'Tails']) == 'Heads':
        await ui.say()
        await tell([story.COIN_HEADS], hero, dragon)
        if dragon.name != 'The Ancient':
            return 'ran_away'
        # The Ancient already blew up the exit. Oops.
        damage = dragon.fireball() * 3
        hero.take(damage)
        ui.sound('inferno')
        await ui.effect('flash_fire', hero)
        await ui.say()
        await tell(story.COIN_HEADS_ANCIENT, hero, dragon, damage=hitpoints(damage))
        return None if hero.alive else 'coin_killed_you_ancient'
    damage = dragon.fireball() * 2
    hero.take(damage)
    ui.sound('fire')
    await ui.effect('flash_fire', hero)
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
        ui.sound('fart')
        await ui.effect('shake', dragon)
        await tell(story.STRANGLED_HER, hero, dragon)
        await ui.say()
        return 'won'
    ui.sound('gag')
    return 'bucked_off'


async def burn(hero) -> bool:
    """Start of her turn: if she's on fire, it hurts. Returns False if that killed her."""
    if 'burning' not in hero.statuses:
        return True
    damage = random.randint(2, 4)
    hero.take(damage)
    hero.tick('burning')
    ui.sound('burn')
    await ui.effect('flash_fire', hero)
    await line(story.STILL_BURNING, hero, damage=hitpoints(damage))
    if 'burning' not in hero.statuses and hero.alive:
        await ui.say(story.FIRE_OUT)
    await ui.say()
    return hero.alive


# ---------- the dragon's turn -------------------------------------------------------------------------------------

async def hurt_hero(hero, dragon, damage: int, fire: bool):
    hero.take(damage)
    ui.sound('fire' if fire else 'claws')
    await ui.wait(0.3)
    ui.sound('die' if not hero.alive else 'hurt')
    await ui.effect('flash_fire' if fire else 'flash_red', hero)


async def catch_fire(hero, turns: int = 3):
    if 'burning' not in hero.statuses:
        await ui.say(story.CATCH_FIRE)
    hero.statuses['burning'] = turns


async def dragon_attacks(hero, dragon, weapon):
    """weapon: what the hero swung this turn (None if she ducked or drank): it's what might shatter."""
    dragon.turn += 1
    if dragon.puff_up and not dragon.puffed and dragon.hp <= dragon.max_hp / 2:
        dragon.puffed = True
        ui.sound('roar')
        await ui.effect('shake', dragon)
        await ui.say()
        await line(story.PUFF_UP, hero, dragon)
    if dragon.enrage_at and not dragon.enraged and dragon.hp <= dragon.enrage_at * dragon.max_hp:
        dragon.enraged = True
        dragon.crit_chance -= 3
        ui.sound('roar')
        await ui.effect('flash_red', dragon)
        await ui.say()
        await line(story.ENRAGE, hero, dragon)

    if dragon.winding_up:  # the big one: BURNINATE / INFERNO
        dragon.winding_up = False
        damage = int(dragon.fireball() * dragon.big_multiplier)
        await ui.say()
        if hero.ducking:
            damage = min(max(1, damage // 4), hero.hp)
            await hurt_hero(hero, dragon, damage, fire=True)
            await line(story.DUCKED_THE_BIG_ONE, hero, dragon, damage=hitpoints(damage))
        else:
            damage = min(damage, hero.hp)
            ui.sound('inferno')
            await hurt_hero(hero, dragon, damage, fire=True)
            big = story.ANCIENT_BIG if dragon.name == 'The Ancient' else story.TROGDOR_BIG
            await line(big, hero, dragon, damage=hitpoints(damage))
            if hero.alive:
                await catch_fire(hero)
        return
    if dragon.big_every and dragon.turn % dragon.big_every == 0:
        dragon.winding_up = True
        ui.sound('inhale')
        await ui.say()
        await line(story.ANCIENT_WINDUP if dragon.name == 'The Ancient' else story.TROGDOR_WINDUP, hero, dragon)
        return
    if dragon.hiccups and random.random() < dragon.hiccups:
        ui.sound('hiccup')
        await ui.say()
        if random.random() < 0.35:
            damage = min(max(1, dragon.fireball() // 2), dragon.hp - 1)
            dragon.take(damage)
            ui.sound('fire')
            await ui.effect('flash_fire', dragon)
            await line(story.HICCUP_FIRE, hero, dragon, damage=hitpoints(damage))
        else:
            await line(random.choice(story.HICCUP), hero, dragon)
        return

    breath = d10() > dragon.breath
    dodge = 4 if hero.ducking else hero.dodge  # ducking: she dodges 6 times in 10
    if d10() > dodge:
        ui.sound('miss')
        await ui.say()
        await ui.say(story.HERO_DODGES)
        return
    damage = dragon.fireball() if breath else dragon.clawing()
    if dragon.puffed:
        damage = int(damage * dragon.puff_up)
    crit = d20() > dragon.crit_chance
    if crit:
        damage = int(damage * dragon.crit_multiplier)
    damage = min(damage, hero.hp)
    await hurt_hero(hero, dragon, damage, fire=breath)
    await line(story.DRAGON_BREATHES if breath else story.DRAGON_CLAWS, hero, dragon, damage=hitpoints(damage))
    if crit:
        await ui.say(story.CRIT)
    if breath and hero.alive and (crit or random.random() < 0.25):
        await catch_fire(hero, 2)
    if weapon and hero.alive and d20() > dragon.weapon_break and weapon in hero.inventory:
        await ui.wait(0.5)
        ui.sound('shatter')
        await ui.wait(0.3)
        ui.sound('cackle')
        await ui.say()
        await lines(story.WEAPON_SHATTERS, hero, dragon, weapon=weapon)
        hero.inventory.remove(weapon)
        hero.statuses['terrified'] = 2
        await ui.say(story.TERRIFIED)
        if 'damp' not in hero.statuses:
            hero.statuses['damp'] = 1
            await ui.say(story.DAMP)


# ---------- the whole fight ---------------------------------------------------------------------------------------

async def fight(hero, dragon) -> str:
    """Returns how it ended: 'won', or one of the losing endings in story.ENDINGS."""
    hero.last_weapon = None
    while hero.alive and dragon.alive:
        await ui.show_battle(hero, dragon)
        if not await burn(hero):
            return 'slain'
        action = await choose_action(hero, dragon)
        ui.sound('select')
        swung = None
        if action == MAGIC_COIN:
            ending = await flip_coin(hero, dragon)
            if ending:
                return ending
        elif action == BARE_HANDS:
            hero.dropped_weapons = True
            return await strangle(hero, dragon)
        elif action == DUCK:
            hero.ducking = True
            ui.sound('duck')
            await ui.say()
            await ui.say(random.choice(story.DUCKS))
        elif action in DRINKS:
            await drink(hero, action)
        else:
            swung = action
            await swing(hero, dragon, action)
        if action != MAGIC_COIN:  # (the coin's story already waited for Enter)
            await ui.pause()
        if dragon.alive and hero.alive:
            await dragon_attacks(hero, dragon, swung)
            await ui.pause()
        hero.ducking = False
        hero.tick('drunk')
    return 'won' if hero.alive else 'slain'
