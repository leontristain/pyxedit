from xelib.xedit.base import XEditBase


class XEditPlugin(XEditBase):
    @property
    def name(self):
        return self.xelib.name(self.handle)

    @property
    def author(self):
        return self.xelib.get_file_author(self.handle)

    @author.setter
    def author(self, value):
        self.xelib.set_file_author(self.handle, value)

    @property
    def description(self):
        return self.xelib.get_description(self.handle)

    @description.setter
    def description(self, value):
        self.xelib.set_description(self.handle, value)

    @property
    def is_esm(self):
        return self.xelib.get_is_esm(self.handle)

    @is_esm.setter
    def is_esm(self, value):
        self.xelib.set_is_esm(self.handle, value)

    @property
    def next_object_id(self):
        return self.xelib.get_next_object_id(self.handle)

    @next_object_id.setter
    def next_object_id(self, value):
        self.xelib.set_next_object_id(self.handle, value)

    def save(self):
        return self.xelib.save_file(self.handle)

    def save_as(self, file_path):
        return self.xelib.save_file(self.handle, file_path=file_path)