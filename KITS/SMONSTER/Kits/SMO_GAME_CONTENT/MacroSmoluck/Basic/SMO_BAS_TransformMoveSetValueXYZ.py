import modo, lx

# Argument: the amount of EdgeWeight applied in percentage
Source_PosX = lx.arg(0)
Source_PosY = lx.arg(1)
Source_PosZ = lx.arg(2)


lx.eval('tool.noChange')
lx.eval('tool.reset xfrm.transform')
lx.eval('tool.flag xfrm.transform auto 0')
lx.eval('tool.setAttr xfrm.transform TX {%f}' %Source_PosX)
lx.eval('tool.setAttr xfrm.transform TY {%f}' %Source_PosY)
lx.eval('tool.setAttr xfrm.transform TZ {%f}' %Source_PosZ)
lx.eval('tool.doApply')