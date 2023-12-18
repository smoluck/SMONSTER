# python
"""
Name:         SMO_GC_DupAndExplodeByDist_Cmd.py

Purpose:      This script is designed to
              Duplicate the Current Selected Mesh, Rename the mesh with a Suffix "_EXPLODE"
              Create a Relativ e Morph Map called EXPLODE, then Create the Morph Influence out of it
              and Freeze the deformation / delete the motrph map in order to export that to PixaFlux

Author:       Franck ELISABETH (with the help of Tom Dymond for debug)
Website:      https://www.linkedin.com/in/smoluck/
Created:      09/07/2020
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo
import random

Cmd_Name = "smo.GC.DupAndExplodeByDist"
# smo.GC.DupAndExplodeByDist


class SMO_GC_DupAndExplodeByDist_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        #self.dyna_Add("Mode", lx.symbol.sTYPE_INTEGER)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact (self):
        pass

    def cmd_UserName (self):
        return 'SMO GC - Duplicate and Explode by Distance'

    def cmd_Desc (self):
        return 'Duplicate the Current Selected Mesh, Rename the mesh with a Suffix "_EXPLODE" Create a Relativ e Morph Map called EXPLODE, then Create the Morph Influence out of it and Freeze the deformation / delete the motrph map in order to export that to PixaFlux.'

    def cmd_Tooltip (self):
        return 'Duplicate the Current Selected Mesh, Rename the mesh with a Suffix "_EXPLODE" Create a Relativ e Morph Map called EXPLODE, then Create the Morph Influence out of it and Freeze the deformation / delete the motrph map in order to export that to PixaFlux.'

    def cmd_Help (self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName (self):
        return 'SMO GC - Duplicate and Explode by Distance'

    def basic_Enable (self, msg):
        return True

    def basic_Execute(self, msg, flags):
        # mode = self.dyna_Int (0)
        scene = modo.scene.current()
        mesh = scene.selectedByType('mesh')[0]
        selitems = len(lx.evalN('query sceneservice selection ? locator'))
        lx.out('selitems',selitems)
        
        
        
        
        
        # ------------------------------ #
        # <----( DEFINE VARIABLES )----> #
        # ------------------------------ #
        
        
        
        
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
        
        
        
        
        
        
        ##################################################################
        # <----( Main Macro )----> Create the Duplicated Exploded Mesh ##
        ##################################################################
        
        lx.eval('select.type item')
        
        if selitems < 1:
            lx.eval('dialog.setup info')
            lx.eval('dialog.title {SMO DupAndExplodeByDist:}')
            lx.eval('dialog.msg {"You must have a mesh item selected to run this script.}')
            lx.eval('+dialog.open')
            sys.exit()
        
        
        ########
        
        
        ########
        u_sys = lx.eval("pref.value units.system ?")
        lx.out(u_sys)
        u_def = lx.eval("pref.value units.default ?")
        lx.out(u_def)
        
        lx.eval("pref.value units.system si")
        lx.eval("pref.value units.default meters")
        
        ##########
        
        ##########
        
        #Create a user values.  
        lx.eval("user.defNew name:UserValue type:distance life:momentary")
        
        #Set the label name for the popup we're going to call
        lx.eval('user.def UserValue dialogname "SMO Duplicate And Explode By Distance"')
        
        #Set the user names for the values that the users will see
        lx.eval("user.def UserValue username {Explode Range}")
        
        #lx.eval("?user.value UserValue")
        
        #The '?' before the user.value call means we are calling a popup to have the user set the value
        try:
            lx.eval("?user.value UserValue")
            userResponse = lx.eval("dialog.result ?")
            
        except:
            userResponse = lx.eval("dialog.result ?")
            lx.out("Thank you for pressing %s." % userResponse)
            sys.exit()
        
        #Now that the user set the values, we can just query it
        user_input = lx.eval("user.value UserValue ?")
        user_input = float(user_input)
        lx.out('Explode Range', user_input)
        
        
        if selitems >= 1:
            Item_Name = lx.eval('item.name ? xfrmcore')
            lx.out('Item name', Item_Name)
            ExplodeItemName = Item_Name + '_' + 'EXPLODED'
            lx.eval('item.duplicate false locator false true')
            lx.eval('item.name {%s} xfrmcore' % ExplodeItemName)
            lx.eval('select.editSet EXPLODED_MESH add')
        
        
        
        lx.eval('select.type polygon')
        layer = lx.eval('query layerservice layer.index ? main')
        polysN = lx.eval('query layerservice poly.N ? visible') #visible poly count
        lx.out(polysN)
        
        lx.eval('vertMap.new EXPLODED morf true {0.78 0.78 0.78} 1.0')
        
        while polysN != 0:
        
            lx.eval('select.polygon add 0 subdiv 0')
            
            disco_polys = lx.eval('query layerservice polys ? selected')
            disco_polysN = lx.eval('query layerservice poly.N ? selected')
            #lx.out('polys:',disco_polys,'count:',disco_polysN)
            
            #randomly choose a poly
            Rand_Polys = random.sample(disco_polys, 1)
            #lx.out('Rand_Polys:',Rand_Polys)
            
            #random transform values
            X = random.uniform((user_input * -1), user_input)
            Y = random.uniform((user_input * -1), user_input)
            Z = random.uniform((user_input * -1), user_input)
            lx.eval('select.drop polygon')
                
            for p in Rand_Polys:
                lx.eval('select.typeFrom polygon')
                lx.eval('select.element %s polygon add %s' % (layer,p))
            
            lx.eval('select.connect')
            lx.eval('tool.set TransformMove on')
            lx.eval('tool.attr xfrm.transform TX %s' % X) 
            lx.eval('tool.attr xfrm.transform TY %s' % Y)
            lx.eval('tool.attr xfrm.transform TZ %s' % Z)
            lx.eval('tool.doApply')
            lx.eval('tool.set TransformMove off')
            
            lx.eval('hide.sel')
            polysN = lx.eval('query layerservice poly.N ? visible') #visible poly count
            lx.out(polysN)
            
        lx.eval('unhide')
        
        lx.eval("pref.value units.system %s" % u_sys)
        lx.eval("pref.value units.default %s" % u_def)
        
        lx.eval('item.addDeformer morphDeform')
        lx.eval('layer.setVisibility')
        lx.eval('select.drop item')
        lx.eval('select.useSet EXPLODED_MESH select')
        lx.eval('deformer.freeze false')
        
        
        
        ##### Morph Map Detection #####
        
        #Define the UV Seam vmap name Search case.
        lx.eval("user.defNew name:DesiredMorphmapName type:string life:momentary")
        DesiredMorphmapName = 'EXPLODED'
        
        #Define the UV Seam vmap name Search case.
        lx.eval("user.defNew name:NoMorphMap type:string life:momentary")
        NoMorphMap = '_____n_o_n_e_____'
        
        
        # Get the number of Morph map available on mesh
        DetectedMorphmapCount = len(lx.evalN('vertMap.list morf ?'))
        lx.out('Morph Map Count:', DetectedMorphmapCount)
        
        # Get the name of UV Seam map available on mesh
        DetectedMorphmapName = lx.eval('vertMap.list morf ?')
        lx.out('Morph Map Name:', DetectedMorphmapName)
        # ------------- UV SEAM Map Detection
        
        selection = list(scene.selectedByType('mesh'))
        #meshitems = scene.selected
        #lx.out(items)
        
        for item in selection:
            if item.geometry.vmaps.uvMaps:
                UVMapsCount = len(item.geometry.vmaps.uvMaps)
                lx.out('UVMap Count:', UVMapsCount)
                for uvmap in item.geometry.vmaps.uvMaps:
                    lx.out('UVMap Name:', uvmap.name)
        if UVMapsCount >= 1 :
            lx.eval('select.vertexMap {%s} txuv 3' % uvmap.name)
        lx.eval('smo.GC.ClearSelectionVmap 1 1')
        lx.eval('!!vertMap.delete EXPLODED')
        
        
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
        
        # ---------------- Compare TotalSafetyCheck value and decide or not to continue the process  --- END


    def cmd_Query(self, index, vaQuery):
        lx.notimpl()


lx.bless(SMO_GC_DupAndExplodeByDist_Cmd, Cmd_Name)
