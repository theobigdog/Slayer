
from slayer_server.adventures.util import AdventureUtil
from slayer_server.slayer_files import Slayer_Root
import os

class SlayerCharacter:
  def __init__(self, raw: dict) -> None:
    self.name = AdventureUtil.get_str(raw, 'name', raise_on_none=True)
    self.hero_class = AdventureUtil.get_str(raw, 'hero_class')
  
  def __str__(self) -> str:
    return self.name + ' of class ' + self.hero_class


class SlayerParty:
  def __init__(self, raw: dict) -> None:
    self.party_dict = dict()
    name = AdventureUtil.get_str(raw, 'name', raise_on_none=True)
    print('party name = ' + name)
    raw_members = AdventureUtil.get_list(raw, 'members')

    for raw_member in raw_members:
      character = SlayerCharacter(raw_member)
      print('  Char: ' + str(character))
    pass
  pass

class PartyManager:
  party_dir = os.path.join(Slayer_Root, 'saves', 'parties')

  def __init__(self) -> None:
    self.party_db = {}
    for entry in os.listdir(PartyManager.party_dir):
      fname = str(entry)
      print('load party: ' + str(entry))
      party = SlayerParty(AdventureUtil.load_yaml(PartyManager.party_dir, fname))
    pass