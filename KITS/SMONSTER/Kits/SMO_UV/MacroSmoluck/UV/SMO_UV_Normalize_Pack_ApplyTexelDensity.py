# python
# Made with Replay
# mechanicalcolor.com

# replay name:"Normalize Texel Density"
lx.eval('texeldensity.normalize')
# replay name:"Pack UVs"
lx.eval('uv.pack pack:true stretch:false orient:false direction:auto gaps:"0.2" byPixel:false gapsByPixel:"10.24" bbox:false stack:false region:normalized udim:1001 regionX:"-1.0" regionY:"-1.0" regionW:"3.0" regionH:"3.0" tileU:1 tileV:1 polygonTag:material background:false writeNew:false')
# replay name:"Fit UVs"
lx.eval('uv.fit sepa:entire gaps:"0.0"')
# replay name:"Set Texel Density"
lx.eval('texeldensity.set per:island mode:all')
