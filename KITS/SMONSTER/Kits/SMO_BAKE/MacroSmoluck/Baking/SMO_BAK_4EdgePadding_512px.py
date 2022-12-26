# python

import modo
import lx

scene = modo.Scene()
render_item = scene.item("Render")

x_channel = render_item.channel('bakeX')
x_channel.set(512)
y_channel = render_item.channel('bakeY')
y_channel.set(512)
lx.eval('pref.value render.bakeBorder 4')