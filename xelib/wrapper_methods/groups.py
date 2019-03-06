from xelib.wrapper_methods.base import WrapperMethodsBase


class GroupsMethods(WrapperMethodsBase):
    def has_group(self, id_, signature):
        return self.has_element(id_, signature)

    def add_group(self, id_, signature):
        return self.add_element(id_, signature)

    def get_child_group(self, id_):
        return self.get_element(id_, 'Child Group')
