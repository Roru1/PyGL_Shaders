from pygl import *
def perspecive(uv,ctx):
    xy = (uv/ctx.size)-vec2(0.5,0)
    y = (uv.y/ctx.size.y)*255
    xy = vec2(xy.x*(1/max(xy.y,0.001)),1-1/max(xy.y,0.001))+vec2(0.5,0)
    color = sample("road.ppm",xy.x,xy.y)
    if(abs(xy.x-0.5)>0.5):
        color = vec3(y,max(0,min(255,y+50)),255.)
    if color.r > 255 or color.g > 255 or color.b > 255:
        print(color)
    return color

def shaderpicker():
    return {"Perspective":perspecive}