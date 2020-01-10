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
        '''
        Extracts a ``.bsa`` container to the destination folder ``dst``.

        Args:
            name (``str``):
                the path to the ``.bsa`` container file
            dst (``str``):
                the path to the destination folder to extract files to
            replace (``bool``):
                if set to ``True``, will attempt to replace existing files

        Returns:
            (``bool``) whether container is extracted successfully
        '''
        return self.raw_api.ExtractContainer(name, dst, replace)

    def extract_file(self, name, src, dst):
        '''
        Extracts the file ``src`` from a ``.bsa`` container to the
        destination folder ``dst``.

        Args:
            name (``str``):
                the path to the ``.bsa`` container file
            src (``str``):
                a file path within ``.bsa`` to extract
            dst (``str``):
                the path to the destination folder to extract file to

        Returns:
            (``bool``) whether file extraction is successful
        '''
        return self.raw_api.ExtractFile(name, src, dst)

    def get_container_files(self, name, folder, ex=True):
        '''
        Returns an array of the file paths, limited to a sub-``folder``, within
        a given ``.bsa`` container.

        Args:
            name (``str``):
                the path to the ``.bsa`` container file
            folder (``str``):
                a subfolder within the container to limit the query to

        Returns:
            (``List[str]``) a list of file paths within the ``folder`` inside
            the ``.bsa`` container file
        '''
        return self.get_string_array(
            lambda len_: self.raw_api.GetContainerFiles(name, folder, len_),
            error_msg=f'Failed to get files in container {name}',
            ex=ex)

    def get_file_container(self, file_path, ex=True):
        '''
        Returns the name of the ``.bsa`` container where the winning version
        of the ``file_path`` is stored.

        Args:
            file_path (``str``):
                the file path to find the winning container for

        Returns:
            (``str``) name of the winning ``.bsa`` container
        '''
        return self.get_string(
            lambda len_: self.raw_api.GetFileContainer(file_path, len_),
            error_msg=f'Failed to get file container for {file_path}',
            ex=ex)

    def get_loaded_containers(self, ex=True):
        '''
        Returns an array of the currently loaded ``.bsa`` container names

        Returns:
            (``List[str]``) a list of currently loaded ``.bsa`` containers
        '''
        return self.get_string_array(
            lambda len_: self.raw_api.GetLoadedContainers(len_),
            error_msg=f'Failed to get loaded containers',
            ex=ex)

    def load_container(self, file_path):
        '''
        Loads the ``.bsa`` container at ``file_path``.

        Args:
            file_path (``str``): the path to the ``.bsa`` container to load

        Returns:
            (``bool``) whether container loaded successfully
        '''
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
        '''
        Creates a new archive ``name`` in ``folder`` containing files at the
        ``file_paths`` relative to ``folder``. Uses archive type
        ``archive_type``. Compresses the archive if ``compress`` is ``True`` and
        packs data if ``share`` is ``True``. Pass a hexadecimal integer as a
        string to ``af`` or ``ff`` to set custom archive flags or file flags,
        respectively. See ``Xelib.ArchiveTypes`` enum for a list of allowed
        archive types.

        Args:
            name (``str``):
                name of archive
            folder (``str``):
                folder to create archive in
            file_paths (``List[str]``):
                a list of files to add to archive
            archive_type (``Xelib.ArchiveTypes``):
                enum representing the type of archive to use
            compress (``bool``):
                whether to compress the archive
            share (``bool``):
                whether to pack the data
            af (``str``):
                a hex integer in string form, used to set custom archive flags
            ff (``str``):
                a hex integer in string form, used to set custom file flags
        '''
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
        '''
        Return the pixel image data for the texture resource ``resource_name``

        .. note::
            This is currently not implemented in ``pyxedit``. Invoking this
            function will raise ``NotImplementedError``.
        '''
        return self.get_image_data(
            lambda width, height:
                self.raw_api.GetTextureData(resource_name, width, height),
            error_msg=f'Failed to get texture data for {resource_name}',
            ex=ex)
