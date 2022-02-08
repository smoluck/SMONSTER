# python

import lx, lxifc, lxu.command

CMD_NAME = 'smo.VENOM.RemappingFCL'


FORMS = [
    {
        "label": "VENOM:   Pie Menu",
        "recommended": "ctrl-alt-n",
        "cmd": "attr.formPopover {SMO_VENOM_PM:sheet}"
    }, {
        "label": "VENOM:   Modo Viewport Mode",
        "recommended": "alt-n",
        "cmd": "@{kit_SMO_VENOM:MacroSmoluck/VeNom/SMO_Venom_DefaultDisplayMode.py}"
    }, {
        "label": "VENOM:   Default Viewport Mode",
        "recommended": "alt-j",
        "cmd": "@{kit_SMO_VENOM:MacroSmoluck/VeNom/SMO_Venom_VeNomDisplayMode.py}"
    }, {
        "label": "VENOM:   Set on Polygon Under Mouse with Similar Facing Ratio Touching (use in Item Mode)",
        "recommended": "ctrl-shift-n",
        "cmd": "smo.VENOM.MainCommand 0 0"
    }, {
        "label": "VENOM:   Set on Polygon Under Mouse with Similar Facing Ratio on Object ( use in Item Mode)",
        "recommended": "ctrl-alt-shift-n",
        "cmd": "smo.VENOM.MainCommand 1 0"
    }, {
        "label": "VENOM:   Set on Current Polygons",
        "recommended": "ctrl-shift-n",
        "cmd": "smo.VENOM.MainCommand 0 0"
    }, {
        "label": "VENOM:   Set on Current Polygons with AutoLoop Mode",
        "recommended": "ctrl-alt-shift-n",
        "cmd": "smo.VENOM.MainCommand 0 1"
    }

]

# max = len(FORMS)
# lx.out(max)

def list_commands():
    fcl = []
    for n, form in enumerate(sorted(FORMS, key=lambda k: k['label']) ):
        fcl.append("smo.labeledPopover {%s} {%s} {%s}" % (form["cmd"], form["label"], form["recommended"]))
        fcl.append("smo.labeledMapKey {%s} {%s}" % (form["cmd"], form["label"]))

        if n < len(FORMS)-1:
            fcl.append('- ')

    return fcl


class SMO_VENOM_KeymapCmdListClass(lxifc.UIValueHints):
    def __init__(self, items):
        self._items = items

    def uiv_Flags(self):
        return lx.symbol.fVALHINT_FORM_COMMAND_LIST

    def uiv_FormCommandListCount(self):
        return len(self._items)

    def uiv_FormCommandListByIndex(self,index):
        return self._items[index]


class SMO_VENOM_KeymapCmdClass(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

        self.dyna_Add('query', lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags(0, lx.symbol.fCMDARG_QUERY)

    def arg_UIValueHints(self, index):
        if index == 0:
            return SMO_VENOM_KeymapCmdListClass(list_commands())

    def cmd_Execute(self,flags):
        pass

    def cmd_Query(self,index,vaQuery):
        pass

lx.bless(SMO_VENOM_KeymapCmdClass, CMD_NAME)
