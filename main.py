import numpy as np

import moderngl

from World import World

from Character import Character

import moderngl_window as mglw


class AppWindow(mglw.WindowConfig):

    gl_version = (3, 3)
    title = "3D First Person"
    window_size = (1280, 720)
    aspect_ratio = 16 / 9
    resizable = True
    fullscreen = True
    MOV_SPEED = 0.2
    dt = 0
    
    # instantiate first person character of the game/simulation 
    character = Character()

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

        self.prog['eye'].value = self.character.posVec # position of camera
        self.prog['center'].value = self.character.posVec + self.character.lookVec # look orientation of camera
        self.prog['up'].value = (0, 0, 1) #where is up, defaults to z = 1

        vertices = []
        
        # generate world and store vertices
        world = World()
        vertices = world.generateWorld()

        vertices = np.array(vertices, dtype='f4')

        # pass vertices to shaders
        self.vbo = self.ctx.buffer(vertices)
        # self.vao = self.ctx.vertex_array(self.prog, [self.vbo.bind("vert")])
        self.vao = self.ctx.vertex_array(self.prog, [
        (self.vbo, "3f 3f", "vert", "vert_color")
    ]);

    

    def render(self, time: float, frame_time: float):
        # apply character movement and rotation
        self.character.move(frame_time)
        self.character.rotate()
        self.prog['eye'].value = self.character.posVec
        self.prog['center'].value = self.character.posVec + self.character.lookVec
        self.ctx.clear(1.0, 1.0, 1.0)
        # render vertices
        self.vao.render(moderngl.TRIANGLES, 65 * 4)
        
        # print FPS
        print(1.0/frame_time)


    def key_event(self, key, action, modifiers):
        # Key presses
        # start character moving
        if action == self.wnd.keys.ACTION_PRESS:
            if key == self.wnd.keys.W:
                self.character.forward = 1
            if key == self.wnd.keys.S:
                self.character.backward = -1                
            if key == self.wnd.keys.D:
                self.character.right = 1 
            if key == self.wnd.keys.A:
                self.character.left = -1 
            if key == self.wnd.keys.Q:
                self.character.movSpeed = 3.0

        # Key releases
        # stop character moving
        elif action == self.wnd.keys.ACTION_RELEASE:
            if key == self.wnd.keys.W:
                self.character.forward = 0
            if key == self.wnd.keys.S:
                self.character.backward = 0
            if key == self.wnd.keys.D:
                self.character.right = 0 
            if key == self.wnd.keys.A:
                self.character.left = 0 
            if key == self.wnd.keys.Q:
                self.character.movSpeed = 2.0
                
    def mouse_position_event(self, x: int, y: int, dx: int, dy: int):
        self.character.setRotation(dx, dy)

        return super().mouse_position_event(x, y, dx, dy)


if __name__ == '__main__':
    
    AppWindow.run()
    