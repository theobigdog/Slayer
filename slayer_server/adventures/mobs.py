
from slayer_server.adventures.util import AdventureUtil

class AdventureMob:
  def __init__(self, raw: list) -> None:
    self.type_id = AdventureUtil.get_type_id(raw)
    self.name = AdventureUtil.get_str(raw, 'name','(NameNotDefined)')
    self.description = AdventureUtil.get_str(raw, 'description', '')

    pass

  def __str__(self) -> str:
    return 'Mob{' + self.mob_id + '} ' + self.name
    pass

  @property
  def mob_id(self) -> str:
    return self.type_id

class AdventureMobDB:
  def __init__(self, home:str) -> None:
    raw = AdventureUtil.load_yaml(home, 'mob_db.yaml')

    self.db = dict[str,AdventureMob]()
    if not isinstance(raw, list):
      raise LookupError('Mob database mob_db.yaml must contain a list')

    print('  mobs')
    for entry in raw:
      mob = AdventureMob(entry)
      print('    ' + str(mob))
      if mob.mob_id in self.db.keys():
        raise LookupError('Duplicate mob ID ' + mob.mob_id)
      self.db[mob.mob_id] = mob
  
  def lookup(self, id) -> AdventureMob:
    mob_id = AdventureUtil.get_type_id(id)
    return None if mob_id == None else self.db.get(mob_id)

class MobRef:
  def __init__(self, raw: dict, mob_db: AdventureMobDB) -> None:
    self.mob = mob_db.lookup(raw)
    self.count = AdventureUtil.get_int(raw, 'count', 1)

  def __str__(self) -> str:
    return self.mob.name + ' x' + str(self.count)
