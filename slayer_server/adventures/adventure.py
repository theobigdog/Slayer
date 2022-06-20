from slayer_server.slayer_files import Slayer_Root
import os
import json

class AdvMain:
  def __init__(self, d) -> None:
    self.__dict__ = d
    pass

  @property
  def name(self) -> str:
    print('retrieving the name...')
    return self.__dict__['name']


class Adventure:
  def __init__(self, key: str, home: str) -> None:
    self.key = key
    self.home = home
    print('key is ' + key)
    print('dir is ' + self.home)

    self.main = self.loadMain()

    print('main is ' + str(self.main))
    print('name is ' + self.main.name)
    print('stuff is ' + str(self.main.stuff))
    pass

  def loadMain(self) -> AdvMain:
    f = open(os.path.join(self.home, 'main.json'))
    main = json.load(f, object_hook=lambda d: AdvMain(d))
    f.close()

    return main
