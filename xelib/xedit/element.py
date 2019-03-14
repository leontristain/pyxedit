from xelib.xedit.base import XEditBase


class XEditElement(XEditBase):
    @property
    def name(self):
        return self.xelib.name(self.handle)

    @property
    def long_name(self):
        return self.xelib.long_name(self.handle)

    @property
    def display_name(self):
        return self.xelib.display_name(self.handle)

    @property
    def path(self):
        return self.xelib.path(self.handle)

    @property
    def long_path(self):
        return self.xelib.long_path(self.handle)

    @property
    def local_path(self):
        return self.xelib.local_path(self.handle)

    @property
    def signature(self):
        return self.xelib.signature(self.handle)

    @property
    def signature_name(self):
        return self.xelib.name_from_signature(self.signature)