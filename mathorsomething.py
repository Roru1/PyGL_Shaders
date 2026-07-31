from pygl import *
from math import floor, ceil, pi, sin
from random import random, seed

class Candidate:
    def __init__(self, position, color):
        self.x = position.x
        self.y = position.y
        self.color = color

blur7 = [0.00000067,0.00002292,0.00019117,0.00038771,0.00019117,0.00002292,0.00000067,0.00002292,0.00078633,0.00655965,0.01330373,0.00655965,0.00078633,0.00002292,0.00019117,0.00655965,0.05472157,0.11098164,0.05472157,0.00655965,0.00019117,0.00038771,0.01330373,0.11098164,0.22508352,0.11098164,0.01330373,0.00038771,0.00019117,0.00655965,0.05472157,0.11098164,0.05472157,0.00655965,0.00019117,0.00002292,0.00078633,0.00655965,0.01330373,0.00655965,0.00078633,0.00002292,0.00000067,0.00002292,0.00019117,0.00038771,0.00019117,0.00002292,0.00000067]

gx = [-1,0,1,-2,0,2,-1,0,1]
gy = [-1,-2,-1,0,0,0,1,2,1]

yellow = vec3(255,255,0)

red = vec3(255,0,0)

green = vec3(0,255,0)

purple = vec3(153, 0, 204)

blue = vec3(0,0,255)

grey = vec3(128)

sqrt2 = sqrt(2)

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
            print(f"perfect fit for {uv}!")
            return green

    if first_past_the_post_distance>0.25:
        print(f"{uv} didn't vote!")
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
            print(f"perfect fit for {uv}!")
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
            print(f"perfect fit for {uv}!")
            return green
    if ctx.textures[1] == "color":
        return first_past_the_post.color
    else:
        return vec3(first_past_the_post_distance*(255/sqrt2))

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
            "voronoi":Shaderdata(voronoi,"First Data is number of points, if second data is color it will show the color, otherwise it will show the distance, third data is the seed, if the third data is x or y, the 4th data is the seed",4)
            }