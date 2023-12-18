# python
"""
Name:               SMO_MIFABOMA_OpenPrefs.py

Purpose:            This Script is designed to:
                    Open the SMO MIFABOMA Kit Preferences.


Author:             Franck ELISABETH
Website:            https://www.linkedin.com/in/smoluck/
Created:            14/05/2020
Copyright:          (c) Franck Elisabeth 2017-2022
"""

import lx

lx.eval('layout.window Preferences false')
lx.eval('layout.window Preferences true')
lx.eval('pref.select SMOKITPREF/SMO_MIFABOMA_Prefs set')