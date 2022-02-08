# python

import lx, lxifc, lxu.command

CMD_NAME = 'smo.GC.EXTRA.RemappingFCL'

FORMS = [
    {
        "label": "GAME CONTENT: Unbevel Polyloops",
        "recommended": "ctrl-shift-k",
        "cmd": "smo.GC.UnbevelLoops 1"
    }, {
        "label": "GAME CONTENT: Unbevel Polyloops Corner mode",
        "recommended": "ctrl-k",
        "cmd": "smo.GC.UnbevelLoops 0"
    }, {
        "label": "GAME CONTENT: Unbevel Edges",
        "recommended": "ctrl-u",
        "cmd": "smo.GC.Unbevel"
    }, {
        "label": "GAME CONTENT: Unbevel Edges Ring",
        "recommended": "ctrl-shift-u",
        "cmd": "smo.GC.UnbevelRing"
    }, {
        "label": "GAME CONTENT: Seneca SuperTaut Pie Menu",
        "recommended": "ctrl-alt-l",
        "cmd": "attr.formPopover {SenecaSuperTaut:sheet}"
    }, {
        "label": "GAME CONTENT: JoinVertex (Weld)",
        "recommended": "ctrl-alt-w",
        "cmd": "@{kit_SMO_GAME_CONTENT:MacroSmoluck/Basic/SMO_BAS_JoinVertex.LXM}"
    }, {
        "label": "GAME CONTENT: Select Boundary Edge of selected Polygon",
        "recommended": "ctrl-alt-top2",
        "cmd": "@AddBoundary.py"
    }, {
        "label": "GAME CONTENT: Replay last Macro",
        "recommended": "ctrl-alt-r",
        "cmd": "macro.replayRecorded 1"
    }, {
        "label": "GAME CONTENT: Duplicate Item",
        "recommended": "ctrl-alt-shift-d",
        "cmd": "item.duplicate false all:true mods:false"
    }, {
        "label": "GAME CONTENT: Set SMO Viewport Preset",
        "recommended": "ctrl-alt-top3",
        "cmd": "@{kit_SMO_GAME_CONTENT:MacroSmoluck/Basic/SMO_BAS_SetupColorScheme_ViewPortPref.LXM}"
    }, {
        "label": "GAME CONTENT: Delete Edge but Keep Vertex",
        "recommended": "ctrl-delete",
        "cmd": "edge.remove true"
    }, {
        "label": "GAME CONTENT: Use AVP Game Shaded (instead of Reflection)",
        "recommended": "numeric6",
        "cmd": "smo.GC.LoadViewportPreset 1"
    }, {
        "label": "GAME CONTENT: Use AVP With Matcap",
        "recommended": "ctrl-numeric6",
        "cmd": "smo.GC.Display.CycleMatCap 0"
    }, {
        "label": "GAME CONTENT: Use AVP With Matcap",
        "recommended": "ctrl-alt-numeric6",
        "cmd": "smo.GC.Display.CycleMatCap 1"
    }, {
        "label": "GAME CONTENT: Push Tool",
        "recommended": "ctrl-alt-p",
        "cmd": "tool.set xfrm.push on"
    }, {
        "label": "GAME CONTENT: Polygon Set Part",
        "recommended": "alt-shift-p",
        "cmd": "poly.setPart"
    }, {
        "label": "GAME CONTENT: Switch to Game Mode View",
        "recommended": "ctrl-alt-shift-g",
        "cmd": "view3d.gameInputMode"
    }, {
        "label": "GAME CONTENT: HardEdgeWeight from Poly",
        "recommended": "ctrl-alt-e",
        "cmd": "@{kit_SMO_GAME_CONTENT:MacroSmoluck/Modeling/SMO_MOD_PolyBoundaryEdgeWeight.LXM}"
    }, {
        "label": "GAME CONTENT: HardEdgeWeight from Edge",
        "recommended": "ctrl-alt-e",
        "cmd": "@{kit_SMO_GAME_CONTENT:MacroSmoluck/Modeling/SMO_MOD_EdgeWeight.LXM}"
    }, {
        "label": "GAME CONTENT: Bridge Edges",
        "recommended": "ctrl-shift-b",
        "cmd": "tool.set edge.bridge on"
    }, {
        "label": "GAME CONTENT: Toggle the Color Correct in OpenGL Mode",
        "recommended": "ctrl-alt-top1",
        "cmd": "glocio.toggle true"
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


class SMO_GAME_CONTENT_EXTRA_KeymapCmdListClass(lxifc.UIValueHints):
    def __init__(self, items):
        self._items = items

    def uiv_Flags(self):
        return lx.symbol.fVALHINT_FORM_COMMAND_LIST

    def uiv_FormCommandListCount(self):
        return len(self._items)

    def uiv_FormCommandListByIndex(self,index):
        return self._items[index]


class SMO_GAME_CONTENT_EXTRA_KeymapCmdClass(lxu.command.BasicCommand):
    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

        self.dyna_Add('query', lx.symbol.sTYPE_INTEGER)
        self.basic_SetFlags(0, lx.symbol.fCMDARG_QUERY)

    def arg_UIValueHints(self, index):
        if index == 0:
            return SMO_GAME_CONTENT_EXTRA_KeymapCmdListClass(list_commands())

    def cmd_Execute(self,flags):
        pass

    def cmd_Query(self,index,vaQuery):
        pass

lx.bless(SMO_GAME_CONTENT_EXTRA_KeymapCmdClass, CMD_NAME)
