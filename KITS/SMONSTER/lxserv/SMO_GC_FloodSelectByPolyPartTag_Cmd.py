# python
"""
Name:         SMO_GC_FloodSelectByPolyPartTag_Cmd.py

Purpose:      This script is designed to
              From selected Polygons, flood select by detected polygon parts

Author:       Franck ELISABETH
Website:      https://www.linkedin.com/in/smoluck/
Created:      29/06/2025
Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx
import lxu
import modo

Cmd_Name = "smo.GC.FloodSelectByPolyPartTag"


class SMO_GC_FloodSelectByPolyPartTag_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO GC - Flood Select by Polygon Part Tag'

    def cmd_Desc(self):
        return 'From selected Polygons, flood select by detected polygon parts'

    def cmd_Tooltip(self):
        return 'From selected Polygons, flood select by detected polygon parts'

    def cmd_Help(self):
        return 'https://www.smoluck.com'

    def basic_ButtonName(self):
        return 'SMO GC - Flood Select by Polygon Part Tag'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        # Get selected polygon indices
        selected_indices = lx.evalN('query layerservice polys ? selected')
        # print(selected_indices)

        # Get part tags using layer service
        part_tags = set()
        tag_name = []
        tag_type = []
        result = ""
        for poly_id in selected_indices:
            # print(poly_id)
            tag_name = lx.evalN('query layerservice poly.tags ? %s' % poly_id)
            # print(tag_name)
            tag_type = lx.evalN('query layerservice poly.tagTypes ? %s' % poly_id)
            # print(tag_type)
            for item in tag_type:
                if "PART" in tag_type:
                    index = tag_type.index("PART")
                    result = tag_name[index]
                    part_tags.add(result)
                # print("result", result)
        # print("--------")
        for item in part_tags:
            # print(item)
            lx.eval('select.polygon add part face %s' % item)

lx.bless(SMO_GC_FloodSelectByPolyPartTag_Cmd, Cmd_Name)
