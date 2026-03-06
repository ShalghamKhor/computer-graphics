import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import glm
from math import sin, cos
import numpy as np
from sphere import generateSphere
from solar_Engine import Object3D



def load_shaders(path):
    with open(path, 'r') as file:
        return file.read()


def _build_texture(base_rgb, accent_rgb, bands=10, noise=0.08, w=512, h=256, seed=0):
    rng = np.random.default_rng(seed)
    u = np.linspace(0.0, 1.0, w, dtype=np.float32)[None, :]
    v = np.linspace(0.0, 1.0, h, dtype=np.float32)[:, None]
    wave = 0.5 + 0.5 * np.sin((v * bands + u * (bands * 0.35)) * 2.0 * np.pi)
    grain = rng.normal(0.0, noise, size=(h, w)).astype(np.float32)
    blend = np.clip(wave + grain, 0.0, 1.0)[..., None]
    base = np.array(base_rgb, dtype=np.float32).reshape(1, 1, 3)
    accent = np.array(accent_rgb, dtype=np.float32).reshape(1, 1, 3)
    tex = base * (1.0 - blend) + accent * blend
    return (np.clip(tex, 0.0, 1.0) * 255).astype(np.uint8)


def _build_earth_texture(w=512, h=256, seed=7):
    rng = np.random.default_rng(seed)
    u = np.linspace(0.0, 1.0, w, dtype=np.float32)[None, :]
    v = np.linspace(0.0, 1.0, h, dtype=np.float32)[:, None]
    continents = (
        np.sin(8.0 * np.pi * u + 3.0 * np.pi * v)
        + 0.7 * np.sin(14.0 * np.pi * u - 5.0 * np.pi * v)
        + 0.35 * np.sin(22.0 * np.pi * (u + v))
    )
    continents += rng.normal(0.0, 0.28, size=(h, w)).astype(np.float32)
    mask = continents > 0.4

    ocean = np.array([0.07, 0.23, 0.62], dtype=np.float32).reshape(1, 1, 3)
    land = np.array([0.14, 0.52, 0.20], dtype=np.float32).reshape(1, 1, 3)
    mountain = np.array([0.50, 0.42, 0.30], dtype=np.float32).reshape(1, 1, 3)

    elev = np.clip(continents, -1.0, 1.8)
    land_mix = np.clip((elev - 0.4) / 1.4, 0.0, 1.0)[..., None]
    land_color = land * (1.0 - land_mix) + mountain * land_mix

    tex = np.tile(ocean, (h, w, 1))
    tex[mask] = land_color[mask]
    clouds = (rng.random((h, w)) > 0.985).astype(np.float32)[..., None]
    tex = np.clip(tex + clouds * 0.25, 0.0, 1.0)
    return (tex * 255).astype(np.uint8)

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
    earth_texture = _build_earth_texture()
    moon_texture = _build_texture((0.48, 0.48, 0.50), (0.66, 0.66, 0.68), bands=18, noise=0.12, seed=2)
    mars_texture = _build_texture((0.55, 0.26, 0.18), (0.76, 0.45, 0.30), bands=12, noise=0.11, seed=3)
    jupiter_texture = _build_texture((0.64, 0.49, 0.36), (0.82, 0.67, 0.52), bands=36, noise=0.05, seed=4)
    saturn_texture = _build_texture((0.63, 0.56, 0.43), (0.80, 0.72, 0.58), bands=30, noise=0.05, seed=5)

    sun = Object3D(vertices_data, shader_program, scaling_factor=2.0, color=glm.vec3(1.0, 1.0, 0.0), specular_strength=0.0, shininess=0.0)
    earth = Object3D(vertices_data, shader_program, scaling_factor=1.0, color=glm.vec3(0.0, 0.0, 1.0), specular_strength=0.5, shininess=32.0, texture_data=earth_texture)
    moon = Object3D(vertices_data, shader_program, scaling_factor=0.5, color=glm.vec3(0.6, 0.6, 0.6), specular_strength=0.3, shininess=16.0, texture_data=moon_texture)
    mars = Object3D(vertices_data, shader_program, scaling_factor=0.8, color=glm.vec3(1.0, 0.5, 0.5), specular_strength=0.4, shininess=24.0, texture_data=mars_texture)
    jupiter = Object3D(vertices_data, shader_program, scaling_factor=1.5, color=glm.vec3(1.0, 0.8, 0.6), specular_strength=0.6, shininess=40.0, texture_data=jupiter_texture)
    saturn = Object3D(vertices_data, shader_program, scaling_factor=1.3, color=glm.vec3(0.8, 0.7, 0.5), specular_strength=0.5, shininess=36.0, texture_data=saturn_texture)

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
