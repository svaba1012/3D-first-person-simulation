class World():
    WALL_COLOR = [0.5, 0.5, 0.5]
    GROUND_COLOR = [0.0, 1.0, 0.0]
    WALL_HEIGHT = 2.0
    
    def __init__(self):
        self.vertices = [];
    
    def makeGround(self):
        '''
        make ground vertices
        set xyPlane color to GROUND_COLOR
        '''
        groundR, groundG, groundB = self.GROUND_COLOR
        self.vertices.append([-1000.0, -1000.0, 0.0, groundR, groundG, groundB])
        self.vertices.append([1000.0, 1000.0, 0.0, groundR, groundG, groundB])
        self.vertices.append([1000.0, -1000.0, 0.0, groundR, groundG, groundB])
        self.vertices.append([-1000.0, -1000.0, 0.0, groundR, groundG, groundB])
        self.vertices.append([1000.0, 1000.0, 0.0, groundR, groundG, groundB])
        self.vertices.append([-1000.0, 1000.0, 0.0, groundR, groundG, groundB])
        

    
    
    def makeWalls(self, wallsArr):
        '''
        wallsArr is array of wall array which is array of wall corners which is 
        xyCoords of that corners
        makes 3d walls with constant WALL_HEIGHT
        '''
        
        wallR, wallG, wallB = self.WALL_COLOR
        for wallLine in wallsArr:
            for i in range(len(wallLine)):
                if(i == len(wallLine) - 1):
                    continue
                self.vertices.append(
                    [wallLine[i]["x"], wallLine[i]["y"], 0.0, wallR, wallG, wallB ])
                self.vertices.append(
                    [wallLine[i]["x"], wallLine[i]["y"], self.WALL_HEIGHT, wallR, wallG, wallB ])
                self.vertices.append(
                    [wallLine[i + 1]["x"], wallLine[i + 1]["y"], 0.0, wallR, wallG, wallB ])
                self.vertices.append(
                    [wallLine[i + 1]["x"], wallLine[i + 1]["y"], self.WALL_HEIGHT, wallR, wallG, wallB ])
                self.vertices.append(
                    [wallLine[i + 1]["x"], wallLine[i + 1]["y"], 0.0, wallR, wallG, wallB ])
                self.vertices.append(
                    [wallLine[i]["x"], wallLine[i]["y"], self.WALL_HEIGHT, wallR, wallG, wallB ])
        return self.vertices
    
    def generateWorld(self):
        '''
        generate vertices for custom world with custom walls
        '''
        self.makeGround()
        return self.makeWalls([[{"x": 0.0, "y": 0.0}, 
                                 {"x": 0.0, "y": 3.0}, 
                                 {"x": 3.0, "y": 3.0},
                                 {"x": 5.0, "y": 5.0},
                                 {"x": 7.0, "y": 5.0},     
                                 ], [
                                {"x": 2.0, "y": 0.0}, 
                                {"x": 2.0, "y": 1.0}, 
                                {"x": 3.0, "y": 1.0},
                                {"x": 5.0, "y": 3.0},
                                {"x": 7.0, "y": 3.0},     
                                 ]])

    