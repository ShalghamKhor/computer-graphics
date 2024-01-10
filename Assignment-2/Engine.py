import ctypes

import glm
import numpy
import numpy as np
from OpenGL import GL

class Object3D:
    def __init__(self, vertices, shaderProgram):
        self.vertices = vertices
        self.shaderProgram = shaderProgram
        self.modelMatrix = glm.mat4(1)
        self.initialize()

    def initialize(self):
        # Generate and bind VAO
        vertex_color = len(self.vertices) // 2
        self.vao = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self.vao)

        # Create VBO for vertices
        self.vertexVBO = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.vertexVBO)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL.GL_STATIC_DRAW)

        # Vertex attribute
        GL.glEnableVertexAttribArray(0)
        GL.glEnableVertexAttribArray(1)
        GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, GL.GL_FALSE, 6*ctypes.sizeof(GL.GLfloat), ctypes.c_void_p(0))
        GL.glVertexAttribPointer(1, 3, GL.GL_FLOAT, GL.GL_FALSE, 6*ctypes.sizeof(GL.GLfloat), ctypes.c_void_p(3*ctypes.sizeof(GL.GLfloat)))


        # Unbind VAO
        GL.glBindVertexArray(0)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)


    def transform(self, matrix):
        self.modelMatrix = matrix

    def display(self):
        GL.glClearColor(0, 0, 0, 1)
        GL.glUseProgram(self.shaderProgram)
        GL.glBindVertexArray(self.vao)

        # Set the model matrix uniform
        modelLoc = GL.glGetUniformLocation(self.shaderProgram, "model")
        GL.glUniformMatrix4fv(modelLoc, 1, GL.GL_FALSE, glm.value_ptr(self.modelMatrix))

        # Draw the object
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, len(self.vertices)//6)

        GL.glBindVertexArray(0)
        GL.glUseProgram(0)
