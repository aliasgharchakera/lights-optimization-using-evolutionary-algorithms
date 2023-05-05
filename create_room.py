import tiles
import lights

STANDARD_INTENSITY = 100
STANDARD_BEAM_ANGLE = 45

class Room:

    def __init__(self, width, height, length):
        self.width = width
        self.height = height
        self.length = length
        self.tiles = []
        for i in range(self.width):
            for j in range(self.length):
                self.tiles.append(tiles.Tile(i, j, 0, 0))
        self.lights = []
        for i in range(self.width):
            for j in range(self.length):
                # create nested lists for these 
                self.lights.append(lights.Lights(i, j, STANDARD_INTENSITY, self.height))

    def create_tiles(self, x, y, obstacle, height):
        self.tiles.append(tiles.Tile(x, y, obstacle, height))

    def num_lit_tiles(self):
        # returns the number of tiles that are lit
        pass

    

    def light_lights(self, x,y):
        # lights up the light on that coordinate 
        self.lights[x*self.width + y].light()

        


        