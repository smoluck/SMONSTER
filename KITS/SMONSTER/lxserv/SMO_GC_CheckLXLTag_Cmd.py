# python
"""
Name:         SMO_GC_CheckLXLTag_Cmd.py

Purpose:      This script is designed to:
              Check Scene LXLT tag state and give the ability to change the Mesh Preset Tag name.

Author:       Franck ELISABETH
Website:      https://www.linkedin.com/in/smoluck/
Created:      08/11/2021
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo

Cmd_Name = "smo.GC.CheckLXLTag"


class SMO_GC_CheckLXLTag_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Mode", lx.symbol.sTYPE_BOOLEAN)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO GC - Check Scene LXLTag'

    def cmd_Desc(self):
        return 'Check Scene LXLT tag state and give the ability to change the Mesh Preset Tag name.'

    def cmd_Tooltip(self):
        return 'Check Scene LXLT tag state and give the ability to change the Mesh Preset Tag name.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO GC - Check Scene LXLTag'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        Mode = self.dyna_Bool(0)
        
        # define function for Subfolder Name
        def SetLXLTagDialog():
            lx.eval('!user.defNew SubFolderName string momentary')
            lx.eval('user.def SubFolderName username "Set a Subfolder Name for those Presets"')
            lx.eval('user.def SubFolderName dialogname "Set a Subfolder Name for those Presets"')
            try:
                lx.eval('user.value SubFolderName')
                return lx.eval('user.value SubFolderName ?')
            except:
                return ''

        # define function for Specific folder path
        def SetSpecificPathDialog():
            lx.eval('!user.defNew SpecificPath string momentary')
            lx.eval('dialog.setup dir')
            lx.eval('dialog.title "Select a Path to open"')
            lx.eval('dialog.open')
            SpecificPath = lx.eval('dialog.result ?')
            lx.out('Path', SpecificPath)
            try:
                return SpecificPath
            except:
                return ''

        scene = modo.scene.current()
        ItemSelected = scene.selected

        sceneItem = [item for item in scene.items() if item.type == 'scene']
        # print(sceneItem)

        SubFolderState = bool(lx.eval('user.value SMO_UseVal_GC_LXLMeshPresetToSubfolder ?'))
        SpecificFolderState = bool(lx.eval('user.value SMO_UseVal_GC_LXLMeshPresetToSpecificFolder ?'))
        # print (SubFolderState)
        # print (SpecificFolderState)



        lx.eval('smo.GC.DeselectAll')
        for item in sceneItem:
            SceneID = item.Ident()
        # print (SceneID)
        lx.eval('select.subItem %s set scene' % SceneID)

        if Mode:
            LXLTag = lx.eval('item.tag mode:string tag:"LXLT" value:?')
            # print(LXLTag)
            Subfolder = SetLXLTagDialog()
            lx.eval('item.tag mode:string tag:LXLT value:"%s"' % Subfolder)

        if not Mode:
            lx.eval('select.subItem %s set scene' % SceneID)
            LXLTag = lx.eval('item.tagRemove LXLT')
        lx.eval('smo.GC.DeselectAll')


lx.bless(SMO_GC_CheckLXLTag_Cmd, Cmd_Name)
