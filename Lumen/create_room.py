import Lumen.tiles as tiles
import Lumen.lights as lights
import math

X = 10 # boxes it will be divided in
Y = 10
STANDARD_INTENSITY = 100
STANDARD_BEAM_ANGLE = 45

MINIMUM_INTENSITY = 0.5
MINIMUM_FILL = 0.6

class Room:

    # externally called functions
    def __init__(self, width, height, length, obstacles):
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
        for c in obstacles:
            self.add_obstacle(c[0], c[1],c[2],c[3])
        # print(self.lights)
        # print(self.tiles)

    def num_lit_tiles(self):
        # returns the number of tiles that are lit
        count = 0
        for i in range(X):
            for j in range(Y):
                if self.tiles[i][j].give_status():
                    count+=1
                else:
                    temp = 0
                    for k in range(8):
                        temp +=self.tiles[i][j].fill_vessel[k]
                    if temp >= MINIMUM_FILL:
                        count+=1
        return count

    def reset(self):
        '''resets the room'''
        self.reset_lights()
        self.reset_tiles()
    
    def light_tiles(self):
        '''lights up all the tiles that are lit'''
        light_functions = self.get_light_functions()
        base_tile_Width = self.width/X
        base_tile_Length = self.length/Y
        for i in range(len(light_functions)):
            temp_x = light_functions[i][0]
            temp_y = light_functions[i][1]
            temp_radius = light_functions[i][2]

            # add all the tiles that are lit
            pos_x = light_functions[i][4]
            pos_y = light_functions[i][5]

            n_of_tiles_h_w = math.ceil(temp_radius/(self.width/X))
            n_of_tiles_h_l = math.ceil(temp_radius/(self.length/Y))
            # calculate tiles in shadow from any obstacle
            # angle_of_light_on_obstacle = 
            
            # shadows 
            shadows = []
            shadows_cordinates = []
            for k in range(n_of_tiles_h_w):
                for j in range(n_of_tiles_h_l):
                    try:
                        if self.tiles[pos_x+k][pos_y+j].obstacle==None or self.tiles[pos_x+k][pos_y+j].height == 0:
                            pass
                        else:
                            pass
                    except:
                        print("error")
                        print(pos_x+k,pos_y+j)
                        print(X,Y)

                    if self.tiles[pos_x+k][pos_y+j].obstacle == None or self.tiles[pos_x+k][pos_y+j].height == 0:
                        continue
                    else:
                        temp = self.shadow_region(k, j, pos_x, pos_y, temp_radius)
                        if temp > 0:
                            shadows.append([temp,temp/(self.width/X),temp/(self.length/Y),self.tiles[pos_x+k][pos_y+j].obstacle])
                            # shadow length, shadow length on width tiles, shadow length on length tiles, obstacle
                            shadows_cordinates.append([k,j])

            min_x = max(0, pos_x - n_of_tiles_h_w)
            max_x = min(X - 1, pos_x + n_of_tiles_h_w)
            min_y = max(0, pos_y - n_of_tiles_h_l)
            max_y = min(Y - 1, pos_y + n_of_tiles_h_l)

            # Iterate over the search area and count the squares that are inside the circle
            for k in range(min_x, max_x + 1):
                for j in range(min_y, max_y + 1):
                    if self.tiles[k][j].give_status():
                        continue
                    dx = abs((k*(self.width/X)) - temp_x)
                    dy = abs((j*(self.length/Y)) - temp_y)
                    distance = math.sqrt(dx**2 + dy**2)

                    if distance <= temp_radius:
                        if temp_radius - distance >= 1:
                            self.tiles[k][j].light_up()
                        else:
                            fill = (temp_radius - distance)/(self.width/X)
                            if fill>=MINIMUM_FILL:
                                self.tiles[k][j].light_up()
                            elif j < pos_y and k == pos_x:
                                # this means it is right above the light
                                self.tiles[k][j].fill(fill,5)
                            elif j > pos_y and k == pos_x:
                                # right below
                                self.tiles[k][j].fill(fill,1)
                            elif j == pos_y and k < pos_x:
                                # on the right
                                self.tiles[k][j].fill(fill,3)
                            elif j == pos_y and k > pos_x:
                                # on the left
                                self.tiles[k][j].fill(fill,7)
                            elif j < pos_y and k < pos_x:
                                # top right
                                self.tiles[k][j].fill(fill,4)
                            elif j < pos_y and k > pos_x:
                                # top left
                                self.tiles[k][j].fill(fill,6)
                            elif j > pos_y and k < pos_x:
                                # bottom right
                                self.tiles[k][j].fill(fill,2)
                            elif j > pos_y and k > pos_x:
                                # bottom left
                                self.tiles[k][j].fill(fill,8)
         
        pass
    # internal functions
    def add_obstacle(self, x, y, obstacle, height):
        '''obstacle is 0 for north wall, 1 for east wall, 2 for south wall, 3 for west wall
        height is 0 for flat and >0 for raised'''
        self.tiles[x][y].create_obstacle(obstacle, height)

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
                    light_functions.append(self.lights[i][j].give_light_functions(self.width,X, self.length,Y,i,j))
        # distance_on_width, distance_on_length, radius
        return light_functions
    
    def reset_tiles(self):
        '''lights down all the tiles'''
        for i in range(X):
            for j in range(Y):
                self.tiles[i][j].light_down()
                self.tiles[i][j].fill_vessel = [0]*8

    def shadow_region(self, x_tile, y_tile,x_light, y_light, radius):
        # returns dimensions of the shadow region
        shadow_length = 0
        direction = self.tiles[x_tile][y_tile].obstacle
        if (direction == 0 or direction == 2) and y_light<=y_tile and x_light == x_tile:
            # north wall the light is above the tile
            base = self.height - self.tiles[x_tile][y_tile].height
            perpendicular = (y_tile-y_light)*(self.length/Y)
            angle = math.tan(perpendicular/base)
            base2 = self.height * math.tan(angle)
            shadow_length = base2 - (x_light*(self.width/X))
        if (direction == 0 or direction ==2) and y_light>=y_tile and x_light == x_tile:
            # north wall the light is below the tile
            base = self.height - self.tiles[x_tile][y_tile].height
            perpendicular = (y_light-y_tile)*(self.length/Y)
            angle = math.tan(perpendicular/base)
            base2 = self.height * math.tan(angle)
            shadow_length = base2 - ((X-x_light)*(self.width/X))
        if (direction == 1 or direction==3) and x_light>=x_tile and y_light == y_tile:
            # east wall the light is right of the tile
            base = self.height - self.tiles[x_tile][y_tile].height
            perpendicular = (x_light-x_tile)*(self.width/X)
            angle = math.tan(perpendicular/base)
            base2 = self.height * math.tan(angle)
            shadow_length = base2 - ((Y-y_light)*(self.length/Y))
        if (direction == 1 or direction == 3) and x_light<=x_tile and y_light == y_tile:
            # east wall the light is left of the tile
            base = self.height - self.tiles[x_tile][y_tile].height
            perpendicular = (x_tile-x_light)*(self.width/X)
            angle = math.tan(perpendicular/base)
            base2 = self.height * math.tan(angle)
            shadow_length = base2 - (y_light*(self.length/Y))

        return shadow_length
    
             

    

        
# room = Room(100, 100, 10)
# print(room.tiles)
        