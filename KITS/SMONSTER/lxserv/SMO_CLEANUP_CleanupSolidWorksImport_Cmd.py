# python
# ---------------------------------------
# Name:         SMO_CLEANUP_CleanupSolidWorksImport_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to:
#               Cleanup SolidWorks Import (from McMaster Website Data) in order to save a new scene with only one Mesh
#               item of the imported asset. It will also convert the VertexNormals Data to HardEdgeWorkflow if needed.
#
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      11/05/2022
# Copyright:    (c) Franck Elisabeth 2017-2022
# ---------------------------------------

import lx, lxu, modo

Command_Name = "smo.CLEANUP.CleanupSolidWorksImport"
# smo.CLEANUP.CleanupSolidWorksImport

class SMO_CLEANUP_CleanupSolidWorksImport_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO CLEANUP CleanupSolidWorksImport'

    def cmd_Desc(self):
        return 'Cleanup SolidWorks Import (from McMaster Website Data) in order to save a new scene with only one Mesh item of the imported asset. It will also convert the VertexNormals Data to HardEdgeWorkflow if needed.'

    def cmd_Tooltip(self):
        return 'Cleanup SolidWorks Import (from McMaster Website Data) in order to save a new scene with only one Mesh item of the imported asset. It will also convert the VertexNormals Data to HardEdgeWorkflow if needed.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO CLEANUP CleanupSolidWorksImport'

    def cmd_Flags(self):
        return lx.symbol.fCMD_UNDO

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        lx.eval('smo.CLEANUP.ConvertAllSolidWorksShape')
        lx.eval('smo.CLEANUP.DelEmptyMeshItem')
        lx.eval('smo.CLEANUP.DelEverythingExceptMeshes')
        lx.eval('smo.CLEANUP.RenameVNrmMapToDefaultSceneWise')
        lx.eval('select.itemType mesh')
        lx.eval('smo.GC.SplitByPart')
        lx.eval('smo.CLEANUP.RemoveAllPartTags')
        lx.eval('select.itemType mesh')
        lx.eval('smo.GC.ConvertToHardEdgeWorkflowUsingGeoBoundaryAsHardEdge 1')
lx.bless(SMO_CLEANUP_CleanupSolidWorksImport_Cmd, Command_Name)