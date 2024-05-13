from vpython import color, box, vector, canvas

import cv2
import numpy as np

scene2 = canvas(width=1300, height=500, background=color.white)  #to change background colour to white

#reading the image
def readMap(filename):
    return cv2.imread(filename)

#calculating the hue from RGB value
def hueOfBGR(bgrValues):
    b = bgrValues[0]/255
    g = bgrValues[1]/255
    r = bgrValues[2]/255
    if b == g == r:
        return 0
    else:
        hueVal = np.degrees(np.arccos((0.5 * ((r-g)+(r-b))) / (np.sqrt(((r-g)*(r-g))+((r-b)*(g-b))))))  #equation from the textbook
    if b > g:  #if B > G
        hueVal = 360-hueVal
    return hueVal//2 #hue values range from 0 to 179 in opencv. Converting angles from 0 to 360 to opencv format

#calcualting the intensity from RGB value
def intensityOfBGR(bgrValues):
    b = bgrValues[0]
    g = bgrValues[1]
    r = bgrValues[2]
    intensity = (float(r)+float(g)+float(b))/3.0
    return intensity

#upper and lower bounds for hues of colours
green = [35, 81]

blue = [83,131]

yellow = [23, 32]

#assigns corresponding colour based on hue
def within(hue):
    if hue==0:
        return "black"
    elif hue>=blue[0] and hue<=blue[1]:
        return "blue"
    elif hue>=green[0] and hue<=green[1]:
        return "green"
    elif hue>=yellow[0] and hue<=yellow[1]:
        return "yellow"
    else:
        return "red"
    
# assigns a number based on the interval that the intensity falls in
def intensityToNum(intensity):
    return intensity//10 + 1

colorToHeight = {"blue" : [color.blue,0.2], "green" : [color.green,0.2], "black" : [color.black,0.2], "red" : [vector(0.9,0.5,0.1),-1], "yellow" : [vector(1,0.7,0.5),0.6]}

# Dividing the image into a grid every 20 pixels and extracting data
def makingGrid(map,grid,mapheight,mapwidth):
    i = 0
    j = 0
    pixel = 20
    for y in range(mapheight//pixel):
        grid.append([])
        i = i + pixel
        j = 0
        for x in range(mapwidth//pixel):
            j = j + pixel
            grid[y].append([within(hueOfBGR(map[i-pixel][j-pixel])), intensityToNum(intensityOfBGR(map[i-pixel][j-pixel]))])

#making the 3D model from the data we got from the image
def makingCityscape(grid):
    cityscape = []
    for i in range(len(grid)):
        cityscape.append([])
        for j in range(len(grid[i])):
            h=colorToHeight[grid[i][j][0]][1] #height corresponding to colour
            if h == -1: #if it is a building
                h = grid[i][j][1]
            hcoord = h/2
            if h==0.6: #if bridge
                cuboid = box(pos = vector(j-(len(grid[i])//2),0.1,i-(len(grid)//2)), color = colorToHeight["black"][0], length=1, width=1, height=0.2)  #shadow
                hcoord+=0.35*grid[i][j][1]
            cuboid = box(pos = vector(j-(len(grid[i])//2),hcoord,i-(len(grid)//2)), color = colorToHeight[grid[i][j][0]][0], length=1, width=1, height=h)  #position is the center of the box
            cityscape[i].append(cuboid)

#---------------------Underground Map----------------

def undergroundMap(filename):
    undergroundMap = readMap(filename)
    undergroundMap = cv2.cvtColor(undergroundMap, cv2.COLOR_BGR2GRAY)
    undergroundMapHeight = undergroundMap.shape[0]
    undergroundMapWidth = undergroundMap.shape[1]
    undergroundGrid = []
    ui = 0
    uj = 0
    pixel = 20
    for y in range(undergroundMapHeight//pixel):
        undergroundGrid.append([])
        ui += pixel
        uj = 0
        for x in range(undergroundMapWidth//pixel):
            uj += pixel
            if undergroundMap[ui-pixel][uj-pixel] < 200 and undergroundMap[ui-pixel][uj-pixel]>100:
                undergroundGrid[y].append(2)
            elif undergroundMap[ui-pixel][uj-pixel] < 100:
                undergroundGrid[y].append(1)
            else:
                undergroundGrid[y].append(0)

    for i in range(len(undergroundGrid)):
        for j in range(len(undergroundGrid[i])):
            if undergroundGrid[i][j] == 1:
                cuboid = box(pos = vector(j-(len(undergroundGrid[i])//2),-4,i-(len(undergroundGrid)//2)), color = vector(0.4,0.4,0.5), length=1, width=1, height=1)  #position is the center of the box
            elif undergroundGrid[i][j] == 2:
                cuboid = box(pos = vector(j-(len(undergroundGrid[i])//2),-2.25,i-(len(undergroundGrid)//2)), color = vector(0.4,0.4,0.5), length=1, width=1, height=4.5)


def main():
    mapPath = input("Enter the path of the map: ")  #Campus.png for campus map
    map = readMap(mapPath)
    mapheight = map.shape[0]
    mapwidth = map.shape[1]
    grid = []
    makingGrid(map,grid,mapheight,mapwidth) #taking data from the image
    undergroundModeQ = "Not decided"
    while (undergroundModeQ!="y" and undergroundModeQ!="n"):
        undergroundModeQ = input("Do you want an underground system? (y/n): ")
    if undergroundModeQ=="y":
        undergroundPath = input("Enter the path of the underground map: ") #munnelsBase.png for the munnels in campus map
        undergroundMap(undergroundPath)  #making the underground system
    makingCityscape(grid) #making the 3D model
    
main()