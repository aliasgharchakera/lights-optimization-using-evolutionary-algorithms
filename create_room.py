import tiles
import lights

X = 10 # boxes it will be divided in
Y = 10
STANDARD_INTENSITY = 100
STANDARD_BEAM_ANGLE = 45

class Room:

    def __init__(self, width, height, length):
        self.width = width
        self.height = height
        self.length = length
        self.tiles = []
        for i in range(X):
            temp = []
            for j in range(Y):
                temp.append(tiles.Tile(i, j, None, 0))
                # self.tiles.append(tiles.Tile(i, j, 0, 0))
            self.tiles.append(temp)
        self.lights = []
        for i in range(X):
            temp = []
            for j in range(Y):
                temp.append(lights.Lights(i, j, STANDARD_INTENSITY, self.height, STANDARD_BEAM_ANGLE))
            self.lights.append(temp)

    def create_tiles(self, x, y, obstacle, height):
        self.tiles.append(tiles.Tile(x, y, obstacle, height))

    def add_obstacle(self, x, y, obstacle):
        '''obstacle is 0 for north wall, 1 for east wall, 2 for south wall, 3 for west wall
        height is 0 for flat and >0 for raised'''
        self.tiles[x][y].create_obstacle(obstacle, 0)

    def num_lit_tiles(self):
        # returns the number of tiles that are lit
        pass

    

    def light_lights(self, x,y):
        # lights up the light on that coordinate 
        self.lights[x*self.width + y].light()

        


        