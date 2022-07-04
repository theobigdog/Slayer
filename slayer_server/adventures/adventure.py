from io import TextIOWrapper
from slayer_server.adventures.adventer_items import AdventureItems
from slayer_server.adventures.util import AdventureUtil
from slayer_server.slayer_files import Slayer_Root
import os
import yaml

class Room:
  def __init__(self, d) -> None:
    self.__dict__ = d


class AdvMain:
  def __init__(self, d) -> None:
    self.parsed = d
    self.room_list = []
    for room in d['rooms']:
      self.room_list.append(Room(room))
    pass

  @property
  def description(self) -> str:
    return self.parsed['description']

  @property
  def name(self) -> str:
    return self.parsed['name']
    
  @property
  def narrative(self) -> str:
    return self.parsed['narrative']
    
  def room_list(self) -> list[Room]:
    return self.room_list


class Adventure:
  def __init__(self, key: str, home: str) -> None:
    self.key = key
    self.home = home
    self.itemdb = AdventureItems(home)

    self.main = self.load()

    print('name is ' + self.main.name)
    print('description is [' + self.main.description + ']')
    # print('narrative: ' + self.main.narrative)
    # print('Contains ' + str(len(self.main.room_list)) + ' rooms')
    # for room in self.main.room_list:
    #   print('  Room name is [' + room.name + ']')
    #   print('    Description: ' + room.description)
    # pass
    print('Keys:')
    for k in self.main.parsed.keys():
      print('  key=' + str(k))

  def load(self) -> AdvMain:
    return AdvMain(AdventureUtil.load_yaml(self.home, 'main.yaml'))

