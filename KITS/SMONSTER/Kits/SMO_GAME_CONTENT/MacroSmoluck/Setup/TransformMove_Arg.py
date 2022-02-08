import lx
from lx import eval, eval1, evalN, out, Monitor, args

arguments = args()  


# Command Block Begin:
lx.eval('tool.setAttr tool:xfrm.transform attr:TX value:{%f}' %arguments[0])
lx.eval('tool.setAttr tool:xfrm.transform attr:TY value:{%f}' %arguments[1])
lx.eval('tool.setAttr tool:xfrm.transform attr:TZ value:{%f}' %arguments[2])
# Command Block End:


# lx.eval('tool.set preset:TransformMove mode:on')
# lx.eval('tool.reset')
# lx.eval('tool.viewType type:xyz')
# lx.eval('tool.flag xfrm.transform auto 1')
# lx.eval('tool.noChange')

# # Command Block Begin:
# lx.eval('tool.setAttr tool:xfrm.transform attr:TX value:{%s}' %arguments[0])
# lx.eval('tool.setAttr tool:xfrm.transform attr:TY value:{%s}' %arguments[1])
# lx.eval('tool.setAttr tool:xfrm.transform attr:TZ value:{%s}' %arguments[2])
# # Command Block End:

# # Launch the Move Tool
# lx.eval('tool.doapply')
# lx.eval('tool.set preset:TransformMove mode:off')