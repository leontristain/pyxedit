from xelib.xedit.base import XEditBase
from xelib.xedit.misc import XEditError


class XEditAttribute:
    '''
    A descriptor class that can be used to quickly declare any sub-field of
    a record as an xedit object property. This encapsulates the logic for
    getting and setting a value at a subpath from the object.
    '''
    def __init__(self,
                 path,
                 required=False,
                 enum=None,
                 object_class=None,
                 read_only=False):
        self.path = path
        self.enum = enum
        self.object_class = object_class
        self.required = required
        self.read_only = read_only

    def __get__(self, obj, type=None):
        '''
        Gets an attribute on a given object as defined by our path. Abides by
        the following rules:
          * if element at path does not exist, a None is returned
          * if element at path exists but is a non-value element, the element
              object itself is returned
          * otherwise, the element value is returned
          * if an enum has been provided for us, we will use the enum to
              translate between enum values and raw values for the caller
        '''
        with obj.manage_handles():
            # get the sub-object at the given path, if a sub_obj can't be
            # gotten, just return None
            sub_obj = obj.get(self.path)
            if not sub_obj:
                return None

            # if the sub-object is a non-value object, just return the object
            # itself, otherwise get the value and transform it via enum if
            # necessary
            if self.is_non_value_object(sub_obj):
                value = sub_obj
            else:
                value = sub_obj.value
                if self.enum:
                    value = self.enum(value)

            # if the value ended up being an object derived from XEditBase,
            # we will need to apply any explicitly-given object class, and
            # make sure to promote it before we return it
            if isinstance(value, XEditBase):
                if self.object_class:
                    value = self.object_class.from_xedit_object(
                                                  value.handle, value)
                value.promote()

            # return the value
            return value

    def __set__(self, obj, value):
        '''
        Sets an attribute on a given object with a given value as defined by our
        path. Abides by the following rules:
          * if a None is provided as value, the element at path is deleted if
              the element can be deleted, otherwise an error will be raised
          * otherwise, the element at path is created if it does not exist, and
              then the value is set on it
          * if the element at path is a non-value element, an error will be
              raised as you cannot set a raw value on a non-value element
          * if an enum has been provided for us, we will use the enum to
              translate between enum values and raw values for the caller
        '''
        # read only attributes are not allowed to set
        if self.read_only:
            raise XEditError(f'Cannot set read-only attribute to {value}')

        # prepare the value to be set
        value = value.value if value and self.enum else value

        with obj.manage_handles():
            # get the sub object, keep track of its original existence
            sub_obj = obj.get(self.path)
            originally_exists = bool(sub_obj)

            # if value is None, we delete the object we found and we're done
            if value is None and sub_obj:
                if sub_obj.is_removable:
                    sub_obj.delete()
                    return
                else:
                    raise XEditError(f'Cannot delete unremovable element '
                                     f'{sub_obj} by setting it to None')

            # otherwise, we are setting a real value, in which case we may
            # need to add the object if it does not yet exist
            if not sub_obj:
                sub_obj = obj.add(self.path)

            # try to set the object (and check if it's a non-value object);
            # if value cannot be successfully set, we need to delete any object
            # we just added
            try:
                if self.is_non_value_object(sub_obj):
                    raise XEditError(f'Cannot set value of non-value '
                                        f'object {sub_obj} to {value}')
                else:
                    sub_obj.value = value
            except Exception:
                if not originally_exists:
                    sub_obj.delete()
                raise

    def is_non_value_object(self, obj):
        return obj.def_type in (obj.DefTypes.dtRecord,
                                obj.DefTypes.dtSubRecord,
                                obj.DefTypes.dtSubRecordArray,
                                obj.DefTypes.dtSubRecordStruct,
                                obj.DefTypes.dtArray,
                                obj.DefTypes.dtStruct)
