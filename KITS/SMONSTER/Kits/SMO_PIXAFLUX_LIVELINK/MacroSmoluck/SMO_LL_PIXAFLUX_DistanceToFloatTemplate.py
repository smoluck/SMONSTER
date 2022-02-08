import lx, lxu, modo, random

User_DefUnit = lx.eval("pref.value units.default ?")
lx.out(u_def)

PFExplodeDistance = lx.eval ('!!user.value Smo_PixaFluxExplodeDistance ?')
lx.out('Explode Range Ditance by Prefs string value: ', PFExplodeDistance)

user_input = lx.eval("user.value Smo_PixaFluxExplodeDistance ?")
if User_DefUnit == "meters" :
    user_input = float(user_input / 100)
if User_DefUnit	 == "millimeters" :
    user_input = float(user_input * 10)
lx.out('Explode Range Distance: ', user_input)