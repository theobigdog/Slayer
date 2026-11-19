"""The game from start to finish: name the hero, pick a path, meet the dragon, fight, and see how it ends."""
import story
import ui
from battle import fight, match, tell
from fighters import PATHS, Dragon, Hero


async def name_the_hero() -> Hero:
    hero = Hero(await ui.ask_text(story.ASK_NAME))
    for line in story.RENAME:
        await ui.say(line)
    await ui.wait(2)
    hero.rename()
    await ui.say()
    await tell([story.NEW_NAME], hero)
    await ui.say()
    return hero


async def pick_a_path(hero: Hero, hard_mode: bool, intro: bool) -> str:
    paths = list(PATHS) if hard_mode else ['Left', 'Right']
    if intro:
        await ui.clear()
        beats = story.INTRO + ([story.INTRO_HARD_MODE] if hard_mode else [])
        await tell(beats, hero)
        await ui.say()
        await ui.say(story.PICK_A_PATH)
        await list_paths(paths)
        answer = await ui.ask_text(story.ASK_PATH)
    else:
        await ui.say()
        await ui.say(story.NO_INTRO)
        answer = await ui.ask_text(story.ASK_PATH_NO_INTRO)
    path = match(answer, paths)
    while not path:
        await ui.say()
        if answer.strip().lower() == 'lower':  # nice try
            await ui.say(story.NO_LOWER_PATH)
        else:
            await ui.say(story.NOT_A_PATH)
        await list_paths(paths)
        answer = await ui.ask_text(story.ASK_PATH_AGAIN)
        path = match(answer, paths)
    if hard_mode and path != 'Lower':
        await ui.say()
        await ui.say(story.CHICKEN)
        if not await ui.yes_no(story.ASK_CHICKEN):
            path = 'Lower'
    return path


async def list_paths(paths: list):
    await ui.say()
    for number, path in enumerate(paths, 1):
        await ui.say(f"  {number}. {path}")
    await ui.say()


async def the_end(hero: Hero, dragon: Dragon, ending: str):
    if ending == 'won':
        await tell(story.VICTORY, hero, dragon)
        await ui.say()
        await tell(story.VICTORY_ANCIENT if dragon.name == 'The Ancient' else story.VICTORY_GO_HOME, hero, dragon)
    else:
        await ui.say()
        await tell(story.ENDINGS[ending], hero, dragon)
    await ui.say()
    await ui.say(story.THE_END)
    await ui.say()
    if ending == 'won' and dragon.name == 'Skippy':
        for line in story.HARD_MODE_UNLOCKED:
            await ui.say(line)
        await ui.say()


async def play() -> str:
    """One whole game. Returns how it ended (the test bot uses this)."""
    await ui.clear()
    hero = await name_the_hero()
    hard_mode = (await ui.ask_text(fill_hero(story.ASK_READY, hero))).strip().lower() == story.HARD_MODE_CODE.lower()
    await ui.say(story.HARD_MODE_ON if hard_mode else story.NOT_READY)
    await ui.say()
    intro = await ui.yes_no(story.ASK_INTRO)
    dragon = Dragon(PATHS[await pick_a_path(hero, hard_mode, intro)])
    if intro:
        await ui.say()
        await tell(story.DRAGON_INTROS[dragon.name], hero, dragon)
    ending = await fight(hero, dragon)
    await the_end(hero, dragon, ending)
    return ending


def fill_hero(text: str, hero: Hero) -> str:
    return text.replace('{hero}', hero.name)
