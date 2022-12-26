# python

import lx
import lxifc
import lxu.command

CMD_NAME = 'smo.GC.151.RemappingFCL'

FORMS = [
    {
        "label": "GAME CONTENT: Channel Haul",
        "recommended": "c",
        "cmd": "tool.set channel.haul on"
    }, {
        "label": "GAME CONTENT: Edge Knife",
        "recommended": "c",
        "cmd": "tool.set edge.knife on"
    }, {
        "label": "GAME CONTENT: Polygon Knife",
        "recommended": "shift-c",
        "cmd": "tool.set poly.knife on"
    }, {
        "label": "GAME CONTENT: Loop Slice",
        "recommended": "alt-c",
        "cmd": "tool.set poly.loopSlice on"
    }, {
        "label": "GAME CONTENT: Mini-Properties Popover",
        "recommended": "shift-space",
        "cmd": "attr.formPopover {MiniProps:sheet} mini lockProficiency:true"
    }, {
        "label": "GAME CONTENT: Original SpaceBar behaviour",
        "recommended": "space",
        "cmd": "select.nextMode"
    }

]


# max = len(FORMS)
# lx.out(max)


def list_commands():
    fcl = []
    for n, form in enumerate(sorted(FORMS, key=lambda k: k['label'])):
        fcl.append("smo.labeledPopover {%s} {%s} {%s}" % (form["cmd"], form["label"], form["recommended"]))
        fcl.append("smo.labeledMapKey {%s} {%s}" % (form["cmd"], form["label"]))

        if n < len(FORMS) - 1:
            fcl.append('- ')

    return fcl


class SMO_GAME_CONTENT_151_KeymapCmdListClass(lxifc.UIValueHints):
    def __init__(self, items):
        self._items = items

    def uiv_Flags(self):
        return lx.symbol.fVALHINT_FORM_COMMAND_LIST

    def uiv_FormCommandListCount(self):
        return len(self._items)

    def uiv_FormCommandListByIndex(self, index):
        return self._items[index]


class SMO_GAME_CONTENT_151_KeymapCmdClass(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

        self.dyna_Add('query', lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags(0, lx.symbol.fCMDARG_QUERY)

    def arg_UIValueHints(self, index):
        if index == 0:
            return SMO_GAME_CONTENT_151_KeymapCmdListClass(list_commands())

    def cmd_Execute(self, flags):
        pass

    def cmd_Query(self, index, vaQuery):
        pass


lx.bless(SMO_GAME_CONTENT_151_KeymapCmdClass, CMD_NAME)
