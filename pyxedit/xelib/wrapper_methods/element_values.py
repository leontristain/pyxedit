from pyxedit.xelib.wrapper_methods.base import WrapperMethodsBase


class ElementValuesMethods(WrapperMethodsBase):
    def name(self, id_, ex=True):
        '''
        Returns the name of an element.

        NOTE: This is not the same as xEdit's ``Name`` function - ``long_name``
        is.

        Args:
            id\\_ (``int``)
                id handle of element

        Returns:
            (``str``) name of element, examples (depending on element) may
            include ``Armor``, ``Block 0``, ``Iron Gauntlets``, ``ITPOTest``,
            and ``"Windhelm" <32,9>``.
        '''
        return self.get_string(
            lambda len_: self.raw_api.Name(id_, len_),
            error_msg=f'Name failed on {id_}',
            ex=ex)

    def long_name(self, id_, ex=True):
        '''
        Returns the long name of an element. This should be identical to
        the ``Name`` function from xEdit scripting.

        Args:
            id\\_ (``int``)
                id handle of element

        Returns:
            (``str``) long name of element
        '''
        return self.get_string(
            lambda len_: self.raw_api.LongName(id_, len_),
            error_msg=f'LongName failed on {id_}',
            ex=ex)

    def display_name(self, id_, ex=True):
        '''
        Returns the display name of an element. This is the string zEdit's
        user interface uses for display purposes.

        Args:
            id\\_ (``int``)
                id handle of element

        Returns:
            (``str``) display name of element
        '''
        return self.get_string(
            lambda len_: self.raw_api.DisplayName(id_, len_),
            error_msg=f'DisplayName failed on {id_}',
            ex=ex)

    def placement_name(self, id_, ex=True):
        '''
        TODO: figure out what this does
        '''
        rec = self.get_links_to(id_, 'NAME', ex=ex)
        return rec > 0 and f'Places {self.name(rec, ex=ex)}'

    def path(self, id_, ex=True):
        '''
        Returns the path of an element. All paths returned from this function
        can be used with ``xelib.get_element``.

        Args:
            id\\_ (``int``)
                id handle of element

        Returns:
            (``str``) path of an element
        '''
        return self.get_string(
            lambda len_: self.raw_api.Path(id_, True, False, False, len_),
            error_msg=f'Path failed on {id_}',
            ex=ex)

    def long_path(self, id_, ex=True):
        '''
        Returns the long path of an element. All paths returned from this
        function can be used with ``xelib.get_element``.

        Args:
            id\\_ (``int``)
                id handle of element

        Returns:
            (``str``) long path of an element
        '''
        return self.get_string(
            lambda len_: self.raw_api.Path(id_, False, False, False, len_),
            error_msg=f'Path failed on {id_}',
            ex=ex)

    def local_path(self, id_, ex=True):
        '''
        Returns the path of an element within its parent record. All paths
        returned from this function can be used with ``xelib.get_element``.

        Args:
            id\\_ (``int``)
                id handle of element

        Returns:
            (``str``) local path of an element
        '''
        return self.get_string(
            lambda len_: self.raw_api.Path(id_, False, True, False, len_),
            error_msg=f'Path failed on {id_}',
            ex=ex)

    def sort_path(self, id_, ex=True):
        '''
        TODO: figure out what this does
        '''
        return self.get_string(
            lambda len_: self.raw_api.Path(id_, False, True, True, len_),
            error_msg=f'Path failed on {id_}',
            ex=ex)

    def path_name(self, id_, sort=False, ex=True):
        '''
        TODO: figure out what this does
        '''
        return self.get_string(
            lambda len_: self.raw_api.PathName(id_, sort, len_),
            error_msg=f'PathName failed on {id_}',
            ex=ex)

    def signature(self, id_, ex=True):
        '''
        Returns the signature of the element

        Args:
            id\\_ (``int``)
                id handle of element

        Returns:
            (``str``) signature of element, such as ``GRUP``, ``ARMO``, ``REFR``
            etc...
        '''
        return self.get_string(
            lambda len_: self.raw_api.Signature(id_, len_),
            error_msg=f'Signature failed on {id_}',
            ex=ex)

    def sort_key(self, id_, ex=True):
        '''
        Returns the sort key of the element

        Args:
            id\\_ (``int``)
                id handle of element


        Returns:
            (``str``) sort key of element
        '''
        return self.get_string(
            lambda len_: self.raw_api.SortKey(id_, len_),
            error_msg=f'SortKey failed on {id_}',
            ex=ex)

    def get_value(self, id_, path='', ex=False):
        '''
        Returns the editor value of an element. This is the same value
        displayed in the record view of xEdit.

        Args:
            id\\_ (``int``)
                id handle of element to start from
            path (``str``)
                subpath under the element leading to element to operate on

        Returns:
            (``str``) value of element
        '''
        return self.get_string(
            lambda len_: self.raw_api.GetValue(id_, path, len_),
            error_msg=f'Failed to get element value at '
                      f'{self.element_context(id_, path)}',
            ex=ex)

    def get_ref_value(self, id_, path='', ex=False):
        '''
        TODO: figure out what this is
        '''
        return self.get_string(
            lambda len_: self.raw_api.GetRefValue(id_, path, len_),
            error_msg=f'Failed to get element ref value at '
                      f'{self.element_context(id_, path)}',
            ex=ex)

    def set_value(self, id_, value, path='', ex=True):
        '''
        Sets the editor value of an element. This is the same value displayed
        in the record view of xEdit.

        Args:
            id\\_ (``int``)
                id handle of element to start from
            path (``str``)
                subpath under the element leading to element to operate on
            value (``str``)
                string value to set on the element
        '''
        return self.verify_execution(
            self.raw_api.SetValue(id_, path, value),
            error_msg=f'Failed to set element value at '
                      f'{self.element_context(id_, path)}',
            ex=ex)

    def get_int_value(self, id_, path='', ex=False):
        '''
        Returns the integer editor value of an element. This is the same value
        displayed in the record view of xEdit.

        Args:
            id\\_ (``int``)
                id handle of element to start from
            path (``str``)
                subpath under the element leading to element to operate on

        Returns:
            (``int``) integer value of element
        '''
        return self.get_integer(
            lambda res: self.raw_api.GetIntValue(id_, path, res),
            error_msg=f'Failed to get int value at '
                      f'{self.element_context(id_, path)}',
            ex=ex)

    def set_int_value(self, id_, value, path='', ex=True):
        '''
        Sets the integer editor value of an element. This is the same value
        displayed in the record view of xEdit.

        Args:
            id\\_ (``int``)
                id handle of element to start from
            path (``str``)
                subpath under the element leading to element to operate on
            value (``int``)
                integer value to set on the element
        '''
        return self.verify_execution(
            self.raw_api.SetIntValue(id_, path, value),
            error_msg=f'Failed to set int value at '
                      f'{self.element_context(id_, path)}',
            ex=ex)

    def get_uint_value(self, id_, path='', ex=False):
        '''
        Returns the unsigned integer editor value of an element. This is the
        same value displayed in the record view of xEdit.

        Args:
            id\\_ (``int``)
                id handle of element to start from
            path (``str``)
                subpath under the element leading to element to operate on

        Returns:
            (``int``) integer value of element
        '''
        return self.get_unsigned_integer(
            lambda res: self.raw_api.GetUIntValue(id_, path, res),
            error_msg=f'Failed to get uint value at '
                      f'{self.element_context(id_, path)}',
            ex=ex)

    def set_uint_value(self, id_, value, path='', ex=True):
        '''
        Sets the unsigned integer editor value of an element. This is the same
        value displayed in the record view of xEdit.

        Args:
            id\\_ (``int``)
                id handle of element to start from
            path (``str``)
                subpath under the element leading to element to operate on
            value (``int``)
                non-negative integer value to set on the element
        '''
        return self.verify_execution(
            self.raw_api.SetUIntValue(id_, path, value),
            error_msg=f'Failed to set uint value at '
                      f'{self.element_context(id_, path)}',
            ex=ex)

    def get_float_value(self, id_, path='', ex=False):
        '''
        Returns the float editor value of an element. This is the same value
        displayed in the record view of xEdit.

        Args:
            id\\_ (``int``)
                id handle of element to start from
            path (``str``)
                subpath under the element leading to element to operate on

        Returns:
            (``float``) float value of element
        '''
        return self.get_double(
            lambda res: self.raw_api.GetFloatValue(id_, path, res),
            error_msg=f'Failed to get float value at '
                      f'{self.element_context(id_, path)}',
            ex=ex)

    def set_float_value(self, id_, value, path='', ex=True):
        '''
        Sets the float editor value of an element. This is the same value
        displayed in the record view of xEdit.

        Args:
            id\\_ (``int``)
                id handle of element to start from
            path (``str``)
                subpath under the element leading to element to operate on
            value (``float``)
                float value to set on the element
        '''
        return self.verify_execution(
            self.raw_api.SetFloatValue(id_, path, value),
            error_msg=f'Failed to set uint value at '
                      f'{self.element_context(id_, path)}',
            ex=ex)

    def set_flag(self, id_, name, state, path='', ex=True):
        '''
        Sets the flag ``name`` to state ``state`` at the element.

        Args:
            id\\_ (``int``)
                id handle of element to start from
            path (``str``)
                subpath under the element leading to element to operate on
            name (``str``)
                name of flag to set
            state (``bool``)
                boolean state to set flag to
        '''
        return self.verify_execution(
            self.raw_api.SetFlag(id_, path, name, state),
            error_msg=f'Failed to set flag value at '
                      f'{self.flag_context(id_, path, name)} to {state}',
            ex=ex)

    def get_flag(self, id_, name, path='', ex=True):
        '''
        Get the state of a flag at the element.

        Args:
            id\\_ (``int``)
                id handle of element to start from
            path (``str``)
                subpath under the element leading to element to operate on
            name (``str``)
                name of flag to get state for

        Returns:
            (``bool``) flag state
        '''
        return self.get_bool(
            lambda res: self.raw_api.GetFlag(id_, path, name, res),
            error_msg=f'Failed to get flag value at: '
                      f'{self.flag_context(id_, path, name)}',
            ex=ex)

    def get_enabled_flags(self, id_, path='', ex=True):
        '''
        Returns an array of enabled flags at an element.

        Args:
            id\\_ (``int``)
                id handle of element to start from
            path (``str``)
                subpath under the element leading to element to operate on

        Returns:
            (``List[str]``) a list of flag names that are set (state is ``True``)
        '''
        comma_separated_flags = self.get_string(
            lambda len_: self.raw_api.GetEnabledFlags(id_, path, len_),
            error_msg=f'Failed to get enabled flags at: '
                      f'{self.element_context(id_, path)}',
            ex=ex)
        return comma_separated_flags.split(',') if comma_separated_flags else []

    def set_enabled_flags(self, id_, flags, path='', ex=True):
        '''
        Ensures the list of enabled flags at an element is the given list.
        This will ensure provided flags are set, and flags not provided are
        unset.

        Args:
            id\\_ (``int``)
                id handle of element to start from
            path (``str``)
                subpath under the element leading to element to operate on
            flags (``List[str]``)
                list of flag names to ensure set (and non-listed unset)
        '''
        return self.verify_execution(
            self.raw_api.SetEnabledFlags(id_, path, ','.join(flags)),
            error_msg=f'Failed to set enabled flags at '
                      f'{self.element_context(id_, path)}',
            ex=ex)

    def get_all_flags(self, id_, path='', ex=True):
        '''
        Returns names of all flags the element supports.

        Args:
            id\\_ (``int``)
                id handle of element to start from
            path (``str``)
                subpath under the element leading to element to operate on

        Returns:
            (``List[str]``) list of supported flag names at the element
        '''
        comma_separated_flags = self.get_string(
            lambda len_: self.raw_api.GetAllFlags(id_, path, len_),
            error_msg=f'Failed to get all flags at: '
                      f'{self.element_context(id_, path)}',
            ex=ex)
        return comma_separated_flags.split(',') if comma_separated_flags else []

    def get_enum_options(self, id_, path='', ex=True):
        '''
        Returns an array of options supported by an enum element.

        Args:
            id\\_ (``int``)
                id handle of element to start from
            path (``str``)
                subpath under the element leading to element to operate on

        Returns:
            (``List[str]``) list of enum options for element
        '''
        return self.get_string(
            lambda len_: self.raw_api.GetEnumOptions(id_, path, len_),
            error_msg=f'Failed to get all enum options at '
                      f'{self.element_context(id_, path)}',
            ex=ex).split(',')

    def signature_from_name(self, name, ex=True):
        '''
        Translates a 'name' string (e.g. ``Armor``) to its signature
        (e.g. ``ARMO``)

        Args:
            name (``str``)
                name string

        Returns:
            (``str``) corresponding signature
        '''
        return self.get_string(
            lambda len_: self.raw_api.SignatureFromName(name, len_),
            error_msg=f'Failed to get signature from name: {name}',
            ex=ex)

    def name_from_signature(self, sig, ex=True):
        '''
        Translates a signature (`e.g. ``ARMO``) to its 'name' string
        (e.g. ``Armor``)

        Args:
            sig (``str``)
                signature

        Returns:
            (``str``) name string
        '''
        return self.get_string(
            lambda len_: self.raw_api.NameFromSignature(sig, len_),
            error_msg=f'Failed to get name from signature: {sig}',
            ex=ex)

    def get_signature_name_map(self, ex=True):
        '''
        Generates a lookup table that can be used to look up 'name' strings
        from signatures.

        Returns:
            (``Dict[str, str]``) A dictionary lookup table that maps signatures
            to their 'name' strings
        '''
        return self.get_dictionary(
            lambda len_: self.raw_api.GetSignatureNameMap(len_),
            error_msg=f'Failed to get signature name map',
            ex=ex)
