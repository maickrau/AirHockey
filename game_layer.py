import cocos
import entity
import physics
import input


class GameLayer(cocos.layer.Layer):

    #Lets the layer receive events from director.window
    is_event_handler = True

    def __init__(self):
        super(GameLayer, self).__init__()
        self.keys_pressed = set()
        self.entity_manager = entity.EntityManager()
        self.physics_manager = physics.PhysicsManager()
        self.input_manager = input.InputManager()

        #Add entities to layer
        for e in self.entity_manager.entities:
            self.add(e)

        #Schedule the update method
        self.schedule(self.update)

    #MAIN GAME LOOP
    #Called every frame
    def update(self, dt):
        #Get input model from input manager
        input_model = self.input_manager.getInputModel(self.keys_pressed)
        #Update entities (velocity is updated but NOT position)
        self.entity_manager.updateEntities(dt, input_model)
        #Give the physics manager the entities to update positions
        self.physics_manager.update(dt, self.entity_manager.entities)
        #Draw entities
        self.entity_manager.drawEntities()

    def on_key_press(self, key, modifiers):
        self.keys_pressed.add(key)

    def on_key_release(self, key, modifiers):
        self.keys_pressed.remove(key)