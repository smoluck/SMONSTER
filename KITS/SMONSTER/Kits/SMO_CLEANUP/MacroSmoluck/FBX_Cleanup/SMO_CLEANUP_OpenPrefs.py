# python
"""
# Name:         SMO_CLEANUP_OpenPrefs.py
# Version:      1.0
#
# Purpose:      This script is designed to:
#               Open the SMO CLEANUP Kit Preferences.
#
#
# Author:       Franck ELISABETH
# Website:      https://www.smoluck.com
#
# Created:      14/05/2020
# Copyright:    (c) Franck Elisabeth 2017-2022
"""

import lx

lx.eval('layout.window Preferences false')
lx.eval('layout.window Preferences true')
lx.eval('pref.select SMOKITPREF/SMO_CLEANUP_Prefs set')