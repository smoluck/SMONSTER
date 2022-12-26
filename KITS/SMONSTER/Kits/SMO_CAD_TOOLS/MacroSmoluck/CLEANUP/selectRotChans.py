# python

import lx

# selectRotChans.py
#
# Original in Perl by er_9, translated to Python by Cristobal Vila
#
# Use and argument to specify desired channel, X, Y or Z:
# @selectRotChans.py X
# @selectRotChans.py Y
# @selectRotChans.py Z

# Defining argument
myarg = lx.arg()

# Select current scene for query.
lx.eval('query sceneservice scene.index ? current')

# Get ID list of locator type items selected in the scene.
myitemsID = lx.evalN('query sceneservice selection ?')

# Drop channels selected.
lx.eval('select.drop channel')

# Seek in the list.
for eachItem in myitemsID:

    # Get rotation item ID.
    myrotID = lx.eval('query sceneservice item.channel ? %s' % eachItem)

    # Select the rotation Y channel, if it exists.
    if myrotID:
        lx.eval('select.channel {%s:%s} add' % (myrotID, myarg))