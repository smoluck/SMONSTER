# python
# ---------------------------------------
# Name:         SMO_DOC_WebLink_Cmd.py
# Version:      1.0
#
# Purpose:      This Command is designed to:
#               Open a WebLink using a String Argument for address.
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      29/08/2022
# Copyright:    (c) Franck Elisabeth 2017-2022
# ---------------------------------------

import lx, lxu, modo

Cmd_Name = "smo.DOC.WebLink"
# smo.DOC.WebLink {https://www.youtube.com/watch?v=zeK736RmjrE}

class SMO_DOC_WebLink_Cmd(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)
        self.dyna_Add("URL Address", lx.symbol.sTYPE_STRING)

    def cmd_Flags(self):
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def cmd_Interact(self):
        pass

    def cmd_UserName(self):
        return 'SMO DOC - Open Documentation WebLink'

    def cmd_Desc(self):
        return 'Open a WebLink using a String Argument for address.'

    def cmd_Tooltip(self):
        return 'Open a WebLink using a String Argument for address.'

    def cmd_Help(self):
        return 'https://twitter.com/sm0luck'

    def basic_ButtonName(self):
        return 'SMO DOC - Open Documentation WebLink'

    def basic_Enable(self, msg):
        return True

    def basic_Execute(self, msg, flags):
        args = lx.args()
        # lx.out(args)
        URL = self.dyna_String(0)
        lx.eval('openURL {%s}' % URL)


lx.bless(SMO_DOC_WebLink_Cmd, Cmd_Name)
