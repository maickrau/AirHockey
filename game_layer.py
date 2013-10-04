import cocos
import entity
import physics


class GameLayer(cocos.layer.Layer):

    #Lets the layer receive events from director.window
    is_event_handler = True

    def __init__(self):
        super(GameLayer, self).__init__()
        #set keys
        self.keys_pressed = set()
        #Initialize entity manager and get entities
        self.entity_manager = entity.EntityManager()
        #Add entities to layer
        for e in self.entity_manager.entities:
            self.add(e)
        #Schedule the update method
        self.schedule(self.update)
        self.physics_manager = physics.PhysicsManager()

    def update(self, dt):
        #Update entities (velocity is updated but NOT position)
        self.entity_manager.updateEntities(dt, self.keys_pressed)
        #Give the physics manager the entities and let it update positions
        self.physics_manager.update(dt, self.entity_manager.entities)
        #Draw entities
        self.entity_manager.drawEntities()

    def on_key_press(self, key, modifiers):
        self.keys_pressed.add(key)

    def on_key_release(self, key, modifiers):
        self.keys_pressed.remove(key)