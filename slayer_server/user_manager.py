
from .slayer_user import SlayerUser
import uuid


class UserManager:
  def __init__(self):
    self.user_dict = {}

  def establish_user(self):
    id = str(uuid.uuid1())
    user = SlayerUser(id)
    self.user_dict[id] = user
    print('Inserting new user with ID=' + id)
    return user

  def lookup_user(self, user_id):
    print('UserManager: request for user ID=' + user_id)
    user = self.user_dict.get(str(user_id))
    if user == None:
      print('  No user found.')
      print('Dict=')
      print(self.user_dict)
    return user
    try:
      user = self.user_dict[str(user_id)]
      return user
    except:
      print('  No user found.')
      print('Dict=')
      print(self.user_dict)
      return None

