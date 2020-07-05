from pyxedit.xelib.wrapper_methods.base import WrapperMethodsBase


class GroupsMethods(WrapperMethodsBase):
    def has_group(self, id_, signature, ex=True):
        '''
        Returns true if a given file has a group for a given signature.

        Args:
            id\\_ (``int``)
                id handle of file
            signature (``str``)
                signature to check whether file has a group for
        '''
        return self.has_element(id_, signature, ex=ex)

    def add_group(self, id_, signature, ex=True):
        '''
        Adds the group of given signature to the given file

        Args:
            id\\_ (``int``)
                id handle of file
            signature (``str``)
                signature to add group for

        Returns:
            (``int``) id handle of group
        '''
        return self.add_element(id_, signature, ex=ex)

    def get_child_group(self, id_, ex=True):
        '''
        Returns a handle to the child group of given element.

        Args:
            id\\_ (``int``)
                id handle of element to get child group for
        '''
        return self.get_element(id_, 'Child Group', ex=ex)
