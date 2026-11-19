"""Plays thousands of games with bots and checks nothing breaks. Also shows how often a sensible player wins.

    python tools/bot_test.py              # 3000 games with each bot
    python tools/bot_test.py 200 show     # 200 games each, and print one whole game so you can read it

Two bots:
  random: types random (sometimes silly) answers, tests every odd path
  smart:  plays sensibly: ducks the big attacks, drinks when hurt, picks the best weapon, never flips the coin,
          and always presses on. Its win rates are the ones to tune the dragons by.
It checks: no crashes, every game ends, no {placeholders} left in the text, and HP never goes below 0.
"""
import asyncio
import collections
import os
import random
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'game'))

import fighters
import story
import ui
from play import play

SILLY = ['', 'asdf', '9', 'Lower', 'Magic Coin', 'Sword', '0', '-1']


class BotUI:
    def __init__(self, smart: bool):
        self.smart = smart
        self.text = []
        self.steps = 0
        self.hero = self.dragon = None

    def step(self):
        self.steps += 1
        if self.steps > 5000:
            raise RuntimeError('game never ended')

    async def say(self, text=''):
        self.text.append(text)

    async def wait(self, seconds):
        pass

    async def pause(self):
        self.step()

    async def clear(self):
        self.text.append('---- (screen cleared) ----')

    async def ask_text(self, prompt):
        self.step()
        if 'llama' in prompt:
            reply = random.choice(['Bubba', '', 'Muffy'])
        elif 'ready' in prompt:
            reply = '' if self.smart else random.choice(['Kool-Aid', 'yes', '', 'kool-aid'])
        else:  # yes / no
            reply = 'n' if self.smart else random.choice(['y', 'yes', 'n', '', 'nah'])
        self.text.append(f'{prompt}{reply}')
        return reply

    async def choose_or_stall(self, prompt, labels, patience, quiet, hidden):
        self.step()
        if self.smart:
            reply = self.smart_pick(prompt, labels)
        elif random.random() < 0.15:
            reply = random.choice(SILLY)
        else:
            reply = random.randrange(len(labels))
        self.text.append(f'{prompt}{labels[reply] if isinstance(reply, int) else reply}')
        return reply

    def smart_pick(self, prompt, labels):
        if prompt == story.ONWARD:
            return 1  # always press on
        if prompt == story.PICK_LOOT:
            order = ['Beefy-Arm Gauntlet', 'Dragon-Tooth Dagger', 'Healing Draught', "Trogdor's Mead", "Skippy's Tiara", 'Peasant Pitchfork', 'Whetstone', 'Femur Club', 'Spare Sword']
            for want in order:
                for i, label in enumerate(labels):
                    if label.startswith(want):
                        return i
            return 0
        if not any('damage' in label or 'Duck' in label for label in labels):
            return 0  # a path: Left
        hero, dragon = self.hero, self.dragon
        options = [what for what, _ in hero.menu()]
        if dragon.winding_up:
            return options.index(fighters.DUCK)
        if hero.hp < 0.4 * hero.max_hp:
            for drink in ("Healing Draught", "Trogdor's Mead"):
                if drink in options:
                    return options.index(drink)
        weapons = [w for w in options if w in fighters.WEAPONS]
        if not weapons:
            return options.index(fighters.DUCK)
        def value(w):
            low, high = fighters.WEAPONS[w]['damage']
            avg = (low + high) / 2 + hero.bonus_damage
            if dragon.armor and not fighters.WEAPONS[w].get('pierce'):
                avg -= dragon.armor
            if dragon.mind_reader and w == hero.last_weapon:
                avg *= 0.5
            return avg
        return options.index(max(weapons, key=value))

    async def show_battle(self, hero, dragon, final):
        self.hero, self.dragon = hero, dragon
        self.text.append(f'[{hero.name} {hero.hp}/{hero.max_hp} {list(hero.statuses)}  vs  {dragon.name} {dragon.hp}/{dragon.max_hp} {list(dragon.statuses)}]')

    async def effect(self, name, who):
        pass

    async def title_screen(self):
        pass

    async def the_end(self):
        pass

    def music(self, name):
        pass

    def sting(self, name):
        pass

    def sound(self, name):
        pass


def run(games: int, smart: bool, show: bool, problems: list) -> collections.Counter:
    endings = collections.Counter()
    for n in range(games):
        bot = BotUI(smart)
        ui.use(bot)
        try:
            ending = asyncio.run(play())
        except Exception as e:
            import traceback
            problems.append(f'game {n}: {type(e).__name__}: {e}\n{traceback.format_exc()}')
            continue
        endings[ending] += 1
        leftover = [t for t in bot.text if re.search(r'\{\w+\}', t)]
        if leftover:
            problems.append(f'game {n}: unfilled text: {leftover[0]}')
        if show and n == 0:
            print('\n'.join(bot.text))
            print('=' * 100)
    return endings


def main():
    games = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
    show = 'show' in sys.argv
    problems = []
    for cls in (fighters.Hero, fighters.Dragon):  # watch HP so it can never go below 0
        original = cls.take
        def take(self, damage, _orig=original):
            _orig(self, damage)
            if self.hp < 0:
                problems.append(f'{self.name} went below 0 HP')
        cls.take = take
    for smart in (False, True):
        endings = run(games, smart, show and smart, problems)
        print(f"\n{'smart' if smart else 'random'} bot, {games} games")
        for ending, count in sorted(endings.items()):
            print(f'  {ending:<50} {count:>5}  {100 * count / games:5.1f}%')
        if smart:
            reached = collections.Counter(e.split(':')[0] for e in endings.elements())
            beat_trogdor = games - sum(c for e, c in endings.items() if e.startswith('Trogdor') and 'won' not in e)
            print(f'  beat the first dragon: {100 * beat_trogdor / games:.0f}%   '
                  f"beat all three: {100 * endings['The Ancient: won'] / games:.0f}%")
    print('\nPROBLEMS:', 'none' if not problems else '')
    for p in problems[:5]:
        print('  ', p)
    return 1 if problems else 0


if __name__ == '__main__':
    sys.exit(main())
