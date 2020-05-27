from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class EmailCaptcha(db.Model):
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
        res = cls.query.filter(cls.email == email).first()
        return res if res is not None else None

    @staticmethod
    def put(obj):
        db.session.add(obj)
        db.session.commit()

    @staticmethod
    def delete(obj):
        db.session.delete(obj)
        db.session.commit()