"""The game window's ASCII art: the title banner and the three dragons (all facing left, at the hero).
Edit freely: keep each dragon about 12 lines tall and 46 characters wide so it fits its corner of the screen."""

BOOT = [
    "BUBBA-DOS  BIOS v1.03   (C) 1982 Bubba Industries",
    "",
    "MEMORY TEST ...... 640K OK",
    "MAN-BUN .......... DETECTED",
    "SAFETY SCISSORS .. DETECTED",
    "DRAGONS .......... 3 FOUND",
    "",
    "C:\\> SLAYER.EXE",
]

BANNER = [
    " ████  ██       ███   ██  ██ ██████ █████ ",
    "██     ██      ██ ██  ██  ██ ██     ██  ██",
    " ████  ██     ██   ██  ████  █████  █████ ",
    "    ██ ██     ███████   ██   ██     ██ ██ ",
    "████   ██████ ██   ██   ██   ██████ ██  ██",
]

SWORD = "o==[]::::::::::::::::::::::::::::::::::>"

DRAGONS = {
    # Trogdor, after Ted's drawing: an S-shaped dragon, wings, ONE beefy arm, burninating to the left.
    'trogdor': r"""
                   ~@~       /\       /\
     \  |  /     ___\V/__   /  \/\   /  \/\
  -   \ | /    ,'VVVVVVV `./ /\/\ \ / /\/\ \
 <=====>*<====<         o  )/     \_/     \_\
  -   / | \    `.^^^^^^^__.'  .--------.
     /  |  \      `--.   `. ,' ,-.  ,-. `.
                      )    )  (   )(   )  )
                    ,'    /`-._`-'  `-' _/
                  ,'  ^  /     `-.  ,-'
                 /   ^ ,'        | |
                (   ^ (__/\/\/\_(___)
                 `-.___     ________`-->
                   _|_|  _|_|
""",
    # Skippy: young, ridged back, a tiara, drooling, playing with a femur and a skull.
    'skippy': r"""
           .*.*.
          _|_|_|_    /\
        ,'  ___  `. /  \/\
       /   ( o )   Y      \/\
   ,--'     `-'    |         \/\
  (__vVvVv_.      /             \
      ~  \ `-._.-'    ,--.       \
      ~   `.   ,-.   (    \       |
           ,`-'   )   `.   )     /
    ,-.   / _  _,'      ) /    ,'
   (x x) =o=====o=     / /__.-' __
    `^'   \_\  \_\    (__)  `--'  `>
""",
    # The Ancient, head-on: flame crest, white-hot slit eyes, arrows stuck in her armor.
    'ancient': r"""
        /\   /\  /\   /\  /\   /\
       /  \ /  \/  \ /  \/  \ /  \
      / /\ V /\ \/\ V /\ \/\ V /\ \
       /__\_____\_______/_____/__\
      /  \__/          \__/  \
     / ,-.  --->     <--- ,-. \
    | (=|=)              (=|=) |
    |  `-'      /\/\      `-'  |
     \     ,-.__\  /__.-.     /
   -->`.  (  VVVVVVVVVV  )  ,'<--
       `.  \ ^^^^^^^^^^ /  .'
    --->`-. `-.______.-' ,-'
      ____|`-.________.-'|____
""",
}
