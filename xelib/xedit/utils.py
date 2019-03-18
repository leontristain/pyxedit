class XEditAttribute:
    def __init__(self, path):
        self.path = path

    def __get__(self, obj, type=None):
        return obj.get_value(path=self.path)

    def __set__(self, obj, value):
        return obj.set_value(value, path=self.path)
