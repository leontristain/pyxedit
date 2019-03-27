from xelib.xedit.attribute import XEditAttribute
from xelib.xedit.base import XEditBase
from xelib.xedit.misc import XEditError


class XEditGenericObject(XEditBase):
    def __repr__(self):
        return f'<{self.__class__.__name__} {self.name}>'

    @property
    def value(self):
        '''
        The value property.

        Xelib handles point to elements that may or may not be an element that
        stores a value. If stored, the value will have a type, and for integer
        values it may be a reference to a record. All of this can be determined
        based on some combination of element_type, def_type, smash_type, and
        value_type.

        The `.type` property already does the work of inspecting the record to
        figure out whether it is a `Value` or `Ref` element. Here, we will
        retrieve the value based on the `.type` property and the value's def
        type.

          - A <Types.Ref> element should return the linked object as the value.
          - A <Types.Value> element should return the appropriately typed value
                based on the DefType
          - Otherwise, a None should be returned.
        '''
        if self.type == self.Types.Ref:
            referenced = self.xelib.get_links_to(self.handle, ex=False)
            return self.objectify(referenced) if referenced else None
        elif self.type == self.Types.Value:
            if self.def_type in (self.DefTypes.dtString,
                                 self.DefTypes.dtLString):
                return self.xelib.get_value(self.handle)
            elif self.def_type == self.DefTypes.dtInteger:
                return self.xelib.get_int_value(self.handle)
            elif self.def_type == self.DefTypes.dtFloat:
                return self.xelib.get_float_value(self.handle)
            else:
                raise NotImplementedError(
                    f'Just encountered value type {self.def_type}, which is '
                    f'not yet supported as a gettable value; we should check '
                    f'it out and add it')

    @value.setter
    def value(self, value):
        '''
        Setter for the value property.
          - A <Types.Ref> element should expect another object to be provided
                and link to it.
          - A <Types.Value> element should be set the appropriately typed value
                based on the DefType
          - Otherwise, attempting to set the value should result in an error.
        '''
        if self.type == self.Types.Ref:
            return self.xelib.set_links_to(self.handle, value.handle)
        elif self.type == self.Types.Value:
            if self.def_type in (self.DefTypes.dtString, self.DefTypes.dtLString):
                return self.xelib.set_value(self.handle, str(value))
            elif self.def_type == self.DefTypes.dtInteger:
                return self.xelib.set_int_value(self.handle, int(value))
            elif self.def_type == self.DefTypes.dtFloat:
                return self.xelib.set_float_value(self.handle, float(value))
            else:
                raise NotImplementedError(
                    f'Just encountered value type {self.def_type}, which is '
                    f'not yet supported as a settable value; we should check '
                    f'it out and add it')
        else:
            raise XEditError(f'Cannot set the value of element {self} with '
                             f'type {self.type}')

    data_size = XEditAttribute('Record Header\\Data Size')
    form_version = XEditAttribute('Record Header\\Form Version')
    editor_id = XEditAttribute('EDID')

    @property
    def form_id(self):
        return self.xelib_run('get_int_value', path='Record Header\\FormID')

    @property
    def form_id_str(self):
        return f'{self.form_id:0>8X}'

    @property
    def plugin(self):
        return self.objectify(self.xelib_run('get_element_file'))

    def copy_into(self, target_plugin, as_new=False):
        # for this to work, self must be a record, and target must be a file
        assert self.element_type == self.ElementTypes.etMainRecord
        assert target_plugin.element_type == target_plugin.ElementTypes.etFile

        # add required masters for copying self into the given plugin
        target_plugin.add_masters_needed_for_copying(self, as_new=as_new)

        # copy our element over as override
        return self.objectify(self.xelib_run('copy_element',
                                             target_plugin.handle,
                                             as_new=as_new))
