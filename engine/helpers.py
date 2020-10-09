import pyglet


def center_img(img: pyglet.image.AbstractImage) -> None:
    img.anchor_x = img.width // 2
    img.anchor_y = img.height // 2
