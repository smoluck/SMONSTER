# python

import lx, lxifc, lxu.command

CMD_NAME = 'smo.SMONSTER.RemappingFCL'


FORMS = [
    {
        "label": "SMONSTER Library Documentation Menu",
        "recommended": "alt-shift-l",
        "cmd": "attr.formPopover {SMONSTER_DOC_LIBRARY_POPOVER:sheet}"
    }, {
        "label": "SMONSTER Training Scene Menu",
        "recommended": "alt-shift-t",
        "cmd": "attr.formPopover {SMONSTER_LOAD_TRAINING_SCENES:sheet}"
    }, {
        "label": "SMONSTER Kits Menu",
        "recommended": "alt-shift-k",
        "cmd": "attr.formPopover {SMONSTER_TAIL_MENU:sheet}"
    }, {
        "label": "SMONSTER Options",
        "recommended": "alt-shift-o",
        "cmd": "@{kit_SMO_MASTER:Scripts/SMONSTER_OpenPrefs.py}"
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


class SMONSTER_KeymapCmdListClass(lxifc.UIValueHints):
    def __init__(self, items):
        self._items = items

    def uiv_Flags(self):
        return lx.symbol.fVALHINT_FORM_COMMAND_LIST

    def uiv_FormCommandListCount(self):
        return len(self._items)

    def uiv_FormCommandListByIndex(self,index):
        return self._items[index]


class SMONSTER_KeymapCmdClass(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

        self.dyna_Add('query', lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags(0, lx.symbol.fCMDARG_QUERY)

    def arg_UIValueHints(self, index):
        if index == 0:
            return SMONSTER_KeymapCmdListClass(list_commands())

    def cmd_Execute(self,flags):
        pass

    def cmd_Query(self,index,vaQuery):
        pass

lx.bless(SMONSTER_KeymapCmdClass, CMD_NAME)
