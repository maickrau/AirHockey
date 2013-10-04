class PhysicsManager():

    def update(self, dt, entities):
        self.__updateEntityPositions__(dt, entities)

    def __updateEntityPositions__(self, dt, entities):
        #TODO Implement collision detection and resolution
        for entity in entities:
            entity.x = entity.x + (entity.vx * dt)
            entity.y = entity.y + (entity.vy * dt)
