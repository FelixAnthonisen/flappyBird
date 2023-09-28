class Entity: 
    def __init__(self, x_pos, y_pos, x_vel, width, height):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_vel = x_vel
        self.y_vel = 0
        self.width = width
        self.height = height

    def update_pos(self):
        self.y_pos += self.y_vel
        self.x_pos += self.x_vel

class Player(Entity):
    def __init__(self, x_pos, y_pos, x_vel, width, height):
        super().__init__(x_pos, y_pos, x_vel, width, height)
        self.centre = (x_pos+(width/2), y_pos+(height/2))
        self.radius = height/2
        self.is_dead = False

    def update_pos(self):
        super().update_pos()
        self.centre = (self.x_pos+(self.width/2), self.y_pos+(self.height/2))
    
    def fall(self):
        self.y_vel += 0.1

    def jump(self):
        self.y_vel = -4