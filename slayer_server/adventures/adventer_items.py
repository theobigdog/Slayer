
import os
import yaml

from slayer_server.adventures.util import AdventureUtil

class AdventureItems:
  def __init__(self, home:str) -> None:
    raw = AdventureUtil.load_yaml(home, 'item_db.yaml')
    pass