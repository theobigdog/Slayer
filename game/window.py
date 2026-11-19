"""window: plays Slayer Classic in a game window that looks like an old green-screen computer.

The game logic never imports this file. main.py picks it with ui.use(Window()), and from then on every
ui.say / ui.choose / ui.show_battle ... lands here.

How the two halves share time: the game runs as one asyncio task, and the frame loop in run() runs beside it.
When the game waits on the player (pause, choose, ask_text), it waits on a Future that the frame loop
completes when the player clicks or presses a key. say() waits while its line types out, so sounds and
effects land at the right moment in the text.
"""
import asyncio
import math
import random
import re
import traceback
from pathlib import Path

import pygame

import art
import sound
import ui

W, H = 1280, 720
ROOT = Path(__file__).resolve().parent.parent
FONT_FILE = ROOT / 'assets' / 'fonts' / 'DejaVuSansMono-Bold.ttf'

# The green screen.
BG = (5, 13, 7)
GREEN = (70, 245, 120)
DIM = (36, 130, 64)
FAINT = (22, 70, 36)
BRIGHT = (205, 255, 215)
RED = (255, 84, 60)
MAGENTA = (255, 110, 230)
AMBER = (255, 190, 70)
CYAN = (90, 220, 255)
TAGS = {'red': RED, 'green': (140, 255, 160), 'magenta': MAGENTA, 'white': BRIGHT}
TAG = re.compile(r'\[(red|green|magenta|white|/)\]')
DRAGON_COLORS = {'green': (150, 255, 90), 'cyan': CYAN, 'red': (255, 110, 60)}

MARGIN = 34
TOP = 34                 # below the title bar
BATTLE_H = 290           # the battle panel's height, when there's a fight on
TYPE_SPEED = 110         # characters a second
EFFECT_TIME = 0.35


class Line:
    def __init__(self, text: str, menu=None):
        self.text = text
        self.menu = menu  # (menu number, choice index) for a clickable menu row


def cells(text: str, base=GREEN) -> list:
    """'[red]Hot[/] dog' -> [('H', RED), ('o', RED), ('t', RED), (' ', GREEN), ...]"""
    out, color = [], base
    pos = 0
    for m in TAG.finditer(text):
        out += [(ch, color) for ch in text[pos:m.start()]]
        color = base if m.group(1) == '/' else TAGS[m.group(1)]
        pos = m.end()
    out += [(ch, color) for ch in text[pos:]]
    return out


def wrap(row_cells: list, width: int) -> list:
    """Word-wraps a line of cells into rows of at most width characters."""
    if not row_cells:
        return [[]]
    rows = []
    while len(row_cells) > width:
        cut = width
        while cut > 0 and row_cells[cut][0] != ' ':
            cut -= 1
        if cut == 0:
            cut = width
        rows.append(row_cells[:cut])
        row_cells = row_cells[cut:]
        while row_cells and row_cells[0][0] == ' ':
            row_cells = row_cells[1:]
    rows.append(row_cells)
    return rows


class Window:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('SLAYER (the classic)')
        self.screen = pygame.display.set_mode((W, H), pygame.SCALED | pygame.RESIZABLE)
        self.canvas = pygame.Surface((W, H))
        self.font = pygame.font.Font(str(FONT_FILE), 19)
        self.big = pygame.font.Font(str(FONT_FILE), 26)
        self.small = pygame.font.Font(str(FONT_FILE), 15)
        self.cw, self.ch = self.font.size('M')[0], self.font.get_linesize() + 2
        self.clock = pygame.time.Clock()
        self.ink = {}  # (text, color, font) -> rendered surface
        self.scanlines = self.make_scanlines()
        self.vignette = self.make_vignette()
        self.reset_text()
        self.mode = 'game'        # 'boot', 'title', 'game'
        self.battle = None        # (hero, dragon) while a fight is on screen
        self.waiting = None       # (kind, future, extra) while the game waits on the player
        self.typed = ''
        self.menu_id = 0
        self.menu_rects = []      # (rect, index) for the menu rows on screen
        self.hover = None
        self.scroll = 0           # rows scrolled back with the mouse wheel
        self.effects = []         # (name, who, started)
        self.floaters = []        # [text, color, x, y, started]
        self.seen_hp = {}
        self.now = 0.0
        self.title_started = 0.0
        self.volume_rect = pygame.Rect(W - 190, 6, 180, 22)
        self.done = False

    def reset_text(self):
        self.lines = []
        self.revealed = 0.0
        self.rows_cache = (None, [])
        self.version = 0

    # ---------- what the game calls (see ui.py) ---------------------------------------------------------------

    async def say(self, text=''):
        self.lines.append(Line(text))
        self.changed()
        await self.typed_out()

    async def wait(self, seconds):
        await self.typed_out()
        await asyncio.sleep(seconds)

    async def pause(self):
        await self.typed_out()
        await self.wait_for('pause')

    async def clear(self):
        self.reset_text()
        self.battle = None
        self.scroll = 0

    async def ask_text(self, prompt):
        return await self.prompt(prompt, 'text')

    async def choose_or_stall(self, prompt, labels, patience, quiet, hidden):
        if hidden:
            return await self.prompt(prompt, 'text')
        self.menu_id += 1
        self.lines.append(Line(''))
        for i, label in enumerate(labels):
            self.lines.append(Line(f'  {i + 1}. {label}', menu=(self.menu_id, i)))
        self.lines.append(Line(''))
        self.changed()
        return await self.prompt(prompt, 'choose', labels, patience)

    async def show_battle(self, hero, dragon, final):
        if not final:
            await self.clear()
        self.battle = (hero, dragon)
        for who in (hero, dragon):
            self.seen_hp.setdefault(id(who), who.hp)

    async def effect(self, name, who):
        self.effects.append((name, who, self.now))
        await asyncio.sleep(0)

    async def title_screen(self):
        self.mode = 'boot'
        self.title_started = self.now
        sound.play('title')
        await self.wait_for('title')
        self.mode = 'game'

    async def the_end(self):
        self.lines.append(Line(''))
        self.lines.append(Line('[white][ ENTER to play again.  ESC to quit. ][/]'))
        self.changed()
        await self.typed_out()
        await self.wait_for('end')

    def music(self, name):
        sound.play(name)

    def sting(self, name):
        sound.sting(name)

    def sound(self, name):
        sound.effect(name)

    # ---------- waiting on the player ---------------------------------------------------------------------------

    async def wait_for(self, kind, extra=None):
        future = asyncio.get_event_loop().create_future()
        self.waiting = (kind, future, extra)
        self.typed = ''
        try:
            return await future
        finally:
            self.waiting = None

    async def typed_out(self):
        while self.revealed < self.total_chars():
            await asyncio.sleep(0)

    async def prompt(self, prompt, kind, labels=None, patience=None):
        self.lines.append(Line(prompt))
        self.prompt_line = self.lines[-1]
        self.prompt_text = prompt
        self.changed()
        await self.typed_out()
        self.asked_at = self.now
        answer = await self.wait_for(kind, (labels, patience))
        shown = labels[answer] if isinstance(answer, int) else answer
        self.prompt_line.text = f'{prompt}[white]{shown}[/]'
        self.changed()
        self.revealed = self.total_chars()
        return answer

    def answer(self, value):
        kind, future, _ = self.waiting
        if not future.done():
            future.set_result(value)
        self.scroll = 0

    # ---------- the text ------------------------------------------------------------------------------------------

    def changed(self):
        self.version += 1

    def text_area(self) -> pygame.Rect:
        top = TOP + (BATTLE_H if self.battle else 8)
        return pygame.Rect(MARGIN, top, W - 2 * MARGIN, H - top - 16)

    def rows(self) -> list:
        """Every line, word-wrapped: [(cells, line)]."""
        if self.rows_cache[0] != (self.version, bool(self.battle)):
            width = self.text_area().width // self.cw
            out = []
            for line in self.lines:
                for row in wrap(cells(line.text), width):
                    out.append((row, line))
            self.rows_cache = ((self.version, bool(self.battle)), out)
        return self.rows_cache[1]

    def total_chars(self) -> int:
        return sum(max(1, len(row)) for row, _ in self.rows())

    # ---------- input ---------------------------------------------------------------------------------------------

    def handle(self, event):
        if event.type == pygame.MOUSEWHEEL:
            self.scroll = max(0, self.scroll + event.y * 3)
            return
        if event.type == pygame.MOUSEMOTION:
            self.hover = next((i for rect, i in self.menu_rects if rect.collidepoint(event.pos)), None)
            return
        clicked = event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
        key = event.key if event.type == pygame.KEYDOWN else None
        if clicked and self.volume_rect.collidepoint(event.pos):
            self.click_volume(event.pos)
            return
        if key == pygame.K_m and not (self.waiting and self.waiting[0] == 'text'):
            sound.toggle()
            return
        enter = key in (pygame.K_RETURN, pygame.K_KP_ENTER)
        if (clicked or enter or key == pygame.K_SPACE) and self.revealed < self.total_chars():
            self.revealed = self.total_chars()  # finish typing this page
            return
        if not self.waiting:
            return
        kind, future, extra = self.waiting
        if kind in ('pause', 'title') and (clicked or enter or key == pygame.K_SPACE):
            if kind == 'title' and self.now - self.title_started < self.boot_time():
                self.title_started = self.now - self.boot_time()  # skip the boot-up
                return
            sound.effect('select')
            self.answer(True)
        elif kind == 'end':
            if enter or clicked:
                self.answer(True)
            elif key == pygame.K_ESCAPE:
                self.done = True
        elif kind == 'text':
            if event.type == pygame.TEXTINPUT and len(self.typed) < 40:
                self.typed += event.text
                sound.effect('type')
            elif key == pygame.K_BACKSPACE:
                self.typed = self.typed[:-1]
            elif enter:
                sound.effect('select')
                self.answer(self.typed)
        elif kind == 'choose':
            labels = extra[0]
            if clicked:
                picked = next((i for rect, i in self.menu_rects if rect.collidepoint(event.pos)), None)
                if picked is not None:
                    self.answer(picked)
            elif event.type == pygame.TEXTINPUT and event.text.isdigit():
                number = int(event.text)
                if 1 <= number <= len(labels):
                    self.answer(number - 1)

    def click_volume(self, pos):
        x = pos[0] - (self.volume_rect.x + 30)
        if x < 0:
            sound.toggle()
        else:
            sound.set_volume(min(1.0, x / 140))

    def boot_time(self) -> float:
        return 0.35 * len(art.BOOT) + 0.8

    # ---------- the frame loop ------------------------------------------------------------------------------------

    async def run(self, game) -> str:
        task = asyncio.ensure_future(game)
        pygame.key.start_text_input()
        while True:
            self.clock.tick(60)
            self.now = pygame.time.get_ticks() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    task.cancel()
                    return 'quit'
                self.handle(event)
            if self.done:
                task.cancel()
                return 'quit'
            if task.done():
                if not task.cancelled() and task.exception():
                    self.crashed(task.exception())
                    task = asyncio.ensure_future(self.wait_for('end'))
                    continue
                return 'again'
            self.advance()
            self.draw()
            await asyncio.sleep(0)

    def crashed(self, error):
        text = ''.join(traceback.format_exception(error))
        print(text)
        try:
            (ROOT / 'crash_log.txt').write_text(text, encoding='utf-8')
        except Exception:
            pass
        self.reset_text()
        self.battle = None
        self.lines = [Line('[red]The game crashed.  Sorry![/]')] + [Line(t) for t in text.strip().splitlines()[-6:]]
        self.lines.append(Line('(The whole error is in crash_log.txt, in the game folder.)'))
        self.changed()
        self.revealed = self.total_chars()

    def advance(self):
        dt = self.clock.get_time() / 1000
        total = self.total_chars()
        if self.revealed < total:
            before = int(self.revealed)
            self.revealed = min(total, self.revealed + TYPE_SPEED * dt * (1 + (total - self.revealed) / 600))
            if int(self.revealed) // 4 != before // 4:
                sound.effect('type')
        if self.waiting and self.waiting[0] == 'choose':
            patience = self.waiting[2][1]
            if patience and self.now - self.asked_at > patience:
                self.answer('')  # took too long: the dragon closes in
        if self.battle:
            for who in self.battle:
                before = self.seen_hp.get(id(who), who.hp)
                if who.hp != before:
                    self.add_floater(who, before - who.hp)
                    self.seen_hp[id(who)] = who.hp

    def add_floater(self, who, change):
        hero = who is self.battle[0]
        x = MARGIN + 10 + 28 * self.cw if hero else W - MARGIN - 50  # just past her HP numbers
        self.floaters.append([str(abs(change)), RED if change > 0 else CYAN, x + random.randint(-12, 12), TOP + 84, self.now])

    # ---------- drawing ------------------------------------------------------------------------------------------

    def text(self, text, color, pos, font=None, surface=None):
        font = font or self.font
        key = (text, color, id(font))
        if key not in self.ink:
            if len(self.ink) > 3000:
                self.ink.clear()
            self.ink[key] = font.render(text, True, color)
        (surface or self.canvas).blit(self.ink[key], pos)
        return self.ink[key].get_width()

    def draw_cells(self, row, x, y, limit=None, highlight=False):
        if limit is not None:
            row = row[:limit]
        if highlight:
            pygame.draw.rect(self.canvas, GREEN, (x - 4, y - 1, max(len(row), 1) * self.cw + 8, self.ch))
        i = 0
        while i < len(row):
            color = row[i][1]
            j = i
            while j < len(row) and row[j][1] == color:
                j += 1
            self.text(''.join(c for c, _ in row[i:j]), BG if highlight else color, (x + i * self.cw, y))
            i = j

    def draw(self):
        c = self.canvas
        c.fill(BG)
        if self.mode in ('boot', 'title') or (self.waiting and self.waiting[0] == 'title'):
            self.draw_title()
        else:
            if self.battle:
                self.draw_battle()
            self.draw_text()
        self.draw_top_bar()
        self.draw_floaters()
        # Effects: shakes and flashes.
        dx = dy = 0
        live = []
        for name, who, started in self.effects:
            age = self.now - started
            if age > EFFECT_TIME:
                continue
            live.append((name, who, started))
            fade = 1 - age / EFFECT_TIME
            if name == 'shake':
                if self.battle and who is self.battle[1]:
                    continue  # the dragon getting hit: only her picture shakes (see draw_battle)
                dx, dy = random.randint(-7, 7) * fade, random.randint(-5, 5) * fade
            else:
                color = {'flash_red': RED, 'flash_fire': (255, 140, 30), 'flash_white': BRIGHT}.get(name, RED)
                flash = pygame.Surface((W, H))
                flash.fill(color)
                flash.set_alpha(int(90 * fade))
                c.blit(flash, (0, 0))
                if name != 'flash_white':
                    dx, dy = random.randint(-4, 4) * fade, random.randint(-3, 3) * fade
        self.effects = live
        self.screen.fill(BG)
        self.screen.blit(c, (dx, dy))
        self.crt()
        pygame.display.flip()

    def crt(self):
        """The old monitor: a soft glow, scanlines, darker corners, and a faint flicker."""
        glow = pygame.transform.smoothscale(self.screen, (W // 5, H // 5))
        glow = pygame.transform.smoothscale(glow, (W, H))
        glow.fill((110, 110, 110), special_flags=pygame.BLEND_MULT)
        self.screen.blit(glow, (0, 0), special_flags=pygame.BLEND_ADD)
        self.screen.blit(self.scanlines, (0, 0))
        self.screen.blit(self.vignette, (0, 0))
        if random.random() < 0.03:
            flicker = pygame.Surface((W, H))
            flicker.fill((0, 0, 0))
            flicker.set_alpha(14)
            self.screen.blit(flicker, (0, 0))

    def make_scanlines(self):
        s = pygame.Surface((W, H), pygame.SRCALPHA)
        for y in range(0, H, 3):
            pygame.draw.line(s, (0, 0, 0, 70), (0, y), (W, y))
        return s

    def make_vignette(self):
        small = pygame.Surface((64, 36), pygame.SRCALPHA)
        for y in range(36):
            for x in range(64):
                d = math.hypot((x - 31.5) / 32, (y - 17.5) / 18)
                small.set_at((x, y), (0, 0, 0, int(min(200, max(0, (d - 0.55) * 330)))))
        return pygame.transform.smoothscale(small, (W, H))

    def draw_top_bar(self):
        pygame.draw.rect(self.canvas, GREEN, (0, 0, W, 30))
        self.text(' SLAYER.EXE  (the classic)', BG, (8, 4))
        on = sound.volume > 0
        x = self.volume_rect.x
        self.text('♪' if on else '♪x', BG, (x + 2, 4))
        bars = int(round(sound.volume * 10))
        self.text('█' * bars + '░' * (10 - bars), BG, (x + 30, 4))
        if self.battle:
            hero, dragon = self.battle
            self.text(f'{hero.name}  vs  {dragon.name}', BG, (W // 2 - len(f'{hero.name}  vs  {dragon.name}') * self.cw // 2, 4))

    def draw_title(self):
        age = self.now - self.title_started
        y = 70
        for i, row in enumerate(art.BOOT):
            if age > 0.35 * i:
                self.text(row, DIM, (MARGIN + 20, y + i * self.ch))
        if age < self.boot_time():
            if int(self.now * 2) % 2:
                self.text('█', GREEN, (MARGIN + 20, y + len(art.BOOT) * self.ch))
            return
        top = 300
        size = 16
        for r, row in enumerate(art.BANNER):
            for col, ch in enumerate(row):
                if ch != ' ':
                    lit = random.random() > 0.015
                    pygame.draw.rect(self.canvas, RED if lit else (120, 30, 20),
                                     (W // 2 - len(row) * size // 2 + col * size, top + r * size * 1.3, size - 2, size * 1.3 - 2))
        self.text(art.SWORD, BRIGHT, (W // 2 - len(art.SWORD) * self.cw // 2, top + 120))
        import story
        self.text(story.TITLE_SUBTITLE, GREEN, (W // 2 - len(story.TITLE_SUBTITLE) * self.cw // 2, top + 165))
        if int(self.now * 1.6) % 2:
            msg = '[ PRESS ENTER ]'
            self.text(msg, BRIGHT, (W // 2 - len(msg) * self.cw // 2, top + 250))

    def draw_text(self):
        area = self.text_area()
        rows = self.rows()
        visible = area.height // self.ch
        # How far the typewriter has got: whole rows, then part of one.
        shown, left = [], self.revealed
        for row, line in rows:
            if left <= 0:
                break
            shown.append((row, line, int(min(len(row), left))))
            left -= max(1, len(row))
        end = max(0, len(shown) - self.scroll)
        start = max(0, end - visible)
        self.menu_rects = []
        active_menu = self.menu_id if self.waiting and self.waiting[0] == 'choose' else None
        y = area.y
        for row, line, limit in shown[start:end]:
            clickable = line.menu and line.menu[0] == active_menu
            if clickable:
                rect = pygame.Rect(area.x - 4, y - 1, area.width, self.ch)
                self.menu_rects.append((rect, line.menu[1]))
            self.draw_cells(row, area.x, y, limit, highlight=clickable and self.hover == line.menu[1])
            y += self.ch
        # The cursor: what she's typing, or a blinking block.
        if self.waiting and self.revealed >= self.total_chars() and self.scroll == 0:
            kind = self.waiting[0]
            last_row = shown[end - 1][0] if end else []
            cx = area.x + len(last_row) * self.cw
            cy = y - self.ch
            if kind == 'text':
                self.text(self.typed, BRIGHT, (cx, cy))
                cx += len(self.typed) * self.cw
            blink = int(self.now * 2.5) % 2
            if kind == 'pause':
                if blink:
                    self.text('▼', GREEN, (area.right - self.cw * 2, area.bottom - self.ch))
            elif kind in ('text', 'choose') and blink:
                self.text('█', GREEN, (cx, cy))
        if self.scroll:
            self.text('(scrolled back: wheel down to return)', DIM, (area.right - 420, area.bottom - self.ch), self.small)

    def draw_battle(self):
        hero, dragon = self.battle
        c = self.canvas
        box = pygame.Rect(MARGIN - 10, TOP + 4, W - 2 * MARGIN + 20, BATTLE_H - 14)
        pygame.draw.rect(c, DIM, box, 2)
        # The hero, left.
        x, y = MARGIN + 10, TOP + 22
        self.text('YOU', DIM, (x, y), self.small)
        self.text(hero.name, BRIGHT, (x, y + 18), self.big)
        self.hp_bar(hero, x, y + 58)
        self.status_line(hero, x, y + 92)
        carrying = ', '.join(hero.weapons) or 'nothing but your man-bun'
        drinks = ', '.join(f'{k} x{v}' for k, v in hero.drinks.items())
        notes = wrap(cells(f'Carrying: {carrying}.' + (f'  Drinks: {drinks}.' if drinks else ''), DIM), 44)
        for i, row in enumerate(notes[:4]):
            self.text(''.join(ch for ch, _ in row), DIM, (x, y + 124 + i * 18), self.small)
        if dragon.winding_up:
            if int(self.now * 3) % 2:
                self.text('!! SOMETHING BIG IS COMING.  DUCK? !!', AMBER, (x, y + 200))
        # The dragon, right: her art, name and health.
        color = DRAGON_COLORS.get(dragon.color, GREEN)
        if dragon.enraged:
            color = RED
        art_rows = art.DRAGONS[dragon.art].strip('\n').splitlines()
        ax = 500
        bob = math.sin(self.now * (5 if dragon.winding_up else 1.6)) * (3 if dragon.alive else 0)
        hit = any(n in ('shake', 'flash_white') and w is dragon and self.now - s < EFFECT_TIME for n, w, s in self.effects)
        for i, row in enumerate(art_rows):
            jitter = random.randint(-3, 3) if hit else 0
            self.text(row, color if dragon.alive else FAINT, (ax + jitter, TOP + 16 + i * 19 + bob), self.small)
        nx = W - MARGIN - 300
        self.text('DRAGON', DIM, (nx, TOP + 22), self.small)
        self.text(dragon.name, color, (nx, TOP + 40), self.big if len(dragon.name) < 16 else self.font)
        self.hp_bar(dragon, nx, TOP + 80)
        self.status_line(dragon, nx, TOP + 114)

    def hp_bar(self, who, x, y):
        cells_n = 16
        full = round(cells_n * who.hp / who.max_hp) if who.max_hp else 0
        color = RED if who.hp <= 0.25 * who.max_hp else AMBER if who.hp <= 0.5 * who.max_hp else GREEN
        self.text('HP', DIM, (x, y))
        self.text('█' * full, color, (x + 3 * self.cw, y))
        self.text('░' * (cells_n - full), FAINT, (x + (3 + full) * self.cw, y))
        self.text(f'{who.hp}/{who.max_hp}', BRIGHT, (x + (4 + cells_n) * self.cw, y))

    def status_line(self, who, x, y):
        for word in ui.status_words(who):
            colour = RED if word in ('ON FIRE', 'FURIOUS') else AMBER if word in ('winding up', 'puffed up') else MAGENTA
            w = self.text(f'[{word}]', colour, (x, y), self.small)
            x += w + 10

    def draw_floaters(self):
        live = []
        for f in self.floaters:
            age = self.now - f[4]
            if age > 1.2:
                continue
            live.append(f)
            self.text(f[0], f[1], (f[2], f[3] - age * 50), self.big)
        self.floaters = live
