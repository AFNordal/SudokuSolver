import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from skimage import data
from skimage import io
from skimage.transform import *
from readDigit import *

def grey(pic):
    img=np.empty([pic.shape[0],pic.shape[1]])
    for c,i in enumerate(pic):
        for c_,j in enumerate(i):
            img[c,c_]=int(sum(j)/3)
    
    return img

def dark(pic):
    rec=255
    for i in pic.flat:
        if i<rec:
            rec=i
    
    return rec


def corners(pic,color,discr):
    recs=[0,0,0,0]
    coords=[[],[],[],[]]
    for y in range(pic.shape[0]):
        for x in range(pic.shape[1]):
            if pic[y][x]<color+discr:
                pic[y][x]=0
                if (pic.shape[0]-y)*(pic.shape[1]-x)>recs[0]:
                    recs[0]=(pic.shape[1]-x)*(pic.shape[0]-y)
                    coords[0]=[x,y]
                if (pic.shape[0]-y)*x>recs[1]:
                    recs[1]=x*(pic.shape[0]-y)
                    coords[1]=[x,y]
                if y*x>recs[2]:
                    recs[2]=x*y
                    coords[2]=[x,y]
                if y*(pic.shape[1]-x)>recs[3]:
                    recs[3]=(pic.shape[1]-x)*y
                    coords[3]=[x,y]
            else:
                pic[y][x]=255

    return coords

def tmap(val,b1,t1,b2,t2):
    ret=b2+(t2-b2)*(val-b1)/(t1-b1)
    return ret

def unwarp(pic,corners,s):
    img=np.empty([s,s])
    for y in range(s):
        y1=tmap(y,0,s-1,corners[0][1],corners[3][1])
        x1=tmap(y,0,s-1,corners[0][0],corners[3][0])
        y2=tmap(y,0,s-1,corners[1][1],corners[2][1])
        x2=tmap(y,0,s-1,corners[1][0],corners[2][0])
        eq=np.polyfit([x1,x2],[y1,y2],1)
        for x in range(s):
            x_=int(tmap(x,0,s-1,x1,x2))
            val=int(eq[0]*x_+eq[1])
            img[y][x]=pic[val][x_]
    return img
        
def digitimg(pic):
    dgs=np.empty([81,int(pic.shape[0]/9),int(pic.shape[1]/9)])
    for i in range(9):
        for j in range(9):
            for y in range(int(pic.shape[0]/9)):
                for x in range(int(pic.shape[1]/9)):
                    dgs[i*9+j,y,x]=pic[i*int(pic.shape[0]/9)+y,j*int(pic.shape[1]/9)+x]
            
    return dgs

def checkEmpty(pic,threshold):
    mean=0
    for i in range(10,20):
        for j in range (10,20):
            if pic[i][j]==0:
                mean+=1
    if mean<threshold:
        return True
    else:
        return False



img=io.imread('./straight.jpg')
img_g=grey(img)
dark=dark(img_g)
corners=corners(img_g,dark,135)
wrp=unwarp(img_g,corners,28*9)
digits=digitimg(wrp)

plt.imshow(img_g)
for i in range(4):
    plt.plot(corners[i][0],corners[i][1],'-ro')
plt.show()
plt.imshow(wrp)
plt.show()
plt.imshow(digits[0])
plt.show()
plt.imshow(wrp)
nums=readSudoku(digits)
for y in range(9):
    for x in range(9):
        if checkEmpty(digits[y*9+x],10)==True:
            plt.plot(x*wrp.shape[1]/9+15,y*wrp.shape[0]/9+15,'-bo')
            nums[y*9+x]=0
        else:
            plt.text(x*wrp.shape[1]/9+15,y*wrp.shape[0]/9+15,nums[y*9+x])
plt.show()
plt.close()