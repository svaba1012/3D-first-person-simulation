import moderngl_window as mglw

class Window(mglw.WindowConfig):
    gl_version = (3, 3)
    title = "3D First Person"
    window_size = (1280, 720)
    aspect_ratio = 16 / 9
    resizable = True