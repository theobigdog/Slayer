
from io import TextIOWrapper
import os
import yaml

class AdventureUtil:
  def get_str(d: dict, field_name: str, def_value: str = None, raise_on_none: bool = False) -> str:
    v = d.get(field_name)
    if v == None and def_value == None and raise_on_none:
      raise LookupError('Missing field \'' + field_name + '\'')
    return str(v) if v != None else def_value

  def get_bool(d: dict, field_name: str, def_value: bool = None) -> bool:
    v = d.get(field_name)
    return bool(v) if v != None else def_value

  def get_int(d:dict, field_name: str, def_value: int = None, raise_on_none: bool = False) -> int:
    v = d.get(field_name)
    if v == None and def_value == None and raise_on_none:
      raise LookupError('Missing field \'' + field_name + '\'')
    return int(v) if v != None else def_value

  def get_list(d: dict, field_name: str, empty_list_if_none: bool = True) -> list:
    v = d.get(field_name)
    if v != None and not isinstance(v, list):
      raise LookupError('Field \'' + field_name + '\' is not a list')
    if v == None and empty_list_if_none:
      v = []
    return v

  def get_type_id(x) -> str:
    if x == None:
      raise LookupError('get_type_id: argument was None')
    if isinstance(x, dict):
      type_id = x.get('type_id')
      if type_id == None:
        raise LookupError('get_type_id: missing field type_id')
      return str(type_id)
    if isinstance(x, str):
      return x
    if isinstance(x, int):
      return str(x)
    raise LookupError('get_type_id: Unable to lookup id from type ' + str(type(x)))

  def load_yaml(home: str, filename: str):
    with AdventureUtil.get_config_file(home, filename) as f:
      return yaml.safe_load(f)

  def get_config_filename(home: str, filename: str) -> str:
    return os.path.join(home, filename)

  def get_config_file(home: str, filename: str) -> TextIOWrapper:
    return open(AdventureUtil.get_config_filename(home, filename))
