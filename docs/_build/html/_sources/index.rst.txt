==================
Welcome To pyxedit
==================

`xEdit <https://github.com/TES5Edit/TES5Edit>`_, written by `ElminsterAU`, is an advanced graphical module editor and conflict detector for Bethesda games. It is one of the major cornerstones of the infrastructure that props up the world of Skyrim Modding. Users typically use this program to analyze and modify the data contained within Bethesda plugin (`.esm`, `.esp`, etc...) files.

Near the end of 2016, prolific Skyrim toolmaker `mator` released the `xedit-lib <https://github.com/matortheeternal/xedit-lib>`_ project, which wraps around xEdit's object pascal code to build a dynamically linked library designed for wrapping by other languages. He went on to wrap it in ES6 Javascript as the `xelib <https://github.com/z-edit/xelib>`_ library, which forms the API backbone for his `zedit <https://github.com/z-edit/zedit>`_ project.

This project, `pyxedit <#>`_, is my attempt to wrap the same xedit-lib library in python, and to also provide a pythonic high level API on top of it.

.. toctree::
   :maxdepth: 1

   overview/index
   tutorials/index