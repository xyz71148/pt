from datetime import datetime
from sqlalchemy import desc, asc
import logging

class BaseModel(object):
    @classmethod
    def row(cls, row_id):
        res = cls.query.filter(cls.id == int(row_id)).first()
        return res if res is not None else None

    @classmethod
    def rows(cls, **kwargs):
        page = kwargs.get('page', "1")
        limit = kwargs.get('limit', "10")
        order = kwargs.get('order', "-id")

        is_deleted = kwargs.get('is_deleted', "false")

        if order[0:1] == "-":
            order_by = desc(getattr(cls, order[1:]))
        else:
            order_by = asc(getattr(cls, order[1:]))

        filter_by = dict()

        if "is_deleted" in vars(cls).keys():
            filter_by["is_deleted"] = False if is_deleted == "false" else True
        filter_by = cls.get_filter_by(filter_by,kwargs)
        res = cls.query.filter_by(**filter_by).order_by(order_by).limit(int(limit)).offset(int(limit) * (int(page) - 1)).all()
        return [cls.to_dict(row) for row in res] if res is not None else None

    @classmethod
    def get_filter_by(cls,filter_by,kwargs):
        logging.info("kwargs: %s",kwargs)
        return filter_by

    @classmethod
    def skip_dict_field(cls):
        return []

    @classmethod
    def to_dict(cls,obj):
        res = dict()
        for key in vars(obj).keys():
            if key in cls.skip_dict_field():
                continue
            if key[0:1] != "_":
                res[key] = vars(obj)[key]
        return res

    @classmethod
    def put(cls, obj):
        if "created_at" in vars(cls).keys():
            if not obj.created_at:
                obj.created_at = datetime.utcnow()

        if "updated_at" in vars(cls).keys():
            obj.updated_at = datetime.utcnow()

        if "is_deleted" in vars(cls).keys():
            obj.is_deleted = False if not obj.is_deleted else True

        cls.get_db().session.add(obj)
        cls.get_db().session.commit()
        return obj

    @classmethod
    def delete(cls, obj):
        obj.is_deleted = True
        obj = cls.put(obj)
        return obj

    @classmethod
    def remove(cls, obj):
        cls.get_db().session.delete(obj)
        cls.get_db().session.commit()