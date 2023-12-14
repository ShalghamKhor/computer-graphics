import sys
import ctypes
import numpy

from OpenGL import GL, GLU
from OpenGL.GL import shaders
from OpenGL.arrays import vbo

import sdl2
from sdl2 import video
from numpy import array

import shader

shaderProgram = None
VAO = None
VBO = None
offset_x = 0.0
offset_y = 0.0


vertexshader = shader.vertShader()
fragmentshader = shader.fragShader()
vertexdata = shader.vertData()


def mouse_position(mouse_x, mouse_y):
    window_width, window_height = 800, 600

    x = (mouse_x / window_width) * 2 - 1
    y = 1 - (mouse_y / window_height) * 2

    return x,y

def initialize(vertexshade, fragmentshade, vertdata):
    global shaderProgram
    global VAO
    global VBO

    vertexShader = shaders.compileShader(vertexshade, GL.GL_VERTEX_SHADER)

    fragmentShader = shaders.compileShader(fragmentshade, GL.GL_FRAGMENT_SHADER)


    vertexData = numpy.array(vertdata, dtype=numpy.float32)

    # Core OpenGL requires that at least one OpenGL vertex array be bound
    VAO = GL.glGenVertexArrays(1)
    GL.glBindVertexArray(VAO)
    shaderProgram = shaders.compileProgram(vertexShader, fragmentShader)

    # Need VBO for triangle vertices and colours
    VBO = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, VBO)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, vertexData.nbytes, vertexData,
                    GL.GL_STATIC_DRAW)

    # enable array and set up data
    GL.glEnableVertexAttribArray(0)
    GL.glEnableVertexAttribArray(1)
    GL.glVertexAttribPointer(0, 4, GL.GL_FLOAT, GL.GL_FALSE, 0,
                             None)
    # the last parameter is a pointer
    GL.glVertexAttribPointer(1, 4, GL.GL_FLOAT, GL.GL_FALSE, 0,
                             ctypes.c_void_p(288))

    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    GL.glBindVertexArray(0)


def render():
    global shaderProgram
    global VAO
    global offset_x
    global offset_y

    GL.glClearColor(0, 0, 0, 1)
    GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

    # active shader program
    GL.glUseProgram(shaderProgram)
    offsetX_location = GL.glGetUniformLocation(shaderProgram, "offsetX")
    offsetY_location = GL.glGetUniformLocation(shaderProgram, "offsetY")
    GL.glUniform1f(offsetX_location, offset_x)
    GL.glUniform1f(offsetY_location, offset_x)

    try:
        GL.glBindVertexArray(VAO)

        # draw triangle
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, 18)
    finally:
        GL.glBindVertexArray(0)
        GL.glUseProgram(0)


def run():
    global offset_x, offset_y
    if sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO) != 0:
        print(sdl2.SDL_GetError())
        return -1

    window = sdl2.SDL_CreateWindow(b"OpenGL demo",
                                   sdl2.SDL_WINDOWPOS_UNDEFINED,
                                   sdl2.SDL_WINDOWPOS_UNDEFINED, 800, 600,
                                   sdl2.SDL_WINDOW_OPENGL)
    if not window:
        print(sdl2.SDL_GetError())
        return -1

    # Force OpenGL 3.3 'core' context.
    # Must set *before* creating GL context!
    video.SDL_GL_SetAttribute(video.SDL_GL_CONTEXT_MAJOR_VERSION, 3)
    video.SDL_GL_SetAttribute(video.SDL_GL_CONTEXT_MINOR_VERSION, 3)
    video.SDL_GL_SetAttribute(video.SDL_GL_CONTEXT_PROFILE_MASK,
                              video.SDL_GL_CONTEXT_PROFILE_CORE)
    context = sdl2.SDL_GL_CreateContext(window)

    # Setup GL shaders, data, etc.
    initialize(vertexshader, fragmentshader, vertexdata)

    event = sdl2.SDL_Event()
    running = True
    while running:
        while sdl2.SDL_PollEvent(ctypes.byref(event)) != 0:
            if event.type == sdl2.SDL_QUIT:
                running = False
            else:
                offset_x, offset_y = mouse_position(event.motion.x, event.motion.y)

        render()

        sdl2.SDL_GL_SwapWindow(window)
        sdl2.SDL_Delay(10)

    sdl2.SDL_GL_DeleteContext(context)
    sdl2.SDL_DestroyWindow(window)
    sdl2.SDL_Quit()
    return 0


if __name__ == "__main__":
    sys.exit(run())