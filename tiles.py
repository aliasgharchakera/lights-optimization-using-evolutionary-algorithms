WIDTH = 50
LENGTH = 50 #inches

class Tile:
    def __init__(self, x, y, obstacle, height):
        self.x = x
        self.y = y
        self.size = [WIDTH, LENGTH]
        self.obstacle = obstacle
        self.height = height
        # obstacle is 0 for north wall, 1 for east wall, 2 for south wall, 3 for west wall
        # height is 0 for flat and >0 for raised
        self.lit = False

    def light_up(self):
        self.lit = True
    
    def light_down(self):
        self.lit = False
    # def draw(self): 
    #     pygame.draw.rect(screen, self.color, self.rect)

    