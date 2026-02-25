import numpy as np
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import pygame



def toPoint(x):
    y = x * 0.6 + 4 * np.random.randn()
    weight = 1.01 * x + 0.02 * np.random.randn()
    return [x, y, weight]

def createDatapoints():
    x = list(range(1, 50))
    x = list(map(lambda val: val + np.random.randn()*3 - 1.5, x))
    return list(map(toPoint, x))



def normalize_dataset(dataset):
    x_vals = [p[0] for p in dataset]
    y_vals = [p[1] for p in dataset]
    weights = [p[2] for p in dataset]
    
    x_min, x_max = min(x_vals), max(x_vals)
    y_min, y_max = min(y_vals), max(y_vals)
    weight_min, weight_max = min(weights), max(weights)
    
    normalized = []
    for x, y, weight in dataset:
        x_clip = (x - x_min) / (x_max - x_min) * 2 - 1
        y_clip = (y - y_min) / (y_max - y_min) * 2 - 1
        normalized_weight = 0.01 + (weight - weight_min) * (0.1 - 0.01) / (weight_max - weight_min)
        normalized.append([x_clip, y_clip, normalized_weight])
    return normalized


def load_shaders(path):
    with open(path, 'r') as file:
        return file.read()

vertex_shader = load_shaders("point_shaders/vertex_shader.txt")
print("vertex shader content", vertex_shader)
fragment_shader = load_shaders("point_shaders/fragment_shader.txt")
print("fragement shader content   ", fragment_shader)


def setup_shaders():
    shader = compileProgram(
        compileShader(vertex_shader, GL_VERTEX_SHADER),
        compileShader(fragment_shader, GL_FRAGMENT_SHADER)
    )
    return shader

def setup_buffers(normalized_data):
    vertices = []
    centers = []
    sizes = []
    indices = []

    quad = [(-0.5, -0.5), (0.5, -0.5), (0.5, 0.5), (-0.5, 0.5)] # a unit quad
    index_pattern = [0, 1, 2, 2, 3, 0] # indices for drawng two triangels per quad

    for i, (cx, cy, size) in enumerate(normalized_data):
        quad_indices = [vi + i * 4 for vi in index_pattern] # offset indices for this quad
        indices.extend(quad_indices)
        for vx, vy in quad:
            vertices.extend([vx, vy])
            centers.extend([cx, cy])
            sizes.append(size)

    # vonvert to numpy arrays
    vertices = np.array(vertices, dtype=np.float32)
    centers = np.array(centers, dtype=np.float32)
    sizes = np.array(sizes, dtype=np.float32)
    indices = np.array(indices, dtype=np.uint32)

    # setup buffers
    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)

    # vertex buffer
    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(0)

    # center buffer
    cbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, cbo)
    glBufferData(GL_ARRAY_BUFFER, centers.nbytes, centers, GL_STATIC_DRAW)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(1)

    # size buffer
    sbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, sbo)
    glBufferData(GL_ARRAY_BUFFER, sizes.nbytes, sizes, GL_STATIC_DRAW)
    glVertexAttribPointer(2, 1, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(2)

    # element buffer
    ebo = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

    return vao, len(indices)

def render():
    glClear(GL_COLOR_BUFFER_BIT)

    glUseProgram(shader_program)
    glUniform3f(glGetUniformLocation(shader_program, "color"), 0.2, 0.6, 0.8) # Circle color
    glBindVertexArray(vao)
    glDrawElements(GL_TRIANGLES, index_count, GL_UNSIGNED_INT, None)






if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 800), pygame.DOUBLEBUF | pygame.OPENGL)
    pygame.display.set_caption("Data Visualization with Pygame")


    glClearColor(0.1, 0.1, 0.1, 1.0)
    dataset = createDatapoints()
    normalized_data = normalize_dataset(dataset)
    shader_program = setup_shaders()
    vao, index_count = setup_buffers(normalized_data)


    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        render()
        pygame.display.flip()
        pygame.time.wait(10)

    pygame.quit()