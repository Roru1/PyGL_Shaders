from pygl import *
from math import floor, ceil, pi, sin, cos, atan2, tau
from random import random, seed

class Candidate:
    def __init__(self, position, color):
        self.x = position.x
        self.y = position.y
        self.color = color

# kernals

blur7 = [0.00000067,0.00002292,0.00019117,0.00038771,0.00019117,0.00002292,0.00000067,0.00002292,0.00078633,0.00655965,0.01330373,0.00655965,0.00078633,0.00002292,0.00019117,0.00655965,0.05472157,0.11098164,0.05472157,0.00655965,0.00019117,0.00038771,0.01330373,0.11098164,0.22508352,0.11098164,0.01330373,0.00038771,0.00019117,0.00655965,0.05472157,0.11098164,0.05472157,0.00655965,0.00019117,0.00002292,0.00078633,0.00655965,0.01330373,0.00655965,0.00078633,0.00002292,0.00000067,0.00002292,0.00019117,0.00038771,0.00019117,0.00002292,0.00000067]

gx = [-1,0,1,-2,0,2,-1,0,1]
gy = [-1,-2,-1,0,0,0,1,2,1]

# dithers

bayer2x2 = [0,2,3,1]

bayer4x4 = [0,8,2,10,12,4,14,6,3,11,1,9,15,7,13,5]

bayer8x8 = [0,32,8,40,2,34,10,42,48,16,56,24,50,18,58,26,12,44,4,36,14,46,6,38,60,28,52,20,62,30,54,22,3,35,11,43,1,33,9,41,51,19,59,27,49,17,57,25,15,47,7,39,13,45,5,37,63,31,55,23,61,29,53,21]

rubbish4x4 = bayer4x4.copy()

rubbish4x4.sort()

rubbish8x8 = bayer8x8.copy()

rubbish8x8.sort()

# halftones

verticalhalftone = [0, 0, 0, 0, 0, 0, 0, 0, 9, 9, 9, 9, 9, 9, 9, 9, 18, 18, 18, 18, 18, 18, 18, 18, 27, 27, 27, 27, 27, 27, 27, 27, 36, 36, 36, 36, 36, 36, 36, 36, 45, 45, 45, 45, 45, 45, 45, 45, 54, 54, 54, 54, 54, 54, 54, 54, 63, 63, 63, 63, 63, 63, 63, 63]

# colors

yellow = vec3(255,255,0)

red = vec3(255,0,0)

green = vec3(0,255,0)

purple = vec3(153, 0, 204)

blue = vec3(0,0,255)

grey = vec3(128)

sqrt2 = sqrt(2)

# helpers

def v3(numba):
    return vec3(numba)

def sam(texture,uv,size):
    uv = uv/size
    return sample(texture,uv.x,uv.y)

def conv(kernsize,kern,texture,uv,size):
    convbuffer = []
    for i in range(kernsize):
        for j in range(kernsize):
            f = i-floor(kernsize/2)
            g = j-floor(kernsize/2)
            index = i*kernsize + j
            dibbit = kern[index]
            color = sam(texture,uv-vec2(g,f),size)*vec3(dibbit)
            convbuffer.append(color)
    avg = vec3(0)
    for x in convbuffer:
        avg = avg+x
    return avg

def dither(patternsize,pattern,uv,value):
    moduv = uv%vec2(patternsize)
    index = moduv.x + moduv.y*patternsize
    if value>pattern[index]/(patternsize**2):
        return vec3(255)
    else:
        return vec3(0)

# shaders

def shader(uv,ctx):
    xy = uv/ctx.size
    if ceil(uv.y/2) == floor(uv.y/2):
        xy.x += 0.5
    return sample(ctx.textures[0],xy.x,xy.y)

def sinheigh(uv,ctx):
    uv = uv/ctx.size
    uv.y += sin(uv.y*3*pi+(pi*ctx.time/(24)))*((sin(pi*ctx.time/48)+1.5)*0.125)
    return sample(ctx.textures[0],uv.x,uv.y)

def sinwide(uv,ctx):
    uv = uv/ctx.size
    uv.y += sin(uv.x*3*pi+(pi*ctx.time/(24)))*((sin(pi*ctx.time/48)+1.5)*0.125)
    return sample(ctx.textures[0],uv.x,uv.y)

def randomdither(uv,ctx):
    uv = uv/ctx.size
    color = sample(ctx.textures[0],uv.x,uv.y)
    if color.greyscale()/255 > random():
        return vec3(255)
    else:
        return vec3(0)

def blur(uv,ctx):
    s = ctx.size

    tex = ctx.textures[0]

    return conv(7,blur7,tex,uv,s)

def sobel(uv,ctx):
    s = ctx.size
    tex = ctx.textures[0]
    color1 = conv(3,gx,tex,uv,s)
    color2 = conv(3,gy,tex,uv,s)

    g = color1.sqr() + color2.sqr()
    g = g.sqrt()
    if g.greyscale()/255>0.2:
        return vec3(255)
    else:
        return vec3(0)

def squarething(uv, ctx):
    p = (vec2(2.0) * uv - ctx.size) / vec2(ctx.size.y)
    a = vec2(-0.2, -0.4)
    b = vec2(0.2, -0.4)
    c = vec2(0.4, 0.4)
    d = vec2(-0.4, 0.4)
    uv = invBilinear(p,a,b,c,d)
    if uv == vec2(-1):
        uv = vec2(0)
        return vec3(0)
    else:
        return sample("cobblestone.ppm",uv.x,uv.y, mode=2)

def fptp(uv, ctx):
    cyp = ctx.textures[0].split(",")
    crp = ctx.textures[1].split(",")
    cpp = ctx.textures[2].split(",")
    candidate_yellow = Candidate(vec2(cyp[0],cyp[1]).float(),yellow)
    candidate_red = Candidate(vec2(crp[0],crp[1]).float(),red)
    candidate_purple = Candidate(vec2(cpp[0],cpp[1]).float(),purple)
    candidates = [candidate_yellow,candidate_red,candidate_purple]
    uv /= ctx.size
    first_past_the_post = candidate_yellow
    first_past_the_post_distance = 100000
    for i in range(3):
        x = candidates[i]
        current_distance = distance(vec2(x.x,x.y),uv)
        if current_distance<first_past_the_post_distance:
            first_past_the_post_distance = current_distance
            first_past_the_post = x
        if current_distance<0.01:
            return green

    if first_past_the_post_distance>0.25:
        return grey
    return first_past_the_post.color

def fptp2(uv, ctx):
    cyp = ctx.textures[0].split(",")
    crp = ctx.textures[1].split(",")
    cpp = ctx.textures[2].split(",")
    candidate_yellow = Candidate(vec2(cyp[0],cyp[1]).float(),yellow)
    candidate_red = Candidate(vec2(crp[0],crp[1]).float(),red)
    candidate_purple = Candidate(vec2(cpp[0],cpp[1]).float(),purple)
    candidates = [candidate_yellow,candidate_red,candidate_purple]
    uv /= ctx.size
    first_past_the_post = candidate_yellow
    first_past_the_post_distance = 10000
    for i in range(3):
        x = candidates[i]
        current_distance = distance(vec2(x.x,x.y),uv)
        if current_distance<first_past_the_post_distance:
            first_past_the_post_distance = current_distance
            first_past_the_post = x
        if current_distance<0.01:
            return green
    return first_past_the_post.color


def voronoi(uv,ctx):
    match ctx.data[2]:
        case "time":
            seed(ctx.time)
        case "x" | "y":
            seed(ctx.data[3])
        case _:
            seed(ctx.textures[2])
    points = []
    uv /= ctx.size
    for _ in range(int(ctx.textures[0])):
        pos = vec2(random(),random())
        if ctx.data[2] == "x":
            pos += vec2(ctx.time/48,0)
        elif ctx.data[2] == "y":
            pos += vec2(0,ctx.time/48)
        pos = pos % vec2(1)
        points.append(Candidate(pos,vec3(random()*255,random()*255,random()*255)))
    first_past_the_post_distance = 10000
    first_past_the_post = points[0]
    for x in points:
        current_distance = distance(vec2(x.x,x.y),uv)
        if current_distance<first_past_the_post_distance:
            first_past_the_post_distance = current_distance
            first_past_the_post = x
        if current_distance<0.01:
            return green
    if ctx.textures[1] == "color":
        return first_past_the_post.color
    else:
        return vec3(first_past_the_post_distance*(255/sqrt2))

def dither2x2(uv,ctx):
    value = sam(ctx.textures[0],uv,ctx.size).greyscale()/255
    return dither(2,bayer2x2,uv,value)

def dither4x4(uv,ctx):
    value = sam(ctx.textures[0],uv,ctx.size).greyscale()/255
    return dither(4,bayer4x4,uv,value)

def dither8x8(uv,ctx):
    value = sam(ctx.textures[0],uv,ctx.size).greyscale()/255
    return dither(8,bayer8x8,uv,value)

def rubbishdither4x4(uv,ctx):
    value = sam(ctx.textures[0],uv,ctx.size).greyscale()/255
    return dither(4,rubbish4x4,uv,value)

def rubbishdither8x8(uv,ctx):
    value = sam(ctx.textures[0],uv,ctx.size).greyscale()/255
    return dither(8,rubbish8x8,uv,value)

def halftone1(uv,ctx):
    value = sam(ctx.textures[0], uv, ctx.size).greyscale() / 255
    return dither(8, verticalhalftone, uv, value)

def generalhalftone(uv,ctx):
    uv = uv/ctx.size
    uv2 = (uv*vec2(5))
    value = sample(ctx.textures[0],uv.x,uv.y).greyscale()
    if value >= sample(ctx.textures[1],uv2.x,uv2.y).greyscale():
        return vec3(255)
    else:
        return vec3(0)

def shader2(uv,ctx):
    uv = uv/ctx.size
    uv /= vec2(2,1)
    a = (uv.y+0.25)
    uv2 = vec2(uv.x*sin(a*3.14159*2),uv.x*cos(a*3.14159*2)) + vec2(0.5)

    return sample(ctx.textures[0],uv2.x,1-uv2.y)

def filmgrain(uv,ctx):
    seed(ctx.time)
    candidates = []
    for _ in range(1000):
        pos = vec2(random(),random())
        candidates.append(Candidate(pos,vec3(pos.x,pos.y,0)))
    uv /= ctx.size
    first_past_the_post = Candidate(vec2(0),vec3(0))
    first_past_the_post_distance = 10000
    for x in candidates:

        current_distance = distance(vec2(x.x, x.y), uv)
        if current_distance < first_past_the_post_distance:
            first_past_the_post_distance = current_distance
            first_past_the_post = x
    winner = first_past_the_post

    return sampleinterpolated(ctx.textures[0],winner.x,winner.y)

def polar(uv,ctx):
    uv /= ctx.size
    uv -= vec2(0.5)
    uv *= vec2(2)
    uv = vec2(sqrt(uv.x*uv.x+uv.y*uv.y),atan2(uv.y,uv.x)/tau)
    return sampleinterpolated(ctx.textures[0],uv.x,uv.y)

def shaderpicker():
    return {"interlaced horizontality":shader,
            "siny":sinheigh,
            "sinx":sinwide,
            "Random Dither":randomdither,
            "blur":blur,
            "sobel mag":sobel,
            "square thing":squarething,
            "First Past the Post (the data are the positions of candidates formatted as x,y)":fptp,
            "ditto but no non-voters":fptp2,
            "voronoi":Shaderdata(voronoi,"Simulates n points on a grid and colors each pixel according to the closest point",["How Many Points?","Color or Distance?","Seed (time for time, x for x translation, y for y translation)","Seed if previous was x or y"]),
            "2x2 dither": dither2x2,
            "4x4 dither": dither4x4,
            "8x8 dither": dither8x8,
            "terrible 4x4 dither": rubbishdither4x4,
            "horrible 8x8 dither": rubbishdither8x8,
            "vertical halftone": halftone1,
            "general halftone": generalhalftone,
            "Cartesian": Shaderdata(shader2,"A cartesian transform", ["Texture"]),
            "Polar": Shaderdata(polar, "A polar transform", ["Texture"]),
            "Film Grain": Shaderdata(filmgrain,"is like film with silver halide crystals, inspired by a captain dissilusion video",["Texture"])
            }