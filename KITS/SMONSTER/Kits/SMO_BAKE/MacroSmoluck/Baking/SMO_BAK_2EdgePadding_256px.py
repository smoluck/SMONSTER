#python
import modo

scene = modo.Scene()
render_item = scene.item("Render")

x_channel = render_item.channel('bakeX')
x_channel.set(256)
y_channel = render_item.channel('bakeY')
y_channel.set(256)
lx.eval('pref.value render.bakeBorder 2')