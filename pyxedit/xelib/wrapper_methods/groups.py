from pyxedit.xelib.wrapper_methods.base import WrapperMethodsBase


class GroupsMethods(WrapperMethodsBase):
    def has_group(self, id_, signature, ex=True):
        return self.has_element(id_, signature, ex=ex)

    def add_group(self, id_, signature, ex=True):
        return self.add_element(id_, signature, ex=ex)

    def get_child_group(self, id_, ex=True):
        return self.get_element(id_, 'Child Group', ex=ex)
