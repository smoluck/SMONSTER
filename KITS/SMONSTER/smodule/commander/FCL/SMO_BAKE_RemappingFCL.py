# python

import lx, lxifc, lxu.command

CMD_NAME = 'smo.BAKE.RemappingFCL'


FORMS = [
    {
        "label": "BAKE: Popover Menu",
        "recommended": "shift-f4",
        "cmd": "attr.formPopover {SMO_BAKE_PO_SH:sheet}"
    }

]

def list_commands():
    fcl = []
    for n, form in enumerate(sorted(FORMS, key=lambda k: k['label']) ):
        fcl.append("smo.labeledPopover {%s} {%s} {%s}" % (form["cmd"], form["label"], form["recommended"]))
        fcl.append("smo.labeledMapKey {%s} {%s}" % (form["cmd"], form["label"]))

        if n < len(FORMS)-1:
            fcl.append('- ')

    return fcl


class SMO_BAKE_KeymapCmdListClass(lxifc.UIValueHints):
    def __init__(self, items):
        self._items = items

    def uiv_Flags(self):
        return lx.symbol.fVALHINT_FORM_COMMAND_LIST

    def uiv_FormCommandListCount(self):
        return len(self._items)

    def uiv_FormCommandListByIndex(self,index):
        return self._items[index]


class SMO_BAKE_KeymapCmdClass(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

        self.dyna_Add('query', lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags(0, lx.symbol.fCMDARG_QUERY)

    def arg_UIValueHints(self, index):
        if index == 0:
            return SMO_BAKE_KeymapCmdListClass(list_commands())

    def cmd_Execute(self,flags):
        pass

    def cmd_Query(self,index,vaQuery):
        pass

lx.bless(SMO_BAKE_KeymapCmdClass, CMD_NAME)
