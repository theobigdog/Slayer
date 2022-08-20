from cgitb import lookup
from slayer_server.adventures.items import AdventureItemDB, ItemRef
from slayer_server.adventures.mobs import AdventureMobDB, MobRef
from slayer_server.adventures.util import AdventureUtil


class AdventureRoom:
  def __init__(self, raw: dict, item_db: AdventureItemDB, mob_db: AdventureMobDB) -> None:
    self.raw = raw
    self.name = AdventureUtil.get_str(raw, 'name', raise_on_none=True)
    print('load room = [' + self.name + ']')
    self.description = AdventureUtil.get_str(raw, 'description')

    self.load_items(raw, item_db)
    self.load_mobs(raw, mob_db)
    self.portals = dict[str,any]()
    pass

  def load_items(self, raw: dict, item_db: AdventureItemDB) -> None:
    self.items = list[ItemRef]()
    for x in AdventureUtil.get_list(raw, 'items'):
      ref = ItemRef(x, item_db)
      self.items.append(ref)
      print('  contains item ' + str(ref))

  def load_mobs(self, raw: dict, mob_db: AdventureMobDB) -> None:
    self.mobs = list[MobRef]()
    for x in AdventureUtil.get_list(raw, 'mobs'):
      ref = MobRef(x, mob_db)
      self.mobs.append(ref)
      print('  contsin mob ' + str(ref))
    pass

  def resolve_portals(self, room_dict: dict) -> None:
    raw_portals = AdventureUtil.get_list(self.raw, 'portals')

    for raw_portal in raw_portals:
      pname = AdventureUtil.get_str(raw_portal, 'name', raise_on_none=True)
      room = room_dict[pname]
      self.portals[pname] = room



class Adventure:
  def __init__(self, key: str, home: str) -> None:
    self.key = key
    self.home = home
    self.rooms = dict[str,AdventureRoom]()

    raw = AdventureUtil.load_yaml(self.home, 'main.yaml')
    self.name = AdventureUtil.get_str(raw, 'name')
    self.description = AdventureUtil.get_str(raw, 'description', '')
    self.narrative = AdventureUtil.get_str(raw, 'narrative', '')

    print('Define Adventure: ' + self.name)
    self.item_db = AdventureItemDB(home)
    self.mob_db = AdventureMobDB(home)
    self.load_items(raw)
    self.load_rooms(raw)

    print('description is [' + self.description + ']')
    # print('Keys:')
    # for k in raw.keys():
    #   print('  key=' + str(k))

  def load_items(self, raw: dict) -> None:
    self.starting_items = []
    for x in  AdventureUtil.get_list(raw, 'items'):
      ref = ItemRef(x, self.item_db)
      self.starting_items.append(ref)
      print('Adventure contains ' + str(ref))

  def load_rooms(self, raw: dict) -> None:
    for x in AdventureUtil.get_list(raw, 'rooms'):
      room = AdventureRoom(x, self.item_db, self.mob_db)
      if room.name in self.rooms.keys():
        raise LookupError('Duplicate room found: ' + room.name)
      self.rooms[room.name] = room

    for room in self.rooms.values():
      print('resolve -> ' + room.name)
      room.resolve_portals(self.rooms)
