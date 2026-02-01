import pandas as pd
from .utils import import_image, sub_image, SCALE_FACTOR


class DungeonTileset(object):
    """
    Manages dungeon wall tiles and backgrounds.

    Attributes:
        wallset_images: DataFrame containing the wallset images
        wall_tiles: DataFrame containing the wall tiles
    """

    def __init__(self):
        # Create a dataframe from the csv file and load each image into the DataFrame
        wallset_images = pd.read_csv('data/imagefiles.csv')
        wallset_images['Image'] = None
        wallset_images = wallset_images.set_index(['File'])

        for i in wallset_images.index:
            wallset_images.loc[i, ['Image']] = import_image('Environments', i)

        self.wallset_images = wallset_images

        # Load sprites.csv with sprite coordinates
        sprites = pd.read_csv('data/sprites.csv')
        sprites = sprites.set_index(['SpriteName'])
        sprites = sprites.astype({
            'Xpos': int, 'Ypos': int, 'Width': int, 'Height': int
        })

        # Load panels.csv with panel blit positions (only need Blit_Xpos and Blit_Ypos)
        panels = pd.read_csv('data/panels.csv')
        panels = panels[['Panel', 'Blit_Xpos', 'Blit_Ypos']]
        panels = panels.set_index(['Panel'])
        panels = panels.astype({
            'Blit_Xpos': int, 'Blit_Ypos': int
        })

        # Load tiles.csv and join with sprites and panels
        wall_tiles = pd.read_csv('data/tiles.csv')
        # Use left join to keep tiles even if SpriteName is empty/missing
        wall_tiles = wall_tiles.join(sprites, on='SpriteName', how='left')
        wall_tiles = wall_tiles.join(panels, on='Panel')
        wall_tiles = wall_tiles.set_index(['Environment', 'Wall', 'Panel'])
        wall_tiles = wall_tiles.astype({
            'Flip': bool,
            'Blit_Xpos_Offset': int,
            'Blit_Ypos_Offset': int
        })

        # Create new column for Image
        wall_tiles['Image'] = None

        # Loop over the dataframe and create images
        for i in wall_tiles.index:
            # Skip tiles with no sprite assigned (empty SpriteName)
            sprite_name = wall_tiles.loc[i, 'SpriteName']
            if pd.isna(sprite_name) or sprite_name == '':
                continue

            loc_size = (
                wall_tiles.loc[i, ['Xpos']].item(),
                wall_tiles.loc[i, ['Ypos']].item(),
                wall_tiles.loc[i, ['Width']].item(),
                wall_tiles.loc[i, ['Height']].item()
            )
            flip = wall_tiles.loc[i, ['Flip']].item()
            wall_tiles.loc[i, ['Image']] = sub_image(
                wallset_images.loc[wall_tiles.loc[i, ['File']].item(), ['Image']].item(),
                loc_size, flip=flip
            )

        self.wall_tiles = wall_tiles

    def image(self, environment, wall, panel):
        return self.wall_tiles.loc[(environment, wall, panel), ['Image']].item()

    def blit_pos(self, environment, wall, panel):
        row = self.wall_tiles.loc[(environment, wall, panel)]
        blit_pos = (
            (row['Blit_Xpos'] + row['Blit_Xpos_Offset']) * SCALE_FACTOR,
            (row['Blit_Ypos'] + row['Blit_Ypos_Offset']) * SCALE_FACTOR
        )
        return blit_pos
