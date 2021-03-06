======================
The Xelib API Tutorial
======================

.. toctree::
   :maxdepth: 1

The Xelib Class
===============

The entry point of the ``Xelib`` API is the ``Xelib`` class. This is importable from the top-level namespace of pyxedit. Typically, you would make an object with the class to interact with the API::

    from pyxedit import Xelib


    xelib = Xelib()

The Xelib Session
=================

The ``Xelib`` API is, ultimately, a python interface to the various methods in ``XEditLib.dll``. For python to make use of a ``.dll`` file, it must first load it into memory, and once python is done with it, it is good to unload it so that the next time you load it you're guaranteed a new instance.

Beyond loading/unloading of the ``.dll`` file, ``XEditLib.dll`` API also has code for starting up/tearing down an xEdit session (see the ``Initialize`` and ``Finalize`` API methods), where all work is expected to be done in the context of an active session. When you're using the ``XEditLib.dll`` functions, you're expected to first run ``Initialize()``, then do all your work, and at the end run ``Finalize()`` before you exit.

The ``Xelib`` API lets you invoke all of this boilerplate logic through its context manager behavior. Entering the context of a ``Xelib`` object will load ``XEditLib.dll`` and run ``Initialize()``, where upon context exit, ``Finalize()`` will run, and then ``XEditLib.dll`` will be unloaded. Please see the below example::

    from pyxedit import Xelib


    with Xelib() as xelib:
        # here, `XEditLib.dll` has been loaded, all API functionality on
        # the xelib object has been set up, and `Initialize()` has been
        # executed; from here on, you can invoke methods on `xelib` to do
        # your work
        pass

    # here, `Finalize()` has been executed, and `XEditLib.dll` has been
    # unloaded.

When you write code with the ``Xelib`` API, it is expected that just about all the code you write will be inside a ``with Xelib() as xelib: ...`` context.

Game Configuration
==================

Once you're inside a session, the first thing is usually to configure it. Here is where you get to tell the API which game you want to work with, and the path to the game install folder. To set the game to SkyrimSE, run the following::

    xelib.set_game_mode(xelib.Games.SkyrimSE)

Note that ``Games`` is an *Enum* object available on the ``Xelib`` class itself. Most enums that the ``Xelib`` API works with will be available on the ``Xelib`` class itself. If you're curious, you can check out other examples like ``xelib.ElementTypes`` or ``xelib.LoaderStates``.

With a game chosen, the xEdit session seems to be able to auto-detect your game folder. To check this, you can run the following to see what game folder it has found::

    xelib.get_game_path()

Most likely, if you already have Skyrim SE installed on your computer, it will show up here. If it doesn't (or if you just want to explicitly point it to a Skyrim SE folder), you can run the following::

    xelib.set_game_path('D:\\SteamLibrary\\steamapps\\common\\Skyrim Special Edition')

Loading Plugins
===============

With the game chosen, and with the library knows where your game is installed to, you can now proceed to load some plugins. The following code snippet shows
how this can be done with the ``Xelib`` API::

    import os
    import time


    xelib.load_plugins(os.linesep.join(['Skyrim.esm',
                                        'Update.esm',
                                        'Dawnguard.esm']))
    while xelib.get_loader_status() == xelib.LoaderStates.Active:
        time.sleep(0.1)

There are several things about the above code. First, `load_plugins` takes in a string that is expected to be a newline-separated list of plugin names, which is why we run ``os.linesep.join`` to turn the list of plugin names into a string that looks like::

    Skyrim.esm
    Update.esm
    Dawnguard.esm

Next, once you tell the library to load those plugins, the function itself is an async function that returns immediately while the plugin continues to load in the background. There's not much you can do before the plugins actually load, so we can repeatedly check the loader state and keep on waiting until it is no longer ``lsActive``.

Once the loader finishes, you're now ready to do anything and everything in the xEdit session. To put everything so far together, you end up with code that looks like this::

    import os
    from pyxedit import Xelib
    import time

    game_path = 'D:\\SteamLibrary\\steamapps\\common\\Skyrim Special Edition'
    plugins = ['Skyrim.esm', 'Update.esm', 'Dawnguard.esm']


    with Xelib() as xelib:
        # configure xelib to work with our game
        xelib.set_game_mode(xelib.Games.SkyrimSE)
        xelib.set_game_path(game_path)

        # load the plugins
        xelib.load_plugins(os.linesep.join(plugins))

        # wait for plugins to finish loading
        while xelib.get_loader_status() == xelib.LoaderStates.Active:
            time.sleep(0.1)

        # we're now ready to do whatever
        pass

Using The Xelib API
===================

Now might be the time to take a look at the `Xelib API Reference <../api_reference/xelib_api_reference.html>`_ for the list of all the methods you have available to you. These can all be accessed from the ``xelib`` object.

.. note::

    In addition to the API reference provided here, it might also be useful to look at `zEdit's xelib API documentation <https://z-edit.github.io/#/docs?t=Development%2FAPIs%2Fxelib>`_. Both zEdit's xelib API and ``pyxedit.Xelib`` are wrappers around ``XEditLib.dll``, it's just that the former is an ES6 Javascript wrapper while the latter is a Python wrapper.
    
    In fact, ``pyxedit.Xelib`` was written using zEdit's xelib API as reference, so a lot of the patterns ended up looking very similar, where you can consider ``pyxedit.Xelib`` to be a python version of an "almost-equivalent". In both cases, methods are largely one-to-one with ``XEditLib.dll`` methods as well.

    That said, there are some differences between zEdit's xelib API and ``pyxedit.Xelib``, `which you can read about here <#>`_.

Handle Management
=================

Much of ``XEditLib.dll``'s API works with the notion of handles, which are similar to pointers and memory management in languages like C/C++. For example, when you retrieve an element, it is given to you in the form of an integer *handle*::

    # try to get the ARMA record at Dawnguard.esm\ARMA\VampireWolfAA
    handle = xelib.get_element(0, 'Dawnguard.esm\\ARMA\\VampireWolfAA')

    # the ARMA record is now available to you as an integer handle
    print(handle)  # should be some integer

    # you can then use the integer as an 'id' to further inspect the ARMA record with
    record_name = xelib.name(handle)
    print(record_name)

It is good to release a handle after you're done using it so that the memory and the integer can be recycled for use by other things. This is typically done with ``XEditLib``'s ``Release`` method, which is available on ``Xelib`` as ``xelib.release``::

    # release the handle
    xelib.release(handle)

But manually keeping track of every handle the API throws at you can be difficult. For this reason, the ``xelib`` object also provides a context manager you can use to manage these handles en-mass::

    # enter a handle management context
    with xelib.manage_handles():
        # within the context, we can invoke methods and use any handles
        # we get back
        handle = xelib.get_element(0, 'Dawnguard.esm\\ARMA\\VampireWolfAA')
        print(xelib.name(handle))

        # when exiting the context, all new handles generated within the
        # context will be automatically released

    # those handles should no longer be valid after exiting the context

The handle management contexts can also be nested to create multiple layers of handle management, which might be useful in complex use cases::

    with xelib.manage_handles():
        # do a task
        ...

        with xelib.manage_handles():
            # do a subtask that might involve lots of handles
            ...
            
            # maybe you get a handle that you want to keep beyond this context,
            # in which case you can promote it to the parent context
            handle_to_keep = ...
            xelib.promote_handle(handle_to_keep)

        # those subtask handles are now released (except for handle_to_keep),
        # continue doing the main task
        ...

    # task is done and all handles are released

