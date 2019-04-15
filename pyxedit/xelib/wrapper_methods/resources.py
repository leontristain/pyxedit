from enum import Enum, unique

from pyxedit.xelib.wrapper_methods.base import WrapperMethodsBase


@unique
class ArchiveTypes(Enum):
    None_ = 0
    TES3 = 1
    FO3 = 2
    SSE = 3
    FO4 = 4
    FO4dds = 5


class ResourcesMethods(WrapperMethodsBase):
    ArchiveTypes = ArchiveTypes

    def extract_container(self, name, dst, replace):
        return self.raw_api.ExtractContainer(name, dst, replace)

    def extract_file(self, name, src, dst):
        return self.raw_api.ExtractFile(name, src, dst)

    def get_container_files(self, name, folder, ex=True):
        return self.get_string_array(
            lambda len_: self.raw_api.GetContainerFiles(name, folder, len_),
            error_msg=f'Failed to get files in container {name}',
            ex=ex)

    def get_file_container(self, file_path, ex=True):
        return self.get_string(
            lambda len_: self.raw_api.GetFileContainer(file_path, len_),
            error_msg=f'Failed to get file container for {file_path}',
            ex=ex)

    def get_loaded_containers(self, ex=True):
        return self.get_string_array(
            lambda len_: self.raw_api.GetLoadedContainers(len_),
            error_msg=f'Failed to get loaded containers',
            ex=ex)

    def load_container(self, file_path):
        return self.raw_api.LoadContainer(file_path)

    def build_archive(self,
                      name,
                      folder,
                      file_paths,
                      archive_type,
                      compress=False,
                      share=False,
                      af='',
                      ff='',
                      ex=True):
        return self.verify_execution(
            self.raw_api.BuildArchive(name,
                                      folder,
                                      file_paths,
                                      archive_type.value,
                                      compress,
                                      share,
                                      af,
                                      ff),
            error_msg=f'Failed to build archive {name}',
            ex=ex)

    def get_texture_data(self, resource_name, ex=True):
        return self.get_image_data(
            lambda width, height:
                self.raw_api.GetTextureData(resource_name, width, height),
            error_msg=f'Failed to get texture data for {resource_name}',
            ex=ex)
