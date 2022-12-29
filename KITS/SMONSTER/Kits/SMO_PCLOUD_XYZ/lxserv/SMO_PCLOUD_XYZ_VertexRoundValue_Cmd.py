# python
"""
Name:               SMO_PCLOUD_XYZ_VertexRoundValue_Cmd.py

Purpose:            This Script is designed to:
                    Open a txt file (Target) and create
                    Vertex at current position defined by the target File 3 float value (separated by a coma)
                    Each line is a new Vertex and round the value to the Centimeter (2 Decimals)

Author:             Franck ELISABETH
Website:            https://www.smoluck.com
Created:            29/11/2019
Copyright:          (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo


class SMO_PCLOUD_XYZ_VertexRoundValue_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO XYZ Vertex Rounded Value'

    def cmd_Desc(self):
        return 'Open a txt file (Target) and create Vertex at current position defined by the target File 3 float value (separated by a coma) Each line is a new Vertex and round the value to the Centimeter (2 Decimals).'

    def cmd_Tooltip(self):
        return 'Open a txt file (Target) and create Vertex at current position defined by the target File 3 float value (separated by a coma) Each line is a new Vertex and round the value to the Centimeter (2 Decimals).'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO XYZ Vertex Rounded Value'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        ITColor = self.dyna_Int(0)
        DrawOpt = self.dyna_Int(1)
        scene = modo.scene.current()
        meshes = scene.selectedByType(lx.symbol.sITYPE_MESH)
        locators = scene.selectedByType(lx.symbol.sITYPE_LOCATOR)

        # Get current scene
        scene = lxu.select.SceneSelection().current()

        # Create new mesh item
        scene_service = lx.service.Scene()
        mesh_type = scene_service.ItemTypeLookup(lx.symbol.sTYPE_MESH)
        mesh_item = scene.ItemAdd(mesh_type)

        # Get mesh object
        chanWrite = lx.object.ChannelWrite(scene.Channels(lx.symbol.s_ACTIONLAYER_SETUP, 0))
        write_mesh_obj = chanWrite.ValueObj(mesh_item, mesh_item.ChannelLookup(lx.symbol.sICHAN_MESH_MESH))
        mesh = lx.object.Mesh(write_mesh_obj)

        decimals = 2  # how many decimals to round to
        print(type(decimals))

        PositionfloatList = []  # Define an array of floats
        file_path = 'C:/TEMP/RA/ROOM_C_1_52.xyz'  # Defines path of output text file
        FileDATA = open(file_path, 'r')  # Opens and read file

        with FileDATA as f:
            line = f.readline()
            pointAccessor = mesh.PointAccessor()  # Add a point using the PointAccessor interface

            for line in f:
                PositionfloatList = map(float, line.split(','))

                FormatedPositionFloatList = ['%.2f' % elem for elem in PositionfloatList]

                PosX_Round = (FormatedPositionFloatList[0])
                PosY_Round = (FormatedPositionFloatList[1])
                PosZ_Round = (FormatedPositionFloatList[2])

                # mesh = modo.Mesh()
                # newPointID = pointAccessor.New(PositionfloatList[0:3])

                # pointA = lx.object.Mesh(mesh.geometry).PointAccessor()
                # pointA.New([float(PosX_Round), float(PosY_Round), float(PosY_Round)])

                newPointID = pointAccessor.New([float(PosX_Round), float(PosY_Round), float(PosZ_Round)])

                # Update the mesh
                mesh.SetMeshEdits(lx.symbol.f_MESHEDIT_POINTS)
        FileDATA.close()  # Closes the file

        lx.eval('vert.merge fixed false 0.004 false false')

        lx.out('End of SMO_XYZ_Vertex_RoundedValue Script')

    def cmd_Query(self, index, vaQuery):
        lx.notimpl()


lx.bless(SMO_PCLOUD_XYZ_VertexRoundValue_Cmd, "smo.PCLOUD.XYZVertexRoundValue")
