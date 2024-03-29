from sqlalchemy.ext.declarative import DeclarativeMeta
import json

def alchemy_encoder():
    _visited_objs = []

    class AlchemyEncoder(json.JSONEncoder):
        def default(self, obj):
            res = None
            if isinstance(obj.__class__, DeclarativeMeta):
                res = obj
                # don't re-visit self
                if obj in _visited_objs:
                    return None
                _visited_objs.append(obj)

                # an SQLAlchemy class
                fields = {}
                for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                    fields[field] = obj.__getattribute__(field)
                # a json-encodable dict
                return fields

            if res is None:
                return None
            return json.JSONEncoder.default(self, res)

    return AlchemyEncoder