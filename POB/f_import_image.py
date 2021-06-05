import sys
import os
import pygame as pg

def import_image(assetClass, fileName, scaleFactor=3, flip=False):

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

def sub_image(image,locSize, scaleFactor=3, flip=False):
    #SurfaceWH = (locSize[2:3])
    locSize = (locSize[0]*scaleFactor,locSize[1]*scaleFactor,locSize[2]*scaleFactor,locSize[3]*scaleFactor)
    img = pg.Surface(locSize[2:])
    img.fill((255,0,255))
    img.blit(image,(0,0),locSize)

    if flip:
        img = pg.transform.flip(img, True, False)

    img.set_colorkey((255,0,255), pg.RLEACCEL)
    return img

def import_sub_image(assetClass, fileName, scaleFactor=3, flip=False):

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