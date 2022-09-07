
from slayer_server.slayer_files import Slayer_Root
import os


class PartyManager:
  party_dir = os.path.join(Slayer_Root, 'party')

  def __init__(self) -> None:
    self.party_dir = {}
    for entry in os.listdir(PartyManager.party_dir):
      key = str(dir)
    pass