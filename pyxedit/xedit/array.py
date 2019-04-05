from pyxedit.xedit.generic import XEditGenericObject
from pyxedit.xedit.misc import XEditError


class XEditArray(XEditGenericObject):
    '''
    The array class for use by array types.
    '''
    def __len__(self):
        '''
        Implements length calculation (`len(obj)`)

        Length calculation for an array class is the same as the num_children
        property.
        '''
        return self.num_children

    def __getitem__(self, index):
        '''
        Implements indexing behavior (`[]` operator)

        Indexing for an array type, like all other 'python-native' behaviors
        on this class, will attempt to operate based on the value of the array
        item object if the array item object is a <Types.Value> or <Types.Ref>
        object. Otherwise, it will operate on the array item object itself.

        The implementation is built on top of the implementation of the
        get_object_at_index method in this same class.
        '''
        obj = self.get_object_at_index(index)

        if obj.type in (obj.Types.Value, obj.Types.Ref):
            to_return = obj.value
        else:
            to_return = obj

        return to_return

    def __iter__(self):
        '''
        Implements iteration behavior (`for item in <obj>`)

        Iteration for an array type, like all other 'python-native' behaviors
        on this class, will attempt to operate based on the value of the array
        item object if the array item object is a <Types.Value> or <Types.Ref>
        object. Otherwise, it will operate on the array item object itself.

        The implementation is a simple for loop iterating over the index range,
        yielding __getitem__-produced values
        '''
        for index in range(len(self)):
            yield self[index]

    def get_object_at_index(self, index):
        '''
        Retrieves the array item object at the given index. This serves as the
        backbone implementation of __getitem__ but strictly works with array
        item objects, so it also provides the user an alternative for when they
        absolutely want the array item objects (instead of possibly their
        values)

        Should support negative indexing, and raise IndexError just like a
        normal __getitem__ would. Probably no need to implement slicing syntax.
        '''
        len_ = len(self)

        # support negative indexing
        if index < 0:
            index += len_

        # raise IndexError on out of range resolved index
        if not 0 <= index < len_:
            raise IndexError(f'XEditArray has {len_} items; resolved '
                             f'index {index} is out of range')

        # return the object at the index
        return self.objectify(self.xelib_run('get_element', path=f'[{index}]'))

    @property
    def objects(self):
        '''
        Yields the array item objects upon iteration. This is a version of
        __iter__ that strictly works with array item objects (instead of
        possibly their values)
        '''
        for index in range(len(self)):
            yield self.get_object_at_index(index)

    def index(self, item, obj=False):
        '''
        Support the .index function found in python lists. (`obj.index(item)`)

        The given item can be any XEditBase-derived object with a handle
        equivalent to an array element here. Implementation is via iterative
        search based on equality.
        '''
        for i, my_item in enumerate(self.objects if obj else self):
            if item == my_item:
                return i
        raise ValueError(f'item equivalent to {item} is not in the list')

    def add(self, value):
        '''
        Support a `.add` function for adding an item into the array.
        Since we will almost never have standalone structs that aren't already
        part of the array they should be in, this method is primarily used for
        simple-value array items where the value can be provided to add as an
        item into the array. For struct arrays, the user is expected to use
        the `add_item_with` method instead.
        '''
        return self.add_item_with(value)

    def remove(self, value):
        '''
        Support a `.add` function for removing an item from the array.
        This method is primarily used for simple-value array items where the
        value can be provided to remove a matching item from the array. For
        struct arrays, the user is expected to use the `remove_item_with`
        method instead.
        '''
        return self.remove_item_with(value)

    def add_item_with(self, value, subpath=''):
        '''
        Adds an item to the array with the given value at the given subpath.

        An xedit object can be given as the value, in which case its form_id_str
        will be set as the value at the given subpath under the array.
        '''
        if isinstance(value, XEditGenericObject):
            value = value.form_id_str
        return self.objectify(
            self.xelib_run('add_array_item', '', subpath, value))

    def has_item_with(self, value, subpath=''):
        '''
        Checks whether an item exists with the given value at the given subpath.

        An xedit object can be given as the value, in which case its form_id_str
        will be used as value for the check.
        '''
        if isinstance(value, XEditGenericObject):
            value = value.form_id_str
        return self.xelib_run('has_array_item', '', subpath, value, ex=False)

    def find_item_with(self, value, subpath=''):
        '''
        Returns the array item with the given value at the given subpath.

        An xedit object can be given as the value, in which case its form_id_str
        will be used as value for the retrieval.
        '''
        if isinstance(value, XEditGenericObject):
            value = value.form_id_str
        item_handle = self.xelib_run(
            'get_array_item', '', subpath, value, ex=False)
        if item_handle:
            return self.objectify(item_handle)

    def remove_item_with(self, value, subpath=''):
        '''
        Removes the array item with the given value at the given subpath.

        An xedit object can be given as the value, in which case its form_id_str
        will be used as value for the removal.
        '''
        if isinstance(value, XEditGenericObject):
            value = value.form_id_str
        return self.xelib_run('remove_array_item', '', subpath, value)

    def move_item(self, sub_object, to_index):
        '''
        Move an object in the array to the given index.
        '''
        if sub_object not in self.objects:
            raise XEditError(f'Attempted to move array item {sub_object} '
                                f'within array {self} of which it does not '
                                f'belong in')
        return self.xelib.move_array_item(sub_object.handle, to_index)
