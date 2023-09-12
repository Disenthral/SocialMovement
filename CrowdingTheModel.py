import pygame
import numpy as np
import random
import time
import sys
import os
print('1')
def resource_path(relative_path):
    try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
asset_url = resource_path('/Users/kennywu/Desktop/FinalProject/BlackDot.png')
bk= pygame.image.load(asset_url)
asset_ur = resource_path('/Users/kennywu/Desktop/FinalProject/RedDot.png')
rk= pygame.image.load(asset_ur)
pygame.init()
width=1200
height=600
running=True
BlackDot=pygame.transform.scale(bk, (5,5))
RedDot=pygame.transform.scale(rk, (7,7))
mass=1
k1=.75#attractive constant
k2=4 #repulsive
r0=20
k3=10 #friction
k4=1 #attraction to dest
dv=3#max velocity
class people:
    def __init__(self,x,y,image):
        self.x=x
        self.y=y
        self.v=[0,0]
        self.dest=random.randint(1,2)
        self.t=1
        if self.dest==2:
            self.dest=-1
        self.second=random.randint(1,2)
        self.image=image
    def cd(self):
        dis=[]
        for i in civ:
            distance=(self.x-i.x,self.y-i.y,self.twod([self.x,self.y],[i.x,i.y]))
            dis.append(distance)
        return dis
    def twod(self, a, b):
        if a==b:
            return 0
        return np.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2) #distance from one point to another
    def cF1(self):         #return mass*dv/#attractive force
        if self.twod((m.x,m.y),(self.x,self.y))>30:
            return [k1*(m.x-self.x),k1*(m.y-self.y)]
        else:
            return [-10* k2*(m.x-self.x),-10* k2*(m.y-self.y)]
    def cF4(self): #
        goal=[0,0]
        if self.dest==1:
            goal[0]=width+500
        else:
            goal[0]=-500
        if self.second==1:
            goal[1]=100
        else:
            goal[1]=height-100
            
        return [k4*(goal[0]-self.x),k4*(goal[1]-self.y)]
    def cF2(self): #negative force
        neigh=self.cd()
        F2=[0,0]
        for i in neigh:
            if i[2]<2*r0 and i[2]>0:
                F2[0] -= -k2*(2*r0-i[2])*i[0]/i[2]
                F2[1] -= -k2*(2*r0-i[2])*i[1]/i[2]
        tw = max(self.y, height-self.y)
        """if tw<r0:
            F2[1] -= -10*k2*(r0-tw)*(1 if self.y < height/2 else -1)
        bw = min(self.y, height-self.y)
        if bw<r0:
            F2[1] -= -10*k2*(r0-bw)*(1 if self.y < height/2 else -1)"""
        return F2
    def cF3(self):
        return [-k3*self.v[0],-k3*self.v[1]]
    def move(self):
        F1=self.cF1()
        F2=self.cF2()
        F3=self.cF3()
        F=[F1[0]+F2[0]+F3[0],F1[1]+F2[1]+F3[1]]
        self.v[0]+=F[0]/mass/self.t
        self.v[1]+=F[1]/mass/self.t
        if abs(self.v[0])+abs(self.v[1])>dv: # max speed
            temp=self.v[0]
            self.v[0]=self.v[0]/(abs(self.v[0])+abs(self.v[1]))*dv
            self.v[1]=self.v[1]/(abs(temp)+abs(self.v[1]))*dv
        prevx=self.x
        self.x+=self.v[0]
        self.y+=self.v[1]
        self.t+=1
        self.x += np.random.normal(-.1, 0.1)
        self.y += np.random.normal(-.1, 0.1)
        if (self.x<0 and prevx>=0) or (self.x>width and prevx<=width):
            self.dest=-self.dest
            self.second=random.randint(1,2)
            self.t=1
            
        
        
grid=np.zeros((width,height))
class model:
    def __init__(self,x,y,image):
        self.x=x
        self.y=y
        self.image=image
    def move(self):
        self.x+=4
        self.y+=2
civ=list()

double=40
single=60
triple=20
while(single>0 or double>0 or triple>0):
    repeat=True
    while repeat:
        x=random.randint(0,width-1)
        y=random.randint(0,height-1)
        a=random.randint(1,10)
        b=random.randint(1,10)
        c=random.randint(1,10)
        d=random.randint(1,10)
        if single>0:
            if grid[x][y]==1:
                continue
            else:
                repeat=False
            grid[x][y]=1
            single-=1
            civ.append(people(x,y,BlackDot))
        elif double>0:
            if x+a-5>width-1 or y+b-5>height-1 or grid[x][y]==1 or grid[x+a-5][y+b-5]==1:
                continue
            else:
                repeat=False
            grid[x][y]=1
            grid[x+a-5][y+b-5]=1
            civ.append(people(x,y,BlackDot))
            civ.append(people(x+a-5,y+b-5,BlackDot))
            double-=1
        else:
            if x+a-5>width-1 or y+b-5>height-1 or x+c-5>width-1 or y+d-5>height-1 or grid[x][y]==1 or grid[x+a-5][y+b-5]==1 or grid[x+c-5][y+d-5]==1:
                continue
            else:
                repeat=False
            grid[x][y]=1
            grid[x+a-5][y+b-5]=1
            grid[x+c-5][y+d-5]=1
            civ.append(people(x,y,BlackDot))
            civ.append(people(x+a-5,y+b-5,BlackDot))
            civ.append(people(x+c-5,y+d-5,BlackDot))
            triple-=1
        

m=model(-10, 0,RedDot)
screen=pygame.display.set_mode((width,height))
pygame.display.set_caption("Model a Model in a Subway")
delay=100
while(m.x<width and running==True):
    screen.fill((255,255,255))
    if delay==0:
        delay=100
        for i in civ:
            i.move()
        m.move()
    for i in civ:
        screen.blit(i.image,(i.x,i.y))
    screen.blit(m.image,(m.x,m.y))
    for event in pygame.event.get():
        if event.type== pygame.QUIT:
            running=False
    delay-=1
    pygame.display.update()
