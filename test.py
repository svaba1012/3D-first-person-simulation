import numpy as np

import moderngl

from World import World

from Window import Window

from Character import Character

import time


    

class PerspectiveProjection(Window):

    MOV_SPEED = 0.2

    character = Character()

    dt = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.movingButtonsPressed = False
        self.forwardPressed = False
        self.backwardPressed = False
        self.leftPressed = False
        self.rightPressed = False

        vertexShaderFile = open("./shaders/vertexShader.glsl", "r")
        fragmentShaderFile = open("./shaders/fragmentShader.glsl", "r")

        vertexShaderCode = vertexShaderFile.read()
        fragmentShaderCode = fragmentShaderFile.read()

        vertexShaderFile.close()
        fragmentShaderFile.close()

        self.prog = self.ctx.program(
            vertex_shader=vertexShaderCode,
            fragment_shader=fragmentShaderCode,
        )

        self.prog['z_near'].value = 0.1
        self.prog['z_far'].value = 1000.0
        self.prog['ratio'].value = self.aspect_ratio
        self.prog['fovy'].value = 60

        self.prog['eye'].value = self.character.posVec
        self.prog['center'].value = self.character.posVec + self.character.lookVec
        self.prog['up'].value = (0, 0, 1) #gde je gore

        grid = []
        
        world = World()

        grid = world.makeWalls([[{"x": 1.0, "y": 2.0}, 
                                 {"x": 2.0, "y": 1.0}, 
                                 {"x": 1.5, "y": 0.0}]])

        grid = np.array(grid, dtype='f4')


        self.vbo = self.ctx.buffer(grid)
        self.vao = self.ctx.vertex_array(self.prog, [self.vbo.bind("vert")])

    

    def render(self, time: float, frame_time: float):
        self.character.move(frame_time)
        self.prog['eye'].value = self.character.posVec
        self.prog['center'].value = self.character.posVec + self.character.lookVec
        self.ctx.clear(1.0, 1.0, 1.0)
        self.vao.render(moderngl.TRIANGLES, 65 * 4)
        
        # print(1.0/frame_time)


    def key_event(self, key, action, modifiers):
        # Key presses
        

        if action == self.wnd.keys.ACTION_PRESS:
            if key == self.wnd.keys.W:
                self.character.forward = 1
            if key == self.wnd.keys.S:
                self.character.forward = -1                
            if key == self.wnd.keys.D:
                self.character.right = 1 
            if key == self.wnd.keys.A:
                self.character.right = -1 
            if key == self.wnd.keys.Q:
                self.character.movSpeed = 1.5

        # Key releases
        elif action == self.wnd.keys.ACTION_RELEASE:
            if key == self.wnd.keys.W:
                self.character.forward = 0
            if key == self.wnd.keys.S:
                self.character.forward = 0
            if key == self.wnd.keys.D:
                self.character.right = 0 
            if key == self.wnd.keys.A:
                self.character.right = 0 
            if key == self.wnd.keys.Q:
                self.character.movSpeed = 1.0
                

    def unicode_char_entered(self, char: str):
        print('character entered:', char)
        


if __name__ == '__main__':
    
    PerspectiveProjection.run()
    