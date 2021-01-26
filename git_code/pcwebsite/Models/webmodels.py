from ..flask_app import app,db


class HDImages(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)