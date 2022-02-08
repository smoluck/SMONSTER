#python

import lx

# Get a list of all of the idents (internal names) of the selected mesh items.
selected_meshes = lx.evalN('query sceneservice selection ? mesh')

# For each selected item in that list...
for item_ident in selected_meshes:
    # Select only that item.
    lx.eval('select.item %s set mesh' % item_ident)

    # And query how many polygons it has in it.
    lx.eval('query layerservice layer.id ? primary')
    polys_left = lx.eval1('query layerservice poly.N ? all')

    # While it still has polygons left...
    while (polys_left > 0):
        # Get the material name of the first polygon in the item.
        material_name = lx.eval1('query layerservice poly.material ? first')
        # Select all polygons that have that material applied to them.
        lx.eval('select.polygon add material face {%s}' % material_name)
        # Cut them.
        lx.eval('select.cut')

        # Create a new mesh item.
        # This will also select the new item we created.
        lx.eval('item.create mesh')
        # Name it to be the same as the material name.
        lx.eval('item.name {%s}' % material_name)

        # Paste the polygons we cut earlier.
        lx.eval('select.paste')

        # Go back and select the original item we were working with - the one we cut from.
        lx.eval('select.item %s set mesh' % item_ident)

        # Now that we've removed some polygons from it, we need to get the new number of polygons left in in the mesh item.
        polys_left = lx.eval1('query layerservice poly.N ? all')

        # If there are no polygons left, delete the empty mesh item.
        # We'll wind up back at the start once this loop is done, because polys_left is 0, and the script will select the next of the originally selected mesh items in the list.
        if polys_left == 0:
            lx.eval('item.delete')