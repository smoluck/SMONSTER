#python
#---------------------------------------
# Name:         SMO_ExportMeshOpRig_AudioNotification.py
# Version: 1.01
#
# Purpose: This script plays n Audio track to prevent of a script end.
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      28/02/2018
# Modified:		02/04/2019
# Copyright:    (c) Franck Elisabeth 2017-2022
#---------------------------------------
import lx

lx.eval('scene.new')


audiopath = lx.eval("query platformservice alias ? {kit_SMO_GAME_CONTENT:Audio/Export_Finish.wav}")

lx.eval('time.range scene out:30.0')
lx.eval('time.range current out:30.0')

# Play an Audio File to tell that the export is done.
lx.eval('audio.playFile {%s}' % audiopath)

lx.eval('!scene.close')