"""Starts Slayer Classic in the command prompt:  python play_in_terminal.py   (python main.py opens the game window)"""
import asyncio
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'game'))

import ui
from play import play

ui.use(ui.TerminalUI())
try:
    asyncio.run(play())
except (KeyboardInterrupt, EOFError):
    print('\n\nChicken.')
