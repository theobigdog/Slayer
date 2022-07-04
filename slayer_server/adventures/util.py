
from io import TextIOWrapper
import os
import yaml

class AdventureUtil:
  def load_yaml(home: str, filename: str):
    with AdventureUtil.get_config_file(home, filename) as f:
      return yaml.safe_load(f)

  def get_config_filename(home: str, filename: str) -> str:
    return os.path.join(home, filename)

  def get_config_file(home: str, filename: str) -> TextIOWrapper:
    return open(AdventureUtil.get_config_filename(home, filename))
