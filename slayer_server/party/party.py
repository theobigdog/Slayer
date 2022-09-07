

from slayer_server.adventures.util import AdventureUtil


class Party:
  def __init__(self, raw: dict) -> None:
    self.name = AdventureUtil.get_str(raw, 'name', '(NameNotDefined)')
    
    pass