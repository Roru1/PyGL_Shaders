class Face:
    def __init__(self,p1,p2,p3,p4):
        self.points = [p1[0],p2[0],p3[0],p4[0]]
        self.depth = (p1[1]+p2[1]+p3[1]+p4[1])/4
    def __lt__(self,other):
        return self.depth < other.depth

import numpy as np
from pygl import *
from math import cos,sin


points = [np.array([1.2,1.2,1.2]),np.array([-1.2,1.2,1.2]),np.array([-1.2,-1.2,1.2]),np.array([1.2,-1.2,1.2]),np.array([1.2,-1.2,-1.2]),np.array([-1.2,-1.2,-1.2]),np.array([-1.2,1.2,-1.2]),np.array([1.2,1.2,-1.2])]

cpos = np.array([0,-5,5])

theta = np.array([np.radians(45),0,0])

e = np.array([0,0,2.77778])

def project(point):
    x = point[0]-cpos[0]
    y = point[1]-cpos[1]
    z = point[2]-cpos[2]
    cosx = cos(theta[0])
    cosy = cos(theta[1])
    cosz = cos(theta[2])
    sinx = sin(theta[0])
    siny = sin(theta[1])
    sinz = sin(theta[2])
    d = np.array([cosy*(sinz*y+cosz*x)-siny*z,sinx*(cosy*z+siny*(sinz*y+cosz*x))+cosx*(cosz*y-sinz*x),cosx*(cosy*z+siny*(sinz*y+cosz*x))-sinx*(cosz*y-sinz*x)])
    b = vec2((e[2]/d[2])*d[0]+e[0],(e[2]/d[2])*d[1]+e[1])
    return b, d[2]

def render3dtest(uv,ctx):
    p = (vec2(2.0) * uv - ctx.size) / vec2(ctx.size.y)
    zangle = 0

    yangle = np.radians(ctx.time*360/48)

    xangle = np.radians(ctx.time*360/48)

    a = np.array([[cos(zangle) * cos(yangle), cos(zangle) * sin(yangle) * sin(xangle) - sin(zangle) * cos(xangle),cos(zangle) * sin(yangle) * cos(xangle) + sin(zangle) * sin(xangle)],[sin(zangle) * cos(yangle), sin(zangle) * sin(yangle) * sin(xangle) + cos(zangle) * cos(xangle),sin(zangle) * sin(yangle) * cos(xangle) - cos(zangle) * sin(xangle)],[-sin(yangle), cos(yangle) * sin(xangle), cos(yangle) * cos(xangle)]])

    rotatedpoints = []

    for x in points:
        rotatedpoints.append(x@a)
    pr1 = project(rotatedpoints[0])
    pr2 = project(rotatedpoints[1])
    pr3 = project(rotatedpoints[2])
    pr4 = project(rotatedpoints[3])
    pr5 = project(rotatedpoints[4])
    pr6 = project(rotatedpoints[5])
    pr7 = project(rotatedpoints[6])
    pr8 = project(rotatedpoints[7])

    f1 = Face(pr1,pr2,pr3,pr4)
    f2 = Face(pr1,pr2,pr7,pr8)
    f3 = Face(pr4,pr1,pr8,pr5)
    f4 = Face(pr2,pr3,pr6,pr7)
    f5 = Face(pr3,pr4,pr5,pr6)
    f6 = Face(pr5,pr6,pr7,pr8)
    faces = [f1,f2,f3,f4,f5,f6]
    faces.sort(reverse=True)

    for face in faces:
        uv = invBilinear(p,face.points[0],face.points[1],face.points[2],face.points[3])
        color = sample(ctx.textures[0],uv.x,uv.y,mode=2,border=vec3(256))
        if color == vec3(256):
            continue
        else:
            break


    return color

def shaderpicker():
    return {"3d Render Test":render3dtest}