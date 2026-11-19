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
    'trogdor': r"""
            __.--.__               *hic*
        _.-'  o  o  `-.
       / _.---.        `.       ___
      ( (_____)    ,-.   \   .-'   `-.
       `-.____.-' ( @ )   \ /  BEEF   \
           |       `-'     Y    ARM    |
           |   /\  /\  /\  |`-._____.-'
           |  /  \/  \/  \ |
            \    ~~~~~~    /\____
             `-.________.-'      `--.__
                /  /    \  \          `-->
              _/__/      \__\_
""",
    'skippy': r"""
                   /\   /\   /\
             _.--./  \_/  \_/  \--._
          .-'   O        O         `-.
         (    .---.                   )
          `-.(_____)        .--.   _.'
       =o====o=   |        (    ) /  \
                  |  /\/\   `--' /    \
                  | (    )      /      \_
                   \ `--'   _.-'  /\/\/  `>
                    `-.___.'     /
                      |  |    __/
                     _|  |_  /
""",
    'ancient': r"""
      ___                          ___
     /   `\.    _.-------._      ./'   \
    |  ->  \\ .'  ___   ___`.   //  <-  |
     \___   \/   (_*_) (_*_) \ /   ___/
         `\  |      __      |  /`
           \ |    /VVVV\    | /    --->
     --->   \|    \^^^^/    |/
             \     ````     /    --->
         .----`-._______.-'----.
        /  --->    |||    <---  \
       /  /  /\    |||    /\  \  \
      /__/__/  \___|||___/  \__\__\
""",
}
