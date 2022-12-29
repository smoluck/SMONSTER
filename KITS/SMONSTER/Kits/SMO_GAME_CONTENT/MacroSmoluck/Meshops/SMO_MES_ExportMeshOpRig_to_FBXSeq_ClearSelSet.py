# python
# Made with Replay
# mechanicalcolor.com

# replay name:"Switch to Item Selection Mode"
lx.eval('select.typeFrom item;center;edge;polygon;vertex;ptag true')
lx.eval('select.type item')
# replay name:"Set the Working Set to SOURCE_MESH"
# lx.eval('select.pickWorkingSet SOURCE_MESH true')
# replay name:"Delete the SelSet"
# lx.eval('select.deleteWorkingSet')

lx.eval('!select.deleteSet SOURCE_MESH false')
