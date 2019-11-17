import cv2 as loadImage
import numpy as np
import time

def mode(x):
    if x>0:
        return x
    return -x    

file1 = open("RIMG_1.coe","r")
actual_image = list(file1.read().split(","))[1:]
actual_image[0] = actual_image[0][-25:]
actual_image[-1] = actual_image[-1][:-2]
factor = 1
c = factor*96*2
img = np.zeros((c,96*factor,3), np.uint8)
count  = 0    
for j in range(0,(192)*factor,factor):
    for i in range(0, (96)*factor,factor):
        if (i//factor-8)%16 == 0 and (j//factor-8)%16 == 0 and j//factor > 96:
            r = 255
            g = 255
            b = 255
        else:
            r = int(actual_image[count][:8], 2)
            g = int(actual_image[count][8:16], 2)
            b = int(actual_image[count][16:], 2)                        

        for m in range(0, factor):
            for n in range(0, factor):
                img[j+n][i+m] = np.array([b,g,r])                
                
        count+=1

#Block matching

endPoints = []
startMilliSec = time.time()
a = 16*factor*2 #factor*96-16*factor
for j in range(16, 65, 16):
    for i in range(16, 65, 16):
        
        #one macroblock (centre case)
        #size = (16*factor) 

        min_sad = 9999999999999999999999999    
        endPoint = 0

        for m in range(j-16, j+16):
            for n in range(i-16, i+16):
                sad = 0
                #calculate sad:
                for k in range(0,16):
                    for l in range(0, 16):
                        b1 = int(img[m+k+96][n+l][0])
                        g1 = int(img[m+k+96][n+l][1])
                        r1 = int(img[m+k+96][n+l][2])
                        b2 = int(img[j+k][i+l][0])
                        g2 = int(img[j+k][i+l][1])
                        r2 = int(img[j+k][i+l][2])
                        toAdd = mode(b1-b2)+mode(g1-g2)+mode(r1-r2)
                        #print(toAdd)
                        sad+=toAdd

                if m==j and i==i and sad == 0:
                    endPoint = ((m+8+96, n+8))
                    min_sad = -1
                if sad < min_sad:                    
                    min_sad = sad
                    #print(min_sad)
                    endPoint = ((m+8+96, n+8))

        endPoints.append(endPoint)            

factor = 4
EndMilliSec = time.time()

endPoints_cordinates = []
for i in range(len(endPoints)):                
    img[endPoints[i][0]][endPoints[i][1]] = np.array([0, 0, 0])
    q = (endPoints[i][0]*factor,endPoints[i][1]*factor )
    endPoints_cordinates.append(q)


print(endPoints_cordinates)

img_to_display = np.zeros((96*factor*2,96*factor,3), np.uint8)

start_points = []

for j in range(0,96*factor*2,factor):
    for i in range(0, 96*factor,factor):
        if (i//factor-8)%16 == 0 and (j//factor-8)%16 == 0 and j//factor > 96:
            start_points.append((j,i))
            r = 255
            g = 255
            b = 255
        else:
            r = int(img[j//factor][i//factor][2])
            g = int(img[j//factor][i//factor][1])
            b = int(img[j//factor][i//factor][0])                        

        for m in range(0, factor):
            for n in range(0, factor):
                img_to_display[j+n][i+m] = np.array([b,g,r])                                      


print(start_points[7])
print(endPoints_cordinates[0])

for j in range(7,11):
    img_to_display =loadImage.arrowedLine(img_to_display,(start_points[j][1],start_points[j][0]),(endPoints_cordinates[j-7][1],endPoints_cordinates[j-7][0]),(0,0,0),factor) 
for j in range(13,17):
    img_to_display =loadImage.arrowedLine(img_to_display,(start_points[j][1],start_points[j][0]),(endPoints_cordinates[j-9][1],endPoints_cordinates[j-9][0]),(0,0,0),factor) 
for j in range(19,23):
    img_to_display =loadImage.arrowedLine(img_to_display,(start_points[j][1],start_points[j][0]),(endPoints_cordinates[j-11][1],endPoints_cordinates[j-11][0]),(0,0,0),factor) 
for j in range(25,29):
    img_to_display =loadImage.arrowedLine(img_to_display,(start_points[j][1],start_points[j][0]),(endPoints_cordinates[j-13][1],endPoints_cordinates[j-13][0]),(0,0,0),factor) 


print("Time = "+str(EndMilliSec-startMilliSec))
     
