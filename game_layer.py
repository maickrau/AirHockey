import cocos
import entity
import physics
import input
import config

class GameLayer(cocos.layer.Layer):

    #Lets the layer receive events from director.window
    is_event_handler = True

    def __init__(self):
        super(GameLayer, self).__init__()
        self.keys_pressed = set()
        self.entity_manager = entity.EntityManager()
        self.input_manager = input.InputManager()
        self.physics_manager = physics.PhysicsManager(self.entity_manager.entities, self.input_manager)

        #Add entities to layer
        for e in self.entity_manager.entities:
            self.add(e)

        #Schedule the render method
        self.schedule(self.entity_manager.render)
        # Set a timer-based updater for physics
        self.entity_manager.updater(self.physics_manager, self.physics_manager.update, config.tick)

    def on_key_press(self, key, modifiers):
        self.input_manager.update_key(key, 1)

    def on_key_release(self, key, modifiers):
        self.input_manager.update_key(key, 0)