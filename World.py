


class World():
    
    def __init__(self):
        self.wallVertices = [];
    
    def makeWalls(self, wallsArr):
        for wallLine in wallsArr:
            for i in range(len(wallLine)):
                if(i == len(wallLine) - 1):
                    continue
                self.wallVertices.append([wallLine[i]["x"], wallLine[i]["y"], 0.0])
                self.wallVertices.append([wallLine[i]["x"], wallLine[i]["y"], 2.0])
                self.wallVertices.append([wallLine[i + 1]["x"], wallLine[i + 1]["y"], 0.0])
                self.wallVertices.append([wallLine[i + 1]["x"], wallLine[i + 1]["y"], 2.0])
                self.wallVertices.append([wallLine[i + 1]["x"], wallLine[i + 1]["y"], 0.0])
                self.wallVertices.append([wallLine[i]["x"], wallLine[i]["y"], 2.0])
        return self.wallVertices

    