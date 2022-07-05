from cgitb import lookup
from slayer_server.adventures.items import AdventureItemDB, ItemRef
from slayer_server.adventures.mobs import AdventureMobDB
from slayer_server.adventures.util import AdventureUtil
from slayer_server.slayer_files import Slayer_Root


class AdventureRoom:
  def __init__(self, raw: dict, item_db: AdventureItemDB) -> None:
    self.name = AdventureUtil.get_str(raw, 'name', raise_on_none=True)
    print('load room = [' + self.name + ']')
    self.description = AdventureUtil.get_str(raw, 'description')

    self.load_items(raw, item_db)
    pass

  def load_items(self, raw: dict, item_db: AdventureItemDB) -> None:
    self.items = []
    for x in AdventureUtil.get_list(raw, 'items'):
      ref = ItemRef(x, item_db)
      self.items.append(ref)
      print('  contains item ' + str(ref))



class Adventure:
  def __init__(self, key: str, home: str) -> None:
    self.key = key
    self.home = home
    self.item_db = AdventureItemDB(home)
    self.mob_db = AdventureMobDB(home)

    raw = AdventureUtil.load_yaml(self.home, 'main.yaml')
    self.name = AdventureUtil.get_str(raw, 'name')
    self.description = AdventureUtil.get_str(raw, 'description', '')
    self.narrative = AdventureUtil.get_str(raw, 'narrative', '')

    print('name is ' + self.name)
    self.load_items(raw)
    self.load_rooms(raw)

    print('description is [' + self.description + ']')
    print('Keys:')
    for k in raw.keys():
      print('  key=' + str(k))

  def load_items(self, raw: dict) -> None:
    self.starting_items = []
    for x in  AdventureUtil.get_list(raw, 'items'):
      ref = ItemRef(x, self.item_db)
      self.starting_items.append(ref)
      print('Adventure contains ' + str(ref))

  def load_rooms(self, raw: dict) -> None:
    self.rooms = []
    for x in AdventureUtil.get_list(raw, 'rooms'):
      self.rooms.append(AdventureRoom(x, self.item_db))
    pass