from globals import IU_ASSET_DIR
import pygame as pg
from os import listdir, sep
from os.path import isfile, join
import logger

# A dictionary allowing key/pair access for entities to load sprite data from a
# keyword, we can then use globals (or whatever to change the names of these keys
# as needed if naming convention changes later on or load method changes
IMAGE_LIBRARY = {}

# This will preload all images used in game
# two schools of thought on this,
#   - load all assets at the begining of the game (standard loading screen)
#   - load all assets at the start of a level (more akin to a 3D game load)
#   - load assets as they are needed
def load_images():
    for file in listdir(IU_ASSET_DIR):
        try:
            asset = join(IU_ASSET_DIR, file)
            if isfile(asset):
                IMAGE_LIBRARY[file.split(sep)[-1]] = pg.image.load(asset)
            else:
                logger.log("image utilities | could not load : {}".format(asset))
        except Exception as e:
            logger.log("!!! EXCEPTION !!!\nimage utilities\n\t{}".format(e))


def get_image(image_name):
    if image_name not in IMAGE_LIBRARY.keys():
        try:
            IMAGE_LIBRARY[image_name] = pg.image.load(join(IU_ASSET_DIR, image_name))
        except Exception as e:
            logger.log("!!! EXCEPTION !!!\nimage utilities\n\t{}".format(e))
    return IMAGE_LIBRARY[image_name]

