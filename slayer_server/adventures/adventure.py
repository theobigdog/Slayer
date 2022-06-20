from slayer_server.slayer_files import Slayer_Root
import os
import json

class AdvMain:
  def __init__(self, d) -> None:
    self.__dict__ = d
    pass

  @property
  def name(self) -> str:
    return self.__dict__['name']


class Adventure:
  def __init__(self, key, manager) -> None:
    self.key = key
    self.home = manager.get_adventure_dir(key)
    print('key is ' + key)
    print('dir is ' + self.home)

    f = open(os.path.join(self.home, 'main.json'))
    self.main = json.load(f, object_hook=lambda d: AdvMain(d))
    f.close()

    print('main is ' + str(self.main))
    print('name is ' + self.main.name)
    print('stuff is ' + str(self.main.stuff))
    pass
