import lx
from lx import eval, eval1, evalN, out, Monitor, args

arguments = args()  


Instance = (lx.eval('query sceneservice selection ? locator'))
print(Instance)
lx.eval('select.item %s add' % Instance)
# lx.eval('item.refSystem %s' % InstancesNameList[i])
lx.eval('item.create locator')
Locator = (lx.eval('query sceneservice selection ? locator'))
print(Locator)
lx.eval('select.item %s add' % Instance)
lx.eval('item.parent')
lx.eval('item.parent parent:{} inPlace:1')
lx.eval('select.drop item')
lx.eval('select.item %s add' % Instance)
lx.eval('select.item %s add' % Locator)
lx.eval('item.parent %s %s inPlace:1' %(Instance, Locator))
lx.eval('select.drop item')
lx.eval('select.item %s add' % Instance)
lx.eval('transform.channel pos.X {%f}' %arguments[0])
lx.eval('transform.channel pos.Y {%f}' %arguments[1])
lx.eval('transform.channel pos.Z {%f}' %arguments[2])
lx.eval('item.parent parent:{} inPlace:1')
lx.eval('select.drop item')
lx.eval('select.item %s add' % Locator)
lx.eval('!delete')
