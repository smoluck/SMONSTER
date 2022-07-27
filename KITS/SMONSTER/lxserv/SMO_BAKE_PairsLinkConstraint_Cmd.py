#python
#---------------------------------------
# Name:         SMO_BAKE_PairsLinkConstraint_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to:
#               Create a Position/Rotation Constraint according to selection order and user preferences. low --> high OR  high --> low.
#
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      06/02/2021
# Copyright:    (c) Franck Elisabeth 2017-2022
#---------------------------------------

import lx, lxu, modo

Cmd_Name = "smo.BAKE.PairsLinkConstraint"
# smo.BAKE.PairsLinkConstraint

class SMO_BAKE_PairsLinkConstraint_Cmd(lxu.command.BasicCommand):
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
        if len(self.current_Selection) == 2 :
            self.current_Selection = self.current_Selection
        else:
            self.current_Selection = None
        
        # Test the stored selection list, only if it it not empty, instantiate the variables.
    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO
    
    def cmd_Interact (self):
        pass
    
    def cmd_UserName (self):
        return 'SMO BAKE - Pairs Link Constraint'
    
    def cmd_Desc (self):
        return 'Create a Position/Rotation Constraint according to selection order and user preferences. low --> high OR  high --> low.'
    
    def cmd_Tooltip (self):
        return 'Create a Position/Rotation Constraint according to selection order and user preferences. low --> high OR  high --> low.'
    
    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'
    
    def basic_ButtonName (self):
        return 'SMO BAKE - Pairs Link Constraint.'
    
    def basic_Enable (self, msg):
        return True
    
    def basic_Execute(self, msg, flags):
        if self.current_Selection is not None:
            scene = modo.scene.current()
            mesh = modo.Mesh()

            Mesh_A = scene.selectedByType('mesh')[0]
            # lx.out('First Mesh:', Mesh_A)

            Mesh_B = scene.selectedByType('mesh')[1]
            # lx.out('Second Mesh:', Mesh_B)

            selitems = len(lx.evalN('query sceneservice selection ? mesh'))
            # lx.out('selitems',selitems)

            sel_items = list(scene.selectedByType("mesh"))


            FirstMeshHighPoly = lx.eval('user.value SMO_UseVal_BAKE_WhenSetBakePairsSelectHighFirst ?')
            # lx.out('Select HighPoly 1st when setting Bake Pairs state:',FirstMeshHighPoly)



            if selitems == 2 :
                lx.eval('select.drop item')
                
                Mesh_A_Name = (Mesh_A.name)
                Mesh_B_Name = (Mesh_B.name)
                # print(Mesh_A.name)
                # print(Mesh_B.name)

                if FirstMeshHighPoly == False :
                    
                    ########################
                    # Select the High Item (constraint) then the Low (.
                    lx.eval('select.subItem %s set mesh 0 0' % Mesh_B_Name)
                    lx.eval('select.subItem %s add mesh 0 0' % Mesh_A_Name)
                    lx.eval('constraintTransform type:pos')
                    lx.eval('select.drop item')

                    lx.eval('select.subItem %s set mesh 0 0' % Mesh_B_Name)
                    lx.eval('select.subItem %s add mesh 0 0' % Mesh_A_Name)
                    lx.eval('constraintTransform type:rot')
                    lx.eval('select.drop item')
                    
                    
                if FirstMeshHighPoly == True :
                    
                    ########################
                    # Select the High Item (constraint) then the Low (.
                    lx.eval('select.subItem %s set mesh 0 0' % Mesh_A_Name)
                    lx.eval('select.subItem %s add mesh 0 0' % Mesh_B_Name)
                    lx.eval('constraintTransform type:pos')
                    lx.eval('select.drop item')

                    lx.eval('select.subItem %s set mesh 0 0' % Mesh_A_Name)
                    lx.eval('select.subItem %s add mesh 0 0' % Mesh_B_Name)
                    lx.eval('constraintTransform type:rot')
                    lx.eval('select.drop item')
                    
                    
    def cmd_Query(self, index, vaQuery):
        lx.notimpl()


lx.bless(SMO_BAKE_PairsLinkConstraint_Cmd, Cmd_Name)
