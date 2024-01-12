import numpy as np
from math import *

class Character():
    # moving forward coeficient
    forward = 0
    # moving right coeficient
    right = 0
    # moving left coeficient
    left = 0
    # moving backward coeficient
    backward = 0 
    
    xyAngle = 0
    zAngle = 0

    ROTATION_SENSITIVITY = 3
    
    def __init__(self):
        self.movSpeed = 2.0
        self.posVec = np.array([0.0,0.0,1.4])
        self.lookVec = np.array ([1.0,1.0,0.0]) / 1.41 

    def attachToScreen(self, eye, center):
        self.eye = eye
        self.center = center

    def move(self, dt):
        
        translationVec = np.array([0,0,0]);

        # move character only in xyPlane
        xyLookVec = np.copy(self.lookVec)
        xyLookVec[2] = 0
        xyLookVec = xyLookVec / np.linalg.norm(xyLookVec)
        
        # set translationVec
        translationVec = xyLookVec * (self.forward + self.backward)
        yxLookVec = np.array([xyLookVec[1], -xyLookVec[0], 0]) * (self.right + self.left)
        translationVec += yxLookVec
        # translationVec = translationVec / np.linalg.norm(translationVec)
        translationVec *= self.movSpeed * dt

        # translate (move) character 
        self.posVec += translationVec

    
    def setRotation(self, dx, dy):
        self.xyAngle += dx
        self.zAngle += dy
    
    def rotate(self):
        
        dx = self.xyAngle
        dy = self.zAngle
        self.xyAngle = 0
        self.zAngle = 0
        xyAngle = dx / 360 * 2 * pi / self.ROTATION_SENSITIVITY
        zAngle = dy / 360 * 2 * pi / self.ROTATION_SENSITIVITY

        #set xyPlane(zAxis) rotation matrix
        rotMatXY = np.array([[cos(xyAngle), -sin(xyAngle), 0.0],
                            [sin(xyAngle), cos(xyAngle), 0.0], 
                            [0.0, 0.0, 1.0]])
        #rotate character around world zAxis
        self.lookVec = np.matmul(self.lookVec, rotMatXY)

        #limit character up and down view
        if((self.lookVec[2] > 0.8 and dy < 0) or (self.lookVec[2] < -0.8 and dy > 0)):
            return
        

        xyLookVec = np.copy(self.lookVec)
        xyLookVec[2] = 0
        # set rotation matrix around character yAxis 
        cosFi = xyLookVec[0] / np.linalg.norm(xyLookVec)
        sinFi = xyLookVec[1] / np.linalg.norm(xyLookVec)
        rotMatZ = np.array([[cos(zAngle), 0.0, 0.0],
                            [0.0, cos(zAngle), -sin(zAngle)/sinFi], 
                            [cosFi * sin(zAngle), sinFi * sin(zAngle), cos(zAngle)]])
        # apply rotation
        self.lookVec = np.matmul(self.lookVec, rotMatZ)    

        
