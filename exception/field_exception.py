class FieldException(Exception):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __str__(self):
        return "<FieldException(code='%s', message='%s')>" % (self.__dict__['code'].value, self.__dict__['message'])

