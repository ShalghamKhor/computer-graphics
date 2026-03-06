import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import glm
from math import sin, cos
from sphere import generateSphere
from solar_Engine import Object3D



def load_shaders(path):
    with open(path, 'r') as file:
        return file.read()

def solar_run():
    pygame.init()
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_FORWARD_COMPATIBLE_FLAG, 1)
    pygame.display.set_mode((1024, 768), DOUBLEBUF | OPENGL)
    print(glGetString(GL_VERSION))
    print(glGetString(GL_SHADING_LANGUAGE_VERSION))
    pygame.display.set_caption("OpenGL Solar System")
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)  # Enable backface culling
    glCullFace(GL_BACK)
    glClearColor(0.1, 0.1, 0.1, 1.0)


    fragment_shader = load_shaders("solar_shaders/fragment_shader.txt")
    print(fragment_shader)
    vertex_shader = load_shaders("solar_shaders/vertex_shader.txt")
    print(vertex_shader)

    shader_program = compileProgram(compileShader(vertex_shader, GL_VERTEX_SHADER), compileShader(fragment_shader, GL_FRAGMENT_SHADER), validate=False)
    vertices_data = generateSphere(64, 64)
    sun = Object3D(vertices_data, shader_program, scaling_factor=2.0, color=glm.vec3(1.0, 1.0, 0.0), specular_strength=0.0, shininess=0.0)
    earth = Object3D(vertices_data, shader_program, scaling_factor=1.0, color=glm.vec3(0.0, 0.0, 1.0), specular_strength=0.5, shininess=32.0)
    moon = Object3D(vertices_data, shader_program, scaling_factor=0.5, color=glm.vec3(0.6, 0.6, 0.6), specular_strength=0.3, shininess=16.0)
    mars = Object3D(vertices_data, shader_program, scaling_factor=0.8, color=glm.vec3(1.0, 0.5, 0.5), specular_strength=0.4, shininess=24.0)
    jupiter = Object3D(vertices_data, shader_program, scaling_factor=1.5, color=glm.vec3(1.0, 0.8, 0.6), specular_strength=0.6, shininess=40.0)
    saturn = Object3D(vertices_data, shader_program, scaling_factor=1.3, color=glm.vec3(0.8, 0.7, 0.5), specular_strength=0.5, shininess=36.0)

    camera = glm.lookAt(glm.vec3(0, 30, 80), glm.vec3(0, 0, 0), glm.vec3(0, 1, 0))
    projection = glm.perspective(glm.radians(45.0), 1024 / 768, 0.1, 200.0)
    light_position = glm.vec3(0, 0, 0)  # Light at the sun's position
    view_position = glm.vec3(0, 30, 80)

    earth_orbit_angle = 0.0
    earth_rotation_angle = 0.0
    moon_orbit_angle = 0.0
    moon_rotation_angle = 0.0
    mars_orbit_angle = 0.0
    mars_rotation_angle = 0.0
    jupiter_orbit_angle = 0.0
    jupiter_rotation_angle = 0.0
    saturn_orbit_angle = 0.0
    saturn_rotation_angle = 0.0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Sun (no rotation or specular lighting)
        sun.transform(glm.mat4(1.0))
        sun.display(camera, projection, view_position,light_position)

        # Earth
        earth_orbit_angle += 0.01
        earth_rotation_angle += 0.02
        earth_transform = glm.rotate(glm.mat4(1.0), earth_orbit_angle, glm.vec3(0, 1, 0))
        earth_transform = glm.translate(earth_transform, glm.vec3(15.0, 0, 15.0))
        earth_transform = glm.rotate(earth_transform, earth_rotation_angle, glm.vec3(0, 1, 0))
        earth.transform(earth_transform)
        earth.display(camera, projection, view_position,light_position)

        # Moon orbiting the Earth
        moon_orbit_angle += 0.05
        moon_rotation_angle += 0.1
        moon_transform = glm.translate(earth_transform, glm.vec3(3 * cos(moon_orbit_angle), 0, 3 * sin(moon_orbit_angle)))
        moon_transform = glm.rotate(moon_transform, moon_rotation_angle, glm.vec3(0, 1, 0))
        moon.transform(moon_transform)
        moon.display(camera, projection, view_position,light_position)

        # Mars
        mars_orbit_angle += 0.008
        mars_rotation_angle += 0.015
        mars_transform = glm.rotate(glm.mat4(1.0), mars_orbit_angle, glm.vec3(0, 1, 0))
        mars_transform = glm.translate(mars_transform, glm.vec3(20.0, 0, 20.0))
        mars_transform = glm.rotate(mars_transform, mars_rotation_angle, glm.vec3(0, 1, 0))
        mars.transform(mars_transform)
        mars.display(camera, projection, view_position,light_position)

        # Jupiter
        jupiter_orbit_angle += 0.004
        jupiter_rotation_angle += 0.01
        jupiter_transform = glm.rotate(glm.mat4(1.0), jupiter_orbit_angle, glm.vec3(0, 1, 0))
        jupiter_transform = glm.translate(jupiter_transform, glm.vec3(25.0, 0, 25.0))
        jupiter_transform = glm.rotate(jupiter_transform, jupiter_rotation_angle, glm.vec3(0, 1, 0))
        jupiter.transform(jupiter_transform)
        jupiter.display(camera, projection, view_position,light_position)

        # Saturn
        saturn_orbit_angle += 0.003
        saturn_rotation_angle += 0.008
        saturn_transform = glm.rotate(glm.mat4(1.0), saturn_orbit_angle, glm.vec3(0, 1, 0))
        saturn_transform = glm.translate(saturn_transform, glm.vec3(30.0, 0, 30.0))
        saturn_transform = glm.rotate(saturn_transform, saturn_rotation_angle, glm.vec3(0, 1, 0))
        saturn.transform(saturn_transform)
        saturn.display(camera, projection, view_position,light_position)

        pygame.display.flip()
        pygame.time.wait(10)

    pygame.quit()


solar_run()
