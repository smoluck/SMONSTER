# python
"""
# Name:         SMO_BATCH_LoadFolderFilesFromUserPref_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to:
#               Batch Load Files stored in a Folder and Process the data using User Defined Preferences.
#               Input and Output Files Format are took from User Preferences SMO BATCH Panel
#
#
# Author:       Franck ELISABETH (with the help of James O'Hare)
# Website:      https://www.smoluck.com
#
# Created:      01/10/2020
# Copyright:    (c) Franck Elisabeth 2017-2022
"""

from os import path

import lx
import lxu
import modo
import os
import sys

Cmd_Name = "smo.BATCH.LoadFolderFilesFromUserPref"
# smo.BATCH.LoadFolderFilesFromUserPref


class SMO_BATCH_LoadFolderFilesFromUserPref_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO BATCH - Load Folder Files from User Prefs'

    def cmd_Desc(self):
        return 'Batch Load Files stored in a Folder and Process the data using User Defined Preferences.'

    def cmd_Tooltip(self):
        return 'Batch Load Files stored in a Folder and Process the data using User Defined Preferences.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO BATCH - Load Folder Files from User Prefs'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):

        # ------------------------------ #
        # <----( DEFINE VARIABLES )----> #
        # ------------------------------ #
        lx.eval("user.defNew name:InputFileFormat_DXF type:boolean life:momentary")
        lx.eval("user.defNew name:InputFileFormat_OBJ type:boolean life:momentary")
        lx.eval("user.defNew name:InputFileFormat_LXO type:boolean life:momentary")
        lx.eval("user.defNew name:InputFileFormat_FBX type:boolean life:momentary")
        lx.eval("user.defNew name:InputFileFormat_SLDPRT type:boolean life:momentary")

        lx.eval("user.defNew name:OutputFileFormat_DXF type:boolean life:momentary")
        lx.eval("user.defNew name:OutputFileFormat_OBJ type:boolean life:momentary")
        lx.eval("user.defNew name:OutputFileFormat_LXO type:boolean life:momentary")
        lx.eval("user.defNew name:OutputFileFormat_FBX type:boolean life:momentary")
        lx.eval("user.defNew name:OutputFileFormat_SLDPRT type:boolean life:momentary")

        lx.eval("user.defNew name:InputFileFormatTotal type:integer life:momentary")
        lx.eval("user.defNew name:OutputFileFormatTotal type:integer life:momentary")

        lx.eval("user.defNew name:InputFileFormat type:string life:momentary")
        lx.eval("user.defNew name:OutputFileFormat type:string life:momentary")

        lx.eval("user.defNew name:Target_Path type:string life:momentary")

        lx.eval("user.defNew name:MergeExistItems type:boolean life:momentary")
        lx.eval("user.defNew name:LoadGeo type:boolean life:momentary")
        lx.eval("user.defNew name:LoadNormals type:boolean life:momentary")
        lx.eval("user.defNew name:LoadMeshSmoothness type:boolean life:momentary")
        lx.eval("user.defNew name:LoadMorphs type:boolean life:momentary")
        lx.eval("user.defNew name:LoadParts type:boolean life:momentary")
        lx.eval("user.defNew name:LoadSelSets type:boolean life:momentary")
        lx.eval("user.defNew name:LoadMats type:boolean life:momentary")
        lx.eval("user.defNew name:InvertMatTransp type:boolean life:momentary")

        lx.eval("user.defNew name:BPLine001 type:string life:momentary")
        lx.eval("user.defNew name:BPLine002 type:string life:momentary")
        lx.eval("user.defNew name:BPLine003 type:string life:momentary")
        lx.eval("user.defNew name:BPLine004 type:string life:momentary")
        lx.eval("user.defNew name:BPLine005 type:string life:momentary")
        lx.eval("user.defNew name:BPLine006 type:string life:momentary")
        lx.eval("user.defNew name:BPLine007 type:string life:momentary")
        lx.eval("user.defNew name:BPLine008 type:string life:momentary")
        lx.eval("user.defNew name:BPLine009 type:string life:momentary")
        lx.eval("user.defNew name:BPLine010 type:string life:momentary")
        lx.eval("user.defNew name:BPLine011 type:string life:momentary")
        lx.eval("user.defNew name:BPLine012 type:string life:momentary")
        lx.eval("user.defNew name:BPLine013 type:string life:momentary")
        lx.eval("user.defNew name:BPLine014 type:string life:momentary")
        lx.eval("user.defNew name:BPLine015 type:string life:momentary")
        lx.eval("user.defNew name:BPLine016 type:string life:momentary")
        lx.eval("user.defNew name:BPLine017 type:string life:momentary")
        lx.eval("user.defNew name:BPLine018 type:string life:momentary")
        lx.eval("user.defNew name:BPLine019 type:string life:momentary")
        lx.eval("user.defNew name:BPLine020 type:string life:momentary")
        # ------------------------------ #

        OutputFileFormat = ""

        ###########################################################################################
        # Get Current Checkbox state for Input File format from Preferences / SMO_BATCH
        ###########################################################################################
        OutputLXO_ConvertStaticMeshes = lx.eval('user.value SMO_UseVal_BATCH_ConvertToStaticMeshes ?')
        lx.out('Output LXO: Convert Meshes to Static Meshes State', OutputLXO_ConvertStaticMeshes)

        InputFileFormat_DXF = lx.eval('user.value SMO_UseVal_BATCH_InputFiles_DXF ?')
        lx.out('Input File Format DXF State:', InputFileFormat_DXF)

        InputFileFormat_SVG = lx.eval('user.value SMO_UseVal_BATCH_InputFiles_SVG ?')
        lx.out('Input File Format SVG State:', InputFileFormat_SVG)

        InputFileFormat_OBJ = lx.eval('user.value SMO_UseVal_BATCH_InputFiles_OBJ ?')
        lx.out('Input File Format OBJ State:', InputFileFormat_OBJ)

        InputFileFormat_LXO = lx.eval('user.value SMO_UseVal_BATCH_InputFiles_LXO ?')
        lx.out('Input File Format LXO State:', InputFileFormat_LXO)

        InputFileFormat_FBX = lx.eval('user.value SMO_UseVal_BATCH_InputFiles_FBX ?')
        lx.out('Input File Format FBX State:', InputFileFormat_FBX)

        InputFileFormat_SLDPRT = lx.eval('user.value SMO_UseVal_BATCH_InputFiles_SLDPRT ?')
        lx.out('Input File Format SLDPRT State:', InputFileFormat_SLDPRT)

        # Get Current Checkbox state for Output File format from Preferences / SMO_BATCH
        OutputFileFormat_DXF = lx.eval('user.value SMO_UseVal_BATCH_OutputFiles_DXF ?')
        lx.out('Output File Format DXF State:', OutputFileFormat_DXF)

        OutputFileFormat_SVG = lx.eval('user.value SMO_UseVal_BATCH_OutputFiles_SVG ?')
        lx.out('Output File Format SVG State:', OutputFileFormat_SVG)

        OutputFileFormat_OBJ = lx.eval('user.value SMO_UseVal_BATCH_OutputFiles_OBJ ?')
        lx.out('Output File Format OBJ State:', OutputFileFormat_OBJ)

        OutputFileFormat_LXO = lx.eval('user.value SMO_UseVal_BATCH_OutputFiles_LXO ?')
        lx.out('Output File Format LXO State:', OutputFileFormat_LXO)

        OutputFileFormat_FBX = lx.eval('user.value SMO_UseVal_BATCH_OutputFiles_FBX ?')
        lx.out('Output File Format FBX State:', OutputFileFormat_FBX)

        # Test Current Checkbox state for Input File format from Preferences / SMO_BATCH
        InputFileFormatTotal = InputFileFormat_DXF + InputFileFormat_SVG + InputFileFormat_OBJ + InputFileFormat_LXO + InputFileFormat_FBX + InputFileFormat_SLDPRT
        # if InputFileFormatTotal != 1:
        #     sys(exit)

        if InputFileFormat_DXF == 1 and InputFileFormatTotal == 1:
            InputFileFormat = "DXF"

        if InputFileFormat_SVG == 1 and InputFileFormatTotal == 1:
            InputFileFormat = "SVG"

        if InputFileFormat_OBJ == 1 and InputFileFormatTotal == 1:
            InputFileFormat = "OBJ"

        if InputFileFormat_LXO == 1 and InputFileFormatTotal == 1:
            InputFileFormat = "LXO"

        if InputFileFormat_FBX == 1 and InputFileFormatTotal == 1:
            InputFileFormat = "FBX"

        if InputFileFormat_SLDPRT == 1 and InputFileFormatTotal == 1:
            InputFileFormat = "SLDPRT"

        # Test Current Checkbox state for Output File format from Preferences / SMO_BATCH
        OutputFileFormatTotal = OutputFileFormat_DXF + OutputFileFormat_SVG + OutputFileFormat_OBJ + OutputFileFormat_LXO + OutputFileFormat_FBX
        # if OutputFileFormatTotal != 1:
        #     sys(exit)

        if OutputFileFormatTotal == 1:
            if OutputFileFormat_DXF == 1:
                OutputFileFormat = "DXF"

            if OutputFileFormat_SVG == 1:
                OutputFileFormat = "SVG"

            if OutputFileFormat_OBJ == 1:
                OutputFileFormat = "OBJ"

            if OutputFileFormat_LXO == 1:
                OutputFileFormat = "LXO"

            if OutputFileFormat_FBX == 1:
                OutputFileFormat = "FBX"

        ###########################################################################################

        ###########################################################################################
        # Get Code lines from Preferences / SMO_BATCH
        ###########################################################################################
        BPLine001 = lx.eval('user.value SMO_UseVal_BATCH_String_Line001 ?')
        lx.out('Batch Process Line 1:', BPLine001)
        BPLine002 = lx.eval('user.value SMO_UseVal_BATCH_String_Line002 ?')
        lx.out('Batch Process Line 2:', BPLine002)
        BPLine003 = lx.eval('user.value SMO_UseVal_BATCH_String_Line003 ?')
        lx.out('Batch Process Line 3:', BPLine003)
        BPLine004 = lx.eval('user.value SMO_UseVal_BATCH_String_Line004 ?')
        lx.out('Batch Process Line 4:', BPLine004)
        BPLine005 = lx.eval('user.value SMO_UseVal_BATCH_String_Line005 ?')
        lx.out('Batch Process Line 5:', BPLine005)
        BPLine006 = lx.eval('user.value SMO_UseVal_BATCH_String_Line006 ?')
        lx.out('Batch Process Line 6:', BPLine006)
        BPLine007 = lx.eval('user.value SMO_UseVal_BATCH_String_Line007 ?')
        lx.out('Batch Process Line 7:', BPLine007)
        BPLine008 = lx.eval('user.value SMO_UseVal_BATCH_String_Line008 ?')
        lx.out('Batch Process Line 8:', BPLine008)
        BPLine009 = lx.eval('user.value SMO_UseVal_BATCH_String_Line009 ?')
        lx.out('Batch Process Line 9:', BPLine009)
        BPLine010 = lx.eval('user.value SMO_UseVal_BATCH_String_Line010 ?')
        lx.out('Batch Process Line 10:', BPLine010)

        BPLine011 = lx.eval('user.value SMO_UseVal_BATCH_String_Line011 ?')
        lx.out('Batch Process Line 11:', BPLine011)
        BPLine012 = lx.eval('user.value SMO_UseVal_BATCH_String_Line012 ?')
        lx.out('Batch Process Line 12:', BPLine012)
        BPLine013 = lx.eval('user.value SMO_UseVal_BATCH_String_Line013 ?')
        lx.out('Batch Process Line 13:', BPLine013)
        BPLine014 = lx.eval('user.value SMO_UseVal_BATCH_String_Line014 ?')
        lx.out('Batch Process Line 14:', BPLine014)
        BPLine015 = lx.eval('user.value SMO_UseVal_BATCH_String_Line015 ?')
        lx.out('Batch Process Line 15:', BPLine015)
        BPLine016 = lx.eval('user.value SMO_UseVal_BATCH_String_Line016 ?')
        lx.out('Batch Process Line 16:', BPLine016)
        BPLine017 = lx.eval('user.value SMO_UseVal_BATCH_String_Line017 ?')
        lx.out('Batch Process Line 17:', BPLine017)
        BPLine018 = lx.eval('user.value SMO_UseVal_BATCH_String_Line018 ?')
        lx.out('Batch Process Line 18:', BPLine018)
        BPLine019 = lx.eval('user.value SMO_UseVal_BATCH_String_Line019 ?')
        lx.out('Batch Process Line 19:', BPLine019)
        BPLine020 = lx.eval('user.value SMO_UseVal_BATCH_String_Line020 ?')
        lx.out('Batch Process Line 20:', BPLine020)

        if len(BPLine001) == 0:
            lx.out('NOTIFICATION: line 001 Empty')
        if len(BPLine002) == 0:
            lx.out('NOTIFICATION: line 002 Empty')
        if len(BPLine003) == 0:
            lx.out('NOTIFICATION: line 003 Empty')
        if len(BPLine004) == 0:
            lx.out('NOTIFICATION: line 004 Empty')
        if len(BPLine005) == 0:
            lx.out('NOTIFICATION: line 005 Empty')
        if len(BPLine006) == 0:
            lx.out('NOTIFICATION: line 006 Empty')
        if len(BPLine007) == 0:
            lx.out('NOTIFICATION: line 007 Empty')
        if len(BPLine008) == 0:
            lx.out('NOTIFICATION: line 008 Empty')
        if len(BPLine009) == 0:
            lx.out('NOTIFICATION: line 009 Empty')
        if len(BPLine010) == 0:
            lx.out('NOTIFICATION: line 010 Empty')

        if len(BPLine011) == 0:
            lx.out('NOTIFICATION: line 011 Empty')
        if len(BPLine012) == 0:
            lx.out('NOTIFICATION: line 012 Empty')
        if len(BPLine013) == 0:
            lx.out('NOTIFICATION: line 013 Empty')
        if len(BPLine014) == 0:
            lx.out('NOTIFICATION: line 014 Empty')
        if len(BPLine015) == 0:
            lx.out('NOTIFICATION: line 015 Empty')
        if len(BPLine016) == 0:
            lx.out('NOTIFICATION: line 016 Empty')
        if len(BPLine017) == 0:
            lx.out('NOTIFICATION: line 017 Empty')
        if len(BPLine018) == 0:
            lx.out('NOTIFICATION: line 018 Empty')
        if len(BPLine019) == 0:
            lx.out('NOTIFICATION: line 019 Empty')
        if len(BPLine020) == 0:
            lx.out('NOTIFICATION: line 020 Empty')

        if len(BPLine001) != 0:
            lx.out('NOTIFICATION: line 001 Used')
        if len(BPLine002) != 0:
            lx.out('NOTIFICATION: line 002 Used')
        if len(BPLine003) != 0:
            lx.out('NOTIFICATION: line 003 Used')
        if len(BPLine004) != 0:
            lx.out('NOTIFICATION: line 004 Used')
        if len(BPLine005) != 0:
            lx.out('NOTIFICATION: line 005 Used')
        if len(BPLine006) != 0:
            lx.out('NOTIFICATION: line 006 Used')
        if len(BPLine007) != 0:
            lx.out('NOTIFICATION: line 007 Used')
        if len(BPLine008) != 0:
            lx.out('NOTIFICATION: line 008 Used')
        if len(BPLine009) != 0:
            lx.out('NOTIFICATION: line 009 Used')
        if len(BPLine010) != 0:
            lx.out('NOTIFICATION: line 010 Used')

        if len(BPLine011) != 0:
            lx.out('NOTIFICATION: line 011 Used')
        if len(BPLine012) != 0:
            lx.out('NOTIFICATION: line 012 Used')
        if len(BPLine013) != 0:
            lx.out('NOTIFICATION: line 013 Used')
        if len(BPLine014) != 0:
            lx.out('NOTIFICATION: line 014 Used')
        if len(BPLine015) != 0:
            lx.out('NOTIFICATION: line 015 Used')
        if len(BPLine016) != 0:
            lx.out('NOTIFICATION: line 016 Used')
        if len(BPLine017) != 0:
            lx.out('NOTIFICATION: line 017 Used')
        if len(BPLine018) != 0:
            lx.out('NOTIFICATION: line 018 Used')
        if len(BPLine019) != 0:
            lx.out('NOTIFICATION: line 019 Used')
        if len(BPLine020) != 0:
            lx.out('NOTIFICATION: line 020 Used')

        ###########################################################################################

        ###########################################################################################
        # Open the Dialog window to get the Target Path
        ###########################################################################################
        lx.eval('dialog.setup dir')
        lx.eval('dialog.title "Select the target Folder to Analyse and Process"')
        # MODO version checks.
        modo_ver = int(lx.eval('query platformservice appversion ?'))
        if modo_ver == 801:
            lx.eval('+dialog.open')
        else:
            lx.eval('dialog.open')
        Target_Path = lx.eval('dialog.result ?')
        lx.out('Path', Target_Path)
        ###########################################################################################

        ###########################################################################################
        # Open DXF Files
        ###########################################################################################
        if InputFileFormat == "DXF":
            DXFPathList = []
            CurratedDXFPathList = []
            for dxf in os.listdir(Target_Path):
                # if '.fbx' in fbx.lower():                     this one will accept .Fbx .FBx .fbX, etc, because it's case insensitive
                if ".dxf" in dxf or ".DXF" in dxf:  # this one will only accept .fbx or .FBX exactly
                    finalPath = Target_Path + "/" + dxf
                    # print(finalPath)
                    finalPath_AbsPath = os.path.abspath(finalPath)
                    # print(finalPath_AbsPath)
                    DXFPathList.append(finalPath_AbsPath)

            for item in DXFPathList:
                FileSize = os.path.getsize(item)
                # print(FileSize)
                if FileSize > 128:
                    # print(item)
                    # print('File Not Empty')
                    CurratedDXFPathList.append(item)
                if FileSize <= 128:
                    print('File Considered Empty')

            if len(CurratedDXFPathList) > 0:
                for item in CurratedDXFPathList:
                    lx.eval("!!scene.open {%s} normal" % item)
                    # lx.eval("!!scene.open {%s} import" % finalPath)

                    scene = modo.Scene()
                    FullScenePath = scene.filename
                    # lx.out('Scene Full Path:', FullScenePath)
                    SceneName = path.splitext(path.basename(scene.filename))[0]
                    lx.out('Currently Opened Scene:', SceneName)

                    if len(BPLine001) != 0:
                        try:
                            lx.eval('%s' % BPLine001)
                        except:
                            lx.out('ERROR: Impossible to run line 001')
                    if len(BPLine001) == 0:
                        lx.out('NOTIFICATION: line 001 Empty')

                    if len(BPLine002) != 0:
                        try:
                            lx.eval('%s' % BPLine002)
                        except:
                            lx.out('ERROR: Impossible to run line 002')
                    if len(BPLine002) == 0:
                        lx.out('NOTIFICATION: line 002 Empty')

                    if len(BPLine003) != 0:
                        try:
                            lx.eval('%s' % BPLine003)
                        except:
                            lx.out('ERROR: Impossible to run line 003')
                    if len(BPLine003) == 0:
                        lx.out('NOTIFICATION: line 003 Empty')

                    if len(BPLine004) != 0:
                        try:
                            lx.eval('%s' % BPLine004)
                        except:
                            lx.out('ERROR: Impossible to run line 004')
                    if len(BPLine004) == 0:
                        lx.out('NOTIFICATION: line 004 Empty')

                    if len(BPLine005) != 0:
                        try:
                            lx.eval('%s' % BPLine005)
                        except:
                            lx.out('ERROR: Impossible to run line 005')
                    if len(BPLine005) == 0:
                        lx.out('NOTIFICATION: line 005 Empty')

                    if len(BPLine006) != 0:
                        try:
                            lx.eval('%s' % BPLine006)
                        except:
                            lx.out('ERROR: Impossible to run line 006')
                    if len(BPLine006) == 0:
                        lx.out('NOTIFICATION: line 006 Empty')

                    if len(BPLine007) != 0:
                        try:
                            lx.eval('%s' % BPLine007)
                        except:
                            lx.out('ERROR: Impossible to run line 007')
                    if len(BPLine007) == 0:
                        lx.out('NOTIFICATION: line 007 Empty')

                    if len(BPLine008) != 0:
                        try:
                            lx.eval('%s' % BPLine008)
                        except:
                            lx.out('ERROR: Impossible to run line 008')
                    if len(BPLine008) == 0:
                        lx.out('NOTIFICATION: line 008 Empty')

                    if len(BPLine009) != 0:
                        try:
                            lx.eval('%s' % BPLine009)
                        except:
                            lx.out('ERROR: Impossible to run line 009')
                    if len(BPLine009) == 0:
                        lx.out('NOTIFICATION: line 009 Empty')

                    if len(BPLine010) != 0:
                        try:
                            lx.eval('%s' % BPLine010)
                        except:
                            lx.out('ERROR: Impossible to run line 010')
                    if len(BPLine010) == 0:
                        lx.out('NOTIFICATION: line 010 Empty')

                    if len(BPLine011) != 0:
                        try:
                            lx.eval('%s' % BPLine011)
                        except:
                            lx.out('ERROR: Impossible to run line 011')
                    if len(BPLine011) == 0:
                        lx.out('NOTIFICATION: line 011 Empty')

                    if len(BPLine012) != 0:
                        try:
                            lx.eval('%s' % BPLine012)
                        except:
                            lx.out('ERROR: Impossible to run line 012')
                    if len(BPLine012) == 0:
                        lx.out('NOTIFICATION: line 012 Empty')

                    if len(BPLine013) != 0:
                        try:
                            lx.eval('%s' % BPLine013)
                        except:
                            lx.out('ERROR: Impossible to run line 013')
                    if len(BPLine013) == 0:
                        lx.out('NOTIFICATION: line 013 Empty')

                    if len(BPLine014) != 0:
                        try:
                            lx.eval('%s' % BPLine014)
                        except:
                            lx.out('ERROR: Impossible to run line 014')
                    if len(BPLine014) == 0:
                        lx.out('NOTIFICATION: line 014 Empty')

                    if len(BPLine015) != 0:
                        try:
                            lx.eval('%s' % BPLine015)
                        except:
                            lx.out('ERROR: Impossible to run line 015')
                    if len(BPLine015) == 0:
                        lx.out('NOTIFICATION: line 015 Empty')

                    if len(BPLine016) != 0:
                        try:
                            lx.eval('%s' % BPLine016)
                        except:
                            lx.out('ERROR: Impossible to run line 016')
                    if len(BPLine016) == 0:
                        lx.out('NOTIFICATION: line 016 Empty')

                    if len(BPLine017) != 0:
                        try:
                            lx.eval('%s' % BPLine017)
                        except:
                            lx.out('ERROR: Impossible to run line 017')
                    if len(BPLine017) == 0:
                        lx.out('NOTIFICATION: line 017 Empty')

                    if len(BPLine018) != 0:
                        try:
                            lx.eval('%s' % BPLine018)
                        except:
                            lx.out('ERROR: Impossible to run line 018')
                    if len(BPLine018) == 0:
                        lx.out('NOTIFICATION: line 018 Empty')

                    if len(BPLine019) != 0:
                        try:
                            lx.eval('%s' % BPLine019)
                        except:
                            lx.out('ERROR: Impossible to run line 019')
                    if len(BPLine019) == 0:
                        lx.out('NOTIFICATION: line 019 Empty')

                    if len(BPLine020) != 0:
                        try:
                            lx.eval('%s' % BPLine020)
                        except:
                            lx.out('ERROR: Impossible to run line 020')
                    if len(BPLine020) == 0:
                        lx.out('NOTIFICATION: line 020 Empty')

                    # Converting Meshes to Static Meshes
                    if OutputLXO_ConvertStaticMeshes == True and OutputFileFormat_LXO == 1:
                        lx.eval('smo.CLEANUP.DelEmptyMeshItem')
                        lx.eval('smo.CLEANUP.DelCam')
                        lx.eval('smo.CLEANUP.DelLight')
                        lx.eval('select.itemType mesh')
                        lx.eval('item.setType triSurf locator')

                    # lx.eval('smo.GC.ConvertSceneTo 1 LXO')
                    # lx.eval('smo.GC.ConvertSceneTo 1 DXF')
                    # lx.eval('smo.GC.ConvertSceneTo 1 SVG')
                    # lx.eval('smo.GC.ConvertSceneTo 1 OBJ')
                    # lx.eval('smo.GC.ConvertSceneTo 1 FBX')
                    lx.eval('smo.GC.ConvertSceneTo 1 %s' % OutputFileFormat)
                    lx.eval('!scene.close')
                    lx.out('Scene Closed')

            del (DXFPathList, CurratedDXFPathList)

        ###########################################################################################
        # Open SVG Files
        ###########################################################################################
        if InputFileFormat == "SVG":
            SVGPathList = []
            CurratedSVGPathList = []
            for svg in os.listdir(Target_Path):
                # if '.svg' in svg.lower():                     this one will accept .Svg .SVg .svG, etc, because it's case insensitive
                if ".svg" in svg or ".SVG" in svg:  # this one will only accept .svg or .SVG exactly
                    finalPath = Target_Path + "/" + svg
                    # print(finalPath)
                    finalPath_AbsPath = os.path.abspath(finalPath)
                    # print(finalPath_AbsPath)
                    SVGPathList.append(finalPath_AbsPath)

            for item in SVGPathList:
                FileSize = os.path.getsize(item)
                # print(FileSize)
                if FileSize > 128:
                    # print(item)
                    # print('File Not Empty')
                    CurratedSVGPathList.append(item)
                if FileSize <= 128:
                    print('File Considered Empty')

            if len(CurratedSVGPathList) > 0:
                for item in CurratedSVGPathList:
                    lx.eval("!!scene.open {%s} normal" % item)
                    # lx.eval("!!scene.open {%s} import" % finalPath)

                    scene = modo.Scene()
                    FullScenePath = scene.filename
                    # lx.out('Scene Full Path:', FullScenePath)
                    SceneName = path.splitext(path.basename(scene.filename))[0]
                    lx.out('Currently Opened Scene:', SceneName)

                    if len(BPLine001) != 0:
                        try:
                            lx.eval('%s' % BPLine001)
                        except:
                            lx.out('ERROR: Impossible to run line 001')
                    if len(BPLine001) == 0:
                        lx.out('NOTIFICATION: line 001 Empty')

                    if len(BPLine002) != 0:
                        try:
                            lx.eval('%s' % BPLine002)
                        except:
                            lx.out('ERROR: Impossible to run line 002')
                    if len(BPLine002) == 0:
                        lx.out('NOTIFICATION: line 002 Empty')

                    if len(BPLine003) != 0:
                        try:
                            lx.eval('%s' % BPLine003)
                        except:
                            lx.out('ERROR: Impossible to run line 003')
                    if len(BPLine003) == 0:
                        lx.out('NOTIFICATION: line 003 Empty')

                    if len(BPLine004) != 0:
                        try:
                            lx.eval('%s' % BPLine004)
                        except:
                            lx.out('ERROR: Impossible to run line 004')
                    if len(BPLine004) == 0:
                        lx.out('NOTIFICATION: line 004 Empty')

                    if len(BPLine005) != 0:
                        try:
                            lx.eval('%s' % BPLine005)
                        except:
                            lx.out('ERROR: Impossible to run line 005')
                    if len(BPLine005) == 0:
                        lx.out('NOTIFICATION: line 005 Empty')

                    if len(BPLine006) != 0:
                        try:
                            lx.eval('%s' % BPLine006)
                        except:
                            lx.out('ERROR: Impossible to run line 006')
                    if len(BPLine006) == 0:
                        lx.out('NOTIFICATION: line 006 Empty')

                    if len(BPLine007) != 0:
                        try:
                            lx.eval('%s' % BPLine007)
                        except:
                            lx.out('ERROR: Impossible to run line 007')
                    if len(BPLine007) == 0:
                        lx.out('NOTIFICATION: line 007 Empty')

                    if len(BPLine008) != 0:
                        try:
                            lx.eval('%s' % BPLine008)
                        except:
                            lx.out('ERROR: Impossible to run line 008')
                    if len(BPLine008) == 0:
                        lx.out('NOTIFICATION: line 008 Empty')

                    if len(BPLine009) != 0:
                        try:
                            lx.eval('%s' % BPLine009)
                        except:
                            lx.out('ERROR: Impossible to run line 009')
                    if len(BPLine009) == 0:
                        lx.out('NOTIFICATION: line 009 Empty')

                    if len(BPLine010) != 0:
                        try:
                            lx.eval('%s' % BPLine010)
                        except:
                            lx.out('ERROR: Impossible to run line 010')
                    if len(BPLine010) == 0:
                        lx.out('NOTIFICATION: line 010 Empty')

                    if len(BPLine011) != 0:
                        try:
                            lx.eval('%s' % BPLine011)
                        except:
                            lx.out('ERROR: Impossible to run line 011')
                    if len(BPLine011) == 0:
                        lx.out('NOTIFICATION: line 011 Empty')

                    if len(BPLine012) != 0:
                        try:
                            lx.eval('%s' % BPLine012)
                        except:
                            lx.out('ERROR: Impossible to run line 012')
                    if len(BPLine012) == 0:
                        lx.out('NOTIFICATION: line 012 Empty')

                    if len(BPLine013) != 0:
                        try:
                            lx.eval('%s' % BPLine013)
                        except:
                            lx.out('ERROR: Impossible to run line 013')
                    if len(BPLine013) == 0:
                        lx.out('NOTIFICATION: line 013 Empty')

                    if len(BPLine014) != 0:
                        try:
                            lx.eval('%s' % BPLine014)
                        except:
                            lx.out('ERROR: Impossible to run line 014')
                    if len(BPLine014) == 0:
                        lx.out('NOTIFICATION: line 014 Empty')

                    if len(BPLine015) != 0:
                        try:
                            lx.eval('%s' % BPLine015)
                        except:
                            lx.out('ERROR: Impossible to run line 015')
                    if len(BPLine015) == 0:
                        lx.out('NOTIFICATION: line 015 Empty')

                    if len(BPLine016) != 0:
                        try:
                            lx.eval('%s' % BPLine016)
                        except:
                            lx.out('ERROR: Impossible to run line 016')
                    if len(BPLine016) == 0:
                        lx.out('NOTIFICATION: line 016 Empty')

                    if len(BPLine017) != 0:
                        try:
                            lx.eval('%s' % BPLine017)
                        except:
                            lx.out('ERROR: Impossible to run line 017')
                    if len(BPLine017) == 0:
                        lx.out('NOTIFICATION: line 017 Empty')

                    if len(BPLine018) != 0:
                        try:
                            lx.eval('%s' % BPLine018)
                        except:
                            lx.out('ERROR: Impossible to run line 018')
                    if len(BPLine018) == 0:
                        lx.out('NOTIFICATION: line 018 Empty')

                    if len(BPLine019) != 0:
                        try:
                            lx.eval('%s' % BPLine019)
                        except:
                            lx.out('ERROR: Impossible to run line 019')
                    if len(BPLine019) == 0:
                        lx.out('NOTIFICATION: line 019 Empty')

                    if len(BPLine020) != 0:
                        try:
                            lx.eval('%s' % BPLine020)
                        except:
                            lx.out('ERROR: Impossible to run line 020')
                    if len(BPLine020) == 0:
                        lx.out('NOTIFICATION: line 020 Empty')

                    # Converting Meshes to Static Meshes
                    if OutputLXO_ConvertStaticMeshes == True and OutputFileFormat_LXO == 1:
                        lx.eval('smo.CLEANUP.DelEmptyMeshItem')
                        lx.eval('smo.CLEANUP.DelCam')
                        lx.eval('smo.CLEANUP.DelLight')
                        lx.eval('select.itemType mesh')
                        lx.eval('item.setType triSurf locator')

                    # lx.eval('smo.GC.ConvertSceneTo 1 LXO')
                    # lx.eval('smo.GC.ConvertSceneTo 1 DXF')
                    # lx.eval('smo.GC.ConvertSceneTo 1 SVG')
                    # lx.eval('smo.GC.ConvertSceneTo 1 OBJ')
                    # lx.eval('smo.GC.ConvertSceneTo 1 FBX')
                    lx.eval('smo.GC.ConvertSceneTo 1 %s' % OutputFileFormat)
                    lx.eval('!scene.close')
                    lx.out('Scene Closed')

            del (SVGPathList, CurratedSVGPathList)

        ###########################################################################################
        # Open OBJ Files
        ###########################################################################################
        if InputFileFormat == "OBJ":
            User_OBJImportStatic = lx.eval('user.value sceneio.obj.import.static ?')
            OBJPathList = []
            CurratedOBJPathList = []
            lx.eval('user.value sceneio.obj.import.static false')
            for obj in os.listdir(Target_Path):
                # print(Target_Path)
                # if '.fbx' in fbx.lower():                     this one will accept .Fbx .FBx .fbX, etc, because it's case insensitive
                if ".obj" in obj or ".OBJ" in obj:  # this one will only accept .fbx or .FBX exactly
                    ID = ""
                    finalPath = Target_Path + "/" + obj
                    # print(finalPath)
                    finalPath_AbsPath = os.path.abspath(finalPath)
                    # print(finalPath_AbsPath)
                    OBJPathList.append(finalPath_AbsPath)

            for item in OBJPathList:
                FileSize = os.path.getsize(item)
                # print(FileSize)
                if FileSize > 128:
                    # print(item)
                    # print('File Not Empty')
                    CurratedOBJPathList.append(item)
                if FileSize <= 128:
                    print('File Considered Empty')

            if len(CurratedOBJPathList) > 0:
                for item in CurratedOBJPathList:
                    lx.eval('loaderOptions.wf_OBJ false false false meters')
                    lx.eval('!!scene.open {%s} normal' % item)
                    lx.eval('smo.GC.DeselectAll')
                    #            scenecurrent = modo.scene.current()
                    #            sceneItem = scenecurrent.selectedByType(lx.symbol.sITYPE_SCENE)
                    #            print(sceneItem)
                    #            for item in sceneItem:
                    #                ID = item.Ident()
                    #            print (ID)
                    #            lx.eval('select.subItem %s set scene' % ID)
                    #            lx.eval('item.tag string FILE "{%s}"' % finalPath)
                    # lx.eval("!!scene.open {%s} import" % finalPath)

                    if len(BPLine001) != 0:
                        try:
                            lx.eval('%s' % BPLine001)
                        except:
                            lx.out('ERROR: Impossible to run line 001')
                    if len(BPLine001) == 0:
                        lx.out('NOTIFICATION: line 001 Empty')

                    if len(BPLine002) != 0:
                        try:
                            lx.eval('%s' % BPLine002)
                        except:
                            lx.out('ERROR: Impossible to run line 002')
                    if len(BPLine002) == 0:
                        lx.out('NOTIFICATION: line 002 Empty')

                    if len(BPLine003) != 0:
                        try:
                            lx.eval('%s' % BPLine003)
                        except:
                            lx.out('ERROR: Impossible to run line 003')
                    if len(BPLine003) == 0:
                        lx.out('NOTIFICATION: line 003 Empty')

                    if len(BPLine004) != 0:
                        try:
                            lx.eval('%s' % BPLine004)
                        except:
                            lx.out('ERROR: Impossible to run line 004')
                    if len(BPLine004) == 0:
                        lx.out('NOTIFICATION: line 004 Empty')

                    if len(BPLine005) != 0:
                        try:
                            lx.eval('%s' % BPLine005)
                        except:
                            lx.out('ERROR: Impossible to run line 005')
                    if len(BPLine005) == 0:
                        lx.out('NOTIFICATION: line 005 Empty')

                    if len(BPLine006) != 0:
                        try:
                            lx.eval('%s' % BPLine006)
                        except:
                            lx.out('ERROR: Impossible to run line 006')
                    if len(BPLine006) == 0:
                        lx.out('NOTIFICATION: line 006 Empty')

                    if len(BPLine007) != 0:
                        try:
                            lx.eval('%s' % BPLine007)
                        except:
                            lx.out('ERROR: Impossible to run line 007')
                    if len(BPLine007) == 0:
                        lx.out('NOTIFICATION: line 007 Empty')

                    if len(BPLine008) != 0:
                        try:
                            lx.eval('%s' % BPLine008)
                        except:
                            lx.out('ERROR: Impossible to run line 008')
                    if len(BPLine008) == 0:
                        lx.out('NOTIFICATION: line 008 Empty')

                    if len(BPLine009) != 0:
                        try:
                            lx.eval('%s' % BPLine009)
                        except:
                            lx.out('ERROR: Impossible to run line 009')
                    if len(BPLine009) == 0:
                        lx.out('NOTIFICATION: line 009 Empty')

                    if len(BPLine010) != 0:
                        try:
                            lx.eval('%s' % BPLine010)
                        except:
                            lx.out('ERROR: Impossible to run line 010')
                    if len(BPLine010) == 0:
                        lx.out('NOTIFICATION: line 010 Empty')

                    if len(BPLine011) != 0:
                        try:
                            lx.eval('%s' % BPLine011)
                        except:
                            lx.out('ERROR: Impossible to run line 011')
                    if len(BPLine011) == 0:
                        lx.out('NOTIFICATION: line 011 Empty')

                    if len(BPLine012) != 0:
                        try:
                            lx.eval('%s' % BPLine012)
                        except:
                            lx.out('ERROR: Impossible to run line 012')
                    if len(BPLine012) == 0:
                        lx.out('NOTIFICATION: line 012 Empty')

                    if len(BPLine013) != 0:
                        try:
                            lx.eval('%s' % BPLine013)
                        except:
                            lx.out('ERROR: Impossible to run line 013')
                    if len(BPLine013) == 0:
                        lx.out('NOTIFICATION: line 013 Empty')

                    if len(BPLine014) != 0:
                        try:
                            lx.eval('%s' % BPLine014)
                        except:
                            lx.out('ERROR: Impossible to run line 014')
                    if len(BPLine014) == 0:
                        lx.out('NOTIFICATION: line 014 Empty')

                    if len(BPLine015) != 0:
                        try:
                            lx.eval('%s' % BPLine015)
                        except:
                            lx.out('ERROR: Impossible to run line 015')
                    if len(BPLine015) == 0:
                        lx.out('NOTIFICATION: line 015 Empty')

                    if len(BPLine016) != 0:
                        try:
                            lx.eval('%s' % BPLine016)
                        except:
                            lx.out('ERROR: Impossible to run line 016')
                    if len(BPLine016) == 0:
                        lx.out('NOTIFICATION: line 016 Empty')

                    if len(BPLine017) != 0:
                        try:
                            lx.eval('%s' % BPLine017)
                        except:
                            lx.out('ERROR: Impossible to run line 017')
                    if len(BPLine017) == 0:
                        lx.out('NOTIFICATION: line 017 Empty')

                    if len(BPLine018) != 0:
                        try:
                            lx.eval('%s' % BPLine018)
                        except:
                            lx.out('ERROR: Impossible to run line 018')
                    if len(BPLine018) == 0:
                        lx.out('NOTIFICATION: line 018 Empty')

                    if len(BPLine019) != 0:
                        try:
                            lx.eval('%s' % BPLine019)
                        except:
                            lx.out('ERROR: Impossible to run line 019')
                    if len(BPLine019) == 0:
                        lx.out('NOTIFICATION: line 019 Empty')

                    if len(BPLine020) != 0:
                        try:
                            lx.eval('%s' % BPLine020)
                        except:
                            lx.out('ERROR: Impossible to run line 020')
                    if len(BPLine020) == 0:
                        lx.out('NOTIFICATION: line 020 Empty')

                    # Converting Meshes to Static Meshes
                    if OutputLXO_ConvertStaticMeshes == True and OutputFileFormat_LXO == 1:
                        # print ('Hello')
                        lx.eval('smo.CLEANUP.DelEmptyMeshItem')
                        lx.eval('smo.CLEANUP.DelCam')
                        lx.eval('smo.CLEANUP.DelLight')
                        lx.eval('select.itemType mesh')
                        lx.eval('item.setType triSurf locator')

                    # lx.eval('smo.GC.ConvertSceneTo 1 LXO')
                    # lx.eval('smo.GC.ConvertSceneTo 1 DXF')
                    # lx.eval('smo.GC.ConvertSceneTo 1 SVG')
                    # lx.eval('smo.GC.ConvertSceneTo 1 OBJ')
                    # lx.eval('smo.GC.ConvertSceneTo 1 FBX')
                    # lx.eval('select.subItem %s set scene' % ID)
                    # Destination = lx.eval('item.tag string FILE ?)' % finalPath)
                    lx.eval('smo.GC.DeselectAll')

                    lx.eval('smo.GC.ConvertSceneTo 1 %s' % OutputFileFormat)
                    lx.eval('!scene.close')
                    lx.out('Scene Closed')

            lx.eval('user.value sceneio.obj.import.static {%s}' % User_OBJImportStatic)
            del (OBJPathList, CurratedOBJPathList)

        ###########################################################################################
        # Open FBX Files
        # lx.eval('loaderOptions.fbx false true true true false false true true false false false false false false false FBXAnimSampleRate_x1 1.0 defaultimport')
        ###########################################################################################
        if InputFileFormat == "FBX":
            FBXPathList = []
            CurratedFBXPathList = []
            for fbx in os.listdir(Target_Path):
                # if '.fbx' in fbx.lower():                     this one will accept .Fbx .FBx .fbX, etc, because it's case insensitive
                if ".fbx" in fbx or ".FBX" in fbx:  # this one will only accept .fbx or .FBX exactly
                    finalPath = Target_Path + "/" + fbx
                    # print(finalPath)
                    finalPath_AbsPath = os.path.abspath(finalPath)
                    # print(finalPath_AbsPath)
                    FBXPathList.append(finalPath_AbsPath)

            for item in FBXPathList:
                FileSize = os.path.getsize(item)
                # print(FileSize)
                if FileSize > 128:
                    # print(item)
                    # print('File Not Empty')
                    CurratedFBXPathList.append(item)
                if FileSize <= 128:
                    print('File Considered Empty')

            if len(CurratedFBXPathList) > 0:
                for item in CurratedFBXPathList:
                    # lx.eval('!!loaderOptions.fbx false true true true false false true true false false false false false false false FBXAnimSampleRate_x1 1.0 defaultimport')
                    lx.eval(
                        '!!loaderOptions.fbx mergeWithExistingItems:false loadGeometry:true loadNormals:true loadMeshSmoothing:true loadBlendShapes:false loadPolygonParts:false loadSelectionSets:true loadMaterials:true invertMatTranAmt:false useMatTranColAsTranAmt:false changeTextureEffect:false loadCameras:false loadLights:false loadAnimation:false loadSampleAnimation:false loadSampleAnimationRate:0 globalScalingFactor:1.0 importUnits:0')

                    # MergeExistItems =
                    # LoadGeo =
                    # LoadNormals =
                    # LoadMeshSmoothness =
                    # LoadMorphs =
                    # LoadParts =
                    # LoadSelSets =
                    # LoadMats =
                    # InvertMatTransp =
                    # lx.eval('!!loaderOptions.fbx %s %s %s %s %s %s %s %s %s false false false false false false FBXAnimSampleRate_x1 1.0 defaultimport' % MergeExistItems, % LoadGeo, % LoadNormals, % LoadMeshSmoothness, % LoadMorphs, % LoadParts, % LoadSelSets, % LoadMats, % InvertMatTransp)
                    lx.eval('!!scene.open {%s} normal' % item)
                    # lx.eval("!!scene.open {%s} import" % finalPath)

                    scene = modo.Scene()
                    FullScenePath = scene.filename
                    # lx.out('Scene Full Path:', FullScenePath)
                    SceneName = path.splitext(path.basename(scene.filename))[0]
                    lx.out('Currently Opened Scene:', SceneName)

                    if len(BPLine001) != 0:
                        try:
                            lx.eval('%s' % BPLine001)
                        except:
                            lx.out('ERROR: Impossible to run line 001')
                    if len(BPLine001) == 0:
                        lx.out('NOTIFICATION: line 001 Empty')

                    if len(BPLine002) != 0:
                        try:
                            lx.eval('%s' % BPLine002)
                        except:
                            lx.out('ERROR: Impossible to run line 002')
                    if len(BPLine002) == 0:
                        lx.out('NOTIFICATION: line 002 Empty')

                    if len(BPLine003) != 0:
                        try:
                            lx.eval('%s' % BPLine003)
                        except:
                            lx.out('ERROR: Impossible to run line 003')
                    if len(BPLine003) == 0:
                        lx.out('NOTIFICATION: line 003 Empty')

                    if len(BPLine004) != 0:
                        try:
                            lx.eval('%s' % BPLine004)
                        except:
                            lx.out('ERROR: Impossible to run line 004')
                    if len(BPLine004) == 0:
                        lx.out('NOTIFICATION: line 004 Empty')

                    if len(BPLine005) != 0:
                        try:
                            lx.eval('%s' % BPLine005)
                        except:
                            lx.out('ERROR: Impossible to run line 005')
                    if len(BPLine005) == 0:
                        lx.out('NOTIFICATION: line 005 Empty')

                    if len(BPLine006) != 0:
                        try:
                            lx.eval('%s' % BPLine006)
                        except:
                            lx.out('ERROR: Impossible to run line 006')
                    if len(BPLine006) == 0:
                        lx.out('NOTIFICATION: line 006 Empty')

                    if len(BPLine007) != 0:
                        try:
                            lx.eval('%s' % BPLine007)
                        except:
                            lx.out('ERROR: Impossible to run line 007')
                    if len(BPLine007) == 0:
                        lx.out('NOTIFICATION: line 007 Empty')

                    if len(BPLine008) != 0:
                        try:
                            lx.eval('%s' % BPLine008)
                        except:
                            lx.out('ERROR: Impossible to run line 008')
                    if len(BPLine008) == 0:
                        lx.out('NOTIFICATION: line 008 Empty')

                    if len(BPLine009) != 0:
                        try:
                            lx.eval('%s' % BPLine009)
                        except:
                            lx.out('ERROR: Impossible to run line 009')
                    if len(BPLine009) == 0:
                        lx.out('NOTIFICATION: line 009 Empty')

                    if len(BPLine010) != 0:
                        try:
                            lx.eval('%s' % BPLine010)
                        except:
                            lx.out('ERROR: Impossible to run line 010')
                    if len(BPLine010) == 0:
                        lx.out('NOTIFICATION: line 010 Empty')

                    if len(BPLine011) != 0:
                        try:
                            lx.eval('%s' % BPLine011)
                        except:
                            lx.out('ERROR: Impossible to run line 011')
                    if len(BPLine011) == 0:
                        lx.out('NOTIFICATION: line 011 Empty')

                    if len(BPLine012) != 0:
                        try:
                            lx.eval('%s' % BPLine012)
                        except:
                            lx.out('ERROR: Impossible to run line 012')
                    if len(BPLine012) == 0:
                        lx.out('NOTIFICATION: line 012 Empty')

                    if len(BPLine013) != 0:
                        try:
                            lx.eval('%s' % BPLine013)
                        except:
                            lx.out('ERROR: Impossible to run line 013')
                    if len(BPLine013) == 0:
                        lx.out('NOTIFICATION: line 013 Empty')

                    if len(BPLine014) != 0:
                        try:
                            lx.eval('%s' % BPLine014)
                        except:
                            lx.out('ERROR: Impossible to run line 014')
                    if len(BPLine014) == 0:
                        lx.out('NOTIFICATION: line 014 Empty')

                    if len(BPLine015) != 0:
                        try:
                            lx.eval('%s' % BPLine015)
                        except:
                            lx.out('ERROR: Impossible to run line 015')
                    if len(BPLine015) == 0:
                        lx.out('NOTIFICATION: line 015 Empty')

                    if len(BPLine016) != 0:
                        try:
                            lx.eval('%s' % BPLine016)
                        except:
                            lx.out('ERROR: Impossible to run line 016')
                    if len(BPLine016) == 0:
                        lx.out('NOTIFICATION: line 016 Empty')

                    if len(BPLine017) != 0:
                        try:
                            lx.eval('%s' % BPLine017)
                        except:
                            lx.out('ERROR: Impossible to run line 017')
                    if len(BPLine017) == 0:
                        lx.out('NOTIFICATION: line 017 Empty')

                    if len(BPLine018) != 0:
                        try:
                            lx.eval('%s' % BPLine018)
                        except:
                            lx.out('ERROR: Impossible to run line 018')
                    if len(BPLine018) == 0:
                        lx.out('NOTIFICATION: line 018 Empty')

                    if len(BPLine019) != 0:
                        try:
                            lx.eval('%s' % BPLine019)
                        except:
                            lx.out('ERROR: Impossible to run line 019')
                    if len(BPLine019) == 0:
                        lx.out('NOTIFICATION: line 019 Empty')

                    if len(BPLine020) != 0:
                        try:
                            lx.eval('%s' % BPLine020)
                        except:
                            lx.out('ERROR: Impossible to run line 020')
                    if len(BPLine020) == 0:
                        lx.out('NOTIFICATION: line 020 Empty')

                    # Converting Meshes to Static Meshes
                    if OutputLXO_ConvertStaticMeshes == True and OutputFileFormat_LXO == 1:
                        lx.eval('smo.CLEANUP.DelEmptyMeshItem')
                        lx.eval('smo.CLEANUP.DelCam')
                        lx.eval('smo.CLEANUP.DelLight')
                        lx.eval('select.itemType mesh')
                        lx.eval('item.setType triSurf locator')

                    # lx.eval('smo.GC.ConvertSceneTo 1 LXO')
                    # lx.eval('smo.GC.ConvertSceneTo 1 DXF')
                    # lx.eval('smo.GC.ConvertSceneTo 1 SVG')
                    # lx.eval('smo.GC.ConvertSceneTo 1 OBJ')
                    # lx.eval('smo.GC.ConvertSceneTo 1 FBX')
                    lx.eval('smo.GC.ConvertSceneTo 1 %s' % OutputFileFormat)
                    lx.eval('!scene.close')
                    lx.out('Scene Closed')

            del (FBXPathList, CurratedFBXPathList)

        ###########################################################################################
        # Open LXO Files
        ###########################################################################################
        if InputFileFormat == "LXO":
            LXOPathList = []
            CurratedLXOPathList = []
            for lxo in os.listdir(Target_Path):
                # if '.lxo' in lxo.lower():
                if ".lxo" in lxo or ".LXO" in lxo:  # this one will only accept .fbx or .FBX exactly
                    finalPath = Target_Path + "/" + lxo
                    # print(finalPath)
                    finalPath_AbsPath = os.path.abspath(finalPath)
                    # print(finalPath_AbsPath)
                    LXOPathList.append(finalPath_AbsPath)

            for item in LXOPathList:
                FileSize = os.path.getsize(item)
                print(FileSize)
                if FileSize > 128:
                    # print(item)
                    # print('File Not Empty')
                    CurratedLXOPathList.append(item)
                if FileSize <= 128:
                    print('File Considered Empty')

            if len(CurratedLXOPathList) > 0:
                for item in CurratedLXOPathList:
                    lx.eval("!!scene.open {%s} normal" % item)
                    # lx.eval("!!scene.open {%s} import" % finalPath)

                    scene = modo.Scene()
                    FullScenePath = scene.filename
                    # lx.out('Scene Full Path:', FullScenePath)
                    SceneName = path.splitext(path.basename(scene.filename))[0]
                    lx.out('Currently Opened Scene:', SceneName)

                    if len(BPLine001) != 0:
                        try:
                            lx.eval('%s' % BPLine001)
                        except:
                            lx.out('ERROR: Impossible to run line 001')
                    if len(BPLine001) == 0:
                        lx.out('NOTIFICATION: line 001 Empty')

                    if len(BPLine002) != 0:
                        try:
                            lx.eval('%s' % BPLine002)
                        except:
                            lx.out('ERROR: Impossible to run line 002')
                    if len(BPLine002) == 0:
                        lx.out('NOTIFICATION: line 002 Empty')

                    if len(BPLine003) != 0:
                        try:
                            lx.eval('%s' % BPLine003)
                        except:
                            lx.out('ERROR: Impossible to run line 003')
                    if len(BPLine003) == 0:
                        lx.out('NOTIFICATION: line 003 Empty')

                    if len(BPLine004) != 0:
                        try:
                            lx.eval('%s' % BPLine004)
                        except:
                            lx.out('ERROR: Impossible to run line 004')
                    if len(BPLine004) == 0:
                        lx.out('NOTIFICATION: line 004 Empty')

                    if len(BPLine005) != 0:
                        try:
                            lx.eval('%s' % BPLine005)
                        except:
                            lx.out('ERROR: Impossible to run line 005')
                    if len(BPLine005) == 0:
                        lx.out('NOTIFICATION: line 005 Empty')

                    if len(BPLine006) != 0:
                        try:
                            lx.eval('%s' % BPLine006)
                        except:
                            lx.out('ERROR: Impossible to run line 006')
                    if len(BPLine006) == 0:
                        lx.out('NOTIFICATION: line 006 Empty')

                    if len(BPLine007) != 0:
                        try:
                            lx.eval('%s' % BPLine007)
                        except:
                            lx.out('ERROR: Impossible to run line 007')
                    if len(BPLine007) == 0:
                        lx.out('NOTIFICATION: line 007 Empty')

                    if len(BPLine008) != 0:
                        try:
                            lx.eval('%s' % BPLine008)
                        except:
                            lx.out('ERROR: Impossible to run line 008')
                    if len(BPLine008) == 0:
                        lx.out('NOTIFICATION: line 008 Empty')

                    if len(BPLine009) != 0:
                        try:
                            lx.eval('%s' % BPLine009)
                        except:
                            lx.out('ERROR: Impossible to run line 009')
                    if len(BPLine009) == 0:
                        lx.out('NOTIFICATION: line 009 Empty')

                    if len(BPLine010) != 0:
                        try:
                            lx.eval('%s' % BPLine010)
                        except:
                            lx.out('ERROR: Impossible to run line 010')
                    if len(BPLine010) == 0:
                        lx.out('NOTIFICATION: line 010 Empty')

                    if len(BPLine011) != 0:
                        try:
                            lx.eval('%s' % BPLine011)
                        except:
                            lx.out('ERROR: Impossible to run line 011')
                    if len(BPLine011) == 0:
                        lx.out('NOTIFICATION: line 011 Empty')

                    if len(BPLine012) != 0:
                        try:
                            lx.eval('%s' % BPLine012)
                        except:
                            lx.out('ERROR: Impossible to run line 012')
                    if len(BPLine012) == 0:
                        lx.out('NOTIFICATION: line 012 Empty')

                    if len(BPLine013) != 0:
                        try:
                            lx.eval('%s' % BPLine013)
                        except:
                            lx.out('ERROR: Impossible to run line 013')
                    if len(BPLine013) == 0:
                        lx.out('NOTIFICATION: line 013 Empty')

                    if len(BPLine014) != 0:
                        try:
                            lx.eval('%s' % BPLine014)
                        except:
                            lx.out('ERROR: Impossible to run line 014')
                    if len(BPLine014) == 0:
                        lx.out('NOTIFICATION: line 014 Empty')

                    if len(BPLine015) != 0:
                        try:
                            lx.eval('%s' % BPLine015)
                        except:
                            lx.out('ERROR: Impossible to run line 015')
                    if len(BPLine015) == 0:
                        lx.out('NOTIFICATION: line 015 Empty')

                    if len(BPLine016) != 0:
                        try:
                            lx.eval('%s' % BPLine016)
                        except:
                            lx.out('ERROR: Impossible to run line 016')
                    if len(BPLine016) == 0:
                        lx.out('NOTIFICATION: line 016 Empty')

                    if len(BPLine017) != 0:
                        try:
                            lx.eval('%s' % BPLine017)
                        except:
                            lx.out('ERROR: Impossible to run line 017')
                    if len(BPLine017) == 0:
                        lx.out('NOTIFICATION: line 017 Empty')

                    if len(BPLine018) != 0:
                        try:
                            lx.eval('%s' % BPLine018)
                        except:
                            lx.out('ERROR: Impossible to run line 018')
                    if len(BPLine018) == 0:
                        lx.out('NOTIFICATION: line 018 Empty')

                    if len(BPLine019) != 0:
                        try:
                            lx.eval('%s' % BPLine019)
                        except:
                            lx.out('ERROR: Impossible to run line 019')
                    if len(BPLine019) == 0:
                        lx.out('NOTIFICATION: line 019 Empty')

                    if len(BPLine020) != 0:
                        try:
                            lx.eval('%s' % BPLine020)
                        except:
                            lx.out('ERROR: Impossible to run line 020')
                    if len(BPLine020) == 0:
                        lx.out('NOTIFICATION: line 020 Empty')

                    # Converting Meshes to Static Meshes
                    if OutputLXO_ConvertStaticMeshes:
                        lx.eval('select.itemType mesh')
                        lx.eval('item.setType triSurf locator')

                    # lx.eval('smo.GC.ConvertSceneTo 1 LXO')
                    # lx.eval('smo.GC.ConvertSceneTo 1 DXF')
                    # lx.eval('smo.GC.ConvertSceneTo 1 SVG')
                    # lx.eval('smo.GC.ConvertSceneTo 1 OBJ')
                    # lx.eval('smo.GC.ConvertSceneTo 1 FBX')
                    if OutputFileFormat == "LXO":
                        lx.eval('scene.saveAs {%s} $LXOB false' % finalPath_AbsPath)
                    if OutputFileFormat != "LXO":
                        lx.eval('smo.GC.ConvertSceneTo 1 %s' % OutputFileFormat)
                    lx.eval('!scene.close')
                    lx.out('Scene Closed')

            del (LXOPathList, CurratedLXOPathList)

        ###########################################################################################
        # Open SLDPRT Files
        ###########################################################################################
        if InputFileFormat == "SLDPRT":
            SLDPRTPathList = []
            CurratedSLDPRTPathList = []
            for sldprt in os.listdir(Target_Path):
                if ".sldprt" in sldprt or ".SLDPRT" in sldprt:  # this one will only accept .sldprt or .SLDPRT exactly
                    finalPath = Target_Path + "/" + sldprt
                    # print(finalPath)
                    finalPath_AbsPath = os.path.abspath(finalPath)
                    # print(finalPath_AbsPath)
                    SLDPRTPathList.append(finalPath_AbsPath)

            for item in SLDPRTPathList:
                FileSize = os.path.getsize(item)
                # print(FileSize)
                if FileSize > 128:
                    # print(item)
                    # print('File Not Empty')
                    CurratedSLDPRTPathList.append(item)
                if FileSize <= 128:
                    print('File Considered Empty')

            if len(CurratedSLDPRTPathList) > 0:
                for item in CurratedSLDPRTPathList:
                    lx.eval("!!scene.open {%s} normal" % item)
                    # lx.eval("!!scene.open {%s} import" % finalPath)

                    scene = modo.Scene()
                    FullScenePath = scene.filename
                    # lx.out('Scene Full Path:', FullScenePath)
                    SceneName = path.splitext(path.basename(scene.filename))[0]
                    lx.out('Currently Opened Scene:', SceneName)

                    if len(BPLine001) != 0:
                        try:
                            lx.eval('%s' % BPLine001)
                        except:
                            lx.out('ERROR: Impossible to run line 001')
                    if len(BPLine001) == 0:
                        lx.out('NOTIFICATION: line 001 Empty')

                    if len(BPLine002) != 0:
                        try:
                            lx.eval('%s' % BPLine002)
                        except:
                            lx.out('ERROR: Impossible to run line 002')
                    if len(BPLine002) == 0:
                        lx.out('NOTIFICATION: line 002 Empty')

                    if len(BPLine003) != 0:
                        try:
                            lx.eval('%s' % BPLine003)
                        except:
                            lx.out('ERROR: Impossible to run line 003')
                    if len(BPLine003) == 0:
                        lx.out('NOTIFICATION: line 003 Empty')

                    if len(BPLine004) != 0:
                        try:
                            lx.eval('%s' % BPLine004)
                        except:
                            lx.out('ERROR: Impossible to run line 004')
                    if len(BPLine004) == 0:
                        lx.out('NOTIFICATION: line 004 Empty')

                    if len(BPLine005) != 0:
                        try:
                            lx.eval('%s' % BPLine005)
                        except:
                            lx.out('ERROR: Impossible to run line 005')
                    if len(BPLine005) == 0:
                        lx.out('NOTIFICATION: line 005 Empty')

                    if len(BPLine006) != 0:
                        try:
                            lx.eval('%s' % BPLine006)
                        except:
                            lx.out('ERROR: Impossible to run line 006')
                    if len(BPLine006) == 0:
                        lx.out('NOTIFICATION: line 006 Empty')

                    if len(BPLine007) != 0:
                        try:
                            lx.eval('%s' % BPLine007)
                        except:
                            lx.out('ERROR: Impossible to run line 007')
                    if len(BPLine007) == 0:
                        lx.out('NOTIFICATION: line 007 Empty')

                    if len(BPLine008) != 0:
                        try:
                            lx.eval('%s' % BPLine008)
                        except:
                            lx.out('ERROR: Impossible to run line 008')
                    if len(BPLine008) == 0:
                        lx.out('NOTIFICATION: line 008 Empty')

                    if len(BPLine009) != 0:
                        try:
                            lx.eval('%s' % BPLine009)
                        except:
                            lx.out('ERROR: Impossible to run line 009')
                    if len(BPLine009) == 0:
                        lx.out('NOTIFICATION: line 009 Empty')

                    if len(BPLine010) != 0:
                        try:
                            lx.eval('%s' % BPLine010)
                        except:
                            lx.out('ERROR: Impossible to run line 010')
                    if len(BPLine010) == 0:
                        lx.out('NOTIFICATION: line 010 Empty')

                    if len(BPLine011) != 0:
                        try:
                            lx.eval('%s' % BPLine011)
                        except:
                            lx.out('ERROR: Impossible to run line 011')
                    if len(BPLine011) == 0:
                        lx.out('NOTIFICATION: line 011 Empty')

                    if len(BPLine012) != 0:
                        try:
                            lx.eval('%s' % BPLine012)
                        except:
                            lx.out('ERROR: Impossible to run line 012')
                    if len(BPLine012) == 0:
                        lx.out('NOTIFICATION: line 012 Empty')

                    if len(BPLine013) != 0:
                        try:
                            lx.eval('%s' % BPLine013)
                        except:
                            lx.out('ERROR: Impossible to run line 013')
                    if len(BPLine013) == 0:
                        lx.out('NOTIFICATION: line 013 Empty')

                    if len(BPLine014) != 0:
                        try:
                            lx.eval('%s' % BPLine014)
                        except:
                            lx.out('ERROR: Impossible to run line 014')
                    if len(BPLine014) == 0:
                        lx.out('NOTIFICATION: line 014 Empty')

                    if len(BPLine015) != 0:
                        try:
                            lx.eval('%s' % BPLine015)
                        except:
                            lx.out('ERROR: Impossible to run line 015')
                    if len(BPLine015) == 0:
                        lx.out('NOTIFICATION: line 015 Empty')

                    if len(BPLine016) != 0:
                        try:
                            lx.eval('%s' % BPLine016)
                        except:
                            lx.out('ERROR: Impossible to run line 016')
                    if len(BPLine016) == 0:
                        lx.out('NOTIFICATION: line 016 Empty')

                    if len(BPLine017) != 0:
                        try:
                            lx.eval('%s' % BPLine017)
                        except:
                            lx.out('ERROR: Impossible to run line 017')
                    if len(BPLine017) == 0:
                        lx.out('NOTIFICATION: line 017 Empty')

                    if len(BPLine018) != 0:
                        try:
                            lx.eval('%s' % BPLine018)
                        except:
                            lx.out('ERROR: Impossible to run line 018')
                    if len(BPLine018) == 0:
                        lx.out('NOTIFICATION: line 018 Empty')

                    if len(BPLine019) != 0:
                        try:
                            lx.eval('%s' % BPLine019)
                        except:
                            lx.out('ERROR: Impossible to run line 019')
                    if len(BPLine019) == 0:
                        lx.out('NOTIFICATION: line 019 Empty')

                    if len(BPLine020) != 0:
                        try:
                            lx.eval('%s' % BPLine020)
                        except:
                            lx.out('ERROR: Impossible to run line 020')
                    if len(BPLine020) == 0:
                        lx.out('NOTIFICATION: line 020 Empty')

                    # Converting Meshes to Static Meshes
                    if OutputLXO_ConvertStaticMeshes and OutputFileFormat_LXO == 1:
                        lx.eval('smo.CLEANUP.DelEmptyMeshItem')
                        lx.eval('smo.CLEANUP.DelCam')
                        lx.eval('smo.CLEANUP.DelLight')
                        lx.eval('select.itemType mesh')
                        lx.eval('item.setType triSurf locator')

                    # lx.eval('smo.GC.ConvertSceneTo 1 LXO')
                    # lx.eval('smo.GC.ConvertSceneTo 1 SLDPRT')
                    # lx.eval('smo.GC.ConvertSceneTo 1 SVG')
                    # lx.eval('smo.GC.ConvertSceneTo 1 OBJ')
                    # lx.eval('smo.GC.ConvertSceneTo 1 FBX')
                    lx.eval('smo.GC.ConvertSceneTo 1 %s' % OutputFileFormat)
                    lx.eval('!scene.close')
                    lx.out('Scene Closed')

            del (SLDPRTPathList, CurratedSLDPRTPathList)

    def cmd_Query(self, index, vaQuery):
        lx.notimpl()


lx.bless(SMO_BATCH_LoadFolderFilesFromUserPref_Cmd, Cmd_Name)
