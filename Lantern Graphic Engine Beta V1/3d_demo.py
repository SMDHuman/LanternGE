from graphics import *
import keyboard
import time
import line

scrx=400
scry=200
win = GraphWin("Game Screen",scrx,scry,autoflush=False) 

dis_of_scr=5
scr_pixel=0.1

scr_pos=[]
for x in range(scrx):
    for y in range(scry):
        scr_pos.append((scr_pixel*(x-scrx/2),scr_pixel*(y-scry/2),(y-scry/2)))

def clear():
    for item in win.items[:]:
        item.undraw()

def draw_line(a,b):
    #print(a[0]+scrx/2,a[1]+scry/2)
    #print(b[0]+scrx/2,b[1]+scry/2)
    Line(Point(a[0]+scrx/2,a[1]+scry/2),Point(b[0]+scrx/2,b[1]+scry/2)).draw(win)

def search(ref,array,slot):
    for i in array:
        if(i[slot]==ref):
            print(array)
            return(i[1-slot])

def scr_dot_ray(point):
#    if(point[2]>0):
     return((search(dis_of_scr,line.draw((0,0),(point[2],point[0])),0),search(dis_of_scr,line.draw((0,0),(point[2],point[1])),0)))
#    else:
#        return((,))
wall=[(0,50,30),(0,-50,30),(0,-50,20),(0,50,20)]
while(1):
    time.sleep(0.05)
    clear()
    for c in range(0,len(wall)-1):
        #print(wall)
        draw_line(scr_dot_ray(wall[c]),scr_dot_ray(wall[c+1]))
    draw_line(scr_dot_ray(wall[len(wall)-1]),scr_dot_ray(wall[0]))
    win.update()
    if(keyboard.is_pressed("d")):
        for i in range(len(wall)):
            wall[i]=(wall[i][0]+2,wall[i][1],wall[i][2])
    if(keyboard.is_pressed("a")):
        for i in range(len(wall)):
            wall[i]=(wall[i][0]-2,wall[i][1],wall[i][2])
    if(keyboard.is_pressed("s")):
        for i in range(len(wall)):
            wall[i]=(wall[i][0],wall[i][1],wall[i][2]-1)
    if(keyboard.is_pressed("w")):
        for i in range(len(wall)):
            wall[i]=(wall[i][0],wall[i][1],wall[i][2]+1)
    #while(not(not(keyboard.is_pressed("s"))and not(keyboard.is_pressed("w"))and
    #          not(keyboard.is_pressed("d"))and not(keyboard.is_pressed("a")))):
    #    pass
input()