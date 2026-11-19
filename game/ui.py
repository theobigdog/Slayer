"""ui: the one place the game talks to the player.

Same idea (and the same call names) as Slayer_UI in Slayer_Next_Gen, so a game window can be plugged in later
without touching the game code. Game code never calls print() or input(); it awaits these instead:

    await say("Skippy swipes at you for 6 hitpoints.")   # print a line (or a blank line with no text)
    await wait(2)                                         # dramatic pause (was time.sleep)
    await pause()                                         # wait for Enter (was next())
    await clear()                                         # clear the screen
    text = await ask_text("Your choice?  ")               # free typing
    yes = await yes_no("Intro (Y/N):  ")                  # True for Y / YES / YEP / YUP / YEAH

Colors go inside the text as tags: [red], [green], [magenta], [white], and [/] to go back to normal.
"""
import asyncio
import os
import re
import sys

YES = ["Y", "YES", "YEP", "YUP", "YEAH"]

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
