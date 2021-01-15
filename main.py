from ursina import *
import math
from ursina.prefabs.first_person_controller import FirstPersonController
from car_controller import CarController
from npc_car_controller import NPCCarController
from ursina.shaders import basic_lighting_shader
from ursina.shaders import lit_with_shadows_shader
from lights import DirectionalLight
import ctypes
import socket
import tkinter
import threading
import random
global hosting
global serverIP
global closing
closing=False
serverIP='127.0.0.1'
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()
width,height=user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
print(width,height)
hosting="none"
identification=str(random.randint(0,1000000000))
print("id: ",identification)

def startHosting():
    global hosting
    global serverIP
    if joinEntry.get() != "":
        serverIP=joinEntry.get()
    else:
        serverIP='127.0.0.1'
    hosting=True
    root.destroy()
def joinHosting():
    global hosting
    global serverIP
    hosting=False
    if joinEntry.get() != "":
        serverIP=joinEntry.get()
    else:
        serverIP='127.0.0.1'
    root.destroy()
def hostConnection(conn,addr):
    global players
    global playerIDs
    global playerCars
    global closing
    global gameSettings
    first=True
    with conn:
        print('Connected by', addr)
        while True:

            try:
                
                data = conn.recv(1024)
                if not data:
                    break
                data=data.decode(encoding='UTF-8',errors='strict')
                #print(data)
                data=data.split(";")
                currentID=data[0]
                if data[0] in list(playerIDs.keys()):
                    players[playerIDs[data[0]]]=data[1:]
                else:
                    npc=NPCCarController(y=30,x=6)
                    playerCars.append(npc)
                    playerIDs[data[0]]=len(players)
                    players.append(data[1:])
                playersToSend=[]
                for i in list(playerIDs.keys()):
                    if i != data[0]:
                        playersToSend.append(";".join(players[playerIDs[i]]))
                
                playersToSend=":".join(playersToSend)
                playersToSend=bytes(playersToSend,encoding="utf-8")
                
                    
                if first:
                    #print(":".join(gameSettings),"utf-8")
                    conn.sendall(bytes(":".join(gameSettings),"utf-8"))
                    first=False
                else:
                    conn.sendall(playersToSend)
            except:

                break
        print("destroying")
        
        players[playerIDs[currentID]]="gone"
                
def hostThread():
    global players
    global playerIDs
    global playerCars
    global closing
    global serverIP
    print(serverIP)
    window.title="host"
    HOST = '0.0.0.0'  # Standard loopback interface address (localhost)
    PORT = 65432        # Port to listen on (non-privileged ports are > 1023)
    playerIDs={identification:0}

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((serverIP, PORT))
        s.listen()
        while True:
            conn, addr = s.accept()
            y = threading.Thread(target=hostConnection,args=(conn,addr),daemon=True)
            y.start()


            
def clientThread():
    global closing
    global players
    global playerCars
    global serverIP
    global gameSettings
    window.title="client"
    #HOST = '127.0.0.1'  # The server's hostname or IP address
    PORT = 65432        # The port used by the server

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        s.connect((serverIP, PORT))
        while True:
            message=";".join([identification,str(round(player.body.world_x,4)),str(round(player.body.world_y,4)),str(round(player.body.world_z,4)),str(round(player.body.world_rotation_x,4)),str(round(player.body.world_rotation_y,4)),str(round(player.body.world_rotation_z,4))])
            message=bytes(message,encoding="UTF-8")
            s.sendall(message)
            data = s.recv(1024)
            data=data.decode(encoding='UTF-8',errors='strict')
            
            #print("###"+data+"###")  
            data=data.split(":")
            if data[0]=="s":
                gameSettings=data
                displayMap(gameSettings[1])

            else:
                while len(players) < len(data) +1:
                    npc=NPCCarController(y=30,x=6)
                    playerCars.append(npc)
                    players.append(players[0])
                for i in range(len(data)):
                    players[i+1]=data[i].split(";")
                

            #print(data)
            #print(players)
            if closing:
                break
            #print('Received', repr(data))
def createMap(width=10,height=10,roads=10,biome="city"):
    if biome=="city":
        layout=[]
        types=["g","b"]
        for i in range(width):
            add=[]
            for j in range(height):
                if i==0 or i==width-1 or j==0 or j==height-1:
                    add.append('b')
                else:
                    r=random.randint(0,100)
                    if r<30:
                        add.append("g")
                    else:
                        add.append("b")
                        
            layout.append(add)
        startx=1
        starty=1
        for i in range(roads):
            endx=random.randint(1,round((width-2)/2))*2-1
            endy=random.randint(1,round((height-2)/2))*2-1
            if random.randint(0,1)==0:
                while startx != endx:
                    layout[startx][starty]="r"
                    if startx>endx:
                        
                        startx-=1
                    else:
                        startx+=1
                while starty != endy:
                    layout[startx][starty]="r"
                    if starty>endy:
                        
                        starty-=1
                    else:
                        starty+=1
            else:
                while starty != endy:
                    layout[startx][starty]="r"
                    if starty>endy:
                        
                        starty-=1
                    else:
                        starty+=1
                while startx != endx:
                    layout[startx][starty]="r"
                    if startx>endx:
                        
                        startx-=1
                    else:
                        startx+=1
    print(layout)
    for i in range(len(layout)):
        layout[i]="£".join(layout[i])
    layout="$".join(layout)
    return layout
            
            
            
        
            
    
    pass
def displayMap(code):
    global player
    code=code.split("$")
    for i in range(len(code)):
        code[i]=code[i].split("£")
    player.map=code
    for i in range(len(code)):
        for j in range(len(code[i])):
            if code[i][j]=="r":
                ground = Entity(model='plane',x=i*10,z=j*10, scale=(10,1,10), shader=lit_with_shadows_shader)
                ground.model.static=True
                adjacent=0
                pairs=0
                for k in range(-1,2):
                    for l in range(-1,2):
                        if code[i+k][j+l]=="r" and not (k==0 and l==0) and abs(k) != abs(l):
                            adjacent+=1
                for k in range(0,2):
                    for l in range(0,2):
                        if code[i+k][j+l]=="r" and code[i-k][j-l]=="r" and not (k==0 and l==0) and abs(k) != abs(l):
                            pairs+=1
                if adjacent > 2 or (adjacent == 2 and pairs == 0):
                    ground.texture="road clear"
                else:
                    ground.texture="road straight"
                    if code[i+1][j] == "r" or code[i-1][j]=="r":
                        ground.rotation_y=90
            elif code[i][j]=="g":
                ground = Entity(model='plane',texture="grass",x=i*10,z=j*10, scale=(10,1,10), shader=lit_with_shadows_shader)
                ground.model.static=True
            elif code[i][j]=="b":
                ground = Entity(model='buildings',color=color.rgb(60,60,60),x=i*10,z=j*10, scale=(5,5,5),shader=lit_with_shadows_shader)
                ground.rotation_y=random.randint(0,3)*90
                ground.model.static=True
                #for k in range(2):
                    #for l in range(2):
                        #building=Entity(model='cube',color=color.rgb(120,120,120),x=i*10+k*4-2,z=j*10+l*4-2, scale=(3.8,random.randint(40,200)/10,3.8),shader=lit_with_shadows_shader)
                        #building.model.static=True
                        #pass
    
                
    pass
global players
global playerCars
global gameSettings
global player
gameSettings=["s",""]

def update():
    players[0]=[str(round(player.body.world_x,4)),str(round(player.body.world_y,4)),str(round(player.body.world_z,4)),str(round(player.body.world_rotation_x,4)),str(round(player.body.world_rotation_y,4)),str(round(player.body.world_rotation_z,4))]
    #print(len(players))
    if len(players) >1:
        #print(players)
        for i in range(1,len(players)):
            if players[i] != "gone" and players[i] != ["g","o","n","e"]:
                
                playerCars[i].x=float(players[i][0])
                playerCars[i].y=float(players[i][1])
                playerCars[i].z=float(players[i][2])

                #playerCars[i].rotation_x=float(players[i][3])
                playerCars[i].rotation_y=float(players[i][4])-90
                #playerCars[i].rotation_z=float(players[i][5])
            elif playerCars[i] != "gone":
                destroy(playerCars[i])
                playerCars[i]="gone"

    pass


    
while True:
    
    
    hosting="none"
    root=tkinter.Tk()
    root.title="drift"
    hostButton=tkinter.Button(root,text="host game",command=startHosting)
    hostButton.pack()
    hostname = socket.gethostname()    
    localIP = socket.gethostbyname(hostname)  
    joinEntry=tkinter.Entry(root)
    joinEntry.insert(0,localIP)
    joinEntry.pack()
    joinButton=tkinter.Button(root,text="join game",command=joinHosting)
    joinButton.pack()

    root.mainloop()

    if hosting=="none":
        break


        
    
    
    # window.vsync = False
    #application.development_mode = False
    app = Ursina()
    #window.position=(0,20)
    window.position=(0,0)
    app.development_mode  = True
    window.color=color.black
    window.exit_button.enabled=False
    window.fps_counter.enabled = True
    window.cog_button.enabled=False
    #window.debug_menu.enabled = False
    window.size=(width,height)
    #window.borderless = False
    player=CarController(y=0.1,x=10,z=10)
    if hosting==True:
        window.title="host"
        code=createMap(width=20,height=20,roads=40)
        gameSettings[1]=code
        displayMap(code)
    elif hosting==False:
        window.title="client"





    #Light(type='ambient', color=(0.3,0.3,0.3,1), direction=(1,1,1))
    #ground = Entity(model='plane',shader=lit_with_shadows_shader, texture='white_cube',scale=(32,1,32),texture_scale=(32,32), collider='mesh',color=color.white)
    #ground = Entity(model='plane',texture="track", scale=(200,1,200), collider='box',shader=lit_with_shadows_shader)
    #ground = Entity(model='plane', scale=(20,1,20),texture_scale=(200,200), texture='road',  collider='box')
    #my_scene = load_blender_scene('gmae')
    
    #ground = Entity(model='plane', scale=(100,1,100), color=color.yellow.tint(-.2), texture='white_cube', texture_scale=(100,100), collider='box',shader=lit_with_shadows_shader)
    sun = DirectionalLight(y=50,x=400,z=400,scale=(100,100,100), rotation=(160,45,0))
    sun._light.show_frustum()
    Sky(color=color.rgb(200,200, 220, a=255) )
    #player = FirstPersonController(model='cube', y=1, origin_y=-.5)

    #player.smokeParticles=0.5
    
    print(hosting)
    players=[[str(round(player.body.world_x,4)),str(round(player.body.world_y,4)),str(round(player.body.world_z,4)),str(round(player.body.world_rotation_x,4)),str(round(player.body.world_rotation_y,4)),str(round(player.body.world_rotation_z,4))]]
    playerCars=["None"]
    if hosting==True:
        window.title="host"
        x = threading.Thread(target=hostThread,daemon=True)
        x.start()
    elif hosting==False:
        window.title="client"
        x = threading.Thread(target=clientThread,daemon=True)
        x.start()
        pass




    app.run()
    print("stoprunning")


    exit()

"""
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
# window.vsync = False
app = Ursina()
# Sky(color=color.gray)
ground = Entity(model='plane', scale=(100,1,100), color=color.yellow.tint(-.2), texture='white_cube', texture_scale=(100,100), collider='box')
e = Entity(model='cube', scale=(1,5,10), x=2, y=.01, rotation_y=45, collider='box', texture='white_cube')
e.texture_scale = (e.scale_z, e.scale_y)
e = Entity(model='cube', scale=(1,5,10), x=-2, y=.01, collider='box', texture='white_cube')
e.texture_scale = (e.scale_z, e.scale_y)

player = FirstPersonController(model='cube', y=1, origin_y=-.5)
player.gun = None

gun = Button(parent=scene, model='cube', color=color.blue, origin_y=-.5, position=(3,0,3), collider='box')
gun.on_click = Sequence(Func(setattr, gun, 'parent', camera), Func(setattr, player, 'gun', gun))

gun_2 = duplicate(gun, z=7, x=8)
slope = Entity(model='cube', collider='box', position=(0,0,8), scale=6, rotation=(45,0,0), texture='brick', texture_scale=(8,8))
slope = Entity(model='cube', collider='box', position=(5,0,10), scale=6, rotation=(80,0,0), texture='brick', texture_scale=(8,8))
# hill = Entity(model='sphere', position=(20,-10,10), scale=(25,25,25), collider='sphere', color=color.green)
# hill = Entity(model='sphere', position=(20,-0,10), scale=(25,25,25), collider='mesh', color=color.green)
# from ursina.shaders import basic_lighting_shader
# for e in scene.entities:
#     e.shader = basic_lighting_shader

def input(key):
    if key == 'left mouse down' and player.gun:
        gun.blink(color.orange)
        bullet = Entity(parent=gun, model='cube', scale=.1, color=color.black)
        bullet.world_parent = scene
        bullet.animate_position(bullet.position+(bullet.forward*50), curve=curve.linear, duration=1)
        destroy(bullet, delay=1)

# player.add_script(NoclipMode())
app.run()"""
