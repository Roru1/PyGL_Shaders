import pygl
from pygl import *

def shader(uv,ctx):
    uv = uv/ctx.size
    source = sample("uvhouse.ppm",uv.x,uv.y,0)/vec3(255)
    tested = source
    y = uv.y*255
    if False:
        return True
    elif tested.b>0.8 and tested.b<0.9:
        return sample("glass.ppm",(source.r),(source.g),0)
    elif tested.b>0.7 and tested.b<0.8:
        return sample("planks.ppm",(source.r),(source.g),0)
    elif tested.b>0.5 and tested.b < 0.7:
        return sample("door.ppm", (source.r), (source.g),0)
    elif tested.b > -1 and tested.b < 0.5:
        return sample("grass.ppm",(source.r),(source.g),0)
    else:
        return vec3(y,max(0,min(255,y+50)),255.)


