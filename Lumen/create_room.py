import Lumen.tiles as tiles
import Lumen.lights as lights
from Lumen.window import Window
import random
import math

X = 10 # boxes it will be divided in
Y = 10
STANDARD_INTENSITY = 100
STANDARD_BEAM_ANGLE = 15


MINIMUM_FILL = 0.6

class Room:

    # externally called functions
    def __init__(self, width, height, length, obstacles, time):
        self.width = width
        self.height = height
        self.length = length
        self.tiles = []
        if random.random() > 0.5:
            x = random.choice([0, X-1])
            y = random.randint(2, Y-3)
        else:
            x = random.randint(2, X-3)
            y = random.choice([0, Y-1])
        self.window = Window(x, y, self.width//3, self.height//3, 2, 100, X, Y, time)
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
        
    def get_window_direct_light(self):
        return self.window.get_lit_coordinates()
        
    def get_window_shadow(self):
        self.window.sun_altitude

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
            

            min_x = max(0, pos_x - n_of_tiles_h_w)
            max_x = min(X - 1, pos_x + n_of_tiles_h_w)
            min_y = max(0, pos_y - n_of_tiles_h_l)
            max_y = min(Y - 1, pos_y + n_of_tiles_h_l)

            shadows = {}
            shadows_north, shadows_south, shadows_west, shadows_east = self.shadow_region_list(min_x, max_x, min_y, max_y, pos_x, pos_y, temp_radius)


            # Iterate over the search area and count the squares that are inside the circle
            for k in range(min_x, max_x + 1):
                for j in range(min_y, max_y + 1):
                    if self.tiles[k][j].give_status():
                        continue
                    
                    # check if the tile is in the shadow
                    shadow_perm = self.shadow_permeability(shadows_north,shadows_south,shadows_east,shadows_west,k,j)
                    dx = abs((k*(self.width/X)) - temp_x)
                    dy = abs((j*(self.length/Y)) - temp_y)
                    distance = math.sqrt(dx**2 + dy**2)

                    if distance <= temp_radius:
                        if temp_radius - distance >= 1 and shadow_perm[0]==1:
                            self.tiles[k][j].light_up()
                        elif shadow_perm[0]<1 and temp_radius - distance >= 1:
                            if shadow_perm[1]==2:
                                self.tiles[k][j].fill(5,shadow_perm[0])
                            elif shadow_perm[1]==4:
                                self.tiles[k][j].fill(7,shadow_perm[0])
                            else:
                                self.tiles[k][j].fill(shadow_perm[1],shadow_perm[0])
                        else:
                            fill = (temp_radius - distance)/(self.width/X)
                            self.fill_less_than_one(k,j,pos_x,pos_y,fill)
                            self.neighbourhood_lights(k,j,0.5)
         
        pass
    # internal functions
    def fill_less_than_one(self, k, j,pos_x,pos_y, fill):
        '''fills the tile at (x,y) with fill'''
        # self.tiles[x][y].fill(fill)
        if fill>=MINIMUM_FILL:
            self.tiles[k][j].light_up()
        elif j < pos_y and k == pos_x:
            # this means it is right above the light
            self.tiles[k][j].fill(5,fill)
        elif j > pos_y and k == pos_x:
            # right below
            self.tiles[k][j].fill(1,fill)
        elif j == pos_y and k < pos_x:
            # on the right
            self.tiles[k][j].fill(3,fill)
        elif j == pos_y and k > pos_x:
            # on the left
            self.tiles[k][j].fill(7,fill)
        elif j < pos_y and k < pos_x:
            # top right
            self.tiles[k][j].fill(4,fill)
        elif j < pos_y and k > pos_x:
            # top left
            self.tiles[k][j].fill(6,fill)
        elif j > pos_y and k < pos_x:
            # bottom right
            self.tiles[k][j].fill(2,fill)
        elif j > pos_y and k > pos_x:
            # bottom left
            self.tiles[k][j].fill(0,fill)
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
        direction_of_shadow = 0 # 0 for north, 1 for east, 2 for south, 3 for west
        if (direction == 0 or direction == 2) and y_light<=y_tile and x_light == x_tile:
            # north wall the light is above the tile
            direction_of_shadow = 0
            base = self.height - self.tiles[x_tile][y_tile].height
            perpendicular = (y_tile-y_light)*(self.length/Y)
            angle = math.tan(perpendicular/base)
            base2 = self.height * math.tan(angle)
            shadow_length = base2 - (x_light*(self.width/X))
        if (direction == 0 or direction ==2) and y_light>=y_tile and x_light == x_tile:
            # north wall the light is below the tile
            direction_of_shadow = 2
            base = self.height - self.tiles[x_tile][y_tile].height
            perpendicular = (y_light-y_tile)*(self.length/Y)
            angle = math.tan(perpendicular/base)
            base2 = self.height * math.tan(angle)
            shadow_length = base2 - ((X-x_light)*(self.width/X))
        if (direction == 1 or direction==3) and x_light>=x_tile and y_light == y_tile:
            # east wall the light is right of the tile
            direction_of_shadow = 1
            base = self.height - self.tiles[x_tile][y_tile].height
            perpendicular = (x_light-x_tile)*(self.width/X)
            angle = math.tan(perpendicular/base)
            base2 = self.height * math.tan(angle)
            shadow_length = base2 - ((Y-y_light)*(self.length/Y))
        if (direction == 1 or direction == 3) and x_light<=x_tile and y_light == y_tile:
            # east wall the light is left of the tile
            direction_of_shadow = 3
            base = self.height - self.tiles[x_tile][y_tile].height
            perpendicular = (x_tile-x_light)*(self.width/X)
            angle = math.tan(perpendicular/base)
            base2 = self.height * math.tan(angle)
            shadow_length = base2 - (y_light*(self.length/Y))

        return shadow_length, direction_of_shadow
    
    def shadow_region_list(self, min_x,max_x,min_y,max_y,x_light,y_light,radius):
        shadow_list_north = {}
        shadow_list_south = {}
        shadow_list_east = {}
        shadow_list_west = {}
        for i in range(min_x,max_x+1):
            for j in range(min_y,max_y+1):
                if self.tiles[i][j].obstacle == None or self.tiles[i][j].height == 0:
                        continue
                else:
                    temp = self.shadow_region(i,j,x_light,y_light,radius)
                    if temp[1] == 0:
                        shadow_list_north[(i,j)] = temp[0]
                        s_temp = temp[0]
                        for k in range(1,math.ceil(s_temp/(self.length/Y))):
                            if j+k > Y:
                                break
                            if (i,j+k) in shadow_list_north:
                                if shadow_list_north[(i,j+k)] > s_temp:
                                    s_temp = s_temp - (self.length/Y)
                                    continue
                            shadow_list_north[(i,j+k)] = s_temp
                            s_temp = s_temp - (self.length/Y)
                    elif temp[1] == 1:
                        shadow_list_south[(i,j)] = temp[0]
                        s_temp = temp[0]
                        for k in range(1,math.ceil(s_temp/(self.length/Y))):
                            if j-k < 0:
                                break
                            if (i,j-k) in shadow_list_south:
                                if shadow_list_south[(i,j-k)] > s_temp:
                                    s_temp = s_temp - (self.length/Y)
                                    continue
                            shadow_list_south[(i,j-k)] = s_temp
                            s_temp = s_temp - (self.length/Y)
                    elif temp[1] == 2:
                        shadow_list_east[(i,j)] = temp[0]
                        s_temp = temp[0]
                        for k in range(1,math.ceil(s_temp/(self.width/X))):
                            if i+k > X:
                                break
                            if (i+k,j) in shadow_list_east:
                                if shadow_list_east[(i+k,j)] > s_temp:
                                    s_temp = s_temp - (self.width/X)
                                    continue
                            shadow_list_east[(i+k,j)] = s_temp
                            s_temp = s_temp - (self.width/X)     
                    elif temp[1] == 3:
                        shadow_list_west[(i,j)] = temp[0]
                        s_temp = temp[0]
                        for k in range(1,math.ceil(s_temp/(self.width/X))):
                            if i-k < 0:
                                break
                            if (i-k,j) in shadow_list_west:
                                if shadow_list_west[(i-k,j)] > s_temp:
                                    s_temp = s_temp - (self.width/X)
                                    continue
                            shadow_list_west[(i-k,j)] = s_temp
                            s_temp = s_temp - (self.width/X)
        return shadow_list_north, shadow_list_east, shadow_list_south, shadow_list_west
    
    def shadow_permeability(self,s_north,s_south,s_east,s_West,x,y):
        if (x,y) in s_north:
            if s_north[(x,y)] > 1:
                return (0,1)
            else:
                return (1-s_north[(x,y)],1)
        elif (x,y) in s_south:
            if s_south[(x,y)] > 1:
                return (0,1)
            else:
                return (1-s_south[(x,y)],1)
        elif (x,y) in s_east:
            if s_east[(x,y)] > 1:
                return (0,1)
            else:
                return (1-s_east[(x,y)],1)
        elif (x,y) in s_West:
            if s_West[(x,y)] > 1:
                return (0,1)
            else:
                return (1-s_West[(x,y)],1)
        else:
            return (1,1)

    def neighbourhood_lights(self,x,y, intensity):
        if intensity < 0.2:
            return
        elif (x <= 0) or (y <= 0) or (x >= X) or (y >= Y):
            return
        else:
            self.tiles[x][y].less_intense_lit(intensity)
            self.neighbourhood_lights(x+1,y,intensity-0.2)
            self.neighbourhood_lights(x-1,y,intensity-0.2)
            self.neighbourhood_lights(x,y+1,intensity-0.2)
            self.neighbourhood_lights(x,y-1,intensity-0.2)

    
    
             

    

        
# room = Room(100, 100, 10)
# print(room.tiles)
        