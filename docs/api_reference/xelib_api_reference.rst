===================
Xelib API Reference
===================

.. toctree::
   :maxdepth: 1

Overview
========

The ``Xelib`` API is a minimal wrapper around ``XEditLib.dll``, accessible via a ``Xelib`` top-level class. Methods on the API are almost one-to-one with ``XEditLib.dll``'s public methods. Users familiar with zEdit's `xelib API <https://z-edit.github.io/#/docs?t=Development%2FAPIs%2Fxelib>`_ can also consider this the "python version" of an almost-equivalent.

To use the ``Xelib`` API, you must first create a ``Xelib`` object and configure it with various initial values, such as the list of Skyrim mod plugins you'd like to load. Then, to do any work, you need to enter a ``session``. Within the session, the plugins will be loaded and you will be free to inspect records, copy values, create and save plugins, etc... See the following example for the basic boilerplate of how people typically would use the library:

.. highlight:: python
.. code-block:: python

    from pyxedit import Xelib

    with Xelib(plugins=['GOT.esp', 'LOTR.esp']).session() as xelib:
        h = xelib.get_element(0, 'GOT.esp\\NPC_\\JonSnow')
        print(xelib.display_name(h))  # prints 'Jon Snow'

.. note::
    **Differences between** ``XEditLib.dll`` **and the** ``Xelib`` **wrapper:**

    The API offered by ``Xelib``, like the `javascript xelib <https://github.com/z-edit/xelib>`_, are near 1-to-1 with the actual functions available on ``XEditLib.dll``. The main difference between calling ``XEditLib.dll`` functions directly and the higher level "xelib" wrappers is that ``XEditLib.dll`` usage is rather complex. With most functions on ``XEditLib.dll``, you are expected to call it, and it always returns a boolean for whether the call was successful. If the call was successful, you would then run some other function, such as ``GetResultString``, ``GetResultArray``, ``GetResultBytes``, to retrieve the
    return value. Whereas, on failure, you are supposed to run ``GetExceptionMessage`` and ``GetExceptionStack`` to retrieve the error information.

    The "xelib" higher-level wrappers, then, abstracts this complex call pattern for you. In this python ``Xelib`` API, the actual result value is directly returned to you. If an error occurs, then either an exception is raised or a falsey value will be returned, depending on the ``ex`` parameter (see below section).

    Additionally, ``XEditLib.dll`` requires you to run ``InitXEdit()`` before doing anything else, and ``CloseXEdit()`` after you're done. The plugin loading mechanism is also a bit complex, where you need to join your list of plugins into a single string to act as input, where the actual load call is an asynchronous call where you need to poll for loader status until the load is complete. Again, ``Xelib`` abstracts this for you in the form of a context manager (``with Xelib(...).session() as xelib: ...``) so you don't have to worry about it.

    Lastly, during an ``XEditLib.dll`` session, every handle you obtain can be released by calling the ``Release`` function on it, and ``XEditLib.dll`` expects you to manually manage each handle. To make it easier, ``Xelib`` will give you a context manager (``with xelib.manage_handles(): ...``) so that you can manage handles in groups. The higher-level ``XEdit`` API (also offered by ``pyxedit``) will go one step further and automatically tie together the lifecycle of a handle to the lifecycle of an element object, so that when an object gets garbage collected, its handle is automatically released.

The `ex` Parameter
==================

Many ``Xelib`` API methods will support an ``ex`` parameter that can be set to
`True` or `False`, and has a default value associated. In the API documentation,
this parameter will not be documented, since it always means the same thing.
When ``ex=False``, the method will not raise an exception, and will instead return some kind of falsey value like `None` if a return value is expected.
When ``ex=True``, any kind of errors encountered in ``XEditLib.dll`` will be
raised as a ``XelibError``.

.. note::
    **This is not necessarily a one-to-one correspondance to the** ``Ex`` **functions of the** `javascript xelib <https://github.com/z-edit/xelib>`_ **library.** I did use the javascript xelib library as a reference for creating this python wrapper, however I think I may have misunderstood `Ex` as short for `Exception`. Later on I `learned <https://stackoverflow.com/questions/3963374/what-does-it-mean-when-ex-is-added-to-a-function-method-name>`_ that it is also likely to mean `Extension`, which seems to be a known pattern in the windows world. Either way, I ended up with ``ex=`` optional parameters to mean `exception`, and I think that's what I will go with in this python wrapper.

.. warning::
    A word of caution for the ``ex=False`` option: while doing so will allow
    you to be more liberal and succinct in your code by ignoring exceptions underneath and turning them into falsey values, it does carry a hefty performance penalty since every error/exception triggered underneath that gets ignored actually has a noticeable performance cost to generate.
    
    For example, if you do a tree walk of all elements under a large number of records, where on each node, you perform errorneous logic, ``ex=False`` may
    hide them away and let you bypass them with a falseyness check, but the speed of your tree walk may slow down to a crawl.

Basic Methods
=============
Basic boilerplate for usage.

.. list-table::
    :widths: 100
    :header-rows: 0
    :align: left

    * - `\_\_init\_\_ <#pyxedit.Xelib.\_\_init\_\_>`_
    * - `session <#pyxedit.Xelib.session>`_

.. autoclass:: pyxedit.Xelib

    .. automethod:: __init__
    .. automethod:: session

Handle Management Methods
=========================
Convenient utilities for managing handles.

.. list-table::
    :widths: 100
    :header-rows: 0
    :align: left

    * - `manage_handles <#pyxedit.Xelib.manage_handles>`_
    * - `promote_handle <#pyxedit.Xelib.promote_handle>`_
    * - `print_handle_management_stack <#pyxedit.Xelib.print_handle_management_stack>`_


.. autoclass:: pyxedit.Xelib

    ...continued...

    .. automethod:: manage_handles
    .. automethod:: promote_handle
    .. automethod:: print_handle_management_stack

Meta Methods
============
Library-specific methods such as getting globals.

.. list-table::
    :widths: 100
    :header-rows: 0
    :align: left

    * - `initialize <#pyxedit.Xelib.initialize>`_
    * - `finalize <#pyxedit.Xelib.finalize>`_
    * - `get_global <#pyxedit.Xelib.get_global>`_
    * - `get_globals <#pyxedit.Xelib.get_globals>`_
    * - `set_sort_mode <#pyxedit.Xelib.set_sort_mode>`_
    * - `release <#pyxedit.Xelib.release>`_
    * - `release_nodes <#pyxedit.Xelib.release_nodes>`_
    * - `switch <#pyxedit.Xelib.switch>`_
    * - `get_duplicate_handles <#pyxedit.Xelib.get_duplicate_handles>`_
    * - `clean_store <#pyxedit.Xelib.clean_store>`_
    * - `reset_store <#pyxedit.Xelib.reset_store>`_

.. autoclass:: pyxedit.Xelib

    ...continued...

    .. automethod:: initialize
    .. automethod:: finalize
    .. automethod:: get_global
    .. automethod:: get_globals
    .. automethod:: set_sort_mode
    .. automethod:: release
    .. automethod:: release_nodes
    .. automethod:: switch
    .. automethod:: get_duplicate_handles
    .. automethod:: clean_store
    .. automethod:: reset_store

Messages Methods
================
Methods for dealing with log and exception messages.

.. list-table::
    :widths: 100
    :header-rows: 0
    :align: left

    * - `get_messages <#pyxedit.Xelib.get_messages>`_
    * - `clear_messages <#pyxedit.Xelib.clear_messages>`_
    * - `get_exception_message <#pyxedit.Xelib.get_exception_message>`_
    * - `get_exception_stack <#pyxedit.Xelib.get_exception_stack>`_

.. autoclass:: pyxedit.Xelib

    ...continued...

    .. automethod:: get_messages
    .. automethod:: clear_messages
    .. automethod:: get_exception_message
    .. automethod:: get_exception_stack

Setup Methods
=============
Methods for dealing with game modes and loading files.

.. list-table::
    :widths: 100
    :header-rows: 0
    :align: left

    * - `get_game_path <#pyxedit.Xelib.get_game_path>`_
    * - `set_game_path <#pyxedit.Xelib.set_game_path>`_
    * - `get_game_language <#pyxedit.Xelib.get_game_language>`_
    * - `set_language <#pyxedit.Xelib.set_language>`_
    * - `set_game_mode <#pyxedit.Xelib.set_game_mode>`_
    * - `get_load_order <#pyxedit.Xelib.get_load_order>`_
    * - `get_active_plugins <#pyxedit.Xelib.get_active_plugins>`_
    * - `load_plugins <#pyxedit.Xelib.load_plugins>`_
    * - `load_plugin <#pyxedit.Xelib.load_plugin>`_
    * - `load_plugin_header <#pyxedit.Xelib.load_plugin_header>`_
    * - `build_references <#pyxedit.Xelib.build_references>`_
    * - `unload_plugin <#pyxedit.Xelib.unload_plugin>`_
    * - `get_loader_status <#pyxedit.Xelib.get_loader_status>`_
    * - `get_loaded_file_names <#pyxedit.Xelib.get_loaded_file_names>`_

.. autoclass:: pyxedit.Xelib

    ...continued...

    .. automethod:: get_game_path
    .. automethod:: set_game_path
    .. automethod:: get_game_language
    .. automethod:: set_language
    .. automethod:: set_game_mode
    .. automethod:: get_load_order
    .. automethod:: get_active_plugins
    .. automethod:: load_plugins
    .. automethod:: load_plugin
    .. automethod:: load_plugin_header
    .. automethod:: build_references
    .. automethod:: unload_plugin
    .. automethod:: get_loader_status
    .. automethod:: get_loaded_file_names

Resources Methods
=================
Methods for handling bethesda archives and game data files.

.. list-table::
    :widths: 100
    :header-rows: 0
    :align: left

    * - `extract_container <#pyxedit.Xelib.extract_container>`_
    * - `extract_file <#pyxedit.Xelib.extract_file>`_
    * - `get_container_files <#pyxedit.Xelib.get_container_files>`_
    * - `get_file_container <#pyxedit.Xelib.get_file_container>`_
    * - `get_loaded_containers <#pyxedit.Xelib.get_loaded_containers>`_
    * - `load_container <#pyxedit.Xelib.load_container>`_
    * - `build_archive <#pyxedit.Xelib.build_archive>`_
    * - `get_texture_data <#pyxedit.Xelib.get_texture_data>`_

.. autoclass:: pyxedit.Xelib

    ...continued...

    .. automethod:: extract_container
    .. automethod:: extract_file
    .. automethod:: get_container_files
    .. automethod:: get_file_container
    .. automethod:: get_loaded_containers
    .. automethod:: load_container
    .. automethod:: build_archive
    .. automethod:: get_texture_data

Elements Methods
================
Methods for handling elements.

.. list-table::
    :widths: 100
    :header-rows: 0
    :align: left

    * - `has_element <#pyxedit.Xelib.has_element>`_
    * - `get_element <#pyxedit.Xelib.get_element>`_
    * - `add_element <#pyxedit.Xelib.add_element>`_
    * - `add_element_value <#pyxedit.Xelib.add_element_value>`_
    * - `remove_element <#pyxedit.Xelib.remove_element>`_
    * - `remove_element_or_parent <#pyxedit.Xelib.remove_element_or_parent>`_
    * - `set_element <#pyxedit.Xelib.set_element>`_
    * - `get_elements <#pyxedit.Xelib.get_elements>`_
    * - `get_def_names <#pyxedit.Xelib.get_def_names>`_
    * - `get_links_to <#pyxedit.Xelib.get_links_to>`_
    * - `set_links_to <#pyxedit.Xelib.set_links_to>`_
    * - `get_container <#pyxedit.Xelib.get_container>`_
    * - `get_element_file <#pyxedit.Xelib.get_element_file>`_
    * - `get_element_group <#pyxedit.Xelib.get_element_group>`_
    * - `get_element_record <#pyxedit.Xelib.get_element_record>`_
    * - `element_count <#pyxedit.Xelib.element_count>`_
    * - `element_equals <#pyxedit.Xelib.element_equals>`_
    * - `element_matches <#pyxedit.Xelib.element_matches>`_
    * - `has_array_item <#pyxedit.Xelib.has_array_item>`_
    * - `get_array_item <#pyxedit.Xelib.get_array_item>`_
    * - `add_array_item <#pyxedit.Xelib.add_array_item>`_
    * - `remove_array_item <#pyxedit.Xelib.remove_array_item>`_
    * - `move_array_item <#pyxedit.Xelib.move_array_item>`_
    * - `copy_element <#pyxedit.Xelib.copy_element>`_
    * - `find_next_element <#pyxedit.Xelib.find_next_element>`_
    * - `find_previous_element <#pyxedit.Xelib.find_previous_element>`_
    * - `get_signature_allowed <#pyxedit.Xelib.get_signature_allowed>`_
    * - `get_allowed_signatures <#pyxedit.Xelib.get_allowed_signatures>`_
    * - `get_is_modified <#pyxedit.Xelib.get_is_modified>`_
    * - `get_is_editable <#pyxedit.Xelib.get_is_editable>`_
    * - `set_is_editable <#pyxedit.Xelib.set_is_editable>`_
    * - `get_is_removable <#pyxedit.Xelib.get_is_removable>`_
    * - `get_can_add <#pyxedit.Xelib.get_can_add>`_
    * - `element_type <#pyxedit.Xelib.element_type>`_
    * - `def_type <#pyxedit.Xelib.def_type>`_
    * - `smash_type <#pyxedit.Xelib.smash_type>`_
    * - `value_type <#pyxedit.Xelib.value_type>`_
    * - `is_sorted <#pyxedit.Xelib.is_sorted>`_
    * - `is_fixed <#pyxedit.Xelib.is_fixed>`_
    * - `is_flags <#pyxedit.Xelib.is_flags>`_

.. autoclass:: pyxedit.Xelib

    ...continued...

    .. automethod:: has_element
    .. automethod:: get_element
    .. automethod:: add_element
    .. automethod:: add_element_value
    .. automethod:: remove_element
    .. automethod:: remove_element_or_parent
    .. automethod:: set_element
    .. automethod:: get_elements
    .. automethod:: get_def_names
    .. automethod:: get_links_to
    .. automethod:: set_links_to
    .. automethod:: get_container
    .. automethod:: get_element_file
    .. automethod:: get_element_group
    .. automethod:: get_element_record
    .. automethod:: element_count
    .. automethod:: element_equals
    .. automethod:: element_matches
    .. automethod:: has_array_item
    .. automethod:: get_array_item
    .. automethod:: add_array_item
    .. automethod:: remove_array_item
    .. automethod:: move_array_item
    .. automethod:: copy_element
    .. automethod:: find_next_element
    .. automethod:: find_previous_element
    .. automethod:: get_signature_allowed
    .. automethod:: get_allowed_signatures
    .. automethod:: get_is_modified
    .. automethod:: get_is_editable
    .. automethod:: set_is_editable
    .. automethod:: get_is_removable
    .. automethod:: get_can_add
    .. automethod:: element_type
    .. automethod:: def_type
    .. automethod:: smash_type
    .. automethod:: value_type
    .. automethod:: is_sorted
    .. automethod:: is_fixed
    .. automethod:: is_flags

Element Value Methods
=====================
Methods for getting or setting values on elements.

.. autoclass:: pyxedit.Xelib

    ...continued...

    .. automethod:: name
    .. automethod:: long_name
    .. automethod:: display_name
    .. automethod:: placement_name
    .. automethod:: path
    .. automethod:: long_path
    .. automethod:: local_path
    .. automethod:: signature
    .. automethod:: sort_key
    .. automethod:: get_value
    .. automethod:: set_value
    .. automethod:: get_int_value
    .. automethod:: set_int_value
    .. automethod:: get_uint_value
    .. automethod:: set_uint_value
    .. automethod:: get_float_value
    .. automethod:: set_float_value
    .. automethod:: get_flag
    .. automethod:: set_flag
    .. automethod:: get_enabled_flags
    .. automethod:: set_enabled_flags
    .. automethod:: get_all_flags
    .. automethod:: get_enum_options
    .. automethod:: signature_from_name
    .. automethod:: name_from_signature
    .. automethod:: get_signature_name_map

Files Methods
=============
Methods for handling files.

.. autoclass:: pyxedit.Xelib

    ...continued...

    .. automethod:: add_file
    .. automethod:: file_by_index
    .. automethod:: file_by_load_order
    .. automethod:: file_by_name
    .. automethod:: file_by_author
    .. automethod:: nuke_file
    .. automethod:: rename_file
    .. automethod:: save_file
    .. automethod:: get_record_count
    .. automethod:: get_override_record_count
    .. automethod:: md5_hash
    .. automethod:: crc_hash
    .. automethod:: get_file_load_order
    .. automethod:: get_file_header
    .. automethod:: sort_editor_ids
    .. automethod:: sort_names

File Values Methods
===================
Methods for getting or setting values on files.

.. autoclass:: pyxedit.Xelib

    ...continued...

    .. automethod:: get_next_object_id
    .. automethod:: set_next_object_id
    .. automethod:: get_file_name
    .. automethod:: get_file_author
    .. automethod:: set_file_author
    .. automethod:: get_file_description
    .. automethod:: set_file_description
    .. automethod:: get_is_esm
    .. automethod:: set_is_esm

Records Methods
===============
Methods for handling records in files.

.. autoclass:: pyxedit.Xelib

    ...continued...

    .. automethod:: get_form_id
    .. automethod:: get_hex_form_id
    .. automethod:: set_form_id
    .. automethod:: get_record
    .. automethod:: get_records
    .. automethod:: get_refrs
    .. automethod:: get_overrides
    .. automethod:: get_master_record
    .. automethod:: get_previous_override
    .. automethod:: get_winning_override
    .. automethod:: get_injection_target
    .. automethod:: find_next_record
    .. automethod:: find_previous_record
    .. automethod:: find_valid_references
    .. automethod:: get_referenced_by
    .. automethod:: exchange_references
    .. automethod:: is_master
    .. automethod:: is_injected
    .. automethod:: is_override
    .. automethod:: is_winning_override
    .. automethod:: get_nodes
    .. automethod:: get_conflict_data
    .. automethod:: get_record_conflict_data
    .. automethod:: get_node_elements

Record Values Methods
=====================
Methods for getting or setting values from records.

.. autoclass:: pyxedit.Xelib

    ...continued...

    .. automethod:: editor_id
    .. automethod:: full_name
    .. automethod:: get_ref_editor_id
    .. automethod:: translate
    .. automethod:: rotate
    .. automethod:: get_record_flag
    .. automethod:: set_record_flag

Masters Methods
===============
Methods for handling masters in files.

.. autoclass:: pyxedit.Xelib

    ...continued...

    .. automethod:: clean_masters
    .. automethod:: sort_masters
    .. automethod:: add_master
    .. automethod:: add_required_masters
    .. automethod:: get_masters
    .. automethod:: get_required_by
    .. automethod:: get_master_names
    .. automethod:: add_all_masters
    .. automethod:: get_available_masters

Groups Methods
==============
Methods for handling groups in files.

.. autoclass:: pyxedit.Xelib

    ...continued...

    .. automethod:: has_group
    .. automethod:: add_group
    .. automethod:: get_child_group

Serialization Methods
=====================
Methods for serializing elements to JSON and deserializing them from JSON.

.. autoclass:: pyxedit.Xelib

    ...continued...

    .. automethod:: element_to_json
    .. automethod:: element_to_dict
    .. automethod:: element_from_json
    .. automethod:: element_from_dict

Plugin Error Methods
====================
Methods for getting and resolving errors/dirty edits in plugin files.

.. autoclass:: pyxedit.Xelib

    ...continued...

    .. automethod check_for_errors
    .. automethod get_error_thread_done
    .. automethod get_errors
    .. automethod remove_identical_records

Enums
=====

``Xelib`` uses the following Enums (list of values), each of which can be accessed as an attribute from the ``Xelib`` class itself.

.. autoclass:: pyxedit.Xelib.ElementTypes
.. autoclass:: pyxedit.Xelib.DefTypes
.. autoclass:: pyxedit.Xelib.SmashTypes
.. autoclass:: pyxedit.Xelib.ValueTypes
.. autoclass:: pyxedit.Xelib.SortBy
.. autoclass:: pyxedit.Xelib.ConflictThis
.. autoclass:: pyxedit.Xelib.ConflictAll
.. autoclass:: pyxedit.Xelib.GetRefrsFlags
.. autoclass:: pyxedit.Xelib.ArchiveTypes
.. autoclass:: pyxedit.Xelib.LoaderStates
.. autoclass:: pyxedit.Xelib.GameModes