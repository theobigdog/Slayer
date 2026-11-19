"""ui: the one place the game talks to the player.

Game code never calls print() or input(); it awaits these instead, and whichever screen is in use
(the command prompt, or the game window in window.py) shows them its own way:

    await say("Skippy swipes at you for 6 hitpoints.")   # print a line (or a blank line with no text)
    await wait(2)                                         # dramatic pause
    await pause()                                         # wait for Enter / a click
    await clear()                                         # clear the screen
    text = await ask_text("¿Como se llama?  ")            # free typing
    yes = await yes_no("Intro (Y/N):  ")                  # True for Y / YES / YEP / YUP / YEAH
    i = await choose("What do you take?  ", labels)       # pick from a numbered list: always a good answer
    a = await choose_or_stall(prompt, labels)             # like choose, but the player can dither: returns the
                                                          #   number picked, or what they typed if it wasn't one
                                                          #   ('' in the window when they take too long)
    await show_battle(hero, dragon)                       # the health bars at the top of a round
    await effect('shake', who)                            # 'shake', 'flash_red', 'flash_fire', 'flash_white'
    await title_screen() / the_end()
    music('battle'); sting('victory'); sound('hit')       # the window plays these; the command prompt stays quiet

Colors go inside the text as tags: [red], [green], [magenta], [white], and [/] to go back to normal.
"""
import asyncio
import os
import re
import sys

YES = ["Y", "YES", "YEP", "YUP", "YEAH"]
STALL_SECONDS = 15  # in the window, dither this long over a weapon and the dragon closes in

_backend = None  # set by use(); every call below hands off to it


def use(backend):
    global _backend
    _backend = backend


async def say(text: str = ''):
    await _backend.say(text)

async def wait(seconds: float):
    await _backend.wait(seconds)

async def pause():
    await _backend.pause()

async def clear():
    await _backend.clear()

async def ask_text(prompt: str) -> str:
    return await _backend.ask_text(prompt)

async def yes_no(prompt: str) -> bool:
    return (await ask_text(prompt)).strip().upper() in YES

async def choose(prompt: str, labels: list) -> int:
    while True:
        answer = await _backend.choose_or_stall(prompt, labels, None, False, False)
        if isinstance(answer, int):
            return answer
        answer = answer.strip()
        if answer.isdigit() and 1 <= int(answer) <= len(labels):
            return int(answer) - 1
        await say("Fascinating.  Let's try one from the list, eh?")

async def choose_or_stall(prompt: str, labels: list, patience=STALL_SECONDS, quiet=False, hidden=False):
    """quiet: don't list the choices again (the command prompt only). hidden: don't show them at all."""
    return await _backend.choose_or_stall(prompt, labels, patience, quiet, hidden)

async def show_battle(hero, dragon, final=False):
    await _backend.show_battle(hero, dragon, final)

async def effect(name: str, who=None):
    await _backend.effect(name, who)

async def title_screen():
    await _backend.title_screen()

async def the_end():
    await _backend.the_end()

def music(name: str):
    _backend.music(name)

def sting(name: str):
    _backend.sting(name)

def sound(name: str):
    _backend.sound(name)


def status_words(fighter) -> list:
    import story
    return [story.STATUS_WORDS.get(s, s) for s in fighter.statuses]


TAG = re.compile(r'\[(red|green|magenta|white|/)\]')


class TerminalUI:
    """The command-prompt game. Works on Windows, Mac and Linux."""

    COLORS = {'red': '\033[1;31m', 'green': '\033[1;32m', 'magenta': '\033[1;35m', 'white': '\033[1;37m', '/': '\033[0m'}

    def __init__(self):
        if sys.platform == 'win32':
            os.system('')  # switches on color codes in the Windows command prompt

    def paint(self, text: str) -> str:
        return TAG.sub(lambda m: self.COLORS[m.group(1)], text) + ('\033[0m' if TAG.search(text) else '')

    async def say(self, text):
        print(self.paint(text))

    async def wait(self, seconds):
        await asyncio.sleep(seconds)

    async def pause(self):
        input(self.paint('[white]   ...[/]'))  # Enter to go on

    async def clear(self):
        print('\033[2J\033[H', end='')

    async def ask_text(self, prompt):
        return input(self.paint(prompt))

    async def choose_or_stall(self, prompt, labels, patience, quiet, hidden):
        if not quiet and not hidden:
            print()
            for number, label in enumerate(labels, 1):
                print(f"  {number}. {label}")
            print()
        answer = input(self.paint(prompt))
        if answer.strip().isdigit() and 1 <= int(answer.strip()) <= len(labels):
            return int(answer.strip()) - 1
        return answer

    async def show_battle(self, hero, dragon, final):
        if final:
            return
        def health(f):
            color = 'red' if f.hp <= 0.25 * f.max_hp else 'white'
            return f"[{color}]Health:  {f.hp}/{f.max_hp}[/]"
        await self.clear()
        width = max(len(hero.name), 20) + 6  # the dragon's column starts here
        gap = ' ' * (width - len(f'Health:  {hero.hp}/{hero.max_hp}'))
        print()
        print(self.paint(f"    [white]{hero.name:<{width}}{dragon.name}[/]"))
        print(self.paint(f"    {health(hero)}{gap}{health(dragon)}"))
        hero_words, dragon_words = ', '.join(status_words(hero)), ', '.join(status_words(dragon))
        if hero_words or dragon_words:
            print(self.paint(f"    [magenta]{hero_words:<{width}}{dragon_words}[/]"))
        print()

    async def effect(self, name, who):
        pass

    async def title_screen(self):
        print(self.paint('\n  [red]S L A Y E R[/]   [white]the classic[/]\n'))

    async def the_end(self):
        pass

    def music(self, name):
        pass

    def sting(self, name):
        pass

    def sound(self, name):
        pass
