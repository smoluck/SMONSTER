#python
#---------------------------------------
# Name:         SMO_QuickTag_SelectBaseShader_Cmd.py
# Version:      1.00
#
# Purpose:      This script is designed to
#               Select BaseShader Item in current Scene (Assuming there is only one)
#
#
#
# Author:       Franck ELISABETH (with the help of Timothee Yeramian)
# Website:      http://www.smoluck.com
#
# Created:      21/06/2020
# Copyright:    (c) Franck Elisabeth 2017-2022
#---------------------------------------

import lx, lxu, modo

Cmd_Name = "smo.QT.SelectBaseShader"
# smo.QT.SelectBaseShader

class SMO_QT_SelectBaseShaderCmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
    
    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO QT - Select BaseShader'
    
    def cmd_Desc (self):
        return 'Select BaseShader Item in current Scene (Assuming there is only one).'
    
    def cmd_Tooltip (self):
        return 'Select BaseShader Item in current Scene (Assuming there is only one).'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO QT - Select BaseShader'
    
    def basic_Enable (self, msg):
        return True

    def basic_Execute(self, msg, flags):
        scene = modo.Scene()
        SceneBaseShader = []
        SceneBaseShaderName = []
        for item in scene.items(itype='defaultShader', superType=True):
            #lx.out('Default Base Shader found:',item)
            if item.name == "Base Shader":
                # print(item)
                SceneBaseShader.append(item)
                # print(item.id)
                SceneBaseShaderName.append(item.id)
        scene.select(SceneBaseShader[0])
        # print(SceneBaseShaderName)

        del SceneBaseShader
        del SceneBaseShaderName


lx.bless(SMO_QT_SelectBaseShaderCmd, Cmd_Name)
