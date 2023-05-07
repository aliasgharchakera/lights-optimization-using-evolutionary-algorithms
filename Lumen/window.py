import ephem
import math
import pytz
from datetime import datetime

LATITUDE = '24.8607'  # latitude of Karachi
LONGITUDE = '67.0011'  # longitude of Karachi
SUN_MAX = 100
X = 10 # boxes it will be divided in
Y = 10

class Window:
    def __init__(self, x, y, width, length, height, room_width, room_length, time):
        self.x = x
        self.y = y
        self.width = width
        self.intensity = SUN_MAX
        self.length = length
        self.height = height
        self.room_width = room_width
        
        self.room_length = room_length
        self.time = time
        self.direction = ''
        # determine the direction of the window using x and y
        if self.y == 0:
            self.direction = 'w'
        elif self.y == room_length:
            self.direction = 'e'
        elif self.x == 0:
            self.direction = 'n'
        elif self.x == room_width:
            self.direction = 's'
            

        # use PyEphem to calculate the sun's position
        o = ephem.Observer() 
        
        tz = pytz.timezone('Asia/Karachi')
        local_time = datetime(2023, 5, 7, time)
        utc_time = tz.localize(local_time).astimezone(pytz.utc)
        o.date = ephem.Date(utc_time) 
        
        o.lat = LATITUDE 
        o.long = LONGITUDE
        o.elevation = self.height  # elevation of the window
        # o.date = ephem.Date('2023/5/7 ' + str(self.time) + ':00:00')  # date and time of the observation
        sun = ephem.Sun()
        sun.compute(o)
        self.sun_altitude = math.degrees(sun.alt) # altitude of the sun in degrees
        self.sun_azimuth = math.degrees(sun.az)  # azimuth of the sun in degrees
        print('time: ', time,'sun_altitude: ', self.sun_altitude, 'sun_azimuth: ', self.sun_azimuth)


    def calculate_surface_area(self):
        pass
        
    def get_lit_coordinates(self):
        width_of_tile = self.room_width/X
        length_of_tile = self.room_length/Y
        lit_coordinates = []
        # calculate the starting and ending coordinates of the lit region
        if self.direction == 'w':
            start_x = 0
            end_x = self.width/width_of_tile
            start_y = self.y
            end_y = min(Y,self.y + self.length/length_of_tile)
        elif self.direction == 'e':
            start_x = max(self.room_width - self.width/width_of_tile, 0)
            end_x = X
            start_y = self.y
            end_y = min(Y, self.y + self.length/length_of_tile)
        elif self.direction == 'n':
            start_x = self.x
            end_x = min(X, self.x + self.width/width_of_tile)
            start_y = 0
            end_y = self.length/length_of_tile
        elif self.direction == 's':
            start_x = self.x
            end_x = min(X, self.x + self.width/width_of_tile)
            start_y = max(self.room_length - self.length/length_of_tile, 0)
            end_y = Y
        
        # iterate through each point in the lit region
        # for x in range(int(start_x), int(end_x)):
        #     for y in range(int(start_y),int(end_y)):
        for x in range(X):
            for y in range(Y):
                # calculate the angle between the window and the point
                dx = (self.x*width_of_tile + self.width/2) - x
                dy = (self.y*length_of_tile + self.length/2) - y
                dz = self.height + self.length
                dot_product = dx*math.cos(math.radians(self.sun_azimuth)) + dy*math.sin(math.radians(self.sun_azimuth))
                angle = math.degrees(math.acos(dot_product/(math.sqrt(dx**2+dy**2+dz**2))))
                # if the angle is less than the sun's altitude, the point is lit
                if angle < self.sun_altitude:
                    lit_coordinates.append((x,y))
        return lit_coordinates
    
    def get_length_shadow(self):
        # we are assuming that the sun at all times is right in front of the window 
        # for a more accurate result you may use a more accurate description of sunlight 
        start_length_sun = self.height * math.tan(math.radians(self.sun_altitude))
        stop_length_sun = (self.height + self.length) * math.tan(math.radians(self.sun_altitude))
        # 0 -> the starting of the direct sunlight 
        # 1 -> the end of the direct sunlight
        return start_length_sun, stop_length_sun
    
    def get_width_shadow(self):
        return self.width
    
    def calculate_direct_sunlight(self):
        starting_sun_light, ending_sun_light = self.get_length_shadow()
        width_of_tile = self.room_width/X
        length_of_tile = self.room_length/Y

        start_x = 0
        end_x = 0
        start_y = 0
        end_y = 0

        # calculate the starting and ending coordinates of the lit region
        if self.direction == 'w':
            start_x = self.x
            end_x = min(X, self.x + math.ceil(self.width/width_of_tile))
            start_y = min(Y,0 + math.ceil(starting_sun_light/length_of_tile))
            end_y = min(Y,math.ceil(starting_sun_light/length_of_tile) + math.ceil(ending_sun_light/length_of_tile))
        elif self.direction == 'e':
            start_x = self.x
            end_x = min(X, self.x + math.ceil(self.width/width_of_tile))
            start_y = max(0,Y - math.ceil(starting_sun_light/length_of_tile))
            end_y = max(0, Y - math.ceil(starting_sun_light/length_of_tile)  - math.ceil(ending_sun_light/length_of_tile))
        elif self.direction == 'n':
            start_x = min(X, 0 + math.ceil(starting_sun_light/width_of_tile))
            end_x = min(X, math.ceil(starting_sun_light/width_of_tile) + math.ceil(ending_sun_light/width_of_tile))
            start_y = self.y
            end_y = min(Y, self.y + math.ceil(self.length/length_of_tile))
        elif self.direction == 's':
            start_x = max(0, X - math.ceil(starting_sun_light/width_of_tile))
            end_x = max(0, X - math.ceil(starting_sun_light/width_of_tile) - math.ceil(ending_sun_light/width_of_tile))
            start_y = self.y
            end_y = self.y + math.ceil(self.length/length_of_tile)

        return start_x, end_x, start_y, end_y, self.direction

        




x = 0
y = 2
width = 3
length = 2
height = 2
room_width = 10
room_length = 10
# time = 12
for time in range(24):
    window = Window(x, y, width, length, height, room_width, room_length, time)
    # window.calculate_direct_sunlight_region()
    # print(window.calculate_direct_sunlight_region())
    # window.get_lit_coordinates()
    print(window.get_lit_coordinates())
    
# # create a window
# window = Window(x=0, y=0, width=2, height=2, elevation=0, intensity=1, room_width=10, room_length=10, time=21)

# # calculate direct sunlight
# direct_sunlight_grid = window.calculate_direct_sunlight(cell_size=1)

# # print the grid
# for row in direct_sunlight_grid:
#     print(row)
