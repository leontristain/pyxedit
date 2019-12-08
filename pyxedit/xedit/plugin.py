from pyxedit.xedit.base import XEditBase


class XEditPlugin(XEditBase):
    def __repr__(self):
        return (f'<{self.__class__.__name__} {self.name} {self.handle}>')

    @property
    def author(self):
        return self.xelib_run('get_file_author')

    @author.setter
    def author(self, value):
        return self.xelib_run('set_file_author', value)

    @property
    def description(self):
        return self.xelib_run('get_description')

    @description.setter
    def description(self, value):
        return self.xelib_run('set_description', value)

    @property
    def is_esm(self):
        return self.xelib_run('get_is_esm')

    @is_esm.setter
    def is_esm(self, value):
        return self.xelib_run('set_is_esm', value)

    @property
    def next_object(self):
        return self.objectify(self.xelib_run('get_next_object_id'))

    @next_object.setter
    def next_object(self, value):
        return self.xelib_run('set_next_object_id', value.handle)

    @property
    def num_records(self):
        return self.xelib_run('get_record_count')

    @property
    def num_override_records(self):
        return self.xelib_run('get_override_record_count')

    @property
    def md5(self):
        return self.xelib_run('md5_hash')

    @property
    def crc(self):
        return self.xelib_run('crc_hash')

    @property
    def load_order(self):
        return self.xelib_run('get_file_load_order')

    @property
    def header(self):
        return self.objectify(self.xelib_run('get_file_header'))

    @property
    def masters(self):
        for handle in self.xelib_run('get_masters'):
            yield self.objectify(handle)

    @property
    def master_names(self):
        return self.xelib_run('get_master_names')

    def add_master(self, master_plugin):
        return self.add_master_by_name(self, master_plugin.name)

    def add_master_by_name(self, master_plugin_name):
        return self.xelib_run('add_master', master_plugin_name)

    def add_all_masters(self):
        return self.xelib_run('add_all_masters')

    def add_masters_needed_for_copying(self, obj, as_new=False):
        return self.xelib.add_required_masters(obj.handle,
                                               self.handle,
                                               as_new=as_new)

    def sort_masters(self):
        return self.xelib_run('sort_masters')

    def clean_masters(self):
        return self.xelib_run('clean_masters')

    def rename(self, new_file_name):
        return self.xelib_run('rename_file', new_file_name)

    def nuke(self):
        return self.xelib_run('nuke_file')

    def save(self):
        return self.xelib_run('save_file')

    def save_as(self, file_path):
        return self.xelib_run('save_file', file_path=str(file_path))
