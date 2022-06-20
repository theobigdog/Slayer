from slayer_server.slayer_files import Slayer_Root
from slayer_server.adventures.adventure import Adventure
import os

class AdventureManager:
  adventure_dir = os.path.join(Slayer_Root, 'adventures')

  def __init__(self) -> None:
    self.adventure_dict = {}
    for dir in os.listdir(AdventureManager.adventure_dir):
      key = str(dir)
      self.adventure_dict[key] = Adventure(key, self)

  def get_adventure_dir(self, key: str) -> str:
    return os.path.join(AdventureManager.adventure_dir, key)


