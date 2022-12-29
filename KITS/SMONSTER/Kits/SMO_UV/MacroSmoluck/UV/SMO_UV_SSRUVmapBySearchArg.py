import lx, lxu, modo
scn = modo.Scene()


# ------------- ARGUMENTS ------------- #
# RenameByDefault = 1
# SearchString = "UVChannel_1"
# TargetString = "TargetUVMap"
# ------------- ARGUMENTS ------------- #
args = lx.args()
lx.out(args)

RenameByDefault = bool(args[0])
lx.out('Rename by user default UVMap name:', RenameByDefault)

SearchString = string(args[1])
lx.out('Searched UVMap name:', SearchString)

TargetString = string(args[2])
lx.out('Target UVMap name:', TargetString)
# ------------- ARGUMENTS ------------- #


DetectedVMapCount = len(lx.evalN('vertMap.list all ?'))
lx.out('Vmap Count:', DetectedVMapCount)
# Get the name of UV Seam map available on mesh
DetectedVMapName = lx.eval('vertMap.list txuv ?')
lx.out('UVmap Name:', DetectedVMapName)
# Get the default UV Map name of the user
DefaultUVMapName =  lx.eval('pref.value application.defaultTexture ?')
lx.out('Current Default UV Map name:', DefaultUVMapName)

RenamedToDefault = 0

for mesh in scn.items('mesh'):
    for VMapName in DetectedVMapPickName:
        if VMapName.startswith('%s' % SearchString ):
            try:
                lx.eval('select.vertexMap {%s} txuv replace' % SearchString)
            except:
                pass
if DetectedVMapCount >= 1 and DetectedVMapName == "_____n_o_n_e_____" :
    lx.out('UV map Selected')
    lx.eval('select.vertexMap {%s} txuv replace' % SearchString)
    if RenameByDefault == 1 :
        lx.eval('vertMap.rename {%s} {%s} txuv active' % (SearchString, DefaultUVMapName))
        lx.out('Detected UV Map Renamed from %s to %s:'% (SearchString, DefaultUVMapName))
    if RenameByDefault == 0 :
        lx.eval('vertMap.rename {%s} {%s} txuv active' % (SearchString, TargetString))
        lx.out('Detected UV Map Renamed from %s to %s:'% (SearchString, TargetString))
    RenamedToDefault = 1
    
elif DetectedVMapCount <= 0 and DetectedVMapName != "_____n_o_n_e_____" and RenamedToDefault == 0:
    lx.out('UV Map not Renamed, because not Detected')
