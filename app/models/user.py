from app.extensions import db
from . import InfoCrud
from werkzeug.security import generate_password_hash, check_password_hash


class User(InfoCrud):
    username = db.Column(db.String(32), nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def _set_fields(self):
        self._exclude = ['delete_time', 'password']

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password, password)

    def reset_password(self, old_password, new_password):
        if self.validate_password(old_password):
            self.password = new_password
            return True
        return False
