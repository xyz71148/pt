from datetime import datetime
from sqlalchemy import desc, asc
import logging


class BaseModel(object):

    @classmethod
    def get_query(cls):
        return cls.query

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

        total = cls.query.filter_by(**filter_by).count()
        rows = cls.query.filter_by(**filter_by).order_by(order_by).limit(int(limit)).offset(int(limit) * (int(page) - 1)).all()

        return dict(
            rows=[cls.to_dict(row) for row in rows] if rows is not None else None,
            page=page,
            total=total,
            limit=limit,
            order=order,
        )

    def get_id(self):
        return self.id

    @classmethod
    def get_filter_by(cls,filter_by,kwargs):
        logging.info("kwargs: %s",kwargs)
        return filter_by

    @classmethod
    def skip_dict_field(cls):
        return []

    def to_dict(self):
        logging.info("===>>>>>self: %s",self)
        logging.info(self)
        res = dict()
        logging.info(vars(self).keys())
        for key in vars(self).keys():
            logging.info('key: %s',key)
            if key in self.skip_dict_field():
                continue
            if key[0:1] != "_":
                res[key] = getattr(self, key)

        logging.info(res)
        logging.info("===>>>>>end")
        return res

    def save(self):
        keys = vars(self.__class__).keys()
        if "created_at" in keys:
            if not self.created_at:
                self.created_at = datetime.utcnow()

        if "updated_at" in keys:
            self.updated_at = datetime.utcnow()

        if "is_deleted" in keys:
            self.is_deleted = False if not self.is_deleted else True

        self.get_db().session.add(self)
        self.get_db().session.commit()
        return self

    def delete(self):
        self.is_deleted = True
        self.save()
        return self

    def remove(self):
        self.get_db().session.delete(self)
        self.get_db().session.commit()