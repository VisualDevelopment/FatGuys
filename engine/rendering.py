from engine import entities
from decimal import *
from engine.mathematics import *
import pyglet, pyglet.sprite as pyglet_sprite, pyglet.text as pyglet_text

sprite_batch: pyglet.graphics.Batch = pyglet.graphics.Batch()


class Translation(entities.Component):
    position: Vec2

    def __init__(self, name: str = "", position: Vec2 = Vec2()) -> None:
        super().__init__(name)
        self.position = position


class Sprite(entities.Entity):
    sprite: pyglet_sprite.Sprite

    def __init__(self, sprite: pyglet_sprite.Sprite, translation: Translation = Translation()) -> None:
        super().__init__()
        self.sprite = sprite
        self.sprite.batch = sprite_batch
        self.update_translation(translation)

    def update_translation(self, translation: Translation = Translation()) -> None:
        self.set_or_add_component(translation)
        self.sprite.update(translation.position.x, translation.position.y)

class Label(entities.Entity):
    label: pyglet_text.Label

    def __init__(self, label: pyglet_text.Label, translation: Translation = Translation()) -> None:
        super().__init__()
        self.label = label
        self.label.batch = sprite_batch
        self.update_translation(translation)

    def update_translation(self, translation: Translation = Translation()) -> None:
        self.set_or_add_component(translation)
        self.label.x, self.label.y = (float(translation.position.x), float(translation.position.y))

    @property
    def text(self) -> str:
        return self.label.text
    
    @text.setter
    def text(self, text: str):
        self.label.text = text

    @property
    def visible(self) -> bool:
        return self.label.visible
    
    @visible.setter
    def visible(self, visible: bool):
        self.label.visible = visible

class RenderingSystem(entities.System):
    def update(self) -> None:
        sprite_batch.draw()
