class BaseModel(object):
    @classmethod
    def row(cls, row_id):
        res = cls.query.filter(cls.id == int(row_id)).first()
        return res if res is not None else None

    @classmethod
    def rows(cls, page=1, limit=10, order="id"):
        res = cls.query.all()
        return [cls.to_dict(row) for row in res] if res is not None else None

    @staticmethod
    def to_dict(obj):
        res = dict()
        for key in vars(obj).keys():
            if key[0:1] != "_":
                res[key] = vars(obj)[key]
        return res
