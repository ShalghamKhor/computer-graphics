import sdl2
import sdl2.ext
from OpenGL.GL import *
import numpy as np
import glm
import OpenGL.GL as gl
import numpy as np
from cube import vertices
import math
from Enigine import Object3D
from Scene import Camera, Scene


def main():
    sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO)
    sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_MAJOR_VERSION, 3)
    sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_MINOR_VERSION, 3)
    sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_PROFILE_MASK, sdl2.SDL_GL_CONTEXT_PROFILE_CORE)

    window = sdl2.SDL_CreateWindow(b"OpenGL Window",
                                sdl2.SDL_WINDOWPOS_UNDEFINED,
                                sdl2.SDL_WINDOWPOS_UNDEFINED, 800, 600,
                                sdl2.SDL_WINDOW_OPENGL)

    glcontext = sdl2.SDL_GL_CreateContext(window)
    glEnable(GL_DEPTH_TEST)
    
    # Load and create shader programs
    vertex_shader = load_shaders("shaders/vertex.tx")
    fragment_shader = load_shaders("shaders/fragment.txt")
    shader_program = create_shader_program(vertex_shader, fragment_shader)
 
    vertices_data = np.array(vertices, dtype=np.float32) # vertex data

    # instance of 3d cube
    object1 = Object3D(vertices_data, shader_program, 0.20)
    object1.transform(glm.translate(glm.mat4(1), glm.vec3(0, 1, -8)))  # transformation for the first cube

    object2 = Object3D(vertices_data, shader_program, 0.40)
    object2.transform(glm.translate(glm.mat4(1), glm.vec3(0, 2, -6)))  # transformation for the second cube

    object3 = Object3D(vertices_data, shader_program, 0.30)
    object3.transform(glm.translate(glm.mat4(1), glm.vec3(-1, 0, -7)))  # transformation for the third cube

   
   
    # Initialize the camera
    camera = Camera()
    center_x = (object1.model_matrix[3][0] + object2.model_matrix[3][0] + object3.model_matrix[3][0]) / 3
    center_y = (object1.model_matrix[3][1] + object2.model_matrix[3][1] + object3.model_matrix[3][1]) / 3
    center_z = (object1.model_matrix[3][2] + object2.model_matrix[3][2] + object3.model_matrix[3][2]) / 3

    # cameras target to the calculated center
    camera.set_target(glm.vec3(center_x, center_y, center_z))

    # cameras initial position
    camera_distance = 10.0
    camera_x = center_x
    camera_y = center_y + camera_distance
    camera_z = center_z

    camera.set_position(glm.vec3(camera_x, camera_y, camera_z))
    camera.set_up_vector(glm.vec3(0.0, 1.0, 0.0))
    camera.set_perspective(45, 800/600, 0.1, 60)

    # create the scene for the 3 cubes
    scene = Scene([object1, object2, object3], camera)
    

 
    running = True
    angle = 0
    rotation_increament = 0.005
    while running:
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                running = False

        # clear the screen
        gl.glClearColor(0.0, 0.0, 0.0, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        angle += rotation_increament 
        camera_x = center_x + camera_distance * math.sin(angle)
        camera_z = center_z + camera_distance * math.cos(angle)
        camera.set_position(glm.vec3(camera_x, camera_y, camera_z))

        scene.display()

        # Swap the window buffers
        sdl2.SDL_GL_SwapWindow(window)

    # clean up
    sdl2.SDL_GL_DeleteContext(glcontext)
    sdl2.ext.quit()

def load_shaders(path):
    with open(path, 'r') as file:
        return file.read()

# compile shaders
def compile_shader(source, shader_type):
    shader = gl.glCreateShader(shader_type)
    gl.glShaderSource(shader, source)
    gl.glCompileShader(shader)

    # Check for errors
    result = gl.glGetShaderiv(shader, gl.GL_COMPILE_STATUS)
    if not result:
        raise RuntimeError(gl.glGetShaderInfoLog(shader).decode())

    return shader

# Linking shaders
def create_shader_program(vertex_source, fragment_source):
    vertex_shader = compile_shader(vertex_source, gl.GL_VERTEX_SHADER)
    fragment_shader = compile_shader(fragment_source, gl.GL_FRAGMENT_SHADER)

    program = gl.glCreateProgram()
    gl.glAttachShader(program, vertex_shader)
    gl.glAttachShader(program, fragment_shader)
    gl.glLinkProgram(program)

    if not gl.glGetProgramiv(program, gl.GL_LINK_STATUS):
        raise RuntimeError(gl.glGetProgramInfoLog(program).decode())

    gl.glDetachShader(program, vertex_shader)
    gl.glDetachShader(program, fragment_shader)
    gl.glDeleteShader(vertex_shader)
    gl.glDeleteShader(fragment_shader)

    return program


if __name__ == "__main__":
    main()
