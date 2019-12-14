======================
XEdit API Reference
======================

.. toctree::
   :maxdepth: 1

Overview
========

The ``XEdit`` API is a high-level API built on top of the ``Xelib`` low-level API. The goal is to make it so that when you use this API, it feels like you're coding in a high-level language like python.

The API will wrap every ``Xelib`` handle into an object with lifecycle management included. Instead of calling the various getter and setter functions with integer handles, you now have access to pythonic properties and object methods, as well as language syntax support on these objects, that allow you to do the same things and more

For example, in ``Xelib``, you might do this:

.. highlight:: python
.. code-block:: python

    from pyxedit import Xelib

    with Xelib(plugins=['GOT.esp', 'LOTR.esp']).session() as xelib:
        h = xelib.get_element(0, 'GOT.esp\\NPC_\\JonSnow')
        print(xelib.display_name(h))  # prints 'Jon Snow'

In ``XEdit``, you can now do this:

.. highlight:: python
.. code-block:: python

    from pyxedit import XEdit

    with XEdit(plugins=['GOT.esp', 'LOTR.esp']).session() as xedit:
        jon_snow = xedit['GOT.esp\\NPC\\JonSnow']
        print(john_snow.display_name)  # prints 'Jon Snow'

As seen above, you would work inside a ``session()`` context manager just like ``Xelib``. Within the session, you have access to an ``xedit`` object. This object is the entry point to everything you will ever do. From here, you can access sub-elements via indexing, the ``.get()`` method, or other methods.

When a method gives you another element, that element will be give to you as an object, and it will an object of some subclass of ``XEditBase``. Usually, you will get an ``XEditGenericObject``. If it's a top-level plugin file, it will be an ``XEditPlugin``. If it's a record, it may be a signature-specific object like an ``XEditArmor`` or ``XEditNPC``. If you land on an array record, it will be given to you as an ``XEditArray`` which supports as much ``Iterable``-like functionality as can be done with the underlying ``XEditLib.dll``.

All object types will inherit from ``XEditBase``. Many object types will also inherit from ``XEditGenericObject``, such that the "general" API methods on them are almost always available. More specialized objects (like ``XEditTexture``) may support specialized properties and methods for your convenience. For example, you can access ``XEditTexture.file_paths`` to get a list of all data file paths associated with a texture.

Instead of having to call ``get_value`` and ``set_value`` in the ``Xelib`` API, with ``XEdit`` you can do assignment directly, and the object will resolve the value type automatically. References can be assigned with objects. In general you pretty much never need to worry about handles.


XEdit
=====

.. autoclass:: pyxedit.xedit.xedit.XEdit

    .. automethod:: __init__
    .. automethod:: session
    .. autoattribute:: game_mode
    .. autoattribute:: game_path
    .. autoattribute:: plugins
    .. autoattribute:: plugin_count
    .. automethod:: add_file
    .. automethod:: quickstart

XEditBase
=========

XEditBase Fundamentals
========================

.. autoclass:: pyxedit.xedit.base.XEditBase

    .. automethod:: __hash__
    .. automethod:: __eq__
    .. autoattribute:: xelib
    .. automethod:: xelib_run

XEditBase Attributes
====================

.. autoclass:: pyxedit.xedit.base.XEditBase

    .. autoattribute:: element_type
    .. autoattribute:: def_type
    .. autoattribute:: smash_type
    .. autoattribute:: value_type
    .. autoattribute:: type
    .. autoattribute:: is_ref
    .. autoattribute:: is_modified
    .. autoattribute:: is_removable
    .. autoattribute:: is_sorted
    .. autoattribute:: is_flags
    .. autoattribute:: can_add
    .. autoattribute:: name
    .. autoattribute:: long_name
    .. autoattribute:: display_name
    .. autoattribute:: path
    .. autoattribute:: long_path
    .. autoattribute:: local_path
    .. autoattribute:: signature
    .. autoattribute:: signature_name

XEditBase Tree Operations
=====================================

.. autoclass:: pyxedit.xedit.base.XEditBase

    .. automethod:: __getitem__
    .. automethod:: get
    .. automethod:: has
    .. automethod:: add
    .. automethod:: get_or_add
    .. automethod:: delete
    .. autoattribute:: has_child_group
    .. autoattribute:: num_child_elements
    .. autoattribute:: num_children
    .. autoattribute:: child_group
    .. autoattribute:: child_elements
    .. autoattribute:: children
    .. automethod:: descendants
    .. autoattribute:: parent
    .. autoattribute:: references
    .. autoattribute:: ls

XEditPlugin
===========

XEditPlugin Attributes
======================

.. autoclass:: pyxedit.xedit.plugin.XEditPlugin

    .. autoattribute:: author
    .. autoattribute:: description
    .. autoattribute:: is_esm
    .. autoattribute:: next_object
    .. autoattribute:: num_records
    .. autoattribute:: num_override_records
    .. autoattribute:: md5
    .. autoattribute:: crc
    .. autoattribute:: load_order
    .. autoattribute:: header
    .. autoattribute:: masters
    .. autoattribute:: master_names

XEditPlugin Operations
======================

.. autoclass:: pyxedit.xedit.plugin.XEditPlugin

    .. automethod:: add_master
    .. automethod:: add_master_by_name
    .. automethod:: add_masters_needed_for_copying
    .. automethod:: sort_masters
    .. automethod:: clean_masters
    .. automethod:: rename
    .. automethod:: nuke
    .. automethod:: save
    .. automethod:: save_as

XEditGenericObject
==================

.. autoclass:: pyxedit.xedit.generic.XEditGenericObject

    .. autoattribute:: value
    .. autoattribute:: form_id
    .. autoattribute:: form_id_str
    .. autoattribute:: local_form_id
    .. autoattribute:: local_form_id_str
    .. autoattribute:: plugin
    .. autoattribute:: is_master
    .. autoattribute:: is_injected
    .. autoattribute:: is_override
    .. autoattribute:: is_winning_override
    .. autoattribute:: master
    .. autoattribute:: overrides
    .. autoattribute:: winning_override
    .. autoattribute:: previous_override
    .. autoattribute:: injection_target
    .. automethod:: copy_into
