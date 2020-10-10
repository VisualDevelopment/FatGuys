from typing import List

from pyglet.text import Label
from engine.mathematics import Vec2, clamp
from engine.rendering import Translation
from engine.entities import Entity
import pyglet
from pyglet.window import key
import engine
import helpers
from decimal import Decimal
import random

window = pyglet.window.Window(caption="Fat Guys")
event_logger = pyglet.window.event.WindowEventLogger()
# window.push_handlers(event_logger)

rendering = engine.rendering.RenderingSystem()
cakes: List[engine.rendering.Sprite] = []
cake_positions: List[Vec2] = []
cake_image = pyglet.image.load(helpers.find_data_file("icon.png"))
engine.helpers.center_img(cake_image)
fat_dude_image = pyglet.image.load(helpers.find_data_file("homer-simpson.png"))
engine.helpers.center_img(fat_dude_image)

# for i in range(10):
#    cake_positions.append(position := Vec2(i * 50, (i * 25) + 100))
#    cakes.append(engine.rendering.Sprite(pyglet.sprite.Sprite(
#        cake_image), Translation("", position)))
missed_label = engine.rendering.Label(Label("Missed: 0", anchor_y="top"), Translation(
    "Missed", Vec2(Decimal(0), Decimal(window.height))))
points_label = engine.rendering.Label(Label("Points: 0", anchor_y="top", anchor_x="right"), Translation(
    "Points", Vec2(Decimal(window.width), Decimal(window.height))))
game_over_label = engine.rendering.Label(Label("GAME OVER", anchor_x="center", anchor_y="center", font_size=24), Translation(
    "GameOver", Vec2(Decimal(window.width) / 2, Decimal(window.height) * 2)))

dude_position: Vec2 = Vec2(window.width // 2, fat_dude_image.height // 2)
fat_dude = engine.rendering.Sprite(pyglet.sprite.Sprite(fat_dude_image),
                                   Translation("Fat Guy", dude_position))
time = Decimal(0)
missed = 0
got = 0
game_running = True
time_since_last_cake = Decimal(0)

holding_keys = {}


@window.event
def on_key_press(symbol: key, modifiers):
    global time, missed, got, game_running, game_over_label, time_since_last_cake
    holding_keys[symbol] = True
    if symbol == key.RETURN and not game_running:
        time = Decimal(0)
        missed = 0
        got = 0
        game_running = True
        game_over_label.update_translation(Translation("GameOver", Vec2(
            Decimal(window.width) / 2, Decimal(window.height) * 2)))
        time_since_last_cake = Decimal(0)
        for cake, cake_position in zip(list(cakes), list(cake_positions)):
            cakes.remove(cake)
            cake_positions.remove(cake_position)
            cake.sprite.visible = False
            cake.sprite.delete()
            cake.sprite = None
        missed_label.text = "Missed: 0"
        points_label.text = "Points: 0"
        dude_position.x, dude_position.y = window.width // 2, fat_dude_image.height // 2
        fat_dude.update_translation(Translation("Fat Guy", dude_position))


@window.event
def on_key_release(symbol: key, modifiers):
    holding_keys[symbol] = False


def aabb(a_pos: Vec2, a_size: Vec2, b_pos: Vec2, b_size: Vec2) -> bool:
    # Collision x-axis?
    collisionX = a_pos.x + a_size.x >= b_pos.x and b_pos.x + b_size.x >= a_pos.x
    # Collision y-axis?
    collisionY = a_pos.y + a_size.y >= b_pos.y and b_pos.y + b_size.y >= a_pos.y
    # Collision only if on both axes
    return collisionX and collisionY


def update(dt: float):
    global time, missed, got, game_running, time_since_last_cake
    window.clear()
    if game_running:
        time += Decimal(dt)
        time_since_last_cake += Decimal(dt)
        difficulty: Decimal = Decimal(2)**(((time+5)/10))

        if time_since_last_cake >= ((Decimal(1))/(2 ** (time/10))) * 3:
            time_since_last_cake = 0
            cake_positions.append(position := Vec2(
                random.randint(0, int(window.width)), window.height))
            cakes.append(engine.rendering.Sprite(
                pyglet.sprite.Sprite(cake_image), Translation("", position)))

        if holding_keys.get(key.A) or holding_keys.get(key.LEFT):
            dude_position.x -= 500 * dt
            dude_position.x = clamp(dude_position.x, 0, window.width)
            fat_dude.update_translation(Translation("Fat Guy", dude_position))

        if holding_keys.get(key.D) or holding_keys.get(key.RIGHT):
            dude_position.x += 500 * dt
            dude_position.x = clamp(dude_position.x, 0, window.width)
            fat_dude.update_translation(Translation("Fat Guy", dude_position))

        dead: List[engine.rendering.Sprite] = []
        dead_positions: List[Vec2] = []

        for cake, cake_position in zip(cakes, cake_positions):
            cake_position.y -= difficulty
            cake.update_translation(Translation("", cake_position))
            if cake_position.y < 10:
                dead.append(cake)
                dead_positions.append(cake_position)
                missed += 1
                missed_label.text = f"Missed: {missed}"
                if missed >= 8:
                    game_running = False
                    game_over_label.update_translation(Translation("GameOver", Vec2(
                        Decimal(window.width) / 2, Decimal(window.height) / 2)))
            elif aabb(Vec2(cake.sprite.x, cake.sprite.y), Vec2(cake.sprite.width, cake.sprite.height), Vec2(fat_dude.sprite.x, fat_dude.sprite.y), Vec2(fat_dude.sprite.width, fat_dude.sprite.height)):
                dead.append(cake)
                dead_positions.append(cake_position)
                got += 1
                points_label.text = f"Points: {got*100}"
        for dead_sprite in dead:
            dead_sprite.sprite.visible = False
            dead_sprite.sprite.delete()
            dead_sprite.sprite = None
            cakes.remove(dead_sprite)
        for dead_position in dead_positions:
            cake_positions.remove(dead_position)

    engine.entities.System.update_all()


pyglet.clock.schedule_interval(update, 1/120.0)


pyglet.app.run()
