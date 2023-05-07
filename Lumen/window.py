import ephem
import math
import pytz
from datetime import datetime

LATITUDE = '24.8607'  # latitude of Karachi
LONGITUDE = '67.0011'  # longitude of Karachi
SUN_MAX = 100

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

    def get_lit_coordinates(self):
        lit_coordinates = []
        # calculate the starting and ending coordinates of the lit region
        if self.direction == 'w':
            start_x = 0
            end_x = self.width
            start_y = self.y
            end_y = self.y + self.length
        elif self.direction == 'e':
            start_x = self.room_width - self.width
            end_x = self.room_width
            start_y = self.y
            end_y = self.y + self.length
        elif self.direction == 'n':
            start_x = self.x
            end_x = self.x + self.width
            start_y = 0
            end_y = self.length
        elif self.direction == 's':
            start_x = self.x
            end_x = self.x + self.width
            start_y = self.room_length - self.length
            end_y = self.room_length
        
        # iterate through each point in the lit region
        for x in range(start_x, end_x):
            for y in range(start_y, end_y):
                # calculate the angle between the window and the point
                dx = (self.x + self.width/2) - x
                dy = (self.y + self.length/2) - y
                dz = self.height
                dot_product = dx*math.cos(math.radians(self.sun_azimuth)) + dy*math.sin(math.radians(self.sun_azimuth))
                angle = math.degrees(math.acos(dot_product/(math.sqrt(dx**2+dy**2+dz**2))))
                # if the angle is less than the sun's altitude, the point is lit
                if angle < self.sun_altitude:
                    lit_coordinates.append((x,y))
        return lit_coordinates


x = 30
y = 100
width = 25
length = 20
height = 5
room_width = 100
room_length = 100
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
