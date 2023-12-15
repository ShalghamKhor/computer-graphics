# Define the vertices for a cube (centered at the origin)
import numpy

cube_vertices = numpy.array([
    # left Face
    -1.0, -1.0, 1.0, 1.0,  # Bottom-left
    -1.0, -1.0, -1.0, 1.0,  # Bottom-right
    -1.0, 1.0, -1.0, 1.0,  # Top-right
    -1.0, 1.0, 1.0, 1.0,  # Top-left

    # right face
    1.0, -1.0, -1.0, 1.0,
    1.0, -1.0, -1.0, 1.0,
    1.0, 1.0, -1.0, 1.0,
    1.0, 1.0, 1.0, 1.0,

    # top face
    -1.0, 1.0, -1.0, 1.0,
    1.0, 1.0, -1.0, 1.0,
    1.0, 1.0, -1.0, 1.0,
    -1.0, 1.0, -1.0, 1.0,

    # bottom face
    -1.0, -1.0, 1.0, 1.0,
    1.0, -1.0, 1.0, 1.0,
    1.0, -1.0, -1.0, 1.0,
    -1.0, -1.0, -1.0, 1.0,

    # ... (define vertices for the other four faces)

# Define colors for each vertex
    # Front face (red)
    1.0, 0.0, 0.0, 1.0,
    1.0, 0.0, 0.0, 1.0,
    1.0, 0.0, 0.0, 1.0,
    1.0, 0.0, 0.0, 1.0,

    # Back face (green)
    0.0, 1.0, 0.0, 1.0,
    0.0, 1.0, 0.0, 1.0,
    0.0, 1.0, 0.0, 1.0,
    0.0, 1.0, 0.0, 1.0,

    # top Face (cyan)
    0.0, 1.0, 1.0, 1.0,
    0.0, 1.0, 1.0, 1.0,
    0.0, 1.0, 1.0,1.0,
    0.0, 1.0, 1.0,1.0,

    # bottom face (red)
    1.0, 0.0, 1.0, 1.0,
    1.0, 0.0, 1.0, 1.0,
    1.0, 0.0, 1.0, 1.0,
    1.0, 0.0, 1.0, 1.0


    # ... (define colors for the other vertices)
])
