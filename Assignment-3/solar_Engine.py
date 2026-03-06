from pygame.locals import *
from OpenGL.GL import *
import glm
import ctypes



class Object3D:
    def __init__(self, vertices, shader_program, scaling_factor, color, specular_strength, shininess):
        self.vertices = vertices
        self.shader_program = shader_program
        self.scaling_factor = scaling_factor
        self.color = color
        self.specular_strength = specular_strength
        self.shininess = shininess
        stride = 6 * 4

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)

        # position attribute
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        # normal attribute
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(12))
        glEnableVertexAttribArray(1)

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    def transform(self, transformation_matrix):
        self.model_matrix = glm.mat4(1.0)
        scaled_matrix = glm.scale(glm.mat4(1.0), glm.vec3(self.scaling_factor))
        self.model_matrix = transformation_matrix * scaled_matrix

    def display(self, view_matrix, projection_matrix, view_position, light_position):
        glUseProgram(self.shader_program)
        glBindVertexArray(self.vao)

        # pass matricess to shader
        model_loc = glGetUniformLocation(self.shader_program, "model")
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, glm.value_ptr(self.model_matrix))

        view_loc = glGetUniformLocation(self.shader_program, "view")
        glUniformMatrix4fv(view_loc, 1, GL_FALSE, glm.value_ptr(view_matrix))

        proj_loc = glGetUniformLocation(self.shader_program, "projection")
        glUniformMatrix4fv(proj_loc, 1, GL_FALSE, glm.value_ptr(projection_matrix))

        # pass lighting and material properties
        color_loc = glGetUniformLocation(self.shader_program, "objectColor")
        glUniform3fv(color_loc, 1, glm.value_ptr(self.color))

        specular_loc = glGetUniformLocation(self.shader_program, "specularStrength")
        glUniform1f(specular_loc, self.specular_strength)

        shininess_loc = glGetUniformLocation(self.shader_program, "shininess")
        glUniform1f(shininess_loc, self.shininess)

        view_pos_loc = glGetUniformLocation(self.shader_program, "viewPos")
        glUniform3fv(view_pos_loc, 1, glm.value_ptr(view_position))

        light_pos_loc = glGetUniformLocation(self.shader_program, "lightPos")
        glUniform3fv(light_pos_loc, 1, glm.value_ptr(light_position))


        glDrawArrays(GL_TRIANGLES, 0, len(self.vertices) // 6)

        glBindVertexArray(0)
        glUseProgram(0)
