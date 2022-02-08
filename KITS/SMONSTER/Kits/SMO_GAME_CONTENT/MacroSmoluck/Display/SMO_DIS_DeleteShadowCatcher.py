#python
#---------------------------------------
# Name:         SMO_DeleteShadowCatcher.py
# Version: 1.0
#
# Purpose: This script is designed to Delete the
# Shadow Catcher Assembly from the scene.
#
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      10/03/2019
# Copyright:    (c) Franck Elisabeth 2017-2022
#---------------------------------------

lx.eval('select.item SMO_Ground_ShadowCatcher_ASS set')
lx.eval('!delete')
