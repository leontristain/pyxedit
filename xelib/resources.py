from enum import Enum, unique

from xelib.lib import raw_api
from xelib.helpers import (get_string,
                           get_string_array,
                           get_image_data,
                           validate)


@unique
class ArchiveTypes(Enum):
    baNone = 0
    baTES3 = 1
    baFO3 = 2
    baSSE = 3
    baFO4 = 4
    baFO4dds = 5


def extract_container(name, dst, replace):
    return raw_api.ExtractContainer(name, dst, replace)


def extract_file(name, src, dst):
    return raw_api.ExtractFile(name, src, dst)


def get_container_files(name, folder):
    return get_string_array(
        lambda len_: raw_api.GetContainerFiles(name, folder, len_),
        error_msg=f'Failed to get files in container {name}')


def get_file_container(file_path):
    return get_string(
        lambda len_: raw_api.GetFileContainer(file_path, len_),
        error_msg=f'Failed to get file container for {file_path}')


def get_loaded_containers():
    return get_string_array(
        lambda len_: raw_api.GetLoadedContainers(len_),
        error_msg=f'Failed to get loaded containers')


def load_container(file_path):
    return raw_api.LoadContainer(file_path)


def build_archive(name,
                  folder,
                  file_paths,
                  archive_type,
                  compress=False,
                  share=False,
                  af='',
                  ff=''):
    validate(raw_api.BuildArchive(name,
                                  folder,
                                  file_paths,
                                  archive_type.value,
                                  compress,
                                  share,
                                  af,
                                  ff),
             f'Failed to build archive {name}')


def get_texture_data(resource_name):
    return get_image_data(
        lambda width, height:
            raw_api.GetTextureData(resource_name, width, height),
        error_msg=f'Failed to get texture data for {resource_name}')
