from graphics import *
import keyboard
import time
import math


def open_window(win_name,x,y):
    global win_x
    global win_y
    global win
    win_x=x
    win_y=y
    win = GraphWin(win_name,win_x,win_y,autoflush=False) 

def import_object(file):
    file=open(file,"r")
    f_obj=file.readlines()
    objects=[]
    for i in f_obj:
        if(i[:2]=="//"):
            pass
        else:
            obj=[]
            block=i.split()
            obj.append(block[0].split(':'))
            for n in block[1:]:
                obj.append(list(map(int,n.split(','))))
            objects.append(obj)
    return(objects)

def search_array(array,key):
    for i in array:
        a=0
        b=0
        c=0
        if(i[0]==key[0] or i[1]==key[0] or i[2]==key[0]):
            a=1
        if(i[0]==key[1] or i[1]==key[1] or i[2]==key[1]):
            b=1
        if(i[0]==key[2] or i[1]==key[2] or i[2]==key[2]):
            c=1
        if(a+b+c>1):
            return(1)
    return(0)

def import_obj(file,opt=0):
    print("LOADING OBJECT...")
    file=open(file,"r")
    f_obj=file.readlines()
    objects_vec=[]
    objects_tri=[]

    for f_line in f_obj:
        if(f_line=="\n"):
            pass

        elif(f_line[:1]=="v"):
            line=f_line.split(" ")
            for i in range(1,len(line)):
                line[i]=float(line[i])
            line.remove("v")
            objects_vec.append(line)

        elif(f_line[:1]=="f"):
            line=f_line.split(" ")
            for i in range(1,len(line)):
                line[i]=int(line[i])
            line.remove("f")
            objects_tri.append(line)
        else:
            pass

    if(opt==1):
        objects_tri_opt=[]
        print(len(objects_tri))
        removed_tri=[[0,0,0]]
        remove=0
        brk=0
        i=0
        for ref in objects_tri:
            i+=1
            objects_tri_opt.append(ref)
            for check in objects_tri[i:]:
                
                a=0
                b=0
                c=0
                if(ref[0]==check[0] or ref[1]==check[0] or ref[2]==check[0]):
                    a=1
                if(ref[0]==check[1] or ref[1]==check[1] or ref[2]==check[1]):
                    b=1
                if(ref[0]==check[2] or ref[1]==check[2] or ref[2]==check[2]):
                    c=1
                if(a+b+c>1):
                    if(search_array(removed_tri,check)):
                        objects_tri_opt.append(check)
                    else:
                        
                        removed_tri.append(check)
                        objects_tri.remove(check)
                    


    print(len(objects_tri))

    return(objects_vec,objects_tri)

def draw_line(line):
    a=line[0]
    b=line[1]
    if(a=="o" and b=="o"):
        pass
    else:
        #print(a[0]+win_x/2,a[1]+win_y/2)
        #print(b[0]+win_x/2,b[1]+win_y/2)
        #print(a,b)
        #input('wait')
        Line(Point(round(a[0]+win_x/2),round(a[1]+win_y/2)),Point(round(b[0]+win_x/2),round(b[1]+win_y/2))).draw(win)

def sin(deg):
    deg%=360
    if(deg<0):
        deg+=360
    if(deg>90):
        deg=180-deg
    elif(deg>180):
        deg+=180
    return(math.sin(math.radians(deg)))

def cos(deg):
    deg%=360
    if(deg<0):
        deg+=360
    if(deg==90 or deg==270):
        return(0)
    elif(deg>180):
        deg=180-(deg-180)
    return(math.cos(math.radians(deg)))

def power(x):
    if(x>=0):
        return(1)
    else:
        return(-1)

def rotate_2d(vec,deg):
    R=math.sqrt(vec[0]**2+vec[1]**2)
    if(R==0):
        return((0,0))
    else:
        a=(power(vec[1])-1)*-180+math.degrees(math.acos(vec[0]/R)*power(vec[1]))
    #print(a,R)
    x,y=cos(a+deg)*R,sin(a+deg)*R
    #print(x,y)
    return((x,y))

def rotate_dot(dot,rot):
    #Z Rotation
    if(rot[2]!=0):
        (dot[0],dot[1])=rotate_2d((dot[0],dot[1]),rot[2])
    #Y Rotation
    if(rot[1]!=0):
        (dot[0],dot[2])=rotate_2d((dot[0],dot[2]),rot[1])
    #X Rotation
    if(rot[0]!=0):
        (dot[2],dot[1])=rotate_2d((dot[2],dot[1]),-rot[0])
    
    return(dot)

def out_camera(a,b):
    x=b[0]-a[0]
    y=b[1]-a[1]
    Cy=1-a[1]
    
    if(y==0):
        y=0.0001

    Cx=x*Cy/y
    C=Cx+a[0]
    return(C)

def screen_draw_vec(A,B,camera):
    A,B=rotate_dot([A[0]-camera[1][0],A[1]-camera[1][1],A[2]-camera[1][2]],camera[2]),rotate_dot([B[0]-camera[1][0],B[1]-camera[1][1],B[2]-camera[1][2]],camera[2])
    #print(dot)

    if(A[2]<1 and B[2]<1):
        return(("o","o"))

    elif(A[2]<=1):
        x,y=out_camera((A[0],A[2]),(B[0],B[2])),out_camera((A[1],A[2]),(B[1],B[2]))
        A=[x,y,1]
    elif(B[2]<=1):
        x,y=out_camera((B[0],B[2]),(A[0],A[2])),out_camera((B[1],B[2]),(A[1],A[2]))
        B=[x,y,1]      
    
    #A
    #print(1)
    #X vector
    x0,Px,Sx=A[0]/A[2],win_x/2,math.tan(math.radians(camera[0]/2))
    x1=Px*x0/Sx
    #Y vector
    Py,y0=win_y/2,A[1]/A[2]
    y1=-Px*y0/Sx

    #B
    #print(1)
    #X vector
    x0=B[0]/B[2]
    x2=Px*x0/Sx
    #Y vector
    y0=B[1]/B[2]
    y2=-Px*y0/Sx

    #print(x,y)
    return(((x1,y1),(x2,y2)))

def render_wall(wall,camera):
    line_row=[2,3,4,5,2]
    for dot in range(4):
        #print('-------------')
        A,B=rotate_dot([wall[line_row[dot]][0],wall[line_row[dot]][1],wall[line_row[dot]][2]],wall[1]),rotate_dot([wall[line_row[dot+1]][0],wall[line_row[dot+1]][1],wall[line_row[dot+1]][2]],wall[1])
        draw_line(screen_draw_vec([A[0]+wall[0][0],A[1]+wall[0][1],A[2]+wall[0][2]],
                                 [B[0]+wall[0][0],B[1]+wall[0][1],B[2]+wall[0][2]],camera))

def render_cube(cube,camera):
    surfaces=[(1,2,3,4),(5,6,7,8),(1,2,6,5),(4,3,7,8),(2,6,7,3),(1,5,8,4)]
    line_corner=[(1,2),(1,5),(2,3),(2,6),(3,4),(3,7),(4,1),(4,8),(5,6),(6,7),(7,8),(8,5)]
    for dot in line_corner:
        #print('-------------')
        A,B=rotate_dot([cube[dot[0]+1][0],cube[dot[0]+1][1],cube[dot[0]+1][2]],cube[1]),rotate_dot([cube[dot[1]+1][0],cube[dot[1]+1][1],cube[dot[1]+1][2]],cube[1])
        draw_line(screen_draw_vec([A[0]+cube[0][0],A[1]+cube[0][1],A[2]+cube[0][2]],
                                 [B[0]+cube[0][0],B[1]+cube[0][1],B[2]+cube[0][2]],camera))

def render_objects(objects,camera):
    #camera=[fov,(vec_x,vec_y,vec_z),(rot_x,rot_y,rot_z)]
    for object in objects:
        if(object[0][0]=='wall'):
            render_wall(object[1:],camera)
        elif(object[0][0]=='cube'):
            render_cube(object[1:],camera)

def render_triangle(objects_vec,objects_tri,camera,scale):
    for triangle in objects_tri:
        line1=[objects_vec[triangle[1]-1][0]-objects_vec[triangle[0]-1][0],
               objects_vec[triangle[1]-1][1]-objects_vec[triangle[0]-1][1],
               objects_vec[triangle[1]-1][2]-objects_vec[triangle[0]-1][2]]

        line2=[objects_vec[triangle[2]-1][0]-objects_vec[triangle[0]-1][0],
               objects_vec[triangle[2]-1][1]-objects_vec[triangle[0]-1][1],
               objects_vec[triangle[2]-1][2]-objects_vec[triangle[0]-1][2]]

        normal=[line1[1]*line2[2]-line1[2]*line2[1],
                line1[2]*line2[0]-line1[0]*line2[2],
                line1[0]*line2[1]-line1[1]*line2[0]]
        l=math.sqrt(normal[0]**2+normal[1]**2+normal[2]**2)
        if(l==0):
            l=0.0001
        normal=[(normal[0]+objects_vec[triangle[0]-1][0])/l,(normal[1]+objects_vec[triangle[0]-1][1])/l,(normal[2]+objects_vec[triangle[0]-1][2])/l]
        
        d=(normal[0]*(objects_vec[triangle[0]-1][0]-camera[1][0])+normal[1]*(objects_vec[triangle[0]-1][1]-camera[1][1])+normal[2]*(objects_vec[triangle[0]-1][2]-camera[1][2]))
        
        if(d<0 or camera[3]):
            A=screen_draw_vec([objects_vec[triangle[0]-1][0]*scale,objects_vec[triangle[0]-1][1]*scale,objects_vec[triangle[0]-1][2]*scale],
                              [objects_vec[triangle[1]-1][0]*scale,objects_vec[triangle[1]-1][1]*scale,objects_vec[triangle[1]-1][2]*scale],camera)
            B=screen_draw_vec([objects_vec[triangle[2]-1][0]*scale,objects_vec[triangle[2]-1][1]*scale,objects_vec[triangle[2]-1][2]*scale],
                              [objects_vec[triangle[1]-1][0]*scale,objects_vec[triangle[1]-1][1]*scale,objects_vec[triangle[1]-1][2]*scale],camera)

            if(A==("o","o") or B==("o","o")):
                pass
            else:
                poly=Polygon(Point(round(A[0][0])+win_x/2,round(A[0][1])+win_y/2),
                             Point(round(A[1][0])+win_x/2,round(A[1][1])+win_y/2),
                             Point(round(B[0][0])+win_x/2,round(B[0][1])+win_y/2))
                color=100
                poly.setFill(color_rgb(color,color,color))
                poly.draw(win)

            #print(A)
            #print(B)
            #print("")
            
def text_screen(pos,size,text):
    msg=Text(Point(pos[0],pos[1]),text)
    msg.setSize(size)
    msg.draw(win)

def update_screen():
    win.update()

def clear_screen():
    for item in win.items[:]:
        item.undraw()

