from slayer_server.adventures.items import AdventureItem
from slayer_server.adventures.util import AdventureUtil
from slayer_server.slayer_files import Slayer_Root

import os


class ItemManager:
  item_dir = os.path.join(Slayer_Root, 'saves', 'items')

  def __init__(self) -> None:
    self.item_dict = {}
    for dir in os.listdir(ItemManager.item_dir):
      key = str(dir)
      print('Load items from ' + key)
      raw = AdventureUtil.load_yaml(ItemManager.item_dir, key)
      self.loadItems(raw)
    pass

  def loadItems(self, raw: list):
    for entry in raw:
      item = AdventureItem(entry)
      print('   ' + str(item))
      if item.item_id in self.item_dict.keys():
        raise LookupError('Duplicate item ID ' + item.item_id)
      self.item_dict[item.item_id] = item

  def lookup(self, id) -> AdventureItem:
    type_id = AdventureUtil.get_type_id(id)
    return None if type_id == None else self.item_dict.get(type_id)