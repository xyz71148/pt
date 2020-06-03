import simplejson as json
from flask_sqlalchemy import SQLAlchemy
from pt.libs.utils import shell_exec_result
import googleapiclient.discovery
from app.helpers.base_model import BaseModel
from app.helpers.helper import cache
from app.helpers.helper import mail_send


def get_compute(v="v1"):
    return googleapiclient.discovery.build('compute', v)


db = SQLAlchemy()

STATUS = dict(
    created="已创建",
    processing="处理中",
    ok="完成",
    error="失败",
    timeout="超时"
)

cache_key_template = "TASK_CACHE_{}"


class Task(db.Model, BaseModel):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Text())
    result = db.Column(db.Text())
    status = db.Column(db.String(20), nullable=False)
    executor = db.Column(db.String(50))

    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime())
    is_deleted = db.Column(db.Boolean())

    def __repr__(self):
        return '<%s id=%d>' % (self.__class__.__name__, self.get_id())

    @staticmethod
    def get_db():
        return db

    @classmethod
    def get(cls, row_id):
        cache_row = cache.get(cache_key_template.format(row_id))
        if cache_row is None:
            obj = cls.row(row_id)
            res = obj.to_dict()
            cache.set(cache_key_template.format(obj.get_id()), json.dumps(res))
        else:
            res = json.loads(cache_row)
        return res

    @classmethod
    def create(cls,data):
        obj = cls()
        obj.data = data
        obj.status = STATUS['created']
        obj.save()
        res = obj.to_dict()
        cache.set(cache_key_template.format(obj.get_id()), json.dumps(res))
        return res

    @classmethod
    def update(cls, row_id, status,executor=None, result=None):
        if status not in STATUS.values():
            raise Exception("invalid status",404)

        row = cls.row(row_id)
        if row is None:
            raise Exception("not found row",404)
        row.status = status
        if result is not None:
            row.result = result
        if executor is not None:
            row.executor = executor
        row.save()
        res = row.to_dict()
        cache.set(cache_key_template.format(row.get_id()), json.dumps(res))
        return res

    @classmethod
    def del_cache(cls, name):
        cache.delete(cache_key_template.format(name))

    @classmethod
    def rows_skip_dict_field(cls):
        return ["result"]

    @classmethod
    def exec(cls, action, params):
        res = ""
        status = STATUS['ok']
        if action == 'email':
            mail_send(**params)
            res = "ok"
        if action == 'shell':
            res = shell_exec_result(params['cmd'])
        try:
            if action == 'instance.delete':
                res = json.dumps(get_compute().instances().delete(**params).execute())
            if action == 'instance.create':
                res = json.dumps(get_compute("beta").instances().insert(**params).execute())
            if action == 'instance.stop':
                res = json.dumps(get_compute().instances().stop(**params).execute())
            if action == 'instance.start':
                res = json.dumps(get_compute().instances().start(**params).execute())
            if action == 'instance.reset':
                res = json.dumps(get_compute().instances().reset(**params).execute())
            if action == 'instance.create_machine_image':
                res = json.dumps(get_compute("beta").machineImages().insert(**params).execute())
        except Exception as e:
            res = str(e)
            status = STATUS['error']
        return status, res