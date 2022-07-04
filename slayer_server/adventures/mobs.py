
from slayer_server.adventures.util import AdventureUtil


class AdventureMobs:
  def __init__(self, home:str) -> None:
    raw = AdventureUtil.load_yaml(home, 'mob_db.yaml')