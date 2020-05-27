from flask_sqlalchemy import SQLAlchemy
from app.helpers.base_model import BaseModel

db = SQLAlchemy()


class EmailCaptcha(db.Model,BaseModel):
    __tablename__ = 'email_captcha'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(10))
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime())

    def __repr__(self):
        return '<%s %r %r>' % (self.__class__.__name__, self.email, self.code)

    @classmethod
    def get_by_email(cls, email):
        res = cls.get_query().filter(cls.email == email).first()
        return res if res is not None else None

    @staticmethod
    def get_db():
        return db