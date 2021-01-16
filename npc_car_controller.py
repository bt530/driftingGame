from ursina import *
import math
import random
from ursina.shaders import lit_with_shadows_shader
from ursina.shaders import basic_lighting_shader
class NPCCarController(Entity):
    def __init__(self, **kwargs):
        super().__init__()
        self.police=False

        self.friction=0.999
        self.acceleration=10
        self.maxTurn=100
        self.turnRate=3
        self.maxWheel=90
        self.minSpeed=1.5
        self.wheelWidth=0.7
        self.wheelFront=0.06
        self.wheelBack=-2.5
        self.wheelHeight=0.25
        self.maxLean=10
        self.leanCoefficient=2
        self.smokeParticles=2
        self.smokeLinger=0.3
        self.smokeRise=1
        self.rubberLinger=2


        self.minSS=self.minSpeed**2
        self.ax=0
        self.az=0
        self.vx=0
        self.vz=0
        self.origin_y = -.5
        self.camera_pivot = Entity(parent=self, y=2)
        

        
        self.gravity = 1
        self.grounded = False
        self.jump_height = 2
        self.jump_duration = .5
        self.jumping = False
        self.air_time = 0

        self.smoke=[]



        self.body=Entity(parent=self,rotation_y=90,model="playerbody",collider="box",texture="Car Texture 1")#,shader=lit_with_shadows_shader)
        self.policeBody=Entity(parent=self,rotation_y=90,model="police",texture="Car Texture 2")#,shader=lit_with_shadows_shader)
        self.policeBody.visible=False
        self.wheel1=Entity(parent=self,x=self.wheelWidth,z=self.wheelFront,y=self.wheelHeight,rotation_y=-90,model="wheel",texture="Car Texture 1")#,shader=lit_with_shadows_shader)
        self.wheel2=Entity(parent=self,x=-self.wheelWidth,z=self.wheelFront,y=self.wheelHeight,rotation_y=90,model="wheel",texture="Car Texture 1")#,shader=lit_with_shadows_shader)

        self.wheel3=Entity(parent=self,x=self.wheelWidth,z=self.wheelBack,y=self.wheelHeight,rotation_y=-90,model="wheel",texture="Car Texture 1")#,shader=lit_with_shadows_shader)
        self.wheel4=Entity(parent=self,x=-self.wheelWidth,z=self.wheelBack,y=self.wheelHeight,rotation_y=90,model="wheel",texture="Car Texture 1")#,shader=lit_with_shadows_shader)
        for key, value in kwargs.items():
            setattr(self, key ,value)

    def change(self):
        self.body.visible=self.police
        self.police=not self.police
        self.policeBody.visible=self.police
    def update(self):
      pass
        

"""
        if self.gravity:
            # # gravity
            ray = raycast(self.world_position+(0,2,0), self.down, ignore=(self,))
            # ray = boxcast(self.world_position+(0,2,0), self.down, ignore=(self,))

            if ray.distance <= 2.1:
                if not self.grounded:
                    self.land()
                self.grounded = True
                # make sure it's not a wall and that the point is not too far up
                if ray.world_normal.y > .7 and ray.world_point.y - self.world_y < .5: # walk up slope
                    self.y = ray.world_point[1]
                return
            else:
                self.grounded = False

            # if not on ground and not on way up in jump, fall
            self.y -= min(self.air_time, ray.distance-.05)
            self.air_time += time.dt * .25 * self.gravity

    def land(self):
        # print('land')
        self.air_time = 0
        self.grounded = True      


    def input(self, key):
        pass"""
"""
        if key == 'space':
            self.jump()
"""



if __name__ == '__main__':
    from ursina import *
    import math
    from ursina.prefabs.first_person_controller import FirstPersonController
    from car_controller import CarController
    from ursina.shaders import basic_lighting_shader
    from ursina.shaders import lit_with_shadows_shader
    from ursina.lights import DirectionalLight
    import ctypes

    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    width,height=user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    print(width,height)


    # window.vsync = False
    #application.development_mode = False
    app = Ursina()
    window.position=(0,0)
    app.development_mode  = True
    window.color=color.black
    window.exit_button.enabled=False
    window.fps_counter.enabled = True
    window.cog_button.enabled=False
    #window.debug_menu.enabled = False
    window.size=(width,height)






    #Light(type='ambient', color=(0.3,0.3,0.3,1), direction=(1,1,1))
    #ground = Entity(model='plane',shader=lit_with_shadows_shader, texture='white_cube',scale=(32,1,32),texture_scale=(32,32), collider='mesh',color=color.white)
    ground = Entity(model='plane',   texture='road',scale=(1000,1,1000), texture_scale=(500,500), collider='box')#,shader=lit_with_shadows_shader)
    #ground = Entity(model='plane', scale=(20,1,20),texture_scale=(200,200), texture='road',  collider='box')



    sun = DirectionalLight(y=10, rotation=(160,90,0))
    #sun._light.show_frustum()
    Sky(color=color.rgb(200,200, 220, a=255) )
    #player = FirstPersonController(model='cube', y=1, origin_y=-.5)
    player=CarController(y=10,x=2)  



    def update():

        pass


    app.run()
