# python
"""
Name:         SMO_GC_GetItemUniqueName_Cmd.py

Purpose:      This script is designed to:
              Get the Mesh Unique Name of the current mesh item selected.

Author:       Franck ELISABETH
Website:      https://www.smoluck.com
Created:      03/12/2020
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo

Cmd_Name = "smo.GC.GetItemUniqueName"
# smo.GC.GetItemUniqueName ?

# ----------- USE CASE
# TestResult = lx.eval('smo.GC.GetItemUniqueName ?')
# lx.out('current Item Unique name is ',TestResult)
# --------------------


class SMO_GC_GetItemUniqueName_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

        # Store the currently selected item, or if nothing is selected, an empty list.
        # Wrap this is a try except, the initial launching of Modo will cause this function
        # to perform a shallow execution before the scene state is established.
        # The script will still continue to run, but it outputs a stack trace since it failed.
        # So to prevent console spew on launch when this plugin is loaded, we use the try/except.
        try:
            self.current_Selection = lxu.select.ItemSelection().current()
        except:
            self.current_Selection = []

        # If we do have something selected, put it in self.current_Selection
        # Using [-1] will grab the newest item that was added to your selection.
        if len(self.current_Selection) > 0:
            self.current_Selection = self.current_Selection[-1]
        else:
            self.current_Selection = None

        # Test the stored selection list, only if it it not empty, instantiate the variables.
        if self.current_Selection:
            self.dyna_Add("Item Unique Name", lx.symbol.sTYPE_STRING)
            self.basic_SetFlags(0, lx.symbol.fCMDARG_QUERY)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO GC - Get Item Unique Name'

    def cmd_Desc(self):
        return 'Get the Item Unique Name of the current selected item.'

    def cmd_Tooltip(self):
        return 'Get the Item Unique Name of the current selected item.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO GC - Get Item Unique Name'

    def basic_Enable(self, msg):
        # Perform the checks for when the command is supposed to be enabled,
        # so users will be informed the command is unavailable by the button being
        # grayed out.
        # :param msg:
        # :type msg: lx.object.Message
        valid_selection = bool(modo.Scene().selected)
        return valid_selection

    def cmd_Query(self, index, vaQuery):
        if self.current_Selection is not None:
            scene = modo.scene.current()
            # store the Unique name of the current mesh layer
            ItemUniqueName = lx.eval('query layerservice layer.id ? main')
            # lx.out('Item Unique Name:', ItemUniqueName)

            # lx.out ('Result of Query:', ItemUniqueName)
            va = lx.object.ValueArray(vaQuery)
            va.AddString(ItemUniqueName)
            return lx.result.OK

        else:
            return


lx.bless(SMO_GC_GetItemUniqueName_Cmd, Cmd_Name)
