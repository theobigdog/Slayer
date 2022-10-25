
from slayer_server.adventures.items import ItemRef
from slayer_server.adventures.util import AdventureUtil
from slayer_server.items.item_manager import ItemManager
from slayer_server.slayer_files import Slayer_Root
import os

class SlayerCharacter:
  def __init__(self, raw: dict, item_db: ItemManager) -> None:
    self.name = AdventureUtil.get_str(raw, 'name', raise_on_none=True)
    self.hero_class = AdventureUtil.get_str(raw, 'hero_class')
    self.items = list[ItemRef]()
    for x in AdventureUtil.get_list(raw, 'inv_items'):
      ref = ItemRef(x, item_db)
      self.items.append(ref)
  
  def __str__(self) -> str:
    desc = self.name + ' of class ' + self.hero_class
    for r in self.items:
      desc = desc + '\n  (' + str(r.count) + ') ' + r.item.name
    return desc

class SlayerParty:
  def __init__(self, raw: dict, item_db: ItemManager) -> None:
    self.party_dict = dict()
    name = AdventureUtil.get_str(raw, 'name', raise_on_none=True)
    print('party name = ' + name)
    raw_members = AdventureUtil.get_list(raw, 'members')

    for raw_member in raw_members:
      character = SlayerCharacter(raw_member, item_db)
      print('  Char: ' + str(character))
    pass
  pass

class PartyManager:
  party_dir = os.path.join(Slayer_Root, 'saves', 'parties')

  def __init__(self, item_db : ItemManager) -> None:
    self.party_db = {}
    for entry in os.listdir(PartyManager.party_dir):
      fname = str(entry)
      print('load party: ' + str(entry))
      party = SlayerParty(AdventureUtil.load_yaml(PartyManager.party_dir, fname), item_db)
    pass