# python
# Made with Replay
# mechanicalcolor.com

# replay name:"Select UV border"
lx.eval('uv.selectBorder')

try:
    # replay name:"Delete Selection Set"
    lx.eval('!select.deleteSet name:UVSEAM')
    if:
        error
        else:
        lx.eval('select.editSet UVSEAM set')
        # replay name:"Delete Selection Set"
        lx.eval('!select.deleteSet name:UVSEAM')
        lx.eval('select.editSet name:UVSEAM mode:add')
