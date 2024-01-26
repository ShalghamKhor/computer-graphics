from OpenGL.GL import *
import numpy as np
import glm
import OpenGL.GL as gl

class Object3D:
    def __init__(self, vertices, shader_program, scaling_factor):
        self.vertices = vertices
        self.shader_program = shader_program
        self.scaling_factor = scaling_factor

        # Create and bind the VAO
        self.vao = gl.glGenVertexArrays(1)
        gl.glBindVertexArray(self.vao)

        # Create VBO, bind it, and upload data
        vbo = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, gl.GL_STATIC_DRAW)

        # Enable vertex attribute arrays and set pointer
        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 6*4, ctypes.c_void_p(0))
        gl.glEnableVertexAttribArray(0)
        
        gl.glVertexAttribPointer(1, 3, gl.GL_FLOAT, gl.GL_FALSE, 6*4, ctypes.c_void_p(12))  # 12 = offset for color
        gl.glEnableVertexAttribArray(1)
        
        # Unbind VAO and VBO
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)
        gl.glBindVertexArray(0)

    def transform(self, transformation_matrix):
        scaled_matrix = glm.scale(transformation_matrix, glm.vec3(self.scaling_factor))
        self.model_matrix = scaled_matrix

    def display(self, view_matrix, projection_matrix ):
        gl.glUseProgram(self.shader_program)

        # Bind the VAO
        gl.glBindVertexArray(self.vao)

        # Set the model matrix uniform
        model_loc = gl.glGetUniformLocation(self.shader_program, "model")

        if isinstance(self.model_matrix, glm.mat4x4):
            matrix_list = np.array(self.model_matrix.to_list(), dtype=np.float32)
            matrix_flat = matrix_list.flatten()
        else:
            matrix_flat = self.model_matrix
        
        gl.glUniformMatrix4fv(model_loc, 1, gl.GL_FALSE, matrix_flat)

        view_loc = gl.glGetUniformLocation(self.shader_program, "view")
        gl.glUniformMatrix4fv(view_loc, 1, gl.GL_FALSE, glm.value_ptr(view_matrix))
        
        proj_loc = gl.glGetUniformLocation(self.shader_program, "projection")
        if isinstance(projection_matrix, glm.mat4x4):
            matrix_flat = glm.value_ptr(projection_matrix)
        else:
            matrix_flat = projection_matrix.flatten()
        gl.glUniformMatrix4fv(proj_loc, 1, gl.GL_FALSE, matrix_flat)
        

        # Draw the object
        gl.glDrawArrays(gl.GL_TRIANGLES, 0, len(self.vertices)//6)

        # Unbind VAO and shader program
        gl.glBindVertexArray(0)
        gl.glUseProgram(0)
