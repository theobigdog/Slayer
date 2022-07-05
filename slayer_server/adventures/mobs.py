
from slayer_server.adventures.util import AdventureUtil

class AdventureMob:
  def __init__(self, raw: list) -> None:
    pass

class AdventureMobDB:
  def __init__(self, home:str) -> None:
    raw = AdventureUtil.load_yaml(home, 'mob_db.yaml')

    self.db = {}
    if not isinstance(raw, list):
      raise LookupError('Mob database mob_db.yaml must contain a list')

    for entry in raw:
      mob = AdventureMob(entry)
