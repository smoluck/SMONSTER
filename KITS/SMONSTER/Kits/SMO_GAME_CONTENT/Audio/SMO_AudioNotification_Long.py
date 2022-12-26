# python
"""
# Name:         SMO_AudioNotification_Long.py
# Version: 1.01
#
# Purpose: This script plays n Audio track to prevent of a script end.
#
# Author:       Franck ELISABETH
# Website:      https://www.smoluck.com
#
# Created:      28/05/2018
# Modified:		03/06/2019
# Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx

OriginalTimeCurrentOut = lx.eval("time.range current out:?")
# lx.out('Original Time Current Out: {%s}' % OriginalTimeCurrentOut )
OriginalTimeSceneOut = lx.eval("time.range scene out: ?")
# lx.out('Original Time Scene Out: {%s}' % OriginalTimeSceneOut )


audiopath = lx.eval("query platformservice alias ? {kit_SMO_GAME_CONTENT:Audio/Export_Finish.wav}")

lx.eval('time.range scene out:30.0')
lx.eval('time.range current out:30.0')

# Play an Audio File to tell that the export is done.
lx.eval('audio.playFile {%s}' % audiopath)

lx.eval('time.range scene out: {%s}' % OriginalTimeSceneOut)
lx.eval('time.range current out: {%s}' % OriginalTimeCurrentOut)