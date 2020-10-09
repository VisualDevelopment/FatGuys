from engine import entities
from decimal import *
from engine.mathematics import *
import pyglet

sprite_batch: pyglet.graphics.Batch = pyglet.graphics.Batch()


class Translation(entities.Component):
    position: Vec2

    def __init__(self, name: str = "", position: Vec2 = Vec2()) -> None:
        super().__init__(name)
        self.position = position


class Sprite(entities.Entity):
    sprite: pyglet.sprite.Sprite

    def __init__(self, sprite: pyglet.sprite.Sprite, translation: Translation = Translation()) -> None:
        super().__init__()
        self.sprite = sprite
        self.sprite.batch = sprite_batch
        self.update_translation(translation)

    def update_translation(self, translation: Translation = Translation()) -> None:
        self.set_or_add_component(translation)
        self.sprite.update(translation.position.x, translation.position.y)


class RenderingSystem(entities.System):
    def update(self) -> None:
        sprite_batch.draw()
