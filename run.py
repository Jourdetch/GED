from PIL import Image, ImageDraw
from math import *

img = Image.open("images/paper.jpg")

#Précision n
n=1

def blackwhite(img):
    fn = lambda i: 255 if i > 150 else 0
    return img.convert('L').point(fn, mode='1')

def get_concat_hor(im1, im2, im3):
    dst = Image.new('RGB', (im1.width + im2.width + im3.width, im1.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    dst.paste(im3, (im1.width+im2.width, 0))
    return dst

def get_concat_ver(im1, im2, im3):
    dst = Image.new('RGB', (im1.width, im1.height + im2.height + im3.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (0, im1.height))
    dst.paste(im3, (0, im1.height+im2.height))
    return dst

def proj_hor(img,xy_begin,xy_end,color,indice=False):
    pixelproj_hor=[]
    for y in range(xy_begin[1],xy_end[1]):
        nb=0
        for x in range(xy_begin[0],xy_end[0]):
            if img.getpixel((x,y)) == (0,0,0):
                nb+=1
        pixelproj_hor.append(nb)

    if indice==True:
        return cut_hor(img,xy_begin,xy_end,pixelproj_hor,color,True)
    return cut_hor(img,xy_begin,xy_end,pixelproj_hor,color)

def proj_ver(img,xy_begin,xy_end,color,indice=False):
    pixelproj_ver=[]
    for x in range(xy_begin[0],xy_end[0]):
        nb=0
        for y in range(xy_begin[1],xy_end[1]):
            if img.getpixel((x,y)) == (0,0,0):
                nb+=1
        pixelproj_ver.append(nb)

    if indice==True:
        return cut_ver(img,xy_begin,xy_end,pixelproj_ver,color,True)
    return cut_ver(img,xy_begin,xy_end,pixelproj_ver,color)

def cut_hor(img,xy_begin,xy_end,pixelproj_hor,color,indice=False):

    occ_max = [0,0]
    nb_occ = 0
    pixelproj_hor.append(999)
    for i in range(len(pixelproj_hor)):
        if pixelproj_hor[i] < n:
            nb_occ += 1
        else :
            if nb_occ > occ_max[1] :
                occ_max[1] = nb_occ
                occ_max[0] = i-nb_occ
            nb_occ = 0
    del pixelproj_hor[len(pixelproj_hor)-1]
    if occ_max[1] == 0 and indice == True:
        for i in range(img.width):
            img.putpixel((i,0),(255,0,0))
            img.putpixel((i,img.height-1),(255,0,0))
        for i in range(img.height):
            img.putpixel((0,i),(255,0,0))
            img.putpixel((img.width-1,i),(255,0,0))
        return img
    elif occ_max[1] == 0:
        return proj_ver(img,xy_begin,xy_end,color,True)

    # for r in range(occ_max[0],occ_max[0]+occ_max[1]):
    #     for k in range(xy_begin[0],xy_end[0]):
    #          img.putpixel((k,r),color)
    lst = list(color)
    lst = [x-5 for x in lst]
    color = tuple(lst)

    img1 = proj_ver(img.crop((0,0,xy_end[0],occ_max[0])),(0,0),(xy_end[0],occ_max[0]),color)
    img2 = img.crop((0,occ_max[0],xy_end[0],occ_max[0]+occ_max[1]))
    img3 = proj_ver(img.crop((0,occ_max[0]+occ_max[1],xy_end[0],xy_end[1])),(0,0),(xy_end[0],xy_end[1]-occ_max[0]-occ_max[1]),color)
    return get_concat_ver(img1,img2,img3)

def cut_ver(img,xy_begin,xy_end,pixelproj_ver,color,indice=False):

    occ_max = [0,0]
    nb_occ = 0
    pixelproj_ver.append(999)
    for i in range(len(pixelproj_ver)):
        if pixelproj_ver[i] < n:
            nb_occ += 1
        else :
            if nb_occ > occ_max[1] :
                occ_max[1] = nb_occ
                occ_max[0] = i-nb_occ
            nb_occ = 0
    del pixelproj_ver[len(pixelproj_ver)-1]
    if occ_max[1] == 0 and indice == True:
        for i in range(img.width):
            img.putpixel((i,0),(255,0,0))
            img.putpixel((i,img.height-1),(255,0,0))
        for i in range(img.height):
            img.putpixel((0,i),(255,0,0))
            img.putpixel((img.width-1,i),(255,0,0))
        return img
    elif occ_max[1] == 0:
        return proj_hor(img,xy_begin,xy_end,color)

    # for r in range(occ_max[0],occ_max[0]+occ_max[1]):
    #     for k in range(xy_begin[1],xy_end[1]):
    #          img.putpixel((r,k),color)
    lst = list(color)
    lst = [x-5 for x in lst]
    color = tuple(lst)

    img1 = proj_hor(img.crop((0,0,occ_max[0],xy_end[1])),(0,0),(occ_max[0],xy_end[1]),color)
    img2 = img.crop((occ_max[0],0,occ_max[0]+occ_max[1],xy_end[1]))
    img3 = proj_hor(img.crop(((occ_max[0]+occ_max[1]),0,xy_end[0],xy_end[1])),(0,0),(xy_end[0]-occ_max[0]-occ_max[1],xy_end[1]),color)
    return get_concat_hor(img1,img2,img3)

img = blackwhite(img)
img = img.convert('RGB')
color = (140,140,140)
img = proj_hor(img,(0,0),img.size,color)

img.show()
