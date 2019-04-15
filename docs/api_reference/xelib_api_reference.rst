.. |hr| raw:: html

    <hr/>

===================
Xelib API Reference
===================

.. toctree::
   :maxdepth: 1

The Xelib Class
===============

.. autoclass:: pyxedit.Xelib

    |hr|

    .. rubric:: Basic Methods
    .. automethod:: __init__
    .. automethod:: __enter__
    .. automethod:: __exit__
    .. automethod:: load_lib
    .. autoattribute:: raw_api
    .. autoattribute:: loaded

    |hr|

    .. rubric:: Handle Management Methods
    Methods for managing handles.

    .. autoattribute:: opened_handles
    .. automethod:: track_handle
    .. automethod:: release_handle
    .. automethod:: release_handles
    .. automethod:: manage_handles
    .. automethod:: promote_handle
    .. automethod:: print_handle_management_stack

    |hr|

    .. rubric:: Meta Methods
    Library-specific methods such as getting globals.

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

    |hr|

    .. rubric:: Messages Methods
    Methods for dealing with log and exception messages.

    .. automethod:: get_messages
    .. automethod:: clear_messages
    .. automethod:: get_exception_message
    .. automethod:: get_exception_stack

    |hr|

    .. rubric:: Setup Methods
    Methods for dealing with game modes and loading files.

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

    |hr|

    .. rubric:: Resources Methods
    Methods for handling bethesda archives and game data files.

    .. automethod:: extract_container
    .. automethod:: extract_file
    .. automethod:: get_container_files
    .. automethod:: get_file_container
    .. automethod:: get_loaded_containers
    .. automethod:: load_container
    .. automethod:: build_archive
    .. automethod:: get_texture_data

    |hr|

    .. rubric:: Elements Methods
    Methods for handling elements.

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

    |hr|

    .. rubric:: Element Value Methods
    Methods for getting or setting values on elements.

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

    |hr|

    .. rubric:: Files Methods
    Methods for handling files.

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

    |hr|

    .. rubric:: File Values Methods
    Methods for getting or setting values on files.

    .. automethod:: get_next_object_id
    .. automethod:: set_next_object_id
    .. automethod:: get_file_name
    .. automethod:: get_file_author
    .. automethod:: set_file_author
    .. automethod:: get_file_description
    .. automethod:: set_file_description
    .. automethod:: get_is_esm
    .. automethod:: set_is_esm

    |hr|

    .. rubric:: Records Methods
    Methods for handling records in files.

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

    |hr|

    .. rubric:: Record Values Methods
    Methods for getting or setting values from records.

    .. automethod:: editor_id
    .. automethod:: full_name
    .. automethod:: get_ref_editor_id
    .. automethod:: translate
    .. automethod:: rotate
    .. automethod:: get_record_flag
    .. automethod:: set_record_flag

    |hr|

    .. rubric:: Masters Methods
    Methods for handling masters in files.

    .. automethod:: clean_masters
    .. automethod:: sort_masters
    .. automethod:: add_master
    .. automethod:: add_required_masters
    .. automethod:: get_masters
    .. automethod:: get_required_by
    .. automethod:: get_master_names
    .. automethod:: add_all_masters
    .. automethod:: get_available_masters

    |hr|

    .. rubric:: Groups Methods
    Methods for handling groups in files.

    .. automethod:: has_group
    .. automethod:: add_group
    .. automethod:: get_child_group

    |hr|

    .. rubric:: Serialization Methods
    Methods for serializing elements to JSON and deserializing them from JSON.

    .. automethod:: element_to_json
    .. automethod:: element_to_dict
    .. automethod:: element_from_json
    .. automethod:: element_from_dict

    |hr|

    .. rubric:: Plugin Error Methods
    Methods for getting and resolving errors/dirty edits in plugin files.

    .. automethod check_for_errors
    .. automethod get_error_thread_done
    .. automethod get_errors
    .. automethod remove_identical_records