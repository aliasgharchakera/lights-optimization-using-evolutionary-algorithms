import math

# beam angle in degrees
# luminous intesity in candela
# distance of floor from light source in meters

# we are assuming that all light comes from the center of the light source
# and that the light source is uniform in intensity

def lumens(beam_angle, luminous_intensity, distance):
    # convert beam angle into steradians
    steradians = 2 * math.pi * (1 - math.cos(math.radians(beam_angle / 2)))
    # calculate surface area taking light
    # the tan(beam_angle) * distance is the height of the triangle which is the radius of the circle
    # surface_area_taking_light = 2 * (distance ** 2) * math.pi * (1 - math.cos(math.radians(beam_angle))) / 2
    surface_area_taking_light = ((math.tan(math.radians(beam_angle)) * distance)** 2 )* math.pi 
    # calculate lumens
    lumens = luminous_intensity * steradians

    # accomodate for the fact that the light is not uniform using neighbourhood

    return lumens, surface_area_taking_light

print(lumens(10, 1000, 5))

def sunlight_spread_lumens(window_width, window_height, distance, sun_angle, sun_intensity):
    # calculate the area of the window
    window_area = window_width * window_height
    # calculate the area of the sun
    sun_area = math.pi * (distance ** 2)
    # calculate the area of the sun that is hitting the window
    sun_area_hitting_window = sun_area * math.cos(math.radians(sun_angle))
    # calculate the intensity of the sun hitting the window
    sun_intensity_hitting_window = sun_intensity * sun_area_hitting_window / sun_area
    # calculate the lumens hitting the window
    lumens_hitting_window = sun_intensity_hitting_window * window_area
    return lumens_hitting_window
    pass

grid = [[0 for x in range(10)] for y in range(10)]

print(sunlight_spread_lumens(10, 10, 5, 45, 1000))