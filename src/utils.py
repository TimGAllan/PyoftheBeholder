import os
import pygame as pg

# Global scale factor for rendering (original 320x200 scaled up)
SCALE_FACTOR = 3


def import_image(assetClass, fileName, scaleFactor=None, flip=False):
    """
    Import an image from a file, scale it up and optionally flip it.

    Args:
        assetClass: The class of image to import (e.g., Environments, UI, Items)
        fileName: The name of the image file to import
        scaleFactor: The factor to multiply the image size by. Default is SCALE_FACTOR.
        flip: Whether to flip the image horizontally or not.
    """
    if scaleFactor is None:
        scaleFactor = SCALE_FACTOR

    path = os.path.join('assets', assetClass, fileName)
    img = pg.image.load(path)

    if flip:
        img = pg.transform.flip(img, True, False)

    if scaleFactor != 1:
        img_size = (img.get_width() * scaleFactor, img.get_height() * scaleFactor)
        img = pg.transform.scale(img, img_size)

    img.set_colorkey((255, 0, 255), pg.RLEACCEL)
    img = img.convert()

    return img


def sub_image(image, loc_size, scaleFactor=None, flip=False):
    """
    Crop and return a sub-image.

    Args:
        image: The image to crop
        loc_size: A tuple containing the (x, y, width, height) of subimage
        scaleFactor: The scale factor applied to the source image. Default is SCALE_FACTOR.
        flip: Whether to flip the image horizontally or not.
    """
    if scaleFactor is None:
        scaleFactor = SCALE_FACTOR

    loc_size = (
        loc_size[0] * scaleFactor,
        loc_size[1] * scaleFactor,
        loc_size[2] * scaleFactor,
        loc_size[3] * scaleFactor
    )
    img = pg.Surface(loc_size[2:])
    img.fill((255, 0, 255))
    img.blit(image, (0, 0), loc_size)

    if flip:
        img = pg.transform.flip(img, True, False)

    img.set_colorkey((255, 0, 255), pg.RLEACCEL)
    return img


