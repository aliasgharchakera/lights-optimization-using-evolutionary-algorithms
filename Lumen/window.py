import ephem
import math

class Window:
    def __init__(self, x, y, width, height, elevation, intensity, room_width, room_length, time):
        self.x = x
        self.y = y
        self.width = width
        self.intensity = intensity
        self.elevation = elevation
        self.height = height
        self.room_width = room_width
        self.room_length = room_length
        self.position = (self.x, self.y)
        self.time = time
        self.direction = ''
        
        # determine the direction of the window using x and y
        if self.x == 0:
            self.direction = 'w'
        elif self.x == room_width:
            self.direction = 'e'
        elif self.y == 0:
            self.direction = 'n'
        elif self.y == room_length:
            self.direction = 's'

        # use PyEphem to calculate the sun's position
        o = ephem.Observer() 
        o.lat = '24.8607'  # latitude of Karachi
        o.long = '67.0011'  # longitude of Karachi
        o.elevation = self.elevation  # elevation of the window
        o.date = ephem.Date('2023/5/7 ' + str(self.time) + ':00:00')  # date and time of the observation
        sun = ephem.Sun()
        sun.compute(o)
        self.sun_altitude = math.degrees(sun.alt)  # altitude of the sun in degrees
        self.sun_azimuth = math.degrees(sun.az)  # azimuth of the sun in degrees

    def calculate_direct_sunlight_region(self):
        direct_sunlight_region = []

        # calculate the position of the sun based on the time of day
        sun_elevation = math.radians(90 - self.sun_altitude)
        sunlight_x = (self.room_width / 2) + ((self.room_length / 2) / math.tan(sun_elevation))

        # check if the sunlight is to the left of the room
        if sunlight_x < 0:
            # check if the window faces west
            if self.direction == 'w':
                direct_sunlight_region.append((self.x, self.y))
                direct_sunlight_region.append((self.x, self.y + self.height))
            else:
                direct_sunlight_region = []
        # check if the sunlight is to the right of the room
        elif sunlight_x > self.room_width:
            # check if the window faces east
            if self.direction == 'e':
                direct_sunlight_region.append((self.x + self.width, self.y))
                direct_sunlight_region.append((self.x + self.width, self.y + self.height))
            else:
                direct_sunlight_region = []
        else:
            # calculate the position of the sun's ray at the height of the window
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
                    direct_sunlight_region.append((self.x, self.y + self.height))
                    direct_sunlight_region.append((self.x + self.width, self.y + self.height))
                else:
                    direct_sunlight_region = []
            else:
                # calculate the intersection points between the sun's ray and the top and bottom edges of the window
                m = math.tan(self.sun_altitude)
                c = sunlight_y - m * sunlight_x
                intersection_y1 = m * self.x + c
                intersection_y2 = m * (self.x + self.width) + c

                # check if the intersection points are inside the window
                if intersection_y1 > self.y and intersection_y1 < self.y + self.height:
                    direct_sunlight_region.append((self.x, intersection_y1))
                if intersection_y2 > self.y and intersection_y2 < self.y + self.height:
                    direct_sunlight_region.append((self.x + self.width, intersection_y2))

        return direct_sunlight_region
    
    def calculate_direct_sunlight(self, cell_size=1):
        grid_width = int(self.room_width / cell_size)
        grid_length = int(self.room_length / cell_size)
        direct_sunlight_grid = [[False for _ in range(grid_length)] for _ in range(grid_width)]

        direct_sunlight_region = self.calculate_direct_sunlight_region()

        if len(direct_sunlight_region) == 2:
            x1, y1 = direct_sunlight_region[0]
            x2, y2 = direct_sunlight_region[1]
            if x1 == x2:  # vertical ray
                x = int(x1 / cell_size)
                for y in range(int(y1 / cell_size), int(y2 / cell_size) + 1):
                    if y >= 0 and y < grid_length:
                        direct_sunlight_grid[x][y] = True
            elif y1 == y2:  # horizontal ray
                y = int(y1 / cell_size)
                for x in range(int(x1 / cell_size), int(x2 / cell_size) + 1):
                    if x >= 0 and x < grid_width:
                        direct_sunlight_grid[x][y] = True

        return direct_sunlight_grid


# for i in range(1):
#     window = Window(0, 3, 3, 5, 2, 100, 10, 10, 15)
#     print(window.calculate_direct_sunlight())
    
# create a window
# window = Window(x=0, y=0, width=2, height=2, elevation=0, intensity=1, room_width=10, room_length=10, time=21)

# # calculate direct sunlight
# direct_sunlight_grid = window.calculate_direct_sunlight(cell_size=1)

# # print the grid
# for row in direct_sunlight_grid:
#     print(row)
