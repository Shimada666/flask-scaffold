from app.extensions import db
from . import InfoCrud


class Post(InfoCrud):
    title = db.Column(db.String(20), nullable=False, default="")
    content = db.Column(db.Text)
