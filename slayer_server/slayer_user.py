
from flask_login import UserMixin


class SlayerUser(UserMixin):
  def __init__(self, id, name):
    self.id = id
    self.name = name
    self.password = self.name + '_secret'

    #self.is_authenticated = True
    UserMixin.is_active = True
    #self.is_anonymous = False

  def to_json(self):
    return {"name": self.name, "email": self.email}

  # def get_id(self):
  #   return self.id

