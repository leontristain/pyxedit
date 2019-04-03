Welcome To pyxedit
===================================

`xEdit <https://github.com/TES5Edit/TES5Edit>`_, written by `ElminsterAU`, is an advanced graphical module editor and conflict detector for Bethesda games. It is one of the major cornerstones of the infrastructure that props up the world of Skyrim Modding. Users typically use this program to analyze and modify the data contained within Bethesda plugin (`.esm`, `.esp`, etc...) files.

Near the end of 2016, prolific Skyrim toolmaker `mator` released the `xedit-lib <https://github.com/matortheeternal/xedit-lib>`_ project, which wraps around xEdit's object pascal code to build a dynamically linked library designed for wrapping by other languages. He went on to wrap it in ES6 Javascript as the `xelib <https://github.com/z-edit/xelib>`_ library, which forms the API backbone for his `zedit <https://github.com/z-edit/zedit>`_ project.

This project, `pyxedit <#>`_, is my attempt to wrap the same xedit-lib library in python, and to also provide a pythonic high level API on top of it.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Package Layout
===================================

`pyxedit` provides two APIs:

The Xelib API
-------------

The ``Xelib`` API is the low-level API, and is designed to be a minimal wrapper around ``XEditLib.dll``. This API is made accessible via a ``Xelib`` top-level class. Methods on the API are almost one-to-one with ``XEditLib.dll``'s public methods. Users familiar with zEdit's xelib API can consider this the "python version" of an almost-equivalent.

The XEdit API
-------------

The ``XEdit`` API is a high-level API where the various data types of xedit have been formalized into python objects through the use of the ``Xelib`` API. This high-level API is made accessible via an ``XEdit`` top-level class. With the XEdit API:

- You work with objects instead of handles, where lifecycle management for handles automatically happen in the background through python's garbage collection.
- The objects it gives you will support many of python's native syntax, such as dictionary indexing to traverse the element tree, assignable properties for getting and setting element values, and list-like syntax for working with arrays. The objects also support many nice, pythonic methods that abstracts away the more verbose Xelib methods, as well as providing more convenient methods where they make sense. For example, to iterate through all child elements of an element, the object will let you simply do ``for item in element.children: ...``
- Objects will specialize depending on the qualities of an element. For example, an object that wraps around an ``ARMA`` record will automatically be an object of an ``XEditArmature`` class that has signature-specific fields available as properties on the class. For the time being, not all signatures are supported, I anticipate more specialized classes will be added as my development needs expand to them. Of course, others are welcome to contribute as well.

Quickstart
===================================

You're going to need python 3.7+, and it's going to have to be the Windows version. I highly recommend doing any kind of python project inside a virtual environment so that packages you install will not pollute into your global python install in a messy and unmanageable way. To install the package::

    > pip install pyxedit

Here's a quick snippet if you just want to dive in and play around with things. Note that for this library to work at all, you will need Skyrim SE (or any other XEditLib-supported game) installed on your computer. The below snippet assumes SkyrimSE with at least the Dawnguard DLC available::

    from xedit import XEdit

    if __name__ == '__main__':
        with XEdit(plugins=['Dawnguard.esm']).session() as xedit:
            dawnguard = xedit['Dawnguard.esm']
            vampire_wolf_aa = dawnguard['ARMA\\VampireWolfAA']

            # print out these element objects
            print(dawnguard)
            print(vampire_wolf_aa)

If you just want to launch the python interpreter and play around in there, you can try the following::

    Python 3.7.2
    > from xedit import XEdit
    > xedit = XEdit.quickstart()  # this will load Dawnguard.esm by default,
                                  # start an xedit context, and give you an
                                  # xedit handle
    > arma = xedit['Dawnguard.esm\\ARMA']
    > arma.ls  # this will print out the list of vampire_wolf_aa's children
    <XEditArmature ARMA 02014CCC DLC1GargoyleAlbinoAA 2>
    <XEditArmature ARMA 02012E89 ShellbugHelmetAA 3>
    <XEditArmature ARMA 02011CF4 DLC1HawkRingAA 4>
    <XEditArmature ARMA 02010E14 DLC1VampireSkeletonFXAA 5>
    <XEditArmature ARMA 02010CFC DLC1GargoyleVariantBossSTONEAA 6>
    <XEditArmature ARMA 02010CFB DLC1GargoyleVariantBossAA 7>
    <XEditArmature ARMA 0200E69F DLC1SeranaHoodAA 8>
    <XEditArmature ARMA 0200CAD2 DLC1IvoryCuirassAlternateAA 9>
    <XEditArmature ARMA 020050CF DawnguardHelmetFullAA 10>
    ...

Here are some more in-depth tutorials:

- :doc:`Xelib Tutorial`
- :doc:`XEdit Tutorial`

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
