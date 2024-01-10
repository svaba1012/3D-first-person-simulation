import numpy as np

class Character():
    forward = 0
    right = 0
    def __init__(self):
        self.movSpeed = 1.0
        self.movVec = np.array([0.0,0.0,0.0])
        self.posVec = np.array([0.0,0.0,1.0])
        self.lookVec = np.array ([1.0,2.0,0]) / 1.41 

    def attachToScreen(self, eye, center):
        self.eye = eye
        self.center = center

    def move(self, dt):
        translationVec = np.array([0,0,0]);
        xyLookVec = np.copy(self.lookVec)
        xyLookVec[2] = 0
        xyLookVec = xyLookVec / np.linalg.norm(xyLookVec)
        translationVec = xyLookVec * self.forward
        
        yxLookVec = np.array([xyLookVec[1], -xyLookVec[0], 0]) * self.right
        translationVec += yxLookVec

        # translationVec = translationVec / np.linalg.norm(translationVec)
        
        translationVec *= self.movSpeed * dt

        self.posVec += translationVec
        



        
        self.posVec += translationVec

    
