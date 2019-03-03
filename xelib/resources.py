from enum import Enum, unique


@unique
class ArchiveTypes(Enum):
    None_ = 'baNone'
    TES3 = 'baTES3'
    FO3 = 'baFO3'
    SSE = 'baSSE'
    FO4 = 'baFO4'
    FO4dds = 'baFO4dds'


def extract_container(name, dst, replace):
    raise NotImplementedError


def extract_file(name, src, dst):
    raise NotImplementedError


def get_container_files(name, folder):
    raise NotImplementedError


def get_file_container(file_path):
    raise NotImplementedError


def get_loaded_containers():
    raise NotImplementedError


def load_container():
    raise NotImplementedError


def build_archive(name,
                  folder,
                  file_paths,
                  archive_type,
                  compress=False,
                  share=False,
                  af='',
                  ff=''):
    raise NotImplementedError


def get_texture_data(resource_name):
    raise NotImplementedError
