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
