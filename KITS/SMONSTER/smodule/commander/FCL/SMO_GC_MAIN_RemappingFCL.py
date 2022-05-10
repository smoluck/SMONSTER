# python

import lx, lxifc, lxu.command

CMD_NAME = 'smo.GC.MAIN.RemappingFCL'


FORMS = [
    {
        "label": "GAME CONTENT: CLEAR -Close Scene- Modo Default Remapping",
        "recommended": "ctrl-w",
        "cmd": "(none)"
    }, {
        "label": "GAME CONTENT: CLEAR -Quit Modo- Modo Default Remapping",
        "recommended": "ctrl-q",
        "cmd": "(none)"
    }, {
        "label": "GAME CONTENT: Pie Menu",
        "recommended": "ctrl-q",
        "cmd": "attr.formPopover {SMO_GC_MASTER_Pie_SH:sheet}"
    }, {
        "label": "GAME CONTENT: Popover Menu",
        "recommended": "ctrl-shift-q",
        "cmd": "attr.formPopover {SMO_GC_MASTER_VMENU_SH:sheet}"
    }, {
        "label": "GAME CONTENT: Vertex Normals Pie Menu",
        "recommended": "ctrl-alt-f1",
        "cmd": "attr.formPopover {SMO_GC_NORMALS_Pie_SH:sheet}"
    }, {
        "label": "GAME CONTENT: Setup Pie Menu",
        "recommended": "ctrl-alt-f2",
        "cmd": "attr.formPopover {SMO_GC_SETUP_Pie_SH:sheet}"
    }, {
        "label": "GAME CONTENT: Export Pie Menu",
        "recommended": "ctrl-alt-f3",
        "cmd": "attr.formPopover {SMO_GC_EXPORT_Pie_SH:sheet}"
    }, {
        "label": "GAME CONTENT: Select Pie Menu",
        "recommended": "ctrl-alt-f4",
        "cmd": "attr.formPopover {SMO_GC_SELECT_Pie_SH:sheet}"
    }, {
        "label": "GAME CONTENT: Modeling Pie Menu",
        "recommended": "ctrl-alt-f5",
        "cmd": "attr.formPopover {SMO_GC_MODELING_Pie_SH:sheet}"
    }, {
        "label": "GAME CONTENT: Cleaning Pie Menu",
        "recommended": "ctrl-alt-f6",
        "cmd": "attr.formPopover {SMO_GC_CLEANING_Pie_SH:sheet}"
    }, {
        "label": "GAME CONTENT: Meshops Pie Menu",
        "recommended": "ctrl-alt-f7",
        "cmd": "attr.formPopover {SMO_GC_MESHOPS_Pie_SH:sheet}"
    }, {
        "label": "GAME CONTENT: Display Pie Menu",
        "recommended": "ctrl-alt-f8",
        "cmd": "attr.formPopover {SMO_GC_DISPLAY_Pie_SH:sheet}"
    }, {
        "label": "GAME CONTENT: UV Pie Menu",
        "recommended": "ctrl-alt-f9",
        "cmd": "attr.formPopover {SMO_GC_UV_Pie_SH:sheet}"
    }, {
        "label": "GAME CONTENT: UV Seam Pie Menu",
        "recommended": "ctrl-alt-f10",
        "cmd": "attr.formPopover {SMO_GC_UV_SEAM_Pie_SH:sheet}"
    }, {
        "label": "GAME CONTENT: Palettes",
        "recommended": "ctrl-alt-shift-x",
        "cmd": "attr.formPopover {SMO_GC_PALETTES_Pie_SH:sheet}"
    }, {
        "label": "GAME CONTENT: Rename an Item from anywhere",
        "recommended": "enter",
        "cmd": "item.name"
    }, {
        "label": "GAME CONTENT: Middle Mouse show Item Properties",
        "recommended": "mmb",
        "cmd": "attr.formPopover {itemprops:general}"
    }, {
        "label": "GAME CONTENT: Toggle FullScreen Mode",
        "recommended": "shift-escape",
        "cmd": "smo.GC.FullScreenToggle"
    }, {
        "label": "GAME CONTENT: Viewport Border Toggles Pie Menu",
        "recommended": "ctrl-alt-space",
        "cmd": "attr.formPopover {SMO_GC_PieSwitcherBorderToggle:sheet}"
    }, {
        "label": "GAME CONTENT: Copy/Paste Pie Menu",
        "recommended": "ctrl-shift-c",
        "cmd": "attr.formPopover {SMO_CAD_TOOLS_CopyOrCut_PM:sheet}"
    }, {
        "label": "GAME CONTENT: Set Smart Material",
        "recommended": "m",
        "cmd": "smo.GC.SetNewMaterialSmartRename 1"
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


class SMO_GAME_CONTENT_MAIN_KeymapCmdListClass(lxifc.UIValueHints):
    def __init__(self, items):
        self._items = items

    def uiv_Flags(self):
        return lx.symbol.fVALHINT_FORM_COMMAND_LIST

    def uiv_FormCommandListCount(self):
        return len(self._items)

    def uiv_FormCommandListByIndex(self,index):
        return self._items[index]


class SMO_GAME_CONTENT_MAIN_KeymapCmdClass(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

        self.dyna_Add('query', lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags(0, lx.symbol.fCMDARG_QUERY)

    def arg_UIValueHints(self, index):
        if index == 0:
            return SMO_GAME_CONTENT_MAIN_KeymapCmdListClass(list_commands())

    def cmd_Execute(self,flags):
        pass

    def cmd_Query(self,index,vaQuery):
        pass

lx.bless(SMO_GAME_CONTENT_MAIN_KeymapCmdClass, CMD_NAME)
