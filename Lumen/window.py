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
        self.lit = False
        # time is in 24 hour format, 0-23, 0 being midnight, 12 being noon and 23 being 11pm
        # the assumption is that the sun rises at 6 from the east and sets at 6 in the west
        self.time = time
        # write a switch to determine the direction of the window using x and y
        if self.x == 0:
            self.direction = 'w'
        elif self.x == room_width:
            self.direction = 'e'
        elif self.y == 0:
            self.direction = 'n'
        elif self.y == room_length:
            self.direction = 's'
        
        self.sun_angle = (time - 12) * 15
    
    def calculate_direct_sunlight_region(self):
        direct_sunlight_region = []

        # calculate the position of the sun based on the time of day
        sun_elevation = math.radians(90 - self.sun_angle)
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
                m = math.tan(self.sun_angle)
                c = sunlight_y - m * sunlight_x
                intersection_y1 = m * self.x + c
                intersection_y2 = m * (self.x + self.width) + c

                # check if the intersection points are inside the window
                if intersection_y1 > self.y and intersection_y1 < self.y + self.height:
                    direct_sunlight_region.append((self.x, intersection_y1))
                if intersection_y2 > self.y and intersection_y2 < self.y + self.height:
                    direct_sunlight_region.append((self.x + self.width, intersection_y2))

        return direct_sunlight_region


window = Window(0, 3, 2, 2, 1, 100, 10, 10, 9)
print(window.calculate_direct_sunlight_region())   