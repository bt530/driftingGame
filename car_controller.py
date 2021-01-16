from ursina import *
import math
import random
import trail_renderer
from ursina.shaders import lit_with_shadows_shader
from ursina.shaders import basic_lighting_shader
class CarController(Entity):
    def __init__(self, **kwargs):
        super().__init__()


        self.police=False

        self.friction=0.999
        self.acceleration=20
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
        self.smokeParticles=5
        self.smokeLinger=0.3
        self.smokeRise=1
        self.rubberLinger=2
        self.minResistance=0.7
        self.smokeRefresh=0.025
        self.smokeT=0
        self.keySensitivity=0#150
        self.mouseSensitivity=1


        self.minSS=self.minSpeed**2
        self.ax=0
        self.az=0
        self.vx=0
        self.vz=0
        self.origin_y = -.5
        self.camera_pivot = Entity(parent=self, y=2)
        self.cursor = Entity(parent=camera.ui,  color=color.pink, scale=0, rotation_z=45)
        self.map=[["r"]]

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
        for i in range(2*round(self.smokeParticles)):
            e=Entity(parent=scene,position=(0,0,0),scale=(4,1,4),y=-.1,billboard=True,color=color.rgba(0, 0, 0, a=0),model="plane",texture="smoke"+str(random.randint(1,3)),shader=basic_lighting_shader)
            self.smoke.append(e)



        self.body=Entity(parent=self,rotation_y=90,)#,shader=lit_with_shadows_shader)
        self.robberBody=Entity(parent=self.body,model="playerbody",collider="box",texture="Car Texture 1")#shader=lit_with_shadows_shader)
        self.policeBody=Entity(parent=self.body,model="police",texture="Car Texture 2")#,shader=lit_with_shadows_shader)
        self.policeBody.visible=False
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
    def change(self):
        self.robberBody.visible=self.police
        self.police=not self.police
        self.policeBody.visible=self.police


    def update(self):

        if self.vx**2 + self.vz**2 > self.minSS:
            self.turn=max(min(self.maxTurn*time.dt,self.camera_pivot.rotation_y*self.turnRate*time.dt),-self.maxTurn*time.dt)

            self.body.rotation_x=max(min(-(self.turn/time.dt)/self.maxTurn*self.leanCoefficient*self.maxLean,self.maxLean),-self.maxLean)

            self.rotation_y+=self.turn
            self.camera_pivot.rotation_y-=self.turn
            

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

            """
                for i in self.smoke:
                        

                    i.y+=self.smokeRise*time.dt
                    #i.x+=1*time.dt
                    i.scale_x=i.scale_x*1.3**time.dt
                    i.scale_z=i.scale_z*1.3**time.dt
                    #i.look_at(self.camera_pivot)"""
            oldmapx=min(len(self.map[0])-1,abs(round((self.x+5)//10)))
            oldmapz=min(len(self.map)-1,abs(round((self.z+5)//10)))
            newmapx=min(len(self.map[0])-1,abs(round((self.x+self.vx*time.dt+5)//10)))
            newmapz=min(len(self.map)-1,abs(round((self.z+self.vz*time.dt+5)//10)))
            if self.map[newmapx][oldmapz] == "r":
                self.x+=self.vx*time.dt
                self.minResistance=0.7
                self.friction=0.999
                oldmapx=newmapx
            elif self.map[newmapx][oldmapz] == "g":
                self.x+=self.vx*time.dt
                self.minResistance=0.2
                self.friction=0.9
                oldmapx=newmapx
            else:
                self.vx=self.vx*0.001
            
            if self.map[oldmapx][newmapz] == "r":
                self.minResistance=0.7
                self.z+=self.vz*time.dt
                self.friction=0.999

            elif self.map[oldmapx][newmapz] == "g":
                self.minResistance=0.2
                self.z+=self.vz*time.dt
                self.friction=0.9
            else:
                self.vz=self.vz*0.001
                self.body.rotation_x=0
                self.turn=0
        else:
            self.body.rotation_x=0
            self.turn=0
        self.smokeT+=time.dt
        self.camera_pivot.rotation_y += (self.mouseSensitivity*(mouse.velocity[0] * self.mouse_sensitivity[1]) - time.dt*self.keySensitivity*(held_keys['a'] - held_keys['d']))
        self.trailRenderer3.color=color.rgba(0, 0, 0, a=180*abs(self.turn/(self.maxTurn*time.dt)))
        self.trailRenderer4.color=color.rgba(0, 0, 0, a=180*abs(self.turn/(self.maxTurn*time.dt)))
        if self.smokeT>self.smokeRefresh:
            self.smokeT=0
            self.smoke[0].world_position=self.wheel3.world_position
            self.smoke[0].scale=(4,1,4)
            self.smoke[1].world_position=self.wheel4.world_position
            self.smoke[1].scale=(4,1,4)
            if 180*abs(self.turn/(self.maxTurn*time.dt)) > 60:
                    self.smoke[0].color=color.rgba(200, 200, 200, a=180*abs(self.turn/(self.maxTurn*time.dt)))
                    self.smoke[1].color=color.rgba(200, 200, 200, a=180*abs(self.turn/(self.maxTurn*time.dt)))
            else:
                    self.smoke[0].color=color.rgba(200, 200, 200, a=0)
                    self.smoke[1].color=color.rgba(200, 200, 200, a=0)
            self.smoke.append(self.smoke.pop(0))
            self.smoke.append(self.smoke.pop(0))
        self.camera_pivot.rotation_x -= mouse.velocity[1] * self.mouse_sensitivity[0]
        self.camera_pivot.rotation_x= clamp(self.camera_pivot.rotation_x, -5, 30)

        self.ax=(held_keys['w'] - held_keys['s'])*math.sin(math.radians(self.rotation_y))*self.acceleration
        self.az=(held_keys['w'] - held_keys['s'])*math.cos(math.radians(self.rotation_y))*self.acceleration

        self.vx=(self.friction*min(self.minResistance,abs(math.sin(math.radians(self.rotation_y))))**time.dt)*(self.vx+(self.ax*time.dt))

        self.vz=(self.friction*min(self.minResistance,abs(math.cos(math.radians(self.rotation_y))))**time.dt)*(self.vz+(self.az*time.dt))


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
        

        """
        if self.gravity:
            # # gravity
            ray = raycast(self.world_position+(0,2,0), self.down, ignore=(self,))
            try:
                self.y = ray.world_point[1]
            except:
                pass"""
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
   
        if key == 'space':
            self.change()




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
