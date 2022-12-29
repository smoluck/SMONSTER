# python
# Made with Replay
# mechanicalcolor.com

lx.eval('tool.set preset:"uv.create" mode:on')
lx.eval('tool.setAttr tool:"uv.create" attr:mode value:manual')

## Set Axis Y
try:
	# Command Block Begin:
	lx.eval('tool.setAttr uv.create axis 1')
	# Command Block End:
except:
	sys.exit

try:
	# Command Block Begin:  
	lx.eval('tool.setAttr tool:"uv.create" attr:sizX value:"0.1"')
	lx.eval('tool.setAttr tool:"uv.create" attr:sizY value:"0.1"')
	lx.eval('tool.setAttr tool:"uv.create" attr:sizZ value:"0.1"')
	# Command Block End:
except:
	sys.exit
	
try:
	# Command Block Begin: 
	lx.eval('tool.setAttr tool:"uv.create" attr:cenX value:"0.0"')
	lx.eval('tool.setAttr tool:"uv.create" attr:cenY value:"0.0"')
	lx.eval('tool.setAttr tool:"uv.create" attr:cenZ value:"0.0"')
	# Command Block End:
except:
	sys.exit
	
lx.eval('tool.apply')

# replay name:"Fit UVs"
lx.eval('uv.fit sepa:entire gaps:"0.0"')

# replay name:"Flip UV Island"
# lx.eval('tool.set preset:TransformScale mode:on')
# lx.eval('tool.setAttr tool:"xfrm.transform" attr:SX value:"-1.0"')

# replay name:"Select Next Mode"
lx.eval('select.nextMode')

# ###########################
# Set specific Texel Density
# replay name:"User Value"
# lx.eval('user.value name:"texeldensity.size3D" value:"0.1"')
# replay name:"User Value"
# lx.eval('user.value name:"texeldensity.sizeUV" value:"512.0"')
# ###########################

# replay name:"Set Texel Density"
lx.eval('texeldensity.set per:island mode:all')



lx.eval('tool.viewType uv')
# replay name:"Move"
lx.eval('tool.set preset:TransformMove mode:on')

try:
	# Command Block Begin: 
	lx.eval('tool.setAttr tool:"xfrm.transform" attr:TX value:"-1.0"')
	lx.eval('tool.setAttr tool:"xfrm.transform" attr:TY value:"0.0"')
	lx.eval('tool.setAttr tool:"xfrm.transform" attr:TZ value:"0.0"')
	lx.eval('tool.setAttr tool:"xfrm.transform" attr:U value:"-1.0"')
	lx.eval('tool.setAttr tool:"xfrm.transform" attr:V value:"0.0"')
	# Command Block End:
except:
	sys.exit
	
# Launch the Move
lx.eval('tool.doapply')