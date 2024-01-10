#!/usr/bin/python2.7
"""

Based on different sources:

* http://www.arcsynthesis.org/gltut/Basics/Tut02%20Vertex%20Attributes.html
* http://schi.iteye.com/blog/1969710
* https://learnopengl.com/Lighting/Basic-Lighting

"""
import sys
import ctypes
import numpy

from OpenGL import GL, GLU
from OpenGL.GL import shaders
from OpenGL.arrays import vbo

import sdl2
from sdl2 import video
from numpy import array
from math import cos, sin, pi

shaderProgram = None
VAO = None
VBO = None

vertexData = numpy.array([
      # Vertex Positions

      # x    y     z     nx    ny   nz

      -0.5, -0.5, -0.5,  0.0,  0.0, -1.0,
       0.5, -0.5, -0.5,  0.0,  0.0, -1.0, 
       0.5,  0.5, -0.5,  0.0,  0.0, -1.0,
       0.5,  0.5, -0.5,  0.0,  0.0, -1.0, 
      -0.5,  0.5, -0.5,  0.0,  0.0, -1.0, 
      -0.5, -0.5, -0.5,  0.0,  0.0, -1.0, 

      -0.5, -0.5,  0.5,  0.0,  0.0, 1.0,
       0.5, -0.5,  0.5,  0.0,  0.0, 1.0,
       0.5,  0.5,  0.5,  0.0,  0.0, 1.0,      
       0.5,  0.5,  0.5,  0.0,  0.0, 1.0,
      -0.5,  0.5,  0.5,  0.0,  0.0, 1.0,
      -0.5, -0.5,  0.5,  0.0,  0.0, 1.0,

        -0.5,  0.5,  0.5, -1.0,  0.0,  0.0,
        -0.5,  0.5, -0.5, -1.0,  0.0,  0.0,
        -0.5, -0.5, -0.5, -1.0,  0.0,  0.0,
        -0.5, -0.5, -0.5, -1.0,  0.0,  0.0,
        -0.5, -0.5,  0.5, -1.0,  0.0,  0.0,
        -0.5,  0.5,  0.5, -1.0,  0.0,  0.0,

        0.5,  0.5,  0.5,  1.0,  0.0,  0.0,
        0.5,  0.5, -0.5,  1.0,  0.0,  0.0,
        0.5, -0.5, -0.5,  1.0,  0.0,  0.0,
        0.5, -0.5, -0.5,  1.0,  0.0,  0.0,
        0.5, -0.5,  0.5,  1.0,  0.0,  0.0,
        0.5,  0.5,  0.5,  1.0,  0.0,  0.0,

        -0.5, -0.5, -0.5,  0.0, -1.0,  0.0,
        0.5, -0.5, -0.5,  0.0, -1.0,  0.0,
        0.5, -0.5,  0.5,  0.0, -1.0,  0.0,
        0.5, -0.5,  0.5,  0.0, -1.0,  0.0,
        -0.5, -0.5,  0.5,  0.0, -1.0,  0.0,
        -0.5, -0.5, -0.5,  0.0, -1.0,  0.0,

        -0.5,  0.5, -0.5,  0.0,  1.0,  0.0,
        0.5,  0.5, -0.5,  0.0,  1.0,  0.0,
        0.5,  0.5,  0.5,  0.0,  1.0,  0.0,
        0.5,  0.5,  0.5,  0.0,  1.0,  0.0,
        -0.5,  0.5,  0.5,  0.0,  1.0,  0.0,
        -0.5,  0.5, -0.5,  0.0,  1.0,  0.0 

    ], dtype=numpy.float32)

def initialize():
    global shaderProgram
    global VAO
    global VBO

    vertexShader = shaders.compileShader("""
#version 330

layout (location=0) in vec3 position;
layout (location=1) in vec3 normal;

out vec3 theNormal;
out vec3 fragPos;

uniform mat4 m;
uniform mat4 p;

void main()
{
    gl_Position = p * m * vec4(position, 1.0);
    fragPos = vec3(m * vec4(position, 1.0));
    theNormal = transpose(inverse(mat3(m))) * normal;
}
""", GL.GL_VERTEX_SHADER)

    fragmentShader = shaders.compileShader("""
#version 330

in vec3 theNormal;
in vec3 fragPos;

out vec4 outputColor;

uniform vec3 lightPos;
uniform vec3 viewPos;

void main()
{
    // ambient component
    float ambInt = 0.3;
    vec3 ambColor = vec3(1.0, 1.0, 1.0);
    vec3 amb = ambInt * ambColor;

    // diffuse component
    vec3 diffColor = vec3(1.0, 1.0, 1.0);
    vec3 lightDir = normalize(lightPos - fragPos);
    vec3 norm = normalize(theNormal);
    float diffInt = max(dot(lightDir, norm), 0.0);
    vec3 diff = diffInt * diffColor;

    // specular component
    float specInt = 1.0;
    vec3 viewDir = normalize(viewPos - fragPos);
    vec3 reflectDir = reflect(-lightDir, norm);
    float specPow = pow(max(dot(viewDir, reflectDir), 0.0), 256);
    vec3 spec = specInt * specPow * diffColor;
    
    //vec4 fragColor = (theNormal + 1.0) / 2.0;
    vec3 fragColor = vec3(0.5, 0.7, 0.1);
    outputColor = vec4((spec + diff + amb) * fragColor, 1.0);
}
""", GL.GL_FRAGMENT_SHADER)

    shaderProgram = shaders.compileProgram(vertexShader, fragmentShader)    

    # Create one "object" (the triangle) and make it active ("bind" it)
    VAO = GL.glGenVertexArrays(1)
    GL.glBindVertexArray(VAO)

    # Allocate a buffer to contain the triangle's vertices and make it active ("bind" it)
    VBO = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, VBO)

    # Transfer the triangle's vertices to the GPU (i.e. the buffer you allocated)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, vertexData.nbytes, vertexData,
        GL.GL_STATIC_DRAW)

    # Enable the first attribute of the triangle: the position of each vertex
    GL.glEnableVertexAttribArray(0)

    # Describe the first attribute: the position
    # - location: 0                 (remember the shader?)
    # - size of each vertex: 3      (vec3)
    # - type of vertices: float
    # - do not normalize            (ignore for now)
    # - stride: 0                   (there is no space between vertices)
    # - offset: None                (start from the first element; no offset)    
    GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, GL.GL_FALSE, 6 * 4, None)

    # The same for the second attribute: the normal of each vertex
    GL.glEnableVertexAttribArray(1)
    
    # The last parameter is actually a pointer
    GL.glVertexAttribPointer(1, 3, GL.GL_FLOAT, GL.GL_FALSE, 6 * 4, ctypes.c_void_p(3 * 4))

    # Cleanup (just in case)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    GL.glBindVertexArray(0)

    GL.glEnable(GL.GL_DEPTH_TEST)


angle = [0, 0, 0]

def render():
    global shaderProgram
    global VAO
    global angle

    GL.glClearColor(0.1, 0.1, 0.1, 1.0)
    GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

    # active shader program
    GL.glUseProgram(shaderProgram)


    # Setup the scale matrix
    scaleMat = numpy.identity(4)
    #scaleMat[0,0] = 0.5
    #scaleMat[1,1] = 0.5

    # Setup the translation matrix
    translMat = numpy.identity(4)
    #translMat[0,3] = 0.5
    #translMat[1,3] = -0.4
    translMat[2,3] = -5

    # Setup the rotation matrix
    angle[1] += 0.1 * pi / 180
    #angle[1] = 3 * pi / 180
    
    rotY = numpy.identity(4)
    rotY[0,0] = cos(angle[1])
    rotY[0,2] = sin(angle[1])
    rotY[2,0] = -sin(angle[1])
    rotY[2,2] = cos(angle[1])

    rotZ = numpy.identity(4)
    rotZ[0,0] = cos(angle[2])
    rotZ[0,1] = -sin(angle[2])
    rotZ[1,0] = sin(angle[2])
    rotZ[1,1] = cos(angle[2])

    rotMat = rotZ @ rotY

    modelMat = translMat @ rotMat @ scaleMat

    # Send it to the shader in the right location
    mLoc = GL.glGetUniformLocation(shaderProgram, "m")
    GL.glUniformMatrix4fv(mLoc, 1, True, modelMat)

    perspMat = numpy.identity(4)
    fov = numpy.radians(60)
    aspect_ratio = 1
    near = 1
    far = 1000
    cot_half = 1.0 / numpy.tan(fov / 2)    
    perspMat[0, 0] = cot_half / aspect_ratio
    perspMat[1, 1] = cot_half
    perspMat[2, 2] = (far + near) / (near - far)
    perspMat[2, 3] = (2 * far * near) / (near - far)
    perspMat[3, 2] = -1
    pLoc = GL.glGetUniformLocation(shaderProgram, "p")
    GL.glUniformMatrix4fv(pLoc, 1, True, perspMat)

    lightPosLoc = GL.glGetUniformLocation(shaderProgram, "lightPos")
    GL.glUniform3f(lightPosLoc, 0.0, 0.0, 0.0)

    viewPosLoc = GL.glGetUniformLocation(shaderProgram, "viewPos")
    GL.glUniform3f(viewPosLoc, 0.0, 0.0, 0.0)

    try:
        # Activate the object
        GL.glBindVertexArray(VAO)

        # draw triangle
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, len(vertexData) // 6)
    
    finally:
        # Cleanup (just in case)
        GL.glBindVertexArray(0)
        GL.glUseProgram(0)


def run():
    if sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO) != 0:
        print(sdl2.SDL_GetError())
        return -1

    window = sdl2.SDL_CreateWindow(b"OpenGL demo",
                                   sdl2.SDL_WINDOWPOS_UNDEFINED,
                                   sdl2.SDL_WINDOWPOS_UNDEFINED, 800, 800,
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
    initialize()

    event = sdl2.SDL_Event()
    running = True
    while running:
        while sdl2.SDL_PollEvent(ctypes.byref(event)) != 0:
            if event.type == sdl2.SDL_QUIT:
                running = False

        render()

        sdl2.SDL_GL_SwapWindow(window)
        sdl2.SDL_Delay(10)

    sdl2.SDL_GL_DeleteContext(context)
    sdl2.SDL_DestroyWindow(window)
    sdl2.SDL_Quit()
    return 0

if __name__ == "__main__":
    sys.exit(run())
