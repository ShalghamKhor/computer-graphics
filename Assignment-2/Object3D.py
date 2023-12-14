import glm
import numpy as np
from OpenGL import GL

class Object3D:
    def __init__(self, vertices, colors, shaderProgram):
        self.vertices = vertices
        self.colors = colors
        self.shaderProgram = shaderProgram
        self.modelMatrix = glm.mat4(1)
        self.initialize()

    def initialize(self):
        # Generate and bind VAO
        self.vao = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self.vao)

        # Create VBO for vertices
        self.vertexVBO = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.vertexVBO)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL.GL_STATIC_DRAW)

        # Vertex attribute
        GL.glEnableVertexAttribArray(0)
        GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, GL.GL_FALSE, 0, None)

        # Create VBO for colors
        self.colorVBO = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.colorVBO)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, self.colors.nbytes, self.colors, GL.GL_STATIC_DRAW)

        # Color attribute
        GL.glEnableVertexAttribArray(1)
        GL.glVertexAttribPointer(1, 3, GL.GL_FLOAT, GL.GL_FALSE, 0, None)

        # Unbind VAO
        GL.glBindVertexArray(0)

    def transform(self, matrix):
        self.modelMatrix = matrix

    def display(self):
        GL.glUseProgram(self.shaderProgram)
        GL.glBindVertexArray(self.vao)

        # Set the model matrix uniform
        modelLoc = GL.glGetUniformLocation(self.shaderProgram, "model")
        GL.glUniformMatrix4fv(modelLoc, 1, GL.GL_FALSE, glm.value_ptr(self.modelMatrix))

        # Draw the object
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, len(self.vertices))

        GL.glBindVertexArray(0)
        GL.glUseProgram(0)
