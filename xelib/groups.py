from xelib.elements import has_element, get_element, add_element


def has_group(id_, signature):
    return has_element(id_, signature)


def add_group(id_, signature):
    return add_element(id_, signature)


def get_child_group(id_):
    return get_element(id_, 'Child Group')
