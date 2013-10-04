import cocos
import entity
import physics


class GameLayer(cocos.layer.Layer):

    def __init__(self):
        super(GameLayer, self).__init__()
        #Initialize entity manager and get entities
        self.entity_manager = entity.EntityManager()
        #Add entities to layer
        for e in self.entity_manager.entities:
            self.add(e)
        #Schedule the update method of this Layer to be called every 0.01 seconds
        self.schedule(self.update)
        self.physics_manager = physics.PhysicsManager()

    def update(self, dt):
        #Update entities (velocity is updated but NOT position)
        self.entity_manager.updateEntities(dt)
        #Give the physics manager the entities and let it update positions
        self.physics_manager.update(dt, self.entity_manager.entities)
        #Draw entities
        self.entity_manager.drawEntities()