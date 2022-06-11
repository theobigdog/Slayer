
from flask_login import UserMixin


class SlayerUser(UserMixin):
  def __init__(self, id):
    self.id = id
    self.name = 'user' + str(self.id)
    self.password = self.name + '_secret'

    self.is_authenticated = True
    self.is_active = True
    self.is_anonymous = False

  def to_json(self):
    return {"name": self.name, "email": self.email}

  def is_authenticated(self):
    return True

  def is_active(self):
    return True

  def is_anonymous(self):
    return False

  def get_id(self):
    return self.id

