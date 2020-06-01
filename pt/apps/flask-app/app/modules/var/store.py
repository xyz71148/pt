import simplejson as json
from flask_sqlalchemy import SQLAlchemy

from app.helpers.base_model import BaseModel
from app.helpers.helper import cache

db = SQLAlchemy()

cache_key_template = "VAR_CACHE_{}"


class Var(db.Model, BaseModel):
    __tablename__ = 'variables'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    value = db.Column(db.Text())
    versions = db.Column(db.Text())
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime())
    is_deleted = db.Column(db.Boolean())

    def __repr__(self):
        return '<%s name=%r id=%d>' % (self.__class__.__name__, self.name,self.id)
    
    @classmethod
    def get_inc(cls, name):
        res = cls.get_query().filter_by(name = name,is_deleted = False).first()
        if res is not None:
            inc = int(res.value[1:]) + 1
        else:
            inc = 1
        val = "_{}".format(inc)
        cls.set(name, val)
        return inc

    @classmethod
    def get(cls, name, is_json=False):
        from_cache = cache.get(cache_key_template.format(name))
        if from_cache is None:
            res = cls.get_query().filter_by(name = name,is_deleted = False).first()
            if res is None:
                value = "{}" if is_json else ""
                obj = cls(name=name, value=value)
                obj.save()
                cache.set(cache_key_template.format(name), value)
                result = json.loads(value) if is_json else ""
            else:
                cache.set(cache_key_template.format(name), res.value)
                result = json.loads(res.value) if is_json else res.value
        else:
            result = json.loads(from_cache) if is_json else from_cache
        return result

    @classmethod
    def set(cls, name, value):
        obj = cls.get_query().filter_by(name = name,is_deleted = False).first()
        if not obj:
            obj = cls(name=name, value=value)
            obj.save()
        else:
            obj.value = value
            obj.save()
        cache.delete(cache_key_template.format(name))
        return True

    @classmethod
    def del_cache(cls, name):
        cache.delete(cache_key_template.format(name))

    @staticmethod
    def get_db():
        return db

