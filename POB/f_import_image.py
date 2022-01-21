import sys
import os
import pygame as pg


# import_image = Imports an image from a file on the local hdd, scales it up in size and flips it if desired.
def import_image(assetClass, fileName, scaleFactor=3, flip=False):
    # assetClass   = The Class of image to import (IE Environments, UI, Items etc)
    # fileName     = The name of the image file to import
    # scaleFactor  = The factor to multiply the image size by. Default is 3.
    # flip         = Whether to flip the image horizontally or not. 

    path = os.path.join('Assets',assetClass, fileName)
    img = pg.image.load(path)

    if flip:
        img = pg.transform.flip(img, True, False)

    if scaleFactor != 1:
        imgWH = (img.get_width()*scaleFactor,img.get_height()*scaleFactor)
        img = pg.transform.scale(img, imgWH)

    img.set_colorkey((255,0,255), pg.RLEACCEL)
    img = img.convert()

    return img

# sub_image = crops and returns an image.
def sub_image(image,locSize, scaleFactor=3, flip=False):
    # image     = the image to crop
    # locSize   = a tuple containing the (x,y,width,height) of subimage
    # flip         = Whether to flip the image horizontally or not. 

    locSize = (locSize[0]*scaleFactor,locSize[1]*scaleFactor,locSize[2]*scaleFactor,locSize[3]*scaleFactor)
    img = pg.Surface(locSize[2:])
    img.fill((255,0,255))
    img.blit(image,(0,0),locSize)

    if flip:
        img = pg.transform.flip(img, True, False)

    img.set_colorkey((255,0,255), pg.RLEACCEL)
    return img

def import_sub_image(assetClass, fileName, locSize, scaleFactor=3, flip=False):

    img = import_image(assetClass, fileName, scaleFactor, flip)
    img = sub_image(img,locSize,scaleFactor,flip)

    return img