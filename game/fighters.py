"""The hero, the three dragons, and the dice."""
import random

import story


def d10() -> int:
    return random.randint(1, 10)

def d20() -> int:
    return random.randint(1, 20)

def hitpoints(n: int) -> str:
    return f"{n} hitpoint" if n == 1 else f"{n} hitpoints"


# ---------- the hero --------------------------------------------------------------------------------------------

MAGIC_COIN = "Magic Coin"
BARE_HANDS = "Bare-Hands"
WEAPONS = {'Sword': (3, 6), 'Battle-Axe': (2, 8), 'Halberd': (1, 10)}  # damage, rolled fresh every swing
MENU = {MAGIC_COIN: "Magic Coin (Run Away, little girl)",
        'Sword': "Sword (3-6 damage)", 'Battle-Axe': "Battle-Axe (2-8 damage)", 'Halberd': "Halberd (1-10 damage)"}


class Hero:
    def __init__(self, name: str):
        self.name = name
        self.max_hp = random.randint(25, 50)
        self.hp = self.max_hp
        self.crit_chance = 15     # a crit when a d20 rolls over this (16-20, so 1 in 4)
        self.crit_multiplier = 3
        self.dodge = 8            # she dodges when a d10 rolls over this (9-10, so 1 in 5)
        self.inventory = [MAGIC_COIN, 'Sword', 'Battle-Axe', 'Halberd']
        self.grip = random.randint(1, 100)  # how hard she can strangle with her man-bun (vs the dragon's strangle)

    def rename(self):
        self.name = f"{random.choice(story.NAMES_1)} {random.choice(story.NAMES_2)}-{random.choice(story.NAMES_3)}"

    def swing(self, weapon: str) -> int:
        low, high = WEAPONS[weapon]
        return random.randint(low, high)

    def take(self, damage: int):
        self.hp = max(0, self.hp - damage)

    @property
    def alive(self) -> bool:
        return self.hp > 0


# ---------- the dragons -----------------------------------------------------------------------------------------
# Ted's numbers and notes from 2021. Rolls work like this:
#   hp: rolled once when she shows up
#   crit_chance: she crits when a d20 rolls over this
#   breath: she breathes fire (instead of clawing) when a d10 rolls over this
#   dodge: the hero misses when a d10 rolls over this (10 = she can't dodge)
#   strangle: the hero's grip (1-100) has to beat this to strangle her
#   weapon_break: the hero's weapon shatters when a d20 rolls over this
#   claws / fire: damage ranges

DRAGONS = {
    'Trogdor The Burninator': dict(  # Easy Mode, down the Left path
        hp=(60, 80),           # modest health
        crit_chance=18,        # poor aim, so crits less likely
        crit_multiplier=4,     # brutal attacks, due to extra, beefy arm
        breath=8,
        dodge=10,              # cannot dodge
        strangle=70,
        weapon_break=17,       # reasonable chance of breaking weapons, due to brutality of attacks
        claws=(2, 6), fire=(3, 8)),
    'Skippy': dict(  # Normal Mode, down the Right path
        hp=(80, 100),          # reasonable health, considering her youth
        crit_chance=16,        # reasonable aim, despite youth
        crit_multiplier=2.25,  # moderate crits, fairly young and not yet "strong"
        breath=6,
        dodge=6,               # good dodge, with young, quick reflexes, and the ability to read minds
        strangle=80,
        weapon_break=18,       # ok chance of breaking weapons - not yet experienced enough to be good at it
        claws=(3, 8), fire=(4, 8)),
    'The Ancient': dict(  # "Beast" (lolz) Mode, down the Lower path (Hard Mode only)
        hp=(80, 120),          # Beefy
        crit_chance=15,        # experience increases crit chance
        crit_multiplier=2.75,  # refined aim results in slightly increased crit damage
        breath=7,
        dodge=7,               # experience increases evasion
        strangle=90,
        weapon_break=15,       # strong attacks = more breakage
        claws=(4, 8), fire=(5, 10)),
}

PATHS = {'Left': 'Trogdor The Burninator', 'Right': 'Skippy', 'Lower': 'The Ancient'}


class Dragon:
    def __init__(self, name: str):
        self.name = name
        for stat, value in DRAGONS[name].items():
            setattr(self, stat, value)
        self.max_hp = random.randint(*self.hp)
        self.hp = self.max_hp

    def fireball(self) -> int:
        return random.randint(*self.fire)

    def take(self, damage: int):
        self.hp = max(0, self.hp - damage)

    @property
    def alive(self) -> bool:
        return self.hp > 0
