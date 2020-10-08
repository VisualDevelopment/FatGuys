from engine.mathematics import Vec2
from engine.rendering import Translation
from engine.entities import Entity
import pyglet
from pyglet.window import key
import engine
import helpers

window = pyglet.window.Window(caption="Fat Guys")
rendering = engine.rendering.RenderingSystem()
ents = []

for i in range(100):
    ents.append(engine.rendering.Sprite(pyglet.sprite.Sprite(pyglet.image.load(helpers.find_data_file("icon.png"))), Translation("", Vec2(i * 50, i * 25))))


@window.event
def on_draw():
    window.clear()
    engine.entities.System.update_all()


@window.event
def on_key_press(symbol: key, modifiers):
    if symbol == key.W:
        pass


pyglet.app.run()
