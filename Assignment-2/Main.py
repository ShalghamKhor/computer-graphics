import sdl2
from OpenGL.GL import *
import ctypes
import sdl2.ext
from OpenGL import GL
from OpenGL.GL import shaders
from sdl2 import video
import glm
import cube
import Shader
from Engine import Object3D
from Scene import Scene

def compile_shader(source, shader_type):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)

    if glGetShaderiv(shader, GL_COMPILE_STATUS) != GL_TRUE:
        raise RuntimeError(glGetShaderInfoLog(shader))

    return shader

def create_shader_program(vertex_src, fragment_src):
    vertex_shader = compile_shader(vertex_src, GL_VERTEX_SHADER)
    fragment_shader = compile_shader(fragment_src, GL_FRAGMENT_SHADER)

    shader_program = glCreateProgram()
    glAttachShader(shader_program, vertex_shader)
    glAttachShader(shader_program, fragment_shader)
    glLinkProgram(shader_program)

    if glGetProgramiv(shader_program, GL_LINK_STATUS) != GL_TRUE:
        raise RuntimeError(glGetProgramInfoLog(shader_program))

    glDeleteShader(vertex_shader)
    glDeleteShader(fragment_shader)

    return shader_program


vertex_shader = """
#version 330 core
layout (location = 0) in vec3 aPos;   // Vertex position
layout (location = 1) in vec3 aColor; // Vertex color

out vec3 ourColor; // Output color to the fragment shader

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

void main()
{
    gl_Position = projection * view * model * vec4(aPos, 1.0);
    ourColor = aColor;
}
"""


fragment_shader = """
#version 330 core
out vec4 FragColor;

in vec3 ourColor;

void main()
{
    FragColor = vec4(ourColor, 1.0);
}
"""
# Initialize SDL2
sdl2.ext.init()

# Create an SDL2 window with OpenGL context
window = sdl2.SDL_CreateWindow(b"3D Scene", sdl2.SDL_WINDOWPOS_UNDEFINED,
                               sdl2.SDL_WINDOWPOS_UNDEFINED, 800, 600, sdl2.SDL_WINDOW_OPENGL)

# Set OpenGL context attributes
video.SDL_GL_SetAttribute(video.SDL_GL_CONTEXT_MAJOR_VERSION, 3)
video.SDL_GL_SetAttribute(video.SDL_GL_CONTEXT_MINOR_VERSION, 3)
video.SDL_GL_SetAttribute(video.SDL_GL_CONTEXT_PROFILE_MASK, video.SDL_GL_CONTEXT_PROFILE_CORE)

# Create the OpenGL context
context = sdl2.SDL_GL_CreateContext(window)
GL.glEnable(GL.GL_DEPTH_TEST)

# Initialize GLEW (if you're using GLEW)
# import OpenGL.GLEW as GLEW
# GLEW.glewInit()

# Ensure glCreateShader is available
if not GL.glCreateShader:
    raise Exception("glCreateShader function not available")

# Load and compile shaders
"""
vertex_shader_code = Shader.vertShader()
fragment_shader_code = Shader.fragShader()

vertex_shader = shaders.compileShader(vertex_shader_code, GL.GL_VERTEX_SHADER)
fragment_shader = shaders.compileShader(fragment_shader_code, GL.GL_FRAGMENT_SHADER)

# Link the shader program
shader_program = shaders.compileProgram(vertex_shader, fragment_shader)
"""
shader_program = create_shader_program(vertex_shader, fragment_shader)


# Cube vertices
vertex = cube.cube_vertices

# Create Object3D instance
objec1 = Object3D(vertex, shader_program)

# Camera settings
camera_position = glm.vec3(4, 3, 3)
camera_target = glm.vec3(0, 0, 0)
camera_up = glm.vec3(0, 1, 0)
fov = 45.0
aspect_ratio = 800 / 600
near = 0.1
far = 100.0

# Create the scene
scene = Scene([objec1], camera_position, camera_target, camera_up, fov, aspect_ratio, near, far)

# Main loop
running = True
while running:
    events = sdl2.ext.get_events()
    for event in events:
        if event.type == sdl2.SDL_QUIT:
            running = False
    GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
    scene.display()

    sdl2.SDL_GL_SwapWindow(window)
    sdl2.SDL_Delay(10)

# Cleanup
sdl2.SDL_GL_DeleteContext(context)
sdl2.SDL_DestroyWindow(window)
sdl2.ext.quit()
