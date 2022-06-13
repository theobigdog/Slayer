
from .slayer_user import SlayerUser
import uuid

import namegenerator
import random


class UserManager:
  def __init__(self):
    self.user_dict = {}

  def establish_user(self):
    id = str(uuid.uuid1())
    name = random.choice(namegenerator.LEFT) + ' ' + random.choice(namegenerator.RIGHT)
    user = SlayerUser(id, name)
    self.user_dict[id] = user
    print('Inserting new user with ID=' + id)
    return user

  def lookup_user(self, user_id):
    print('UserManager: request for user ID=' + user_id)
    user = self.user_dict.get(str(user_id))
    if user == None:
      print('  No user found.')
    return user

