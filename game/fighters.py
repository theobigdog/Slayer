"""The hero, the three dragons, the loot, and the dice."""
import random

import story


def d10() -> int:
    return random.randint(1, 10)

def d20() -> int:
    return random.randint(1, 20)

def hitpoints(n: int) -> str:
    return f"{n} hitpoint" if n == 1 else f"{n} hitpoints"


# ---------- weapons and things you carry -------------------------------------------------------------------------

MAGIC_COIN = "Magic Coin"
BARE_HANDS = "Bare-Hands"
DUCK = "Duck"

# Weapons: damage range, rolled every swing. 'pierce': it finds the gaps in The Ancient's armor.
WEAPONS = {
    'Sword': dict(damage=(3, 6)),
    'Battle-Axe': dict(damage=(2, 8)),
    'Halberd': dict(damage=(1, 10), pierce=True),
    # found in the dragons' hoards:
    'Peasant Pitchfork': dict(damage=(2, 9), pierce=True),
    'Femur Club': dict(damage=(4, 8)),
    'Dragon-Tooth Dagger': dict(damage=(5, 9), pierce=True),
}

# Things you drink: how much they heal, and anything else they do.
DRINKS = {
    "Trogdor's Mead": dict(heal=(10, 15), drunk=3),
    "Healing Draught": dict(heal=(15, 22)),
}

# What's in each hoard. After a win you see three of these and keep one.
HOARDS = {
    'Trogdor The Burninator': ["Trogdor's Mead", 'Peasant Pitchfork', 'Beefy-Arm Gauntlet', 'Whetstone', 'Spare Sword'],
    'Skippy': ['Femur Club', "Skippy's Tiara", 'Healing Draught', 'Whetstone', 'Spare Sword'],
    'The Ancient': [],  # (nobody leaves The Ancient's cave)
}
# The loot that isn't a weapon or a drink: what it does is in Hero.take_loot.
TRINKETS = {'Beefy-Arm Gauntlet', "Skippy's Tiara", 'Whetstone', 'Spare Sword'}


# ---------- the hero --------------------------------------------------------------------------------------------

class Hero:
    def __init__(self, name: str):
        self.name = name
        self.max_hp = random.randint(25, 50)
        self.hp = self.max_hp
        self.crit_chance = 15     # a crit when a d20 rolls over this (16-20, so 1 in 4)
        self.crit_multiplier = 3
        self.dodge = 8            # she dodges when a d10 rolls over this (9-10, so 1 in 5)
        self.bonus_damage = 0     # the Beefy-Arm Gauntlet, Whetstones
        self.inventory = [MAGIC_COIN, 'Sword', 'Battle-Axe', 'Halberd']
        self.drinks = {}          # name -> how many
        self.grip = random.randint(1, 100)  # how hard she can strangle with her man-bun (vs the dragon's strangle)
        self.statuses = {}        # 'burning', 'drunk', 'terrified' -> turns left; 'damp' -> it doesn't dry
        self.ducking = False
        self.dropped_weapons = False  # she froze up and went for the man-bun
        self.last_weapon = None
        self.wins = 0

    def rename(self):
        self.name = f"{random.choice(story.NAMES_1)} {random.choice(story.NAMES_2)}-{random.choice(story.NAMES_3)}"

    @property
    def weapons(self) -> list:
        return [item for item in self.inventory if item in WEAPONS]

    def menu(self) -> list:
        """What she can do this turn, in menu order: (what, the label)."""
        options = [(w, f"{w} ({WEAPONS[w]['damage'][0] + self.bonus_damage}-{WEAPONS[w]['damage'][1] + self.bonus_damage} damage)")
                   for w in self.weapons]
        options += [(d, f"{d} x{n} ({story.DRINK_LABELS[d]})") for d, n in self.drinks.items() if n]
        options.append((DUCK, story.DUCK_LABEL))
        if MAGIC_COIN in self.inventory:
            options.append((MAGIC_COIN, "Magic Coin (Run Away, little girl)"))
        return options

    def swing(self, weapon: str) -> int:
        low, high = WEAPONS[weapon]['damage']
        damage = random.randint(low, high) + self.bonus_damage
        if 'drunk' in self.statuses:
            damage += 2
        if 'terrified' in self.statuses:
            damage = max(1, damage // 2)
        return damage

    def take(self, damage: int):
        self.hp = max(0, self.hp - damage)

    def heal(self, amount: int) -> int:
        amount = min(amount, self.max_hp - self.hp)
        self.hp += amount
        return amount

    def tick(self, status: str):
        """One turn of a status wears off."""
        if status in self.statuses and status != 'damp':
            self.statuses[status] -= 1
            if self.statuses[status] <= 0:
                del self.statuses[status]

    def take_loot(self, item: str):
        if item in WEAPONS:
            self.inventory.append(item)
        elif item in DRINKS:
            self.drinks[item] = self.drinks.get(item, 0) + 2
        elif item == 'Beefy-Arm Gauntlet':
            self.bonus_damage += 2
        elif item == 'Whetstone':
            self.bonus_damage += 1
        elif item == "Skippy's Tiara":
            self.dodge -= 1  # dodges on 8-10 instead of 9-10
        elif item == 'Spare Sword':
            self.inventory.append('Sword')  # (a second Sword is fine: one more thing to break)

    def grow(self) -> int:
        """After a win: tougher, a bit luckier, and patched up. Returns how much max HP she gained."""
        gain = random.randint(6, 10)
        self.max_hp += gain
        self.hp = self.max_hp
        self.crit_chance = max(12, self.crit_chance - 1)
        self.statuses = {k: v for k, v in self.statuses.items() if k == 'damp'}  # (the damp stays)
        self.wins += 1
        return gain

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
# New in the upgrade (Nov 2026): each dragon's trick, and her big attack every few turns.

DRAGONS = {
    'Trogdor The Burninator': dict(  # Easy Mode, down the Left path
        hp=(60, 80),           # modest health
        crit_chance=18,        # poor aim, so crits less likely
        crit_multiplier=4,     # brutal attacks, due to extra, beefy arm
        breath=8,
        dodge=10,              # cannot dodge
        strangle=70,
        weapon_break=17,       # reasonable chance of breaking weapons, due to brutality of attacks
        claws=(2, 6), fire=(3, 8),
        big_every=4,           # BURNINATE: winds up, then lets rip, every 4th turn
        big_multiplier=2.5,
        hiccups=0.2,           # she's still drunk: 1 turn in 5 she hiccups instead of attacking
        art='trogdor', color='green', song='drunk', fight_song='battle'),
    'Skippy': dict(  # Normal Mode, down the Right path
        hp=(80, 100),          # reasonable health, considering her youth
        crit_chance=16,        # reasonable aim, despite youth
        crit_multiplier=2.25,  # moderate crits, fairly young and not yet "strong"
        breath=6,
        dodge=6,               # good dodge, with young, quick reflexes, and the ability to read minds
        strangle=80,
        weapon_break=18,       # ok chance of breaking weapons - not yet experienced enough to be good at it
        claws=(3, 8), fire=(4, 8),
        mind_reader=3,         # use the same weapon twice in a row and she's that much harder to hit
        puff_up=1.4,           # at half health she doubles in size again: her hits get this much harder
        art='skippy', color='cyan', song='skippy', fight_song='battle'),
    'The Ancient': dict(  # "Beast" (lolz) Mode, down the Lower path
        hp=(80, 120),          # Beefy
        crit_chance=15,        # experience increases crit chance
        crit_multiplier=2.75,  # refined aim results in slightly increased crit damage
        breath=7,
        dodge=7,               # experience increases evasion
        strangle=90,
        weapon_break=15,       # strong attacks = more breakage
        claws=(4, 8), fire=(5, 10),
        armor=2,               # her scales take this much off every hit, unless the weapon pierces
        big_every=3,           # INFERNO: draws a breath, then lets rip, every 3rd turn
        big_multiplier=2,
        enrage_at=0.3,         # at 30% health she's FURIOUS: more crits
        art='ancient', color='red', song='ancient', fight_song='inferno'),
}

# Tuning for the run (Nov 2026), on top of Ted's numbers above: (her health, her damage), each a multiplier.
# Tuned by simulation (tools/bot_test.py's smart bot) so a sensible player beats the first dragon about 80% of the
# time, the second about half the time after that, and The Ancient about half the time after both (about 1 in 5
# sensible players win the whole run). Straight to The Ancient with Kool-Aid is meant to be much harder.
SCALE = {'Trogdor The Burninator': (0.85, 0.85), 'Skippy': (0.65, 0.55), 'The Ancient': (0.7, 0.7)}

PATHS = {'Left': 'Trogdor The Burninator', 'Right': 'Skippy', 'Lower': 'The Ancient'}


class Dragon:
    def __init__(self, name: str):
        self.name = name
        self.armor = 0
        self.big_every = 0
        self.big_multiplier = 1
        self.hiccups = 0
        self.mind_reader = 0
        self.puff_up = 0
        self.enrage_at = 0
        for stat, value in DRAGONS[name].items():
            setattr(self, stat, value)
        self.hp_scale, self.damage_scale = SCALE[name]
        self.max_hp = max(1, round(random.randint(*self.hp) * self.hp_scale))
        self.hp = self.max_hp
        self.turn = 0
        self.winding_up = False   # next turn is the big one
        self.puffed = False
        self.enraged = False

    def fireball(self) -> int:
        return max(1, round(random.randint(*self.fire) * self.damage_scale))

    def clawing(self) -> int:
        return max(1, round(random.randint(*self.claws) * self.damage_scale))

    def take(self, damage: int):
        self.hp = max(0, self.hp - damage)

    @property
    def alive(self) -> bool:
        return self.hp > 0

    @property
    def statuses(self) -> dict:
        shown = {}
        if self.winding_up:
            shown['winding up'] = 1
        if self.puffed:
            shown['puffed up'] = 1
        if self.enraged:
            shown['FURIOUS'] = 1
        return shown
