from functools import wraps
from sqlalchemy.engine import Row

def convert_db_row_to_dict(func):
    @wraps(func)
    def wrapper(*args, **kw):
        print('{} called'.format(func.__name__))
        result = []
        try:
            res = func(*args, **kw)
        finally:
            print('{} finished'.format(func.__name__))

            if isinstance(res, list) and all(isinstance(x, Row) for x in res):
                for one_res in res:
                    u = one_res._asdict()
                    result.append(u)
        return result
    return wrapper