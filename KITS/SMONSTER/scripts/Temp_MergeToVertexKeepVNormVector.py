import lx
import lxu
import modo

selitems = len(lx.evalN("query sceneservice selection ? locator"))
lx.out('selitems',selitems)

if selitems != 1:
	lx.eval('dialog.setup info')
	lx.eval('dialog.title {PP Copy Vertex Normals:}')
	lx.eval('dialog.msg {"You must have 1 mesh item selected to run this script.}')
	lx.eval('+dialog.open')
	sys.exit()

#The command will be enabled if 2 verts is selected.
layer = lx.eval('query layerservice layer.index ? main')
vertcount = lx.eval('query layerservice vert.N ? selected')
verts_sel = lx.eval('query layerservice verts ? selected')
lx.out('vertcount', vertcount)
lx.out('verts selected', verts_sel)
		
#If more or less than 2 verts are selected display this dialog and exit command
	
#Store Vert Id	
v0 = verts_sel[-1]
v1 = verts_sel[0]
lx.out(v0)
lx.out(v1)

lx.eval('select.editSet temp_join add')


# Scene
scene = modo.Scene()
# Get first mesh object
mesh = scene.selectedByType('mesh')[0]
# Activate mesh geo
with mesh.geometry as meshGeo:
	# Loop all normal maps
	for map in meshGeo.vmaps.getMapsByType(lx.symbol.i_VMAP_NORMAL):
		# Loop all selected verts
		for vert in meshGeo.vertices.selected:
			vn0= map.getNormal(vert.Index())
			print (map.name, '\nvert:', map.getNormal(vert.Index()))

#select first vert and get normal values
lx.eval('select.drop vertex')

for vert in verts_sel[:-1]:
	lx.eval('select.element %s vertex add %s' % (layer, vert))
lx.eval('select.element %s vertex add %s' % (layer, v0))
# @kit_SMO_GAME_CONTENT:MacroSmoluck/Basic/SMO_BAS_JoinVertex.LXM
lx.eval('!vert.join false')
lx.eval('select.useSet temp_join select')

#Select Second vert and tranfer values from first vert


for vert in lx.eval('query layerservice verts ? selected'):
    lx.eval('select.drop vertex')
    lx.eval('select.element %s vertex add %s' % (layer, vert))
    lx.eval('vertMap.setVertex "Vertex Normal" normal 0 %s %s' %(vert, vn0[0]))
    lx.eval('vertMap.setVertex "Vertex Normal" normal 1 %s %s' %(vert, vn0[1]))
    lx.eval('vertMap.setVertex "Vertex Normal" normal 2 %s %s' %(vert, vn0[2]))
lx.eval('select.deleteSet temp_join')