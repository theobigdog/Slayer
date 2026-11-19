"""Plays thousands of games with a bot that types random (sometimes silly) answers, and checks nothing breaks.

    python tools/bot_test.py            # 5000 games
    python tools/bot_test.py 200 show   # 200 games, and print one whole game so you can read it

It checks: no crashes, every game ends, no {placeholders} left in the text, and HP never goes below 0.
Then it prints how often each ending happened, per dragon.
"""
import asyncio
import collections
import os
import random
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'game'))

import fighters
import ui
from play import play

GOOD = {'weapon': ['1', '2', '3', '4', 'sword', 'Halberd', 'BATTLE-AXE', 'magic coin'],
        'path': ['1', '2', '3', 'left', 'Right', 'Lower'],
        'yes_no': ['y', 'yes', 'nah', 'n', ''],
        'ready': ['Kool-Aid', 'kool-aid', 'yes', ''],
        'name': ['Bubba', '', 'Muffy']}
SILLY = ['', 'asdf', '9', 'Lower', 'Magic Coin', 'Sword', '0', '-1']


class BotUI:
    def __init__(self, silly=0.15):
        self.silly = silly
        self.text = []
        self.steps = 0

    def answer(self, kind):
        self.steps += 1
        if self.steps > 2000:
            raise RuntimeError('game never ended')
        return random.choice(SILLY if random.random() < self.silly else GOOD[kind])

    async def say(self, text=''):
        self.text.append(text)

    async def wait(self, seconds):
        pass

    async def pause(self):
        self.steps += 1

    async def clear(self):
        self.text.append('---- (screen cleared) ----')

    async def ask_text(self, prompt):
        kind = ('weapon' if 'choice' in prompt or 'choose something' in prompt.lower() or 'Choose something' in prompt
                else 'path' if 'tunnel' in prompt or 'Which one' in prompt or prompt.startswith('Choose:')
                else 'ready' if 'ready' in prompt
                else 'name' if 'llama' in prompt
                else 'yes_no')
        reply = self.answer(kind)
        self.text.append(f"{prompt}{reply}")
        return reply


def main():
    games = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    show = 'show' in sys.argv
    endings = collections.Counter()
    problems = []
    originals = {}
    for cls in (fighters.Hero, fighters.Dragon):  # watch HP so it can never go below 0
        originals[cls] = cls.take
        def take(self, damage, _orig=originals[cls]):
            _orig(self, damage)
            if self.hp < 0:
                problems.append(f'{self.name} went below 0 HP')
        cls.take = take
    met = []  # which dragon each game met
    dragon_init = fighters.Dragon.__init__
    def meet(self, name):
        met.append(name)
        dragon_init(self, name)
    fighters.Dragon.__init__ = meet
    for n in range(games):
        bot = BotUI()
        ui.use(bot)
        try:
            ending = asyncio.run(play())
        except Exception as e:
            problems.append(f'game {n}: {type(e).__name__}: {e}')
            continue
        dragon = met[-1]
        endings[(dragon, ending)] += 1
        leftover = [t for t in bot.text if re.search(r'\{(hero|dragon|weapon|damage)\}', t)]
        if leftover:
            problems.append(f'game {n}: unfilled text: {leftover[0]}')
        if show and n == 0:
            print('\n'.join(bot.text))
            print('=' * 100)
    print(f'{games} games')
    for (dragon, ending), count in sorted(endings.items()):
        print(f'  {dragon:<24} {ending:<26} {count}')
    print('PROBLEMS:', 'none' if not problems else '')
    for p in problems[:20]:
        print('  ', p)
    return 1 if problems else 0


if __name__ == '__main__':
    sys.exit(main())
