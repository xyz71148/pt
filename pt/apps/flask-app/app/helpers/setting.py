from app.helpers.helper import cache
import simplejson as json
from app.modules.var.store import Var


class Setting(object):
    @staticmethod
    def get(name, namespace="setting", default=None, update=False):
        setting = Var.get(namespace + ".json", is_json=True)
        if name not in setting.keys():
            if update:
                setting[name] = default
                Var.set(namespace + ".json", json.dumps(setting))
                cache.set("SETTING_CACHE_{}".format(namespace), json.dumps(setting))
            return default
        else:
            return setting[name]

    @staticmethod
    def set(name, value, namespace="setting"):
        setting = Var.get(namespace + ".json", is_json=True)
        if setting is None:
            setting = dict()
        setting[name] = value
        cache.set("SETTING_CACHE_{}".format(namespace), json.dumps(setting))
        Var.set(namespace + ".json", json.dumps(setting))

    @staticmethod
    def remove(name, namespace = "setting"):
        setting = Var.get(namespace + ".json", is_json=True)
        if name in setting.keys():
            del setting[name]
            Var.set(namespace + ".json", json.dumps(setting))
            cache.set("SETTING_CACHE_{}".format(namespace), json.dumps(setting))

    @staticmethod
    def rows(namespace="setting"):
        return Var.get(namespace + ".json", is_json=True)
