from pygl import *
import pygl
from math import sin,cos,pi

def translation(uv,ctx):
    xy = uv/ctx.size
    x=xy.x
    y=xy.y
    x += ctx.time*(1/48)

    return sample("cobblestone.ppm",x,y)

def rotation(uv,ctx):
    xy = uv/ctx.size
    x = xy.x-0.5
    y = xy.y-0.5
    angle = ctx.time * 2*3.14159/48
    c = cos(angle)
    s = sin(angle)

    xy = vec2(float(c*x-s*y)+0.5,float(s*x+c*y)+0.5)
    color = sample("cobblestone.ppm",xy.x,xy.y)
    return color

def scale(uv,ctx):
    scaling = vec2(sin((pi/24) * ctx.time) + 1)
    xy = (uv / ctx.size) - vec2(0.5)
    xy *= scaling
    xy += vec2(0.5)
    return sample("cobblestone.ppm",xy.x,xy.y)

def shaderpicker():
    return {"Translation (animated)": translation,"Rotation (animated)":rotation,"Scaling (animated)":scale}