import glm
from OpenGL import GL
from OpenGL.GL import shaders
import cube
import Shader
import Object3D
import Scene
import sdl2
import sdl2.ext

sdl2.ext.init()
window = sdl2.ext.Window("3D Scene", size=(800, 600))
window.show()
context = sdl2.SDL_GL_CreateContext(window.window)


vertex = cube.cube_vertices
color = cube.cube_colors
vertex_shader = Shader.vertShader()
fragment_shader = Shader.fragShader()

vertex_shader = shaders.compileShader(vertex_shader, GL.GL_VERTEX_SHADER)
fragment_shader = shaders.compileShader(fragment_shader, GL.GL_FRAGMENT_SHADER)
shader_program = shaders.compileProgram(vertex_shader, fragment_shader)
objec1 = Object3D(vertex, color, shader_program)


# Camera settings
camera_position = glm.vec3(4, 3, 3)
camera_target = glm.vec3(0, 0, 0)
camera_up = glm.vec3(0, 1, 0)
fov = 45.0
aspect_ratio = 800 / 600  # Assuming a window size of 800x600
near = 0.1
far = 100.0

# Create the scene
scene = Scene([objec1], camera_position, camera_target, camera_up, fov, aspect_ratio, near, far)


running = True
while running:
    events = sdl2.ext.get_events()
    for event in events:
        if event.type == sdl2.SDL_QUIT:
            running = False

    GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
    scene.display()

    sdl2.SDL_GL_SwapWindow(window.window)
    sdl2.SDL_Delay(10)

sdl2.SDL_GL_DeleteContext(context)
window.close()
sdl2.ext.quit()