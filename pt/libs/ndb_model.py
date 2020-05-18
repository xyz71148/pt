from google.cloud import ndb


class BaseModel(ndb.Model):
    @classmethod
    def get_fields(cls):
        res = dict()
        for key in cls.__dict__.keys():
            obj = str(type(cls.__dict__[key]))
            if "google.cloud.ndb.model" in obj:
                res[key] = dict(
                    type=obj.replace("<class 'google.cloud.ndb.model.", "").replace("Property'>", "")
                )
        return res

    @classmethod
    def get_detail(cls, obj, form_list=False):
        res = dict(
            id=obj.key.id(),
        )
        fields = cls.get_fields().keys()
        for field in fields:
            val = getattr(obj, field)
            if field in ["expired_at", "updated_at", "created_at"]:
                val = val.timestamp() if val is not None else 0
            res[field] = val
        return res

    @classmethod
    def rows(cls, page=1, limit=10, order="-created_at"):
        page = int(page)
        limit = int(limit)
        total = cls.query().filter().count()
        offset = (page - 1) * limit
        order_param = +getattr(cls, order[1:]) if order[0:1] == "+" else -getattr(cls, order[1:])
        rows = cls.query().filter().order(order_param).fetch(limit, offset=offset)

        return dict(
            rows=[cls.get_detail(row, form_list=True) for row in rows] if rows is not None else None,
            page=page,
            total=total,
            limit=limit,
            order=order,
            fields=cls.get_fields()
        )

    @classmethod
    def row(cls, row_id):
        row_id = int(row_id)
        res = cls.query(cls.key == ndb.Key(cls, row_id)).get()
        return res if res is not None else None
