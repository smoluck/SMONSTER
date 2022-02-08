# python
# Made with Replay
# mechanicalcolor.com

lx.eval('select.type polygon')
# replay name:"Selection All"
lx.eval('select.all')
# replay name:"RepositionCenter.LXM"
lx.eval('smo.GC.Setup.MoveRotateCenterToSelection 1 0')
lx.eval('select.type polygon')
# replay name:"Selection All"
lx.eval('select.all')
# replay name:"Align Work Plane to Selected"
lx.eval('workPlane.fitSelect')
# replay name:"Item"
lx.eval('select.type item')
lx.eval('select.convert type:center')
lx.eval('matchWorkplaneRot')
# replay name:"Reset Work Plane"
lx.eval('workPlane.reset')
# replay name:"Item"
lx.eval('select.type item')
