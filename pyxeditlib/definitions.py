from ctypes import c_bool, c_double, c_int, c_ubyte, c_uint, c_wchar_p, POINTER
from enum import Enum, unique

def params(**params_types):
    '''
    A function that returns the dictionary of parameters given, makes following
    code look a bit better on the eyes.
    '''
    return params_types

def ret(return_type=None):
    '''
    A function that returns the thing given and defaults to None, makes the
    following code look a bit better on the eyes.
    '''
    return return_type

@unique
class DelphiTypes(Enum):
    '''
    A lookup table that returns the python ctypes type give a delphi type
    '''
    Byte = c_ubyte
    Cardinal = c_uint
    Double = c_double
    Integer = c_int
    WordBool = c_bool
    PByte = POINTER(c_ubyte)
    PCardinal = POINTER(c_uint)
    PDouble = POINTER(c_double)
    PInteger = POINTER(c_int)
    PWordBool = POINTER(c_bool)
    PWideChar = c_wchar_p

class XEditLibSignatures(Enum):
    '''
    A lookup table that returns the parameter names and types, and the return
    types, of each xedit-lib method
    '''
    # meta methods
    InitXEdit = params(), ret()
    CloseXEdit = params(), ret()
    GetResultString = params(str='PWideChar', maxLen='Integer'), ret('WordBool')
    GetResultArray = params(_res='PCardinal', maxLen='Integer'), ret('WordBool')
    GetResultBytes = params(_res='PByte', maxLen='Integer'), ret('WordBool')
    GetGlobal = params(key='PWideChar', len='PInteger'), ret('WordBool')
    GetGlobals = params(len='PInteger'), ret('WordBool')
    SetSortMode = params(_sortBy='Byte', _reverse='WordBool'), ret('WordBool')
    Release = params(_id='Cardinal'), ret('WordBool')
    ReleaseNodes = params(_id='Cardinal'), ret('WordBool')
    Switch = params(_id='Cardinal', _id2='Cardinal'), ret('WordBool')
    GetDuplicateHandles = params(_id='Cardinal', len='PInteger'), ret('WordBool')
    CleanStore = params(), ret('WordBool')
    ResetStore = params(), ret('WordBool')

    # message methods
    GetMessagesLength = params(), ret()
    GetMessages = params(str='PWideChar', maxLen='Integer'), ret('WordBool')
    ClearMessages = params(), ret()
    GetExceptionMessageLength = params(), ret()
    GetExceptionMessage = params(str='PWideChar', len='Integer'), ret('WordBool')
    GetExceptionStackLength = params(), ret()
    GetExceptionStack = params(str='PWideChar', len='Integer'), ret('WordBool')

    # loading up and set up methods
    GetGamePath = params(mode='Integer', len='PInteger'), ret('WordBool')
    SetGamePath = params(path='PWideChar'), ret('WordBool')
    GetGameLanguage = params(mode='Integer', len='PInteger'), ret('WordBool')
    SetLanguage = params(lang='PWideChar'), ret('WordBool')
    SetBackupPath = params(path='PWideChar'), ret('WordBool')
    SetGameMode = params(mode='Integer'), ret('WordBool')
    GetLoadOrder = params(len='PInteger'), ret('WordBool')
    GetActivePlugins = params(len='PInteger'), ret('WordBool')
    LoadPlugins = params(loadOrder='PWideChar', smartLoad='WordBool'), ret('WordBool')
    LoadPlugin = params(filename='PWideChar'), ret('WordBool')
    LoadPluginHeader = params(fileName='PWideChar', _res='PCardinal'), ret('WordBool')
    BuildReferences = params(_id='Cardinal', synchronous='WordBool'), ret('WordBool')
    GetLoaderStatus = params(status='PByte'), ret('WordBool')
    UnloadPlugin = params(_id='Cardinal'), ret('WordBool')

    # resource handling methods
    ExtractContainer = params(name='PWideChar', destination='PWideChar', replace='WordBool'), ret('WordBool')
    ExtractFile = params(name='PWideChar', source='PWideChar', destination='PWideChar'), ret('WordBool')
    GetContainerFiles = params(name='PWideChar', path='PWideChar', len='PInteger'), ret('WordBool')
    GetFileContainer = params(path='PWideChar', len='PInteger'), ret('WordBool')
    GetLoadedContainers = params(len='PInteger'), ret('WordBool')
    LoadContainer = params(filePath='PWideChar'), ret('WordBool')
    BuildArchive = params(name='PWideChar',
                          folder='PWideChar',
                          filePaths='PWideChar',
                          archiveType='Integer',
                          bCompress='WordBool',
                          bShare='WordBool',
                          af='PWideChar',
                          ff='PWideChar'), ret('WordBool')
    GetTextureData = params(resourceName='PWideChar', width='PInteger', height='PInteger'), ret('WordBool')

    # file handling methods
    AddFile = params(filename='PWideChar', _res='PCardinal'), ret('WordBool')
    FileByIndex = params(index='Integer', _res='PCardinal'), ret('WordBool')
    FileByLoadOrder = params(loadOrder='Integer', _res='PCardinal'), ret('WordBool')
    FileByName = params(name='PWideChar', _res='PCardinal'), ret('WordBool')
    FileByAuthor = params(author='PWideChar', _res='PCardinal'), ret('WordBool')
    NukeFile = params(_id='Cardinal'), ret('WordBool')
    RenameFile = params(_id='Cardinal', filename='PWideChar'), ret('WordBool')
    SaveFile = params(_id='Cardinal', filePath='PWideChar'), ret('WordBool')
    MD5Hash = params(_id='Cardinal', len='PInteger'), ret('WordBool')
    CRCHash = params(_id='Cardinal', len='PInteger'), ret('WordBool')
    GetRecordCount = params(_id='Cardinal', count='PInteger'), ret('WordBool')
    GetOverrideRecordCount = params(_id='Cardinal', count='PInteger'), ret('WordBool')
    SortEditorIDs = params(_id='Cardinal', sig='PWideChar'), ret('WordBool')
    SortNames = params(_id='Cardinal', sig='PWideChar'), ret('WordBool')
    GetFileLoadOrder = params(_id='Cardinal', loadOrder='PInteger'), ret('WordBool')

    # master handling methods
    CleanMasters = params(_id='Cardinal'), ret('WordBool')
    SortMasters = params(_id='Cardinal'), ret('WordBool')
    AddMaster = params(_id='Cardinal', masterName='PWideChar'), ret('WordBool')
    AddMasters = params(_id='Cardinal', masters='PWideChar'), ret('WordBool')
    AddRequiredMasters = params(_id='Cardinal', _id2='Cardinal', asNew='WordBool'), ret('WordBool')
    GetMasters = params(_id='Cardinal', len='PInteger'), ret('WordBool')
    GetRequiredBy = params(_id='Cardinal', len='PInteger'), ret('WordBool')
    GetMasterNames = params(_id='Cardinal', len='PInteger'), ret('WordBool')

    # element handling methods
    HasElement = params(_id='Cardinal', path='PWideChar', bool='PWordBool'), ret('WordBool')
    GetElement = params(_id='Cardinal', path='PWideChar', _res='PCardinal'), ret('WordBool')
    AddElement = params(_id='Cardinal', path='PWideChar', _res='PCardinal'), ret('WordBool')
    AddElementValue = params(_id='Cardinal', path='PWideChar', value='PWideChar', _res='PCardinal'), ret('WordBool')
    RemoveElement = params(_id='Cardinal', path='PWideChar'), ret('WordBool')
    RemoveElementOrParent = params(_id='Cardinal'), ret('WordBool')
    SetElement = params(_id='Cardinal', _id2='Cardinal'), ret('WordBool')
    GetElements = params(_id='Cardinal', path='PWideChar', sort='WordBool', filter='WordBool', len='PInteger'), ret('WordBool')
    GetDefNames = params(_id='Cardinal', len='PInteger'), ret('WordBool')
    GetAddList = params(_id='Cardinal', len='PInteger'), ret('WordBool')
    GetLinksTo = params(_id='Cardinal', path='PWideChar', _res='PCardinal'), ret('WordBool')
    SetLinksTo = params(_id='Cardinal', path='PWideChar', _id2='Cardinal'), ret('WordBool')
    GetElementIndex = params(_id='Cardinal', index='PInteger'), ret('WordBool')
    GetContainer = params(_id='Cardinal', _res='PCardinal'), ret('WordBool')
    GetElementFile = params(_id='Cardinal', _res='PCardinal'), ret('WordBool')
    GetElementGroup = params(_id='Cardinal', _res='PCardinal'), ret('WordBool')
    GetElementRecord = params(_id='Cardinal', _res='PCardinal'), ret('WordBool')
    ElementCount = params(_id='Cardinal', count='PInteger'), ret('WordBool')
    ElementEquals = params(_id='Cardinal', _id2='Cardinal', bool='PWordBool'), ret('WordBool')
    ElementMatches = params(_id='Cardinal', path='PWideChar', value='PWideChar', bool='PWordBool'), ret('WordBool')
    HasArrayItem = params(_id='Cardinal', path='PWideChar', subpath='PWideChar', value='PWideChar', bool='PWordBool'), ret('WordBool')
    GetArrayItem = params(_id='Cardinal', path='PWideChar', subpath='PWideChar', value='PWideChar', _res='PCardinal'), ret('WordBool')
    AddArrayItem = params(_id='Cardinal', path='PWideChar', subpath='PWideChar', value='PWideChar', _res='PCardinal'), ret('WordBool')
    RemoveArrayItem = params(_id='Cardinal', path='PWideChar', subpath='PWideChar', value='PWideChar'), ret('WordBool')
    MoveArrayItem = params(_id='Cardinal', index='Integer'), ret('WordBool')
    CopyElement = params(_id='Cardinal', _id2='Cardinal', aAsNew='WordBool', _res='PCardinal'), ret('WordBool')
    FindNextElement = params(_id='Cardinal', search='PWideChar', byPath='WordBool', byValue='WordBool', _res='PCardinal'), ret('WordBool')
    FindPreviousElement = params(_id='Cardinal', search='PWideChar', byPath='WordBool', byValue='WordBool', _res='PCardinal'), ret('WordBool')
    GetSignatureAllowed = params(_id='Cardinal', sig='PWideChar', bool='PWordBool'), ret('WordBool')
    GetAllowedSignatures = params(_id='Cardinal', len='PInteger'), ret('WordBool')
    GetIsModified = params(_id='Cardinal', bool='PWordBool'), ret('WordBool')
    GetIsEditable = params(_id='Cardinal', bool='PWordBool'), ret('WordBool')
    SetIsEditable = params(_id='Cardinal', bool='WordBool'), ret('WordBool')
    GetIsRemoveable = params(_id='Cardinal', bool='PWordBool'), ret('WordBool')
    GetCanAdd = params(_id='Cardinal', bool='PWordBool'), ret('WordBool')
    SortKey = params(_id='Cardinal', len='PInteger'), ret('WordBool')
    ElementType = params(_id='Cardinal', enum='PByte'), ret('WordBool')
    DefType = params(_id='Cardinal', enum='PByte'), ret('WordBool')
    SmashType = params(_id='Cardinal', enum='PByte'), ret('WordBool')
    ValueType = params(_id='Cardinal', enum='PByte'), ret('WordBool')
    IsSorted = params(_id='Cardinal', bool='PWordBool'), ret('WordBool')
    IsFixed = params(_id='Cardinal', bool='PWordBool'), ret('WordBool')

    # plugin error methods
    CheckForErrors = params(_id='Cardinal'), ret('WordBool')
    GetErrorThreadDone = params(), ret('WordBool')
    GetErrors = params(len='PInteger'), ret('WordBool')
    RemoveIdenticalRecords = params(_id='Cardinal', removeITMs='WordBool', removeITPOs='WordBool'), ret('WordBool')

    # serialization methods
    ElementToJson = params(_id='Cardinal', len='PInteger'), ret('WordBool')
    ElementFromJson = params(_id='Cardinal', path='PWideChar', json='PWideChar'), ret('WordBool')

    # element value methods
    Name = params(_id='Cardinal', len='PInteger'), ret('WordBool')
    LongName = params(_id='Cardinal', len='PInteger'), ret('WordBool')
    DisplayName = params(_id='Cardinal', len='PInteger'), ret('WordBool')
    Path = params(_id='Cardinal', short='WordBool', local='WordBool', len='PInteger'), ret('WordBool')
    Signature = params(_id='Cardinal', len='PInteger'), ret('WordBool')
    GetValue = params(_id='Cardinal', path='PWideChar', len='PInteger'), ret('WordBool')
    SetValue = params(_id='Cardinal', path='PWideChar', value='PWideChar'), ret('WordBool')
    GetIntValue = params(_id='Cardinal', path='PWideChar', value='PInteger'), ret('WordBool')
    SetIntValue = params(_id='Cardinal', path='PWideChar', value='Integer'), ret('WordBool')
    GetUIntValue = params(_id='Cardinal', path='PWideChar', value='PCardinal'), ret('WordBool')
    SetUIntValue = params(_id='Cardinal', path='PWideChar', value='Cardinal'), ret('WordBool')
    GetFloatValue = params(_id='Cardinal', path='PWideChar', value='PDouble'), ret('WordBool')
    SetFloatValue = params(_id='Cardinal', path='PWideChar', value='Double'), ret('WordBool')
    GetFlag = params(_id='Cardinal', path='PWideChar', name='PWideChar', enabled='PWordBool'), ret('WordBool')
    SetFlag = params(_id='Cardinal', path='PWideChar', name='PWideChar', enabled='WordBool'), ret('WordBool')
    GetAllFlags = params(_id='Cardinal', path='PWideChar', len='PInteger'), ret('WordBool')
    GetEnabledFlags = params(_id='Cardinal', path='PWideChar', len='PInteger'), ret('WordBool')
    SetEnabledFlags = params(_id='Cardinal', path='PWideChar', flags='PWideChar'), ret('WordBool')
    GetEnumOptions = params(_id='Cardinal', path='PWideChar', len='PInteger'), ret('WordBool')
    SignatureFromName = params(name='PWideChar', len='PInteger'), ret('WordBool')
    NameFromSignature = params(sig='PWideChar', len='PInteger'), ret('WordBool')
    GetSignatureNameMap = params(len='PInteger'), ret('WordBool')

    # record handling methods
    GetFormID = params(_id='Cardinal', formID='PCardinal', native='WordBool'), ret('WordBool')
    SetFormID = params(_id='Cardinal', formID='Cardinal', native='WordBool', fixReferences='WordBool'), ret('WordBool')
    GetRecord = params(_id='Cardinal', formID='Cardinal', searchMasters='WordBool', _res='PCardinal'), ret('WordBool')
    GetRecords = params(_id='Cardinal', search='PWideChar', includeOverrides='WordBool', len='PInteger'), ret('WordBool')
    GetREFRs = params(_id='Cardinal', search='PWideChar', flags='Cardinal', len='PInteger'), ret('WordBool')
    GetOverrides = params(_id='Cardinal', count='PInteger'), ret('WordBool')
    GetMasterRecord = params(_id='Cardinal', _res='PCardinal'), ret('WordBool')
    GetPreviousOverride = params(_id='Cardinal', _id2='Cardinal', _res='PCardinal'), ret('WordBool')
    GetWinningOverride = params(_id='Cardinal', _res='PCardinal'), ret('WordBool')
    GetInjectionTarget = params(_id='Cardinal', _res='PCardinal'), ret('WordBool')
    FindNextRecord = params(_id='Cardinal', search='PWideChar', byEdid='WordBool', byName='WordBool', _res='PCardinal'), ret('WordBool')
    FindPreviousRecord = params(_id='Cardinal', search='PWideChar', byEdid='WordBool', byName='WordBool', _res='PCardinal'), ret('WordBool')
    FindValidReferences = params(_id='Cardinal', signature='PWideChar', search='PWideChar', limitTo='Integer', len='PInteger'), ret('WordBool')
    GetReferencedBy = params(_id='Cardinal', len='PInteger'), ret('WordBool')
    ExchangeReferences = params(_id='Cardinal', oldFormID='Cardinal', newFormID='Cardinal'), ret('WordBool')
    IsMaster = params(_id='Cardinal', bool='PWordBool'), ret('WordBool')
    IsInjected = params(_id='Cardinal', bool='PWordBool'), ret('WordBool')
    IsOverride = params(_id='Cardinal', bool='PWordBool'), ret('WordBool')
    IsWinningOverride = params(_id='Cardinal', bool='PWordBool'), ret('WordBool')
    GetNodes = params(_id='Cardinal', _res='PCardinal'), ret('WordBool')
    GetConflictData = params(_id='Cardinal', _id2='Cardinal', conflictAll='PByte', conflictThis='PByte'), ret('WordBool')
    GetNodeElements = params(_id='Cardinal', _id2='Cardinal', len='PInteger'), ret('WordBool')

    # filtering methods
    FilterRecord = params(_id='Cardinal'), ret('WordBool')
    ResetFilter = params(), ret('WordBool')


def generate_python_from_pascal(pascal_paste):
    '''
    A helper function that can be passed a paste of the lines from the pascal
    '{$region 'API functions'}' sections in xedit-lib source code, and it will
    parse the definitions and print you python definitions in the format above.

    @param pascal_paste: a dirty paste of pascal code as described
    '''
    lines = pascal_paste.strip().splitlines()
    lines = [line.strip() for line in lines
             if line.strip() and
             not line.startswith('{') and
             not line.endswith('}')]

    for line in lines:
        is_procedure = False

        # parse the first word
        if line.startswith('function '):
            line = line[len('function '):]
        elif line.startswith('procedure '):
            line = line[len('procedure '):]
            is_procedure = True
        else:
            raise ValueError(f'cannot read line `{line}`')
        line = line.strip()

        # parse the name
        name = ''
        for char in line:
            if char.isalpha() or char.isdigit():
                name += char
            else:
                break
        line = line[len(name):]
        if not name:
            raise ValueError(f'cannot read a name from line `{line}`')
        line = line.strip()

        # if it's a procedure, there's no parameters or return
        # values to worry about, so just print and continue
        if is_procedure:
            print(f'''{name} = params(), ret()''')
            continue

        # otherwise, parse everything between the parentheses as the params
        # string if it exists
        params_str = ''
        if line.startswith('('):
            try:
                params_end = line.index(')')
            except ValueError:
                raise ValueError(f'could not find a `)` in rest of line '
                                 f'`{line}`')
            params_str = line[:params_end].strip('()').strip()
            line = line[params_end:].strip('()').strip()

        # parse parameters from params string
        parameters = {}
        if params_str:
            for param_def in [part.strip() for part in params_str.split(';')]:
                try:
                    before, after = param_def.split(':')
                    param_names = [name.strip()
                                for name in before.strip().split(',')]
                    param_type = after.strip()
                    for param_name in param_names:
                        parameters[param_name] = param_type
                except Exception as e:
                    raise ValueError(f'failed to parse parameters from '
                                     f'`{line}`: {str(e)}')

        # the next part should start with a colon, get rid of it and strip
        if not line.startswith(':'):
            raise ValueError(f'expected line `{line}` to start with a colon`')
        line = line[1:].strip()

        # there should now be a return type until the next semicolon
        return_type = ''
        for char in line:
            if char.isalpha() or char.isdigit():
                return_type += char
            else:
                break
        
        # with the parameters and the return type, we can now print out the
        # python declaration for it
        params_parts = [f"{param_name}='{param_type}'"
                        for param_name, param_type in parameters.items()]
        params_string = ', '.join(params_parts)
        print(f'''{name} = params({params_string}), ret('{return_type}')''')
