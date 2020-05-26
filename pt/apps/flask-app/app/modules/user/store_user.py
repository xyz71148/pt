from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class BaseModel(object):
    @classmethod
    def row(cls, row_id):
        res = cls.query.filter(cls.id == int(row_id)).first()
        return res if res is not None else None

    @staticmethod
    def toDict(obj):
        res = dict()
        for key in vars(obj).keys():
            if key[0:1] != "_":
                res[key] = vars(obj)[key]
        return res

    @staticmethod
    def put(obj):
        db.session.add(obj)
        db.session.commit()

class User(db.Model,BaseModel):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100),unique=True,index=True)
    name = db.Column(db.String(100),unique=True,index=True)
    level = db.Column(db.Integer)
    password = db.Column(db.String(32))
    created_at = db.Column(db.Date())
    updated_at = db.Column(db.Date())

    def __repr__(self):
        return '%s (id=%r,name=%r)' % (self.__class__.__name__, self.id,self.name)

    @classmethod
    def get_by_email(cls, email):
        res = cls.query.filter(cls.email == email).first()
        return res if res is not None else None

