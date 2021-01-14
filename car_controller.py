from ursina import *
import math
import random
import trail_renderer
from ursina.shaders import lit_with_shadows_shader
from ursina.shaders import basic_lighting_shader
class CarController(Entity):
    def __init__(self, **kwargs):
        super().__init__()

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
        self.cursor = Entity(parent=camera.ui, model='quad', color=color.pink, scale=0, rotation_z=45)

        camera.parent = self.camera_pivot
        camera.position = (0,0,-10)
        camera.rotation = (0,0,0)
        camera.fov = 90
        mouse.locked = True
        self.mouse_sensitivity = Vec2(40, 40)

        self.gravity = 1
        self.grounded = False
        self.jump_height = 2
        self.jump_duration = .5
        self.jumping = False
        self.air_time = 0

        self.smoke=[]



        self.body=Entity(parent=self,rotation_y=90,model="playerbody",texture="Car Texture 1")#,shader=lit_with_shadows_shader)
        self.wheel1=Entity(parent=self,x=self.wheelWidth,z=self.wheelFront,y=self.wheelHeight,rotation_y=-90,model="wheel",texture="Car Texture 1")#,shader=lit_with_shadows_shader)
        self.wheel2=Entity(parent=self,x=-self.wheelWidth,z=self.wheelFront,y=self.wheelHeight,rotation_y=90,model="wheel",texture="Car Texture 1")#,shader=lit_with_shadows_shader)

        self.wheel3=Entity(parent=self,x=self.wheelWidth,z=self.wheelBack,y=self.wheelHeight,rotation_y=-90,model="wheel",texture="Car Texture 1")#,shader=lit_with_shadows_shader)
        self.wheel4=Entity(parent=self,x=-self.wheelWidth,z=self.wheelBack,y=self.wheelHeight,rotation_y=90,model="wheel",texture="Car Texture 1")#,shader=lit_with_shadows_shader)
        self.wheel3base=Entity(parent=self.wheel3,y=0)
        self.wheel4base=Entity(parent=self.wheel4,y=0)
        self.trailRenderer3 = trail_renderer.TrailRenderer(target=self.wheel3base,thickness=40,length=20,shader=basic_lighting_shader)
        self.trailRenderer4 = trail_renderer.TrailRenderer(target=self.wheel4base,thickness=40,length=20,shader=basic_lighting_shader)
        for key, value in kwargs.items():
            setattr(self, key ,value)


    def update(self):
        self.camera_pivot.rotation_y += mouse.velocity[0] * self.mouse_sensitivity[1]
        if self.vx**2 + self.vz**2 > self.minSS:
            self.turn=max(min(self.maxTurn*time.dt,self.camera_pivot.rotation_y*self.turnRate*time.dt),-self.maxTurn*time.dt)

            self.body.rotation_x=max(min(-(self.turn/time.dt)/self.maxTurn*self.leanCoefficient*self.maxLean,self.maxLean),-self.maxLean)

            self.rotation_y+=self.turn
            self.camera_pivot.rotation_y-=self.turn
            
            if random.randint(1,10000)/abs(self.turn/(self.maxTurn*time.dt)) < 100000*time.dt*self.smokeParticles:
                e=Entity(parent=scene,position=self.wheel3.world_position,scale=(4,1,4),y=-.1,billboard=True,color=color.rgba(200, 200, 200, a=255*abs(self.turn/(self.maxTurn*time.dt))),model="plane",texture="smoke"+str(random.randint(1,3)),shader=basic_lighting_shader)
                self.smoke.append(e)

                
                self.smoke[-1].fade_out(duration=self.smokeLinger)
                destroy(self.smoke[-1],delay=self.smokeLinger)
                e=Entity(parent=scene,position=self.wheel4.world_position,scale=(4,1,4),y=-.1,billboard=True,color=color.rgba(200, 200, 200, a=255*abs(self.turn/(self.maxTurn*time.dt))),model="plane",texture="smoke"+str(random.randint(1,3)),shader=basic_lighting_shader)
                self.smoke.append(e)

                
                self.smoke[-1].fade_out(duration=self.smokeLinger)
                destroy(self.smoke[-1],delay=self.smokeLinger)
            """
            e=Entity(parent=scene,rotation_y=self.wheel1.world_rotation_y,position=self.wheel3.world_position,scale=(1,1,0.2),y=0.1,color=color.rgba(0, 0, 0, a=255*abs(self.turn/(self.maxTurn*time.dt))),model="plane",shader=basic_lighting_shader)
            e.fade_out(duration=self.rubberLinger)
            destroy(e,delay=self.rubberLinger)

            e=Entity(parent=scene,rotation_y=self.wheel1.world_rotation_y,position=self.wheel4.world_position,scale=(1,1,0.2),y=0.1,color=color.rgba(0, 0, 0, a=255*abs(self.turn/(self.maxTurn*time.dt))),model="plane",shader=basic_lighting_shader)
            e.fade_out(duration=self.rubberLinger)
            destroy(e,delay=self.rubberLinger)
            """

            """
            e=Entity(parent=scene,rotation_y=self.wheel1.world_rotation_y,position=self.wheel1.world_position,scale=(1,1,0.2),y=0.1,color=color.rgba(0, 0, 0, a=255*abs(self.turn/(self.maxTurn*time.dt))),model="plane",shader=basic_lighting_shader)
            e.fade_out(duration=self.rubberLinger)
            destroy(e,delay=self.rubberLinger)

            e=Entity(parent=scene,rotation_y=self.wheel1.world_rotation_y,position=self.wheel2.world_position,scale=(1,1,0.2),y=0.1,color=color.rgba(0, 0, 0, a=255*abs(self.turn/(self.maxTurn*time.dt))),model="plane",shader=basic_lighting_shader)
            e.fade_out(duration=self.rubberLinger)
            destroy(e,delay=self.rubberLinger)"""
            self.trailRenderer3.color=color.rgba(0, 0, 0, a=180*abs(self.turn/(self.maxTurn*time.dt)))
            self.trailRenderer4.color=color.rgba(0, 0, 0, a=180*abs(self.turn/(self.maxTurn*time.dt)))
            for i in self.smoke:
                    if i.is_empty():
                        self.smoke.remove(i)
                    else:
                        i.y+=self.smokeRise*time.dt
                        #i.x+=1*time.dt
                        i.scale_x=i.scale_x*1.3**time.dt
                        i.scale_z=i.scale_z*1.3**time.dt
                        #i.look_at(self.camera_pivot)
            self.x+=self.vx*time.dt
            self.z+=self.vz*time.dt
        else:
            self.body.rotation_x=0
        self.camera_pivot.rotation_x -= mouse.velocity[1] * self.mouse_sensitivity[0]
        self.camera_pivot.rotation_x= clamp(self.camera_pivot.rotation_x, -5, 30)

        self.ax=(held_keys['w'] - held_keys['s'])*math.sin(math.radians(self.rotation_y))*self.acceleration
        self.az=(held_keys['w'] - held_keys['s'])*math.cos(math.radians(self.rotation_y))*self.acceleration

        self.vx=(self.friction*abs(math.sin(math.radians(self.rotation_y)))**time.dt)*(self.vx+(self.ax*time.dt))

        self.vz=(self.friction*abs(math.cos(math.radians(self.rotation_y)))**time.dt)*(self.vz+(self.az*time.dt))


        try:
            self.wheelRotation=math.degrees(math.atan(self.vx/self.vz))-self.rotation_y
            if self.wheelRotation%360>90 and self.wheelRotation%360<270:
                self.wheelRotation+=180
            self.wheelRotation=self.wheelRotation%360
            if self.wheelRotation<90 and self.wheelRotation>90-(90-self.maxWheel):
                self.wheelRotation=90-(90-self.maxWheel)
            elif self.wheelRotation>270 and self.wheelRotation<270+(90-self.maxWheel):
                self.wheelRotation=270+(90-self.maxWheel)
            self.wheel1.rotation_y=self.wheelRotation-90
            self.wheel2.rotation_y=self.wheelRotation+90
        except Exception as e:
            #print(e)
            pass
        


        if self.gravity:
            # # gravity
            ray = raycast(self.world_position+(0,2,0), self.down, ignore=(self,))
            try:
                self.y = ray.world_point[1]
            except:
                pass
            """
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
            self.air_time += time.dt * .25 * self.gravity"""

    def land(self):
        # print('land')
        self.air_time = 0
        self.grounded = True      


    def input(self, key):
        pass
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
