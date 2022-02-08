#python
#---------------------------------------
# Name:         SMO_Venom_VeNomDisplayMode.py
# Version:      1.0
# 
# Purpose:      This script is designed to:
#               Hide the wireframe on current Item selection and hide Vertex Normals
# 
# 
# 
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
# 
# Created:      15/04/2020
# Copyright:    (c) Franck Elisabeth 2017-2022
#---------------------------------------

lx.eval('view3d.selItemMode none')
lx.eval('tool.set util.normshow off')