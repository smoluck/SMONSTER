# python

import lx
import lxifc
import lxu.command

CMD_NAME = 'smo.CB.RemappingFCL'

FORMS = [
    {
        "label": "COLOR BAR: by Type",
        "recommended": "shift-f1",
        "cmd": "attr.formPopover {SMO_COLOR_BAR_ByType_SH:sheet}"
    }, {
        "label": "COLOR BAR: by Color",
        "recommended": "shift-f2",
        "cmd": "attr.formPopover {SMO_COLOR_BAR_ByColor_SH:sheet}"
    }, {
        "label": "COLOR BAR: by Cycle",
        "recommended": "shift-f3",
        "cmd": "attr.formPopover {SMO_COLOR_BAR_Cycle_SH:sheet}"
    }, {
        "label": "COLOR BAR: Locator Shape",
        "recommended": "shift-f8",
        "cmd": "attr.formPopover {SMO_COLOR_BAR_LOC_SHAPE_PM:sheet}"
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


class SMO_COLOR_BAR_KeymapCmdListClass(lxifc.UIValueHints):
    def __init__(self, items):
        self._items = items

    def uiv_Flags(self):
        return lx.symbol.fVALHINT_FORM_COMMAND_LIST

    def uiv_FormCommandListCount(self):
        return len(self._items)

    def uiv_FormCommandListByIndex(self, index):
        return self._items[index]


class SMO_CB_KeymapCmdClass(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

        self.dyna_Add('query', lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags(0, lx.symbol.fCMDARG_QUERY)

    def arg_UIValueHints(self, index):
        if index == 0:
            return SMO_COLOR_BAR_KeymapCmdListClass(list_commands())

    def cmd_Execute(self, flags):
        pass

    def cmd_Query(self, index, vaQuery):
        pass


lx.bless(SMO_CB_KeymapCmdClass, CMD_NAME)
