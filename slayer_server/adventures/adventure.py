from io import TextIOWrapper
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

  def room_list(self) -> list[Room]:
    return self.room_list


class Adventure:
  def __init__(self, key: str, home: str) -> None:
    self.key = key
    self.home = home

    self.main = self.load()

    print('name is ' + self.main.name)
    print('description is [' + self.main.description + ']')
    print('Contains ' + str(len(self.main.room_list)) + ' rooms')
    for room in self.main.room_list:
      print('  Room name is [' + room.name + ']')
      print('    Description: ' + room.description)
    pass

  def load(self) -> AdvMain:
    with self.get_config_file('main.yaml') as f:
      main = yaml.safe_load(f)
      return AdvMain(main)

  def get_config_filename(self, filename) -> str:
    return os.path.join(self.home, filename)

  def get_config_file(self, filename) -> TextIOWrapper:
    return open(self.get_config_filename(filename))
