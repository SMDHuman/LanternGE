import lantern_engine as G
import time
import keyboard

#Setup 1000x500 screen named 'Screen'
G.open_window('Screen',1000,500)


obj=G.import_object("object/walls.txt")
obj_vec,obj_tri=G.import_obj("object/Spaceship.obj")


scale=0.5
camera=[70,[0,2,-10],[0,0,0],0]
move_speed=25
rotate_speed=100
brk=1
fps=0
fpsT=time.time()
up=1
atime = 0

def update():  
    if(keyboard.is_pressed("d")):
        camera[1][0]+=G.cos(camera[2][1])*move_speed*atime
        camera[1][2]+=-G.sin(camera[2][1])*move_speed*atime
        up=1
    if(keyboard.is_pressed("a")):
        camera[1][0]-=G.cos(camera[2][1])*move_speed*atime
        camera[1][2]-=-G.sin(camera[2][1])*move_speed*atime
        up=1
    if(keyboard.is_pressed("s")):
        camera[1][2]-=G.cos(camera[2][1])*move_speed*atime
        camera[1][0]-=G.sin(camera[2][1])*move_speed*atime
        up=1
    if(keyboard.is_pressed("w")):
        camera[1][2]+=G.cos(camera[2][1])*move_speed*atime
        camera[1][0]+=G.sin(camera[2][1])*move_speed*atime
        up=1
        
    if(keyboard.is_pressed("up")):
        camera[2][0]+=rotate_speed*atime
        up=1
    if(keyboard.is_pressed("down")):
        camera[2][0]-=rotate_speed*atime
        up=1
    if(keyboard.is_pressed("left")):
        camera[2][1]-=rotate_speed*atime
        up=1
    if(keyboard.is_pressed("right")):
        camera[2][1]+=rotate_speed*atime
        up=1
    if(keyboard.is_pressed("r") and camera[3]==0):
        camera[3]=1
        time.sleep(1)
    if(keyboard.is_pressed("r") and camera[3]==1):
        camera[3]=0
        time.sleep(1)

    obj[3][2][1]+=50*atime
    obj[3][2][0]+=50*atime

    if(keyboard.is_pressed("escape")):
        global brk
        brk=0

while(brk):
    update()
    stime=time.time()
    G.clear_screen()
    
    G.render_objects(obj,camera)
    G.render_triangle(obj_vec,obj_tri,camera,scale)
    G.update_screen()

    atime=time.time()-stime