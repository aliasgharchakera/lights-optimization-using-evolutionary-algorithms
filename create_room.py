import tiles
import lights

X = 10 # boxes it will be divided in
Y = 10
STANDARD_INTENSITY = 100
STANDARD_BEAM_ANGLE = 45

MINIMUM_INTENSITY = 0.5

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
        print(self.lights)
        print(self.tiles)

    def add_obstacle(self, x, y, obstacle):
        '''obstacle is 0 for north wall, 1 for east wall, 2 for south wall, 3 for west wall
        height is 0 for flat and >0 for raised'''
        self.tiles[x][y].create_obstacle(obstacle, 0)

    def light_light(self, x, y):
        '''lights up the light at (x,y)'''
        self.lights[x][y].light()

    def reset_lights(self):
        '''turns off all the lights'''
        for i in range(X):
            for j in range(Y):
                self.lights[i][j].unlight()
        
    
    def get_light_functions(self):
        '''returns a list of tuples of the form (distance_on_width, distance_on_length, radius)'''
        light_functions = []
        for i in range(X):
            for j in range(Y):
                if self.lights[i][j].give_status():
                    light_functions.append(self.lights[i][j].give_light_functions(self.width,X, self.length,Y))
        # distance_on_width, distance_on_length, radius
        return light_functions
    
    def reset_tiles(self):
        '''lights down all the tiles'''
        for i in range(X):
            for j in range(Y):
                self.tiles[i][j].light_down()
    
    def light_tiles(self):
        '''lights up all the tiles that are lit'''
        light_functions = self.get_light_functions()

        for i in range(len(light_functions)):
            temp_x = light_functions[i][0]
            temp_y = light_functions[i][1]
            temp_radius = light_functions[i][2]

            # add all the tiles that are lit
            pos_x = (self.width/X)*temp_x
            pos_y = (self.length/Y)*temp_y
        
                
        pass
    def num_lit_tiles(self):
        '''returns the number of tiles that are lit'''
        pass

    

        
room = Room(100, 100, 10)
print(room.tiles)
        