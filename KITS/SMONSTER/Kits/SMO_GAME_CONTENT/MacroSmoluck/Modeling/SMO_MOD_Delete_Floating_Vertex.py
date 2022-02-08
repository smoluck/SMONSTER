# python
# Made with Replay
# mechanicalcolor.com

lx.eval('select.type vertex')
# replay name:"Select Vertices"
lx.eval('select.vertex action:remove test:0 mode:all value:0')
# replay name:"Select Vertices"
lx.eval('select.vertex action:add test:poly mode:equal value:0')
# replay name:"Delete Selection"
lx.eval('!delete')
# replay name:"Item"
lx.eval('select.type item')
