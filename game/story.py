"""Ted's story for Slayer Classic: every word the narrator says lives here, nothing else.

Copied from Slayer_v1_0.py (June 2021), word for word except a handful of clear typos (see the README).

How it's laid out:
- A "beat" is a list of lines. The game shows a beat, then waits for Enter before the next one.
- A story is a list of beats.
- A number inside a beat is a dramatic pause in seconds, like the old time.sleep().
- {hero} and {dragon} get swapped for the hero's and the dragon's names.
- Color tags work like in Slayer_Next_Gen: [red]...[/], [white]...[/], [green]...[/], [magenta]...[/].
"""

# ---------- getting started ---------------------------------------------------------------------------------

ASK_NAME = "¿Como se llama?  "
RENAME = ["No.  No, that won't do at all.",
          "You need something with more pep.  More flavor!"]
NEW_NAME = ["How about {hero}?  Yes, I like that.",
            "Henceforth, you shall be known as {hero}"]
ASK_READY = "Are you ready, {hero}?  "
HARD_MODE_CODE = "Kool-Aid"
HARD_MODE_ON = "Hard-mode enabled"
NOT_READY = "Alrighty then.  Like it or not, this bus ain't stoppin'."
ASK_INTRO = "Intro (Y/N):  "
NO_INTRO = "In a hurry, are we?  Death will come for you either way!!"

INTRO = [
    ['After hours of hunting through the caves of The Dragon Cliffs, you have stumbled upon a tunnel, hidden between what look like a few stalagmites and stalactites.',
     'As you get closer, the spikes look much more like teeth of some kind.  How had you never noticed these before?',
     'A foul odor emanates from the tunnel.  Death.  Decay.  Dustmites.',
     'Deep gouges, like those you would expect to come from something with awfully strong claws, line the tunnel, almost like the passageway had been dug out by a giant cougar.'],
    ['You try not to get too excited, as, this is not likely the halls for which you have been searching.',
     'But as you continue, you find large patches of stone which appear to have been burned straight through, scorch-marks still obvious on the surfaces; somehow still looking like fresh marks.',
     'You begin to find small mounds of what appear to be the remnants of critters found in the nearby forests.'],
    ['Scattered amongst these bits, you catch a patch of color in one of the heaps, and move closer to investigate.',
     'You recognize the emblem on the shred of fabric you find in that heap:  2 mice, fighting over a hunk of bread as a trap begins to close on them; the family crest of your closest neighbors.  They are a silly family.',
     'Well, they were.  These particular neighbors are the reason you are searching here, once again, for they are those, most recently devastated by what appears to have been a dragon attack.',
     '"This must be it!" you say to yourself.  "I think I\'ve finally found it!!"'],
    ['Having searched for the fabled Halls of the Wyrm since you were a young child, the thrill in this moment is unlike any you\'ve felt before.',
     'Some would even say you are acting as giddy as a school-girl.  Stop skipping down the path already.  I can see you.'],
    ['After an hour of trekking down the tunnel, you reach a fork in the road.',
     'To the left veers a twisting, turning path along a cliffside with a sheer drop-off, the bottom of which is not in sight.',
     'To the right, a path through what looks like freshly dug and melted solid rock, disappears after a bend, a few dozen feet in.'],
]
INTRO_HARD_MODE = [
    "Your veteran warrior intuition must catch ahold of some detail of a chunk of the floor that just doesn't seem right.",
    "To the naked eye, it looks like just more tunnel floor.  However, when more closely inspected, underneath a mat of old cobwebs, it turns out there is a third fork extending downwards.",
]
PICK_A_PATH = 'So all that remains is to choose;  which pathway will you take?'
ASK_PATH = "Which one?  "
ASK_PATH_NO_INTRO = "So which tunnel?  "
ASK_PATH_AGAIN = "Choose:  "
NO_LOWER_PATH = "What makes you think there is a lower tunnel?  I gave you your options."
NOT_A_PATH = "Fascinating.  Let's try one from the list, eh?"
CHICKEN = "You entered the code for Hard Mode, and now you're not choosing it?  Chicken."
ASK_CHICKEN = "Are you sure you don't want to take the Lower path?  "


# ---------- the dragons' entrances ----------------------------------------------------------------------------

DRAGON_INTROS = {
    'Trogdor The Burninator': [
        ['You continue to skip down the path, passing what look to have been a few bottles of mead.  Based on their smell, their contents have not been gone for terribly long.',
         'Skipping (I said STOP) down the twisting route starts to make you feel dizzy, almost drunk.  If you\'re looking to battle a dragon, you\'d better start taking this more seriously.'],
        ['A little further along, the smell of mead reaches your nostrils, once again, only this time, much more pungent and "fresh".  The further you go, the stronger the smell becomes.',
         'You begin to hear a distant, rhythmic sound, almost like growling.  As you continue along your merry way, the growling gets louder and louder; the rumbling echoing through the tunnel.',
         'Rounding yet another bend in the path, the tunnel begins to widen, and the rumbling has increased dramatically in volume; you\'ve finally reached the other side.'],
        ['The tunnel continues to widen into a large cavern.  Conveniently spaced fires dot the ground, allowing you to see into the far reaches.',
         'There, in the center of the cave, lies what looks like a very serpentine dragon, with a beefy arm growing out of its side?  One of the most bizarre creatures you\'ve ever come across.',
         'It almost looks cartoonish.  You don\'t really know what a "cartoon" is, but it definitely looks like a character from one.'],
        ['The rumbling appears to be coming from the dragon.  "Is it... snoring?" you ask yourself?  You see the dragon\'s chest rise and fall, in time with the rumbling.',
         '"She\'s passed out?  What gives?" you wonder.  Being a noble warrior, not wanting to take advantage of the situation, you carefully walk up to the sleeping beast.  It does not stir.'],
        ['"Hey," you quietly say.  Nothing.  "I said Hey", you speak a little louder.  Nothing.  "HEY!!" you scream in her face, as you poke her with the bottom of your torch.',
         'Clearly still groggy, she rumbles, "Hmmmm what the...." She begins to stir when she sees you.  "Hi," she says.  "You need something?  Can\'t you see, I\'m trying to get some rest?"',
         '"I\'m dead-tired and hung-over as shit" she mumbles, rubbing at her eyes with her clawed arm, "so I hope this is important."',
         '"Are you serious?" you think to yourself.  "Are you the fierce beast who just attacked my neighbors, The Rodents?"',
         '"Hmmmm.... I guess so," she mumbles.  "I don\'t much remember last night.  I was drunk as shit."'],
        ['Well this really chaps your hide.  She slaughtered your neighbors and friends, just because she got drunk?  How does a dragon get drunk, anyway?  You thought they were magical.',
         '"Prepare to defend yourself, for I am {hero}, and I am here for the vengeance of my town, which you have repeatedly ravaged."',
         '"Are you serious?  Do we have to do this right now?  I\'m very tired, and very sorry, ok?" she speaks, as if this will assuage anything.',
         '"If you don\'t mind your p\'s and q\'s, you are in for it."',
         'Enraged by her comments, you bust out your dagger, kept in its sheath around your neck.  It is an heirloom, and, having saved your ass many times, you know it is an excellent, deadly weapon.',
         'As you attempt to strike her, her beefy arm grabs the dagger, mid-swipe, and shatters it on the cave floor.',
         'As you look in shock at the broken pieces of your treasured weapon, she rears up, wobbling slightly.'],
        ['She booms, "You dare to attack me?  I am {dragon}, and with my beefy arm, I will crush you like a worm!"',
         'And so it begins....'],
    ],
    'Skippy': [
        ['You wander down the freshly-carved path, which appears to have been dug through completely solid rock.  There are very few curves and corners - it is mostly a straight path.',
         'After a few minutes, the tunnel begins to widen, and brighten.  You peer down the length of the cavern, only to find a young, blue ridged-back dragon, apparently playing with human bones.'],
        ['"I am the fiercestest warrior!", she grumbles, as she swings a femur towards a nearby skull.',
         '"No, I am the fiercestest warrior!", she roars as she head-butts the femur with the skull.',
         'This goes on for a few minutes and you wonder, "What the hell is the matter with this thing?  Does it not hear me breathing back here?"',
         '"YES, I hear you breathing, and I can read your mind!", she roars, as she turns to face you.',
         '"Do you not realize that I have been mocking you?  I am {dragon}, and I demand your respect!"'],
        ['"{dragon}?" you wonder.  "Isn\'t that a boy\'s name?" you ask her.',
         'Enraged by your question, she puffs out her chest and booms "I am {dragon}, and you will now learn to respect a dragon as young as I!"',
         'As she puffs up, you stare in horror as she appears to have doubled in size.  Her mouth opens showing modest, but very sharp teeth, drool running down her chin.',
         '"Wow does she look hungry," you think as you begin to back away.  She begins to laugh hysterically.',
         '"Shit."'],
    ],
    'The Ancient': [
        ["The tunnel is in complete shambles.",
         "You shimmy and crawl and squeeze your way through, deeply questioning your decision-making skills.",
         "You reach multiple crevices which barely allow your passage, and it is clear that it would be nigh impossible to turn back.",
         '"Geez...  I hope this tunnel has an exit!" you say to yourself.'],
        ["As the tunnel comes to an end, a cave begins to appear, a thick layer of dust and detritus covering everything in sight.",
         "A few dusty, rusty coins are scattered around, which you kick playfully.  And stupidly."],
        ["Suddenly, two white-hot slits appear in the distance, and there is rumbling of a voice, so deep, it rattles and shakes the very walls of the cave.",
         "",
         "[red]WHO DARES ENTER THE CAVE OF THE ANCIENT?![/]",
         "[red]ALL WHO ENTER SHALL DIE!!  COME NOW, FACE THE WRATH OF THE ANCIENT!![/]"],
        ["A vision of unimaginable wealth appears as The Ancient releases a massive fireball towards you.",
         "You deftly duck the blast, but quickly realize that the projectile is now headed for the tunnel exit.",
         '"No!!" you yell, as the exit collapses.  "Well I sure do hope there is another way out of here."'],
        ["As you turn back around, a second fireball flies at your face!",
         "With your cat-like skills and reflexes, you parry the blast which ricochets towards the ceiling of the cave.",
         "The massive blast lights up almost the entire cave, providing a vision of The Ancient.",
         "You've heard (old-wives) tales of such a beast, but since a young age, you knew they were bullshit.  Nothing like that could exist.",
         "She is gigantic.  A flame-crested, coal-black dragon; her iridescent scales covered in battle scars; her very presence demanding awe and disbelief.",
         "Multiple arrows remain embedded in her impenetrable armor."],
        ["This is gonna suck."],
        ["This is it.  This is the battle for which you have been waiting your entire life!",
         2,
         "Let's rock!"],
    ],
}


# ---------- the fight -------------------------------------------------------------------------------------------

CHOOSE_WEAPON = "Choose your weapon:"
ASK_WEAPON = "Your choice?  "
COIN_USED_UP = "That's no longer listed as an option, now is it.  You used it up, remember?  Pick something else, and make it snappy!"
WEAPON_BROKEN = "Do you not remember what just happened?  The dragon shattered it.  It's broke and you ain't fixin' it right now."
STALLING = ["You are, quite literally, playing with fire...  Please choose something from the list, or get eviscerated and burnt to a crisp:  ",
            "Seriously, she is closing in!  Choose something; anything!  Now!!!  "]
FROZE = [
    ["Having taken too long to decide what to do, {dragon} closes in, opening her ample maw to show rows of huge, razor-sharp teeth",
     "Fear takes ahold of you, and you drop all weapons.  You might have peed a little too.  We'll check later!"],
    ["Suddenly, you feel a surge of strength and confidence; dodging the gaping mouth of {dragon}, you hop onto her back and start pounding her in the neck.",
     "The scales, being highly protective, absorb every punch, leaving you with a fractured wrist on one side, and a very bruised hand on the other.",
     '"Mierda," you grunt as {dragon} begins to buck.',
     '"Time to improvise," you think to yourself.  Deftly, you untie your man-bun, reaching for {dragon}\'s neck.'],
]

HERO_MISSES = "You missed her!  That was a poor choice."
HERO_HITS = "You swing your mighty {weapon}, striking {dragon}, for {damage}."
CRIT = "[magenta]Critical Hit!![/]"

HERO_DODGES = "You evaded the attack.  Wow, I didn't think you had it in you!"
DRAGON_CLAWS = "{dragon} swipes at you with her wicked claws, slicing you for {damage}."
DRAGON_BREATHES = "{dragon} opens her maw, showing rows of razor-sharp teeth, and shoots a fireball-blast at you, spraying you in the face for {damage}."
WEAPON_SHATTERS = [
    "As you are assaulted by her attack, your {weapon} is shattered, leaving you standing there, mouth agape and even more terrified.",
    "{dragon} cackles with glee, as she begins to smack her gums together.",
    '"She looks hungry," you think, as you stand there beginning to shudder.  At this point, you may have tinkled a little.  Don\'t judge!',
]

COIN_TOSS = [
    'As the Wise-Wizard instructed, before you had to.... nevermind, that\'s a tale for a different story.',
    'You quickly rub the "Heads" side of the coin and flick it into the air.',
    'The coin flips and spins into the air, beginning to sparkle and crackle, like lightning will shoot out of its arse.',
]
COIN_HEADS = [
    'Rather than falling into your awaiting hand, the coin floats in the air, heading toward {dragon}.',
    'It is almost impossible for you to take your eyes off of the coin, mesmerizing as it is.',
    '{dragon} is not so lucky and remains transfixed by the coin, as electricity crackles all around it.',
    '"This is my only chance for survival," you think to yourself, as you bolt for the tunnel exit.',
]
COIN_HEADS_ANCIENT = [
    ['Having already forgotten about the first, destructive blast, you screech to a halt in front of the entrance, and begin to sob.',
     '{dragon} lifts up onto her hind legs, releasing a massive fireball in your direction as you stare at it stupidly.'],
    ["The incoming bolt strikes you in the chest for {damage}."],
]
COIN_TAILS = [
    "The sparkling fizzles, and the coin returns to your waiting hand, burning it terribly, as it is still white-freakin'-hot.",
    "You quickly drop the coin, yelling obscenities, and stare at an incoming fireball from {dragon}.",
    "The projectile slams into your face, messing up your teeth, real bad, for {damage} of damage.",
]

BARE_HANDS = [
    "As you wrap your man-bun around her neck, {dragon} begins to buck and jump and twist and roar.",
    "The agitation loosens up a few strands of your hair, which tickle against your nose, causing you to almost sneeze, and almost giggle.",
]
STRANGLED_HER = [
    ["{dragon} continues to buck and writhe, but your grip is tight, and, eventually, her head slams down into the ground; a large fart escaping with her last breath.",
     "She is dead.  You are victorious!!"],
]


# ---------- how it ends -----------------------------------------------------------------------------------------
# Every ending is followed by "The End."

THE_END = "The End."

VICTORY = [
    ['[green]You have survived!!!  You have slain the beast!  You are victorious and all should bow down before you, for you are the Dragonslayer![/]'],
    ["You attempt to sever her head, hoping for a stunning trophy to mount upon your wall at home, but your weapons are all blunted from battle.",
     "You bust out your only remaining tool, however, your safety scissors don't seem to do the trick, so you give up.",
     "Why the hell are you carrying those anyway?  Are you in kindergarten or something?"],
]
VICTORY_ANCIENT = [
    ["You look around at the mounds of treasure, quite pleased with yourself and now filthy rich.",
     "Then it hits you:  you have no way out of here!",
     "You search everywhere but are unable to find any way out.",
     '"How did the goram dragon get in and out?" you ponder.'],
    ["Eventually, the gas released when {dragon} died, has diffused throughout the cave.",
     "Unbeknownst to you, one of its primary components was sulfuric acid, which you have inhaled as you searched for an exit.",
     "After a few torturous hours, you succumb to the lesions growing in your lungs, drowning on your own mucus.",
     'Your last thought, "Well that sucked."',
     "And it did."],
]
VICTORY_GO_HOME = [  # Trogdor and Skippy
    ['After gathering all the treasure you can possibly carry, you head back down the entrance tunnel, and back home.',
     "Upon your return, you are greeted with fanfare and applause from the citizens of your small town, which had been devastated by dragon attacks.",
     '"I have been tested and found worthy," you think to yourself, as you pass out and fall off your horse onto your face, in front of everyone.'],
    ['You wake, very sore, in a foreign bed, and realize you are in The Bubba\'s hut, the town cleric.',
     '"What happened?" you ask, as you attempt to sit up.',
     '"You goram fool," he says.  "You\'ve inhaled a significant amount of sulfuric acid, during your battle."',
     '"The shit\'s as deadly as it gets.  You don\'t have long to live.  I hope it was worth it."'],
    ['As you lay in The Bubba\'s bed over the next few weeks, you cry yourself to sleep each night.',
     '"I am such a greedy moron," you sob one morning.  These are your last thoughts as you suffocate on your own mucus.'],
    ["You have died.  I, too, hope it was worth it."],
]
HARD_MODE_UNLOCKED = [  # after beating Skippy
    'You have completed the adventure on "Regular" mode.',
    'For any future attempts, use code "[magenta]Kool-Aid[/]" when prompted for readyness at the beginning of this story.',
    'This will enable "Hard" mode, should you have the cajones to really test yourself.',
]

SLAIN = [["[red]You have been slain.  You are terrible, and you deserved this.[/]"]]

RAN_AWAY = [
    ["You flee down the tunnel, muttering awful things about yourself.",
     '"I am such a wuss...  I\'ll never be a true warrior.  I\'ll never be anything." you curse as you continue down the tunnel, hearing endless, angry shrieks behind you.'],
    ['You may have survived, but your courage, your self-worth and your pride are all wounded beyond repair.'],
    ['You live a very long, very sad, lonely life.  As you die on your bed in your empty house, you sob uncontrollably.',
     'Then you die.  Alone.  And you poop yourself.  It\'s disgusting.'],
]
COIN_KILLED_YOU_ANCIENT = [["Well I guess that's that."]]
COIN_KILLED_YOU = [
    ["You have been weighed.  You have been measured.  And you have been found wanting.",
     "You are slain.  Dead dead deadskies.",
     "It was inevitable."],
]
BUCKED_OFF = [
    ["You are no match for the brutal strength of this majestic creature, and you are bucked off almost immediately.",
     'As you splat into a huge pile of dragon shit, apparently in {dragon}\'s toity, you flail madly, but you are no match for the remaining digestive enzymes in the pile.',
     'You sink further into the swamp of dragon poop, attempting to breathe, but only getting more poop in your mouth and lungs.'],
    ['After a few seconds, you dissolve into the pile leaving only bones and teeth behind.',
     'Your last thought:  "What the hell was I thi...."',
     '"thinking"?  Not too much.  It\'s a goram dragon after all.'],
]

# Which story each way of losing tells (the keys are what battle.fight() returns).
ENDINGS = {
    'slain': SLAIN,
    'ran_away': RAN_AWAY,
    'coin_killed_you_ancient': COIN_KILLED_YOU_ANCIENT,
    'coin_killed_you': COIN_KILLED_YOU,
    'bucked_off': BUCKED_OFF,
}

# ---------- random hero names ("Smug Frog-Hater") ---------------------------------------------------------------

NAMES_1 = ["Smug", "Conceited", "Silly", "Happy", "Sad", "Amorphic", "Petty", "Pretty", "Largish", "Smelly", "Farty", "Tender", "Kind", "Jerky", "Angry", "Tumescent", "Ridiculous", "Stupid", "Skanky", "Master", "Gassy", "Broken"]
NAMES_2 = ["Pussy-Willow", "Monkey", "Frog", "Turtle", "Fish", "Dog", "Tapir", "Beaver", "Kitten", "Child", "Worm", "Gas", "Tyrant", "Giraffe", "Fungus", "Crab", "Fart", "Smegma", "Warrior", "Battle-Cat", "Counselor", "Magician", "Bunghole", "Baby", "Doctor", "Rock"]
NAMES_3 = ["Smurf", "Mouth", "Lips", "Fungus", "Womanizer", "Grass", "Smegma", "Clutz", "Bunghole", "Kitten", "Baby", "Doctor", "Snarfblat", "Hunter", "Eater", "Sniffer", "Spanker", "Robot", "Trash-can", "Ingestor", "Hater", "Player"]


# =================================================================================================================
# DRAFTS BY CLAUDE (Nov 19, 2026) FOR TED TO REWRITE
# Everything below is new for the upgrade: the dragons' tricks, ducking, statuses, loot and the run from one
# dragon to the next. Rewrite anything. Keep the {names} in curly brackets where you want them filled in.
# =================================================================================================================

TITLE_SUBTITLE = "the classic.  now with more ways to die."

DUCK_LABEL = "Duck and cover (no attack, but much harder to hit)"
DRINK_LABELS = {"Trogdor's Mead": "heals 10-15, gets you drunk", "Healing Draught": "heals 15-22"}

# --- ducking ---
DUCKS = ["You throw yourself flat on the cave floor and cover your head.  Very brave.  Very dignified.",
         "You dive behind a rock.  It's a small rock.  Most of you is still showing.",
         "You curl up into a ball and hope for the best.  Your mother would be so proud."]
DUCKED_THE_BIG_ONE = "The blast roars right over your head.  It only singes your man-bun, for {damage}."

# --- drinking ---
DRINK_MEAD = "You chug a bottle of Trogdor's Mead.  It burns going down.  You feel GREAT.  You heal for {heal}, and you're a little drunk."
DRINK_DRAUGHT = "You gulp down the Healing Draught.  It tastes like feet.  You heal for {heal}."

# --- statuses ---
STATUS_WORDS = {'burning': 'ON FIRE', 'drunk': 'drunk', 'terrified': 'terrified', 'damp': 'damp'}
CATCH_FIRE = "Your clothes catch fire.  You are now, technically, a torch."
STILL_BURNING = "You're still on fire, for {damage}.  Stop, drop and roll?  No time!"
FIRE_OUT = "The fire on your back finally goes out.  You smell like a campfire.  And pee."
TERRIFIED = "Your hands won't stop shaking.  Your next few swings are going to be... not great."
DAMP = "(Your pants are now officially damp.  That's not going away.)"
NOT_TERRIFIED = "You pull yourself together.  Mostly."

# --- Trogdor: still drunk, and BURNINATING ---
HICCUP = ["{dragon} hiccups so hard she falls over, and spends her whole turn trying to get back up.",
          "{dragon} lets out an enormous belch, giggles at it, and forgets what she was doing.",
          "{dragon} sways, squints at you, and swipes at the empty air two feet to your left."]
HICCUP_FIRE = "{dragon} hiccups out a little fireball.  Right into her own beefy arm, for {damage}.  \"OW.  Who did that?\""
TROGDOR_WINDUP = "{dragon} sucks in a huge breath, cheeks puffing out like a bullfrog.  Something big is coming."
TROGDOR_BIG = "\"BURNINATE!!!\"  {dragon} spews a river of fire across the whole cave, for {damage}."

# --- Skippy: reads your mind, and puffs up ---
MIND_READ = "\"I KNEW you'd do that!\" {dragon} giggles, reading your mind and dancing right out of the way."
PUFF_UP = "{dragon} puffs out her chest and doubles in size AGAIN.  She's done playing.  Her hits are going to hurt a lot more now."

# --- The Ancient: armored, breathes an inferno, gets FURIOUS ---
ARMOR = "Her ancient scales soak up most of it."
PIERCE = "Your {weapon} finds a gap between her scales!"
ANCIENT_WINDUP = "{dragon} draws a breath so deep that the coins on the floor slide toward her.  Her throat glows white-hot."
ANCIENT_BIG = "{dragon} unleashes an INFERNO.  The whole cave turns white, for {damage}."
ENRAGE = "The arrows stuck in her hide start to glow red-hot.  {dragon} is FURIOUS."

# --- winning a fight in the middle of a run ---
YOU_WON = "[green]You have slain {dragon}!  You are victorious![/]"
PICK_UP_WEAPONS = "You pick your weapons back up off the cave floor.  Some of them have pee on them."
GROW = "Something about killing a dragon makes you feel tougher.  Max health +{gain}, and you're patched up to full."
HOARD = ["You dig through {dragon}'s hoard.  Most of it is junk, half-melted, or covered in something sticky.",
         "Three things catch your eye.  You can only carry one more thing."]
PICK_LOOT = "What do you take?  "
LOOT_LABELS = {
    "Trogdor's Mead": "Trogdor's Mead x2 (heals 10-15, gets you drunk)",
    'Peasant Pitchfork': "Peasant Pitchfork (2-9 damage, finds the gaps in armor)",
    'Beefy-Arm Gauntlet': "Beefy-Arm Gauntlet (+2 damage with every weapon)",
    'Whetstone': "Whetstone (+1 damage with every weapon)",
    'Spare Sword': "Spare Sword (in case the last one gets shattered)",
    'Femur Club': "Femur Club (4-8 damage, previous owner unknown)",
    "Skippy's Tiara": "Skippy's Tiara (you dodge more often; it's very sparkly)",
    'Healing Draught': "Healing Draught x2 (heals 15-22)",
}
TOOK_LOOT = "You take the {item}.  Good choice.  Probably."
ONWARD = "So:  home, or deeper?  "
HOME_OR_DEEPER = ["Head home, a hero", "Press on, deeper into the Dragon Cliffs"]

BRIDGE_TO_SKIPPY = [
    ["Behind Trogdor's pile of empty mead barrels, a crack in the wall opens into a freshly-dug tunnel.",
     "It smells like old bones and little-kid sweat.  You hear giggling somewhere far ahead.",
     '"Oh good," you mutter.  "Another one."'],
]
BRIDGE_TO_TROGDOR = [
    ["Past Skippy's bone pile, a narrow ledge winds out along the cliffside, over a drop with no bottom in sight.",
     "You smell mead.  Lots of mead.  And something is snoring loud enough to shake pebbles off the cliff.",
     '"Oh good," you mutter.  "Another one."'],
]
BRIDGE_TO_ANCIENT = [
    ["Two dragons down.  You head back to the fork, feeling pretty good about yourself.  Smug, even.",
     "Then you notice it:  a chunk of the floor that just doesn't seem right."],
    ["Under a mat of old cobwebs, there's a third tunnel, dropping straight down into the dark.",
     "Warm air breathes up out of it.  In.  Out.  In.  Out.",
     '"That\'s not wind," you whisper.  You climb down anyway, because of course you do.'],
]
