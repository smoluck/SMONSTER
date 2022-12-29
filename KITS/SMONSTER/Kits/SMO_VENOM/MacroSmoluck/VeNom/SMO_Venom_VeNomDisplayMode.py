# python
"""
Name:           SMO_Venom_VeNomDisplayMode.py

Purpose:        This script is designed to:
                Hide the wireframe on current Item selection and hide Vertex Normals

Author:         Franck ELISABETH
Website:        https://www.smoluck.com
Created:        15/04/2020
Copyright:      (c) Franck Elisabeth 2017-2022
"""

import lx

lx.eval('view3d.selItemMode none')
lx.eval('tool.set util.normshow off')