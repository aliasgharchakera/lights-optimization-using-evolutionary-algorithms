import ephem
import math

class Window:
    def __init__(self, x, y, width, length, height, intensity, room_width, room_length, time):
        self.x = x
        self.y = y
        self.width = width
        self.intensity = intensity
        self.length = length
        self.height = height
        self.room_width = room_width
        self.room_length = room_length
        self.position = (self.x, self.y)
        self.time = time
        self.direction = ''
        # [[0, 0], [0,1]
        #  [1, 0], [1,1]]
        # determine the direction of the window using x and y
        if self.y == 0:
            self.direction = 'w'
        elif self.y == room_width:
            self.direction = 'e'
        elif self.x == 0:
            self.direction = 'n'
        elif self.x == room_length:
            self.direction = 's'

        # use PyEphem to calculate the sun's position
        o = ephem.Observer() 
        # 31.5204° N, 74.3587° E
        o.lat = '31.5204'  # latitude of Karachi
        o.long = '74.3587'  # longitude of Karachi
        o.elevation = self.height  # elevation of the window
        time2 = "{:02d}:00".format(time)
        # time += 5
        o.date = ephem.Date('2023/5/7 ' + time2 + ':00:00')  # date and time of the observation
        print(o.date)
        sun = ephem.Sun()
        sun.compute(o)
        self.sun_altitude = math.degrees(sun.alt) # altitude of the sun in degrees
        # print(self.sun_altitude)
        # self.sun_angle = (12 - self.time) * 15
        # sun_elevation = math.radians(90 - self.sun_angle)
        # sunlight_x = (self.room_width / 2) + ((self.room_length / 2) / math.tan(sun_elevation))
        # print(self.sun_altitude, self.sun_angle, self.time) 
        # self.sun_altitude = 150
        # self.sun_azimuth = math.degrees(sun.az)  # azimuth of the sun in degrees
        

    def calculate_direct_sunlight_region(self):
        direct_sunlight_region = []

        # calculate the position of the sun based on the time of day
        sun_elevation = math.radians(self.sun_altitude)
        sunlight_x = (self.room_width / 2) + ((self.room_length / 2) / math.tan(sun_elevation))
        print('sun_altitude', self.sun_altitude, 'sun_elevation', sun_elevation, 'sunlight_x', sunlight_x)
        # print('sun_elevation', sun_elevation, 'sunlight_x', sunlight_x)

        # check if the sunlight is to the left of the room
        if sunlight_x < 0:
            # check if the window faces west
            if self.direction == 'w':
                direct_sunlight_region.append((self.x, self.y))
                direct_sunlight_region.append((self.x, self.y + self.length))
            else:
                direct_sunlight_region = []
        # check if the sunlight is to the right of the room
        elif sunlight_x > self.room_width:
            # check if the window faces east
            if self.direction == 'e':
                direct_sunlight_region.append((self.x + self.width, self.y))
                direct_sunlight_region.append((self.x + self.width, self.y + self.length))
            else:
                direct_sunlight_region = []
        else:
            # calculate the position of the sun's ray at the length of the window
            sunlight_y = (sunlight_x - (self.room_width / 2)) * math.tan(sun_elevation)

            # check if the sunlight is above the room
            if sunlight_y < 0:
                # check if the window faces north
                if self.direction == 'n':
                    direct_sunlight_region.append((self.x, self.y))
                    direct_sunlight_region.append((self.x + self.width, self.y))
                else:
                    direct_sunlight_region = []
            # check if the sunlight is below the room
            elif sunlight_y > self.room_length:
                # check if the window faces south
                if self.direction == 's':
                    direct_sunlight_region.append((self.x, self.y + self.length))
                    direct_sunlight_region.append((self.x + self.width, self.y + self.length))
                else:
                    direct_sunlight_region = []
            else:
                # calculate the intersection points between the sun's ray and the top and bottom edges of the window
                m = math.tan(self.sun_altitude)
                c = sunlight_y - m * sunlight_x
                intersection_y1 = m * self.x + c
                intersection_y2 = m * (self.x + self.width) + c

                # check if the intersection points are inside the window
                if intersection_y1 > self.y and intersection_y1 < self.y + self.length:
                    direct_sunlight_region.append((self.x, intersection_y1))
                if intersection_y2 > self.y and intersection_y2 < self.y + self.length:
                    direct_sunlight_region.append((self.x + self.width, intersection_y2))

        return direct_sunlight_region
    

x = 25
y = 0
width = 25
height = 10
elevation = 5
intensity = 100
room_width = 100
room_length = 100
for time in range(24):
    window = Window(x, y, width, height, elevation, intensity, room_width, room_length, time)
    # window.calculate_direct_sunlight_region()
    print(window.calculate_direct_sunlight_region())
    
# # create a window
# window = Window(x=0, y=0, width=2, height=2, elevation=0, intensity=1, room_width=10, room_length=10, time=21)

# # calculate direct sunlight
# direct_sunlight_grid = window.calculate_direct_sunlight(cell_size=1)

# # print the grid
# for row in direct_sunlight_grid:
#     print(row)
