from xeditlib import XEdit

# To start, create an XEdit object, tell it what game you want to open, and
# what plugins you want to load. With the xedit object, invoke the `session`
# method to generate a context manager that handles the opening and closing
# of the xedit context. Specifically, on entering the context, the code will
# load the xedit-lib DLL, set configuration (game mode, plugins, etc...),
# initialize the xedit runtime, and load the plugins. On exiting the context,
# the code will finalize the xedit runtime and then unload the DLL.
with XEdit(game='SkyrimSE', plugins=['The Ordinary Women.esp']).session() as xedit:
    # inside this context, it's as if you have an xEdit window that's fully
    # loaded, you can now proceed to look at things

    # for example, you can see what plugins are available
    xedit.plugin_names

    # you can traverse down to a plugin object
    tow = xedit['The Ordinary Women.esp']

    # you can traverse far down to a record if you like
    tow_bryling = xedit['The Ordinary Women.esp\\NPC_\\Bryling']

    # indexing will raise an exception on any error; you can alternatively
    # use the .get function to traverse/query the tree so that it will return
    # a None on error, just like a python dictionary would
    tow = xedit.get('The Ordinary Women.esp')
    tow_bryling = xedit.get('The Ordinary Women.esp\\NPC_\\Bryling')

    # from any object, you can further traverse to its child objects, the
    # following will all work
    tow_bryling = tow['NPC_\\Bryling']
    tow_bryling = tow['NPC_']['Bryling']

    # you should be able to get and set values easily via properties
    bryling_texture_lighting = tow_bryling['QNAM']
    bryling_texture_lighting.Red = 120
    bryling_texture_lighting.Green = 130
    bryling_texture_lighting.Blue = 225

    # you should be able to nullify a field
    tow_bryling['WNAM'] = None

    # you should be able to delete objects
    tow_bryling.delete()

    # you should be able to work with arrays in pythonic fashion as well
    # (to be figured out)

    # the object returned will be of a specific subclass if an existing one
    # matches the record signature. For example, tow_bryling here should be
    # of type XEditNPC; specific subclasses can contain properties and methods
    # that apply to that record type

    # if no matching subclasses can be found, a XEditGenericObject object will
    # be returned; this object allows you to look at generic metadata like the
    # name, path, signature, etc..., and allow you to further traverse

    # plugins will always be an XEditPlugin object. You can check for plugin-
    # specific things like `is_esm`, and you can do things to the plugin like
    # saving it.
    tow.is_esm
    tow.save_as('D:\\SkyrimModding\\my_modified_tow.esp')  # as a new file
    tow.save()  # save in place

    # maybe eventually we could have things like cleaning a plugin?
    tow.clean()

    # or maybe turning a plugin into a pseudo esl?
    if tow.is_candidate_for_pseudo_esl:
        tow.is_pseudo_esl = True

    # or maybe merge a bunch of plugins?
    xelib.merge_plugins(['A.esp', 'B.esp', 'C.esp'], dest='merged.esp')

    # or maybe generate a patch?
    xelib.create_merged_patch(dest='merged_patch.esp')

    # and you can do it all right there in python! Imagine how powerful this
    # could be when combined with python's amazing library and ecosystem for
    # automating everything on your PC. Imagine how many people can start
    # hacking this stuff when they can do it in a language as simple, succinct,
    # intuitive, and newbie-friendly as python, the language used by most CS101
    # classes!

    # when working in xedit, under the hood every new record you open will take
    # up a "handle"; it is good practice to release handles after you are done
    # with them. In the XEdit high level API here, each object is associated
    # with a handle.

    # you can use the `manage_handles` context manager on any object to initiate
    # a context where all new handles obtained during the context will be
    # released after the context
    with xedit.manage_handles:
        armo = xedit['Skyrim.esp\\ARMO']

        # `armo` will have an active handle here, and you can do things to it

    # `armo` will have been released here; further attempting to use the object
    # will raise errors

    # the `manage_handles` context can be nested if you're doing something
    # particularly complex and want to properly manage your handles

    with xedit.manage_handles:
        ...
        ...
        with xedit.manage_handles:
            ...
            ...
        ...
    ...

    # The top-level xedit context that you are already in will not only manage
    # the top-level handles (i.e. they are released after), but also ensure the
    # whole DLL is unloaded after, such that the next time you start over you're
    # starting afresh.

    # the actual handle associated with the object can be inspected with:
    tow_bryling.handle

    # you also have access to a `xelib` object on the class, that you can
    # invoke methods from the lower-level xelib api with, and if you need
    # the current handle, it's provided as I just mentioned above.
    xedit.xelib.set_float_value(tow_bryling.handle, 3.0, path='X')
    tow_bryling.xelib.set_float_value(tow_bryling.handle, 3.0, path='X')
    # these both work, since the `xelib` handle is available on every object
    # traversed from the root `xedit` object

    # this xelib API should be near-identical to the javascript xelib API
    # used in mator's zedit. After all, both are wrappers around xedit-lib, and
    # I followed a lot of his xelib patterns when implementing this python
    # wrapper.

# And that's it! The API in a nutshell.

# One thing to note is that Skyrim has A LOT of record types! So it will
# probably take a long time for all of them to have a good class implemented
# to make accessing them easy. I will implement classes as my usage of this API
# touch upon them. Of course, I'm going to always welcome pull requests, just
# make sure you have good code quality, the fields are well conceived and match
# well with the actual record fields, and unit test is included to ensure it
# works

# If a high-level class isn't yet implemented, remember you always have the
# lower-level xelib API to fall back on right there in the class.
