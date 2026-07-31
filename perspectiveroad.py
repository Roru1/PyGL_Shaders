from pygl import *
def perspective(uv,ctx):
    xy = (uv/ctx.size)-vec2(0.5,0)
    y = (uv.y/ctx.size.y)*255
    xy = vec2(xy.x*(1/max(xy.y,0.001)),1-1/max(xy.y,0.001))+vec2(0.5,-ctx.time/48)
    color = sample("road.ppm",xy.x,xy.y,0,0)
    if(abs(xy.x-0.5)>0.5):
        color = vec3(y,max(0,min(255,y+50)),255.)
    if color.r > 255 or color.g > 255 or color.b > 255:
        print(color)
    return color

def reverseperspective1(uv,ctx):
    uv = uv/ctx.size-vec2(0.5,0)
    uv.x = uv.x*(uv.y)+0.5
    return sample(ctx.textures[0],uv.x,uv.y)

def reverseperspective2(uv,ctx):
    uv = uv/ctx.size
    uv.y = 1/(1-uv.y+1)
    return sample(ctx.textures[0],uv.x,uv.y)

def shaderpicker():
    return {"Perspective":perspective,"Perspective Inverse P1 (texture 1 used)":reverseperspective1,"Perspective Inverse P2 (texture 1 is output of P1)":reverseperspective2}