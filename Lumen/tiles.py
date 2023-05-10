WIDTH = 50
LENGTH = 50 #inches
MINIMUM_INTENSITY = 0.5

class Tile:
    def __init__(self, x, y, obstacle, height):
        self.x = x
        self.y = y
        #self.size = [WIDTH, LENGTH]
        self.obstacle = obstacle
        self.height = height
        # obstacle is 0 for north wall, 1 for east wall, 2 for south wall, 3 for west wall
        # height is 0 for flat and >0 for raised
        self.lit = False
        self.fill_vessel = [0]*8
        self.intensity = 0
         # list of 8 zeros, one for each direction
        # for direction see the diagram on group
        
    def __str__(self) -> str:
        return f"{self.lit}"

    def light_up(self):
        self.lit = True

    def fill(self, direction, percentage):
        if self.fill_vessel[direction] < percentage:
            self.fill_vessel[direction] = percentage
    
    def light_down(self):
        self.lit = False
    # def draw(self): 
    #     pygame.draw.rect(screen, self.color, self.rect)
    def create_obstacle(self, obstacle,height):
        self.obstacle = obstacle
        self.height = height
        '''obstacle is 0 for north wall, 1 for east wall, 2 for south wall, 3 for west wall
        height is 0 for flat and >0 for raised'''

    def give_status(self):
        return self.lit
    
    def less_intense_lit(self,intensity):
        if self.lit!=True:
            self.intensity = self.intensity + intensity
        if self.intensity >= MINIMUM_INTENSITY:
            self.lit = True

    



    