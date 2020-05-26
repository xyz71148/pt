from app.helpers.helper import cache
import simplejson as json
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Var(db.Model):
    __tablename__ = 'vars'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    value = db.Column(db.Text())

    def __repr__(self):
        return '<%s %r>' % (self.__class__.__name__, self.name)

    @staticmethod
    def get_inc(key):
        res = Var.query.filter(Var.name == key).get()
        if res is not None:
            inc = int(res.value[1:]) + 1
        else:
            inc = 1
        val = "_{}".format(inc)
        Var.set(key, val)
        return inc

    @staticmethod
    def get(name, is_json=True):
        from_cache = cache.get("VAR_CACHE_{}".format(name))
        if from_cache is None:
            res = Var.query.filter(Var.name == name).first()
            if res is None:
                value = "{}" if json else ""
                var = Var(name=name, value=value)
                Var.put(var)
                cache.set("VAR_CACHE_{}".format(name), value)
                setting = json.loads(value) if is_json else ""
            else:
                cache.set("VAR_CACHE_{}".format(name), res.value)
                setting = json.loads(res.value) if is_json else res.value
        else:
            setting = json.loads(from_cache) if is_json else from_cache
        return setting

    @staticmethod
    def set(name, value):
        exists = Var.query.filter(Var.name == name).first()
        if not exists:
            var = Var(name=name, value=value)
            Var.put(var)
        else:
            exists.value = value
            Var.put(exists)
        cache.delete("VAR_CACHE_{}".format(name))
        return True

    @classmethod
    def del_cache(cls, name):
        cache.delete("VAR_CACHE_{}".format(name))

    @classmethod
    def remove(cls, name):
        cache.delete("VAR_CACHE_{}".format(name))
        var = Var.query.filter(Var.name == name).first()
        Var.delete(var)

    @staticmethod
    def rows():
        res = Var.query.all()
        return res if res is not None else None

    @staticmethod
    def put(obj):
        db.session.add(obj)
        db.session.commit()

    @staticmethod
    def delete(obj):
        db.session.delete(obj)
        db.session.commit()
