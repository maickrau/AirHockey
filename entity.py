import cocos
import math


class EntityManager():

    def __init__(self):
        #super(EntityManager, self).__init__()
        self.entities = self.__generateEntities__()

    def __generateEntities__(self):
        ball1 = Ball(50, 50)
        ball2 = Ball(400, 50)
        return [ball1, ball2]

    def updateEntities(self, dt, keys):
        for entity in self.entities:
            entity.update(dt, keys)

    def drawEntities(self):
        for entity in self.entities:
            entity.draw()


class Entity(cocos.sprite.Sprite):

    def __init__(self, sprite_sheet):
        super(Entity, self).__init__(sprite_sheet)
        #Initialize velocity x and y to 0, 0
        self.vx = 0
        self.vy = 0
        #Initialize maximum ABSOLUTE velocity to 0, 0 (0=no maximum velocity)
        self.maxVelX = 0
        self.maxVelY = 0
        #Initialize acceleration to 0,0
        self.accX = 0
        self.accY = 0

    #General update method for an Entity.
    # !! We do NOT update the position based on velocity here !! #
    # !! Positions are updated by the physics module update   !! #
    # !! method that is called from the game layer            !! #
    def update(self, dt, keys):
        #Update velocity
        #TODO Refactor the two blocks below(duplication for x and y axis)
        #Calculate what the velocity would be ignoring maximum velocity
        potentialVx = self.vx + (self.accX * dt)
        #If absolute potential current velocity is greater that max vel
        #and maxvelx is not set to unlimited(0)
        if math.fabs(potentialVx) > self.maxVelX and not self.maxVelX == 0:
            #If current potential velocity was negative assign negative max vel
            if (self.accX < 0):
                self.vx = -self.maxVelX
            #Else assign the max vel
            else:
                self.vx = self.maxVelX
        #Else if potential velocity wasn't more than max vel assign it to vel
        else:
            self.vx = potentialVx

        #Same as above for y axis
        potentialVy = self.vy + (self.accY * dt)
        if math.fabs(potentialVy) > self.maxVelY and not self.maxVelY == 0:
            if (self.accY < 0):
                self.vy = -self.maxVelY
            else:
                self.vy = self.maxVelY
        else:
            self.vy = potentialVy


class Ball(Entity):

    #Constructor for Ball instance, defaults pos x and y to 0, 0 if not given
    def __init__(self, x=0, y=0):
        super(Ball, self).__init__('ball.png')
        self.position = x, y

    def update(self, dt, keys):
        #Call parent update method
        Entity.update(self, dt, keys)


class PlayerControlledBall(Ball):

    #Constructor for player controlled ball.
    #Parameter "number" is 1 for left and 2 for right(used to assign controls)
    def __init__(self, number):
        super(PlayerControlledBall, self).__init__()
        self.maxVelX = 150
        self.maxVelY = 100