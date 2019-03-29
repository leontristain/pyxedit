from xelib.xedit.attribute import XEditAttribute
from xelib.xedit.base import XEditBase
from xelib.xedit.misc import XEditError


class XEditGenericObject(XEditBase):
    def __repr__(self):
        return (f'<{self.__class__.__name__} '
                f'{self.signature or "----"} '
                f'{self.form_id_str or "--------"} '
                f'{self.name} {self.handle}>')

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
        form_id = self.xelib_run('get_form_id', ex=False)
        if form_id:
            return form_id

    @property
    def form_id_str(self):
        form_id = self.form_id
        if form_id:
            return f'{form_id:0>8X}'

    @property
    def local_form_id(self):
        form_id = self.xelib_run('get_form_id', local=True, ex=False)
        if form_id:
            return form_id

    @property
    def local_form_id_str(self):
        local_form_id = self.local_form_id
        if local_form_id:
            return f'{local_form_id:0>8X}'

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

    def find_text_values(self):
        '''
        Iterate over all descendants of the current node and yields any
        non-empty text values found.
        '''
        for descendant in self.descendants:
            if descendant.def_type in (descendant.DefTypes.dtString,
                                       descendant.DefTypes.dtLString):
                value = descendant.value
                if value:
                    yield value

    def find_related_objects(self,
                             signatures=None,
                             recurse=False,
                             same_plugin=False):
        '''
        Iterates over all descendants of the current node and yields any
        non-empty reference targets.

        @param signatures: a list of signatures can be provided here to
                           limit the target types traversed and yielded
        @param recurse: whether to further traverse from any found valid target
        @param same_plugin: if set to True, only reference targets belonging
                            to the same plugin as this object will be considered
                            valid for yielding and recursing
        '''
        signatures = signatures or []

        # start by finding related objects for `self`; we may add to this
        # list if recurse is set to True
        to_visit = [self]

        for item in to_visit:
            # iterate over item's descendants
            for descendant in item.descendants:

                # if descendant element is not a reference, ignore
                if descendant.type != descendant.Types.Ref:
                    continue

                # if the descendent element is the 'FormID' element, ignore
                # (since all records have a 'FormID' element that just points
                #  to itself)
                if descendant.name == 'FormID':
                    continue

                # attempt to retrieve the reference target, if there's nothing
                # there, ignore
                ref_target = descendant.value
                if not ref_target:
                    continue

                # if we have already walked over this record, ignore
                if ref_target in to_visit:
                    continue

                # if we specified a list of signatures, and the ref target is
                # not one of the signatures, ignore
                if signatures and ref_target.signature not in signatures:
                    continue

                # if we specified same_plugin, and the ref target does not
                # belong to the same plugin, ignore
                if same_plugin and ref_target.plugin != self.plugin:
                    continue

                # okay, by this point the reference is a valid one we care
                # about; if we are recursing, add it back to the visit list
                if recurse:
                    to_visit.append(ref_target)

                # and finally, yield it to the caller
                yield ref_target
