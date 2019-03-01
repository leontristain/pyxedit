import ctypes

from pyxeditlib.definitions import DelphiTypes, XEditLibSignatures


def load_lib(dll_path):
    lib = ctypes.CDLL(str(dll_path))
    types_mapping = {mapping.name: mapping.value for mapping in DelphiTypes}
    for signature in XEditLibSignatures:
        method_name = signature.name
        params, return_type = signature.value
        try:
            method = getattr(lib, method_name)
            method.argtypes = [types_mapping[delphi_type]
                               for _, delphi_type in params.items()]
            if return_type:
                method.restype = types_mapping[return_type]
        except AttributeError:
            print(f'WARNING: missing function {method_name}')
    return lib
