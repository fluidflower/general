import cv2
import numpy as np
import subprocess


def drawline(img,pt1,pt2,color,thickness=1,style='dotted',gap=20):
    dist =((pt1[0]-pt2[0])**2+(pt1[1]-pt2[1])**2)**.5
    pts= []
    for i in  np.arange(0,dist,gap):
        r=i/dist
        x=int((pt1[0]*(1-r)+pt2[0]*r)+.5)
        y=int((pt1[1]*(1-r)+pt2[1]*r)+.5)
        p = (x,y)
        pts.append(p)

    if style=='dotted':
        for p in pts:
            cv2.circle(img,p,thickness,color,-1)
    else:
        s=pts[0]
        e=pts[0]
        i=0
        for p in pts:
            s=e
            e=p
            if i%2==1:
                cv2.line(img,s,e,color,thickness)
            i+=1

def drawpoly(img,pts,color,thickness=1,style='dotted',):
    s=pts[0]
    e=pts[0]
    pts.append(pts.pop(0))
    for p in pts:
        s=e
        e=p
        if style=='solid':
            cv2.line(img,(int(s[0]), int(s[1])),(int(e[0]), int(e[1])),color,thickness)
        else:
            drawline(img,s,e,color,thickness,style)

def drawrect(img,pt1,pt2,color,thickness=1,style='dotted'):
    pts = [pt1,(pt2[0],pt1[1]),pt2,(pt1[0],pt2[1])] 
    drawpoly(img,pts,color,thickness,style)

def laserGridMMToPixels(coords, shape):
    pxPerMMX = shape[1]/284
    pxPerMMY = shape[0]/150
    offsetMMX = 2
    offsetMMY = 1.33

    pX = (coords[0] + offsetMMX)*pxPerMMX
    pY = shape[0] - (coords[1] + offsetMMY)*pxPerMMY

    return (int(pX), int(pY))


image = cv2.imread('../figure_6_bottom.png')

font = cv2.FONT_HERSHEY_DUPLEX
fontScale = 0.6
thickness = 1

colorB = (0, 164, 255)
topLeftB = laserGridMMToPixels((0, 120), image.shape)
bottomRightB = laserGridMMToPixels((110, 60), image.shape)
drawrect(image, topLeftB, bottomRightB, colorB, 2, style='solid')
bottomLeftCornerOfText = laserGridMMToPixels((1, 114), image.shape)

colorA = (144, 238, 144)
topLeftA = laserGridMMToPixels((110, 60), image.shape)
bottomRightA = laserGridMMToPixels((280, 0), image.shape)
drawrect(image, topLeftA, bottomRightA, colorA, 2, style='solid')
bottomLeftCornerOfText = laserGridMMToPixels((111, 54), image.shape)

colorC = (198, 166, 67)
topLeftC = laserGridMMToPixels((110, 40), image.shape)
bottomRightC = laserGridMMToPixels((260, 10), image.shape)
drawrect(image, topLeftC, bottomRightC, colorC, 2, style='solid')
bottomLeftCornerOfText = laserGridMMToPixels((111, 34), image.shape)

colorInj = (0, 0, 255)
injection1 = laserGridMMToPixels((90, 30), image.shape)
cv2.circle(image, injection1, 5, colorInj, 3)
injection2 = laserGridMMToPixels((170, 70), image.shape)
cv2.circle(image, injection2, 5, colorInj, 3)

colorObs = (204, 50, 153)
obs1 = laserGridMMToPixels((150, 50), image.shape)
cv2.circle(image, obs1, 5, colorObs, 3)
obs2 = laserGridMMToPixels((170, 110), image.shape)
cv2.circle(image, obs2, 5, colorObs, 3)

cv2.imwrite('temp.png', image)
subprocess.run(["convert", "temp.png", "-font", "helvetica-bold", "-pointsize", "24", "-fill", "#90EE90",
                "-stroke", "#90EE90", "-annotate", "+320+290", "Box A", "-fill", "#FFA400",
                "-stroke", "#FFA400", "-annotate", "+10+110", "Box B", "-fill", "#43A6C6",
                "-stroke", "#43A6C6", "-annotate", "+320+350", "Box C", "figure_8_improved.png"])
subprocess.run(["rm", "temp.png"])
