# python
# Made with Replay
# mechanicalcolor.com


# replay name:"Set the Workplane to Polygon Selection"
lx.eval('workPlane.fitSelect')
# replay name:"Convert selection to Item"
lx.eval('select.type item')
# replay name:"Convert selection to Center"
lx.eval('select.convert type:center')
# replay name:"Match Center to Workplane Position"
lx.eval('matchWorkplanePos')
# replay name:"Match Center to Workplane Rotation"
lx.eval('matchWorkplaneRot')
# replay name:"Reset the Workplane"
lx.eval('workPlane.reset')
# replay name:"Item"
lx.eval('select.typeFrom typelist:"polygon;vertex;ptag;item;pivot;center;edge" enable:true')
