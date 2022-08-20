
from slayer_server.adventures.util import AdventureUtil

class AdventureItem:
  def __init__(self, raw:dict) -> None:
    self.type_id = AdventureUtil.get_type_id(raw)
    self.name = AdventureUtil.get_str(raw, 'name','(NameNotDefined)')
    self.description = AdventureUtil.get_str(raw, 'description', '')
    self.equipable = AdventureUtil.get_bool(raw, 'equipable', False)
    pass

  def __str__(self) -> str:
    return 'AdventureItem: {' + self.type_id + '} "' + self.name + "' E:" + str(self.equipable)
    pass

  @property
  def item_id(self) -> str:
    return self.type_id

class AdventureItemDB:
  def __init__(self, home:str) -> None:
    raw = AdventureUtil.load_yaml(home, 'item_db.yaml')

    self.db = dict[str,AdventureItem]()
    if not isinstance(raw, list):
      raise LookupError('Item database item_db.yaml must contain a list')

    print('  items')
    for entry in raw:
      item = AdventureItem(entry)
      print('    ' + str(item))
      if item.item_id in self.db.keys():
        raise LookupError('Duplicate item ID ' + item.item_id)
      self.db[item.item_id] = item
    pass

  def lookup(self, id) -> AdventureItem:
    type_id = AdventureUtil.get_type_id(id)
    return None if type_id == None else self.db.get(type_id)


class ItemRef:
  def __init__(self, raw: dict, item_db: AdventureItemDB) -> None:
    self.item = item_db.lookup(raw)
    self.count = AdventureUtil.get_int(raw, 'count', 1)

  def __str__(self) -> str:
    return self.item.name + ' x' + str(self.count)

