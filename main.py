"""Starts Slayer Classic in its game window:  python main.py
(python play_in_terminal.py plays it in the command prompt instead.)"""
import asyncio
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'game'))

import ui
from play import play
from window import Window


async def main():
    window = Window()
    ui.use(window)
    while await window.run(play()) == 'again':
        pass

asyncio.run(main())
