# python
"""
Name:         SMO_GC_SplitEachPolyIndividualy_Cmd.py

Purpose:      This script is designed to
              Separate current Mesh by Polygons.
              It Split each polygon into an individual item.

Author:       Franck ELISABETH (with the help of Tom Dymond for debug)
Website:      https://www.smoluck.com
Created:      17/09/2020
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo

Cmd_Name = "smo.GC.SplitEachPolyIndividualy"
# smo.GC.SplitEachPolyIndividualy 1


class SMO_GC_SplitEachPolyIndividualy_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("Incremental Save Mode", lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags (0, lx.symbol.fCMDARG_OPTIONAL)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact (self):
        pass

    def cmd_UserName (self):
        return 'SMO GC - Split each Polygon Individually'

    def cmd_Desc (self):
        return 'Separate current Mesh by Polygons. It Split each polygon into an individual item.'

    def cmd_Tooltip (self):
        return 'Separate current Mesh by Polygons. It Split each polygon into an individual item.'

    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName (self):
        return 'SMO GC - Split each Polygon Individually'

    def basic_Enable (self, msg):
        return True

    def basic_Execute(self, msg, flags):
        scene = modo.Scene()
        
        Incremental_Save_Mode = self.dyna_Int (0)



        # ---------------- COPY/PASTE Check Procedure ---------------- #
        ## create variables
        lx.eval("user.defNew name:User_Pref_CopyDeselectChangedState type:boolean life:momentary")
        lx.eval("user.defNew name:User_Pref_PasteSelectionChangedState type:boolean life:momentary")
        lx.eval("user.defNew name:User_Pref_PasteDeselectChangedState type:boolean life:momentary")

        lx.eval("user.defNew name:User_Pref_CopyDeselect type:boolean life:momentary")
        lx.eval("user.defNew name:User_Pref_PasteSelection type:boolean life:momentary")
        lx.eval("user.defNew name:User_Pref_PasteDeselect type:boolean life:momentary")
        ###################

        # Look at current Copy / Paste user Preferences:
        User_Pref_CopyDeselect = lx.eval('pref.value application.copyDeSelection ?')
        lx.out('User Pref: Deselect Elements after Copying', User_Pref_CopyDeselect)
        User_Pref_PasteSelection = lx.eval('pref.value application.pasteSelection ?')
        lx.out('User Pref: Select Pasted Elements', User_Pref_PasteSelection)
        User_Pref_PasteDeselect = lx.eval('pref.value application.pasteDeSelection ?')
        lx.out('User Pref: Deselect Elements Before Pasting', User_Pref_PasteDeselect)
        # Is Copy Deselect False ?
        if User_Pref_CopyDeselect == 0:
            lx.eval('pref.value application.copyDeSelection true')
            User_Pref_CopyDeselectChangedState = 1

        # Is Paste Selection False ?
        if User_Pref_PasteSelection == 0:
            lx.eval('pref.value application.pasteSelection true')
            User_Pref_PasteSelectionChangedState = 1

        # Is Paste Deselect False ?
        if User_Pref_PasteDeselect == 0:
            lx.eval('pref.value application.pasteDeSelection true')
            User_Pref_PasteDeselectChangedState = 1

        # Is Copy Deselect True ?
        if User_Pref_CopyDeselect == 1:
            User_Pref_CopyDeselectChangedState = 0

        # Is Paste Selection True ?
        if User_Pref_PasteSelection == 1:
            User_Pref_PasteSelectionChangedState = 0

        # Is Paste Deselect True ?
        if User_Pref_PasteDeselect == 1:
            User_Pref_PasteDeselectChangedState = 0
        # -------------------------------------------- #



        lx.eval('select.type item')
        
        # Get the selected layer.
        TargetMesh = lx.eval('query layerservice layers ? selected')
        #lx.out('Target Mesh Layer:', TargetMesh)
        
        ItemUniqueName = lx.eval('query layerservice layer.id ? main')# store the Unique name of the current mesh layer
        #lx.out('Item Unique Name:', ItemUniqueName)
        
        Target_Name = lx.eval('item.name ? xfrmcore')
        #lx.out('Item Name:', Target_Name)
        
        TotalPoly = lx.eval('query layerservice poly.N ? all')
        #lx.out('Count Selected Poly',TotalPoly)
        
        
        # Create the monitor item
        m = lx.Monitor()
        m.init(1)
        
        MaxSteps = (TotalPoly - 1)
        
        
        for steps in range(MaxSteps) :
            m.step(1)
        
            TotalPolyInMesh = lx.eval('query layerservice poly.N ? all')
            #lx.out('Count Selected Poly',TotalPolyInMesh)
            
            if TotalPoly > 0 :
                lx.eval('select.type polygon')
                lx.eval('select.drop polygon')
                # Select the first polygon.
                lx.eval('select.element layer:%s type:polygon mode:add index:1' % TargetMesh)
                lx.eval('cut')
                lx.eval('layer.new')
                lx.eval('paste')
                lx.eval('select.type item')
                lx.eval('item.name {%s} xfrmcore' % Target_Name)
                lx.eval('select.subItem %s set mesh;replicator;meshInst;camera;light;txtrLocator;backdrop;groupLocator;replicator;surfGen;locator;falloff;deform;locdeform;weightContainer;morphContainer;deformGroup;deformMDD2;ABCStreamingDeformer;morphDeform;itemInfluence;genInfluence;deform.push;deform.wrap;softLag;ABCCurvesDeform.sample;ABCdeform.sample;force.root;baseVolume;chanModify;itemModify;meshoperation;chanEffect;defaultShader;defaultShader 0 0' % ItemUniqueName)
                if Incremental_Save_Mode == 1 :
                    lx.eval('@incSaveEXP.py')



        # -------------- COPY/PASTE END Procedure  -------------- #
        # Restore user Preferences:
        if User_Pref_CopyDeselectChangedState == 1 :
            lx.eval('pref.value application.copyDeSelection false')
            lx.out('"Deselect Elements after Copying" have been Restored')
        if User_Pref_PasteSelectionChangedState == 1 :
            lx.eval('pref.value application.pasteSelection false')
            lx.out('"Select Pasted Elements" have been Restored')
        if User_Pref_PasteDeselectChangedState == 1 :
            lx.eval('pref.value application.pasteDeSelection false')
            lx.out('"Deselect Elements Before Pasting" have been Restored')
        # -------------------------------------------- #
            

    def cmd_Query(self, index, vaQuery):
        lx.notimpl()


lx.bless(SMO_GC_SplitEachPolyIndividualy_Cmd, Cmd_Name)
