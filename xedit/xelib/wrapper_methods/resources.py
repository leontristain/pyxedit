from enum import Enum, unique

from xedit.xelib.wrapper_methods.base import WrapperMethodsBase


@unique
class ArchiveTypes(Enum):
    baNone = 0
    baTES3 = 1
    baFO3 = 2
    baSSE = 3
    baFO4 = 4
    baFO4dds = 5


class ResourcesMethods(WrapperMethodsBase):
    ArchiveTypes = ArchiveTypes

    def extract_container(self, name, dst, replace):
        return self.raw_api.ExtractContainer(name, dst, replace)

    def extract_file(self, name, src, dst):
        return self.raw_api.ExtractFile(name, src, dst)

    def get_container_files(self, name, folder):
        return self.get_string_array(
            lambda len_: self.raw_api.GetContainerFiles(name, folder, len_),
            error_msg=f'Failed to get files in container {name}')

    def get_file_container(self, file_path):
        return self.get_string(
            lambda len_: self.raw_api.GetFileContainer(file_path, len_),
            error_msg=f'Failed to get file container for {file_path}')

    def get_loaded_containers(self):
        return self.get_string_array(
            lambda len_: self.raw_api.GetLoadedContainers(len_),
            error_msg=f'Failed to get loaded containers')

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
                      ff=''):
        return self.verify_execution(
            self.raw_api.BuildArchive(name,
                                      folder,
                                      file_paths,
                                      archive_type.value,
                                      compress,
                                      share,
                                      af,
                                      ff),
            error_msg=f'Failed to build archive {name}')

    def get_texture_data(self, resource_name):
        return self.get_image_data(
            lambda width, height:
                self.raw_api.GetTextureData(resource_name, width, height),
            error_msg=f'Failed to get texture data for {resource_name}')
