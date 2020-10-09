from engine.mathematics import Vec2
from engine.rendering import Translation
from engine.entities import Entity
import pyglet
from pyglet.window import key
import engine
import helpers
from decimal import *

window = pyglet.window.Window(caption="Fat Guys")
event_logger = pyglet.window.event.WindowEventLogger()
window.push_handlers(event_logger)

rendering = engine.rendering.RenderingSystem()
ents = []
cake_image = pyglet.image.load(helpers.find_data_file("icon.png"))
engine.helpers.center_img(cake_image)
fat_dude_image = pyglet.image.load(helpers.find_data_file("homer-simpson.png"))
engine.helpers.center_img(fat_dude_image)

for i in range(10):
    ents.append(engine.rendering.Sprite(pyglet.sprite.Sprite(
        cake_image), Translation("", Vec2(i * 50, i * 25))))

dude_position: Vec2 = Vec2(window.width // 2, fat_dude_image.height // 2)
ents.append(fat_dude := engine.rendering.Sprite(pyglet.sprite.Sprite(fat_dude_image),
                                                Translation("Fat Guy", dude_position)))

holding_keys = {}


@window.event
def on_key_press(symbol: key, modifiers):
    holding_keys[symbol] = True


@window.event
def on_key_release(symbol: key, modifiers):
    holding_keys[symbol] = False


def update(dt):
    window.clear()

    if holding_keys.get(key.A):
        dude_position.x -= 200 * dt
        print(dude_position)
        fat_dude.update_translation(Translation("Fat Guy", dude_position))

    if holding_keys.get(key.D):
        dude_position.x += 200 * dt
        print(dude_position)
        fat_dude.update_translation(Translation("Fat Guy", dude_position))

    engine.entities.System.update_all()


pyglet.clock.schedule_interval(update, 1/120.0)


pyglet.app.run()
