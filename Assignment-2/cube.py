import numpy as np


cube_vertices = np.array([
    # Front face (red)
    -1.0, -1.0,  1.0, 1.0,  # Bottom-left
     1.0, -1.0,  1.0, 1.0,  # Bottom-right
     1.0,  1.0,  1.0, 1.0,  # Top-right
    -1.0, -1.0,  1.0, 1.0,  # Bottom-left
     1.0,  1.0,  1.0, 1.0,  # Top-right
    -1.0,  1.0,  1.0, 1.0,  # Top-left
    # Back face (green)
    -1.0, -1.0, -1.0, 1.0,  # Bottom-left
     1.0, -1.0, -1.0, 1.0,  # Bottom-right
     1.0,  1.0, -1.0, 1.0,  # Top-right
    -1.0, -1.0, -1.0, 1.0,  # Bottom-left
     1.0,  1.0, -1.0, 1.0,  # Top-right
    -1.0,  1.0, -1.0, 1.0,  # Top-left

    # Top face (blue)
    -1.0,  1.0, -1.0, 1.0,   # Bottom-left
     1.0,  1.0, -1.0, 1.0,  # Bottom-right
     1.0,  1.0,  1.0, 1.0,  # Top-right
    -1.0,  1.0, -1.0, 1.0,  # Bottom-left
     1.0,  1.0,  1.0, 1.0,  # Top-right
    -1.0,  1.0,  1.0, 1.0,  # Top-left

    # Bottom face (yellow)
    -1.0, -1.0, -1.0, 1.0,  # Bottom-left
     1.0, -1.0, -1.0, 1.0,  # Bottom-right
     1.0, -1.0,  1.0, 1.0,  # Top-right
    -1.0, -1.0, -1.0, 1.0,  # Bottom-left
     1.0, -1.0,  1.0, 1.0,  # Top-right
    -1.0, -1.0,  1.0, 1.0,  # Top-left

    # Left face (magenta)
    -1.0, -1.0, -1.0, 1.0,  # Bottom-left
    -1.0, -1.0,  1.0, 1.0,  # Bottom-right
    -1.0,  1.0,  1.0, 1.0,  # Top-right
    -1.0, -1.0, -1.0, 1.0,  # Bottom-left
    -1.0,  1.0,  1.0, 1.0,  # Top-right
    -1.0,  1.0, -1.0, 1.0,  # Top-left

    # Right face (cyan)
     1.0, -1.0,  1.0, 1.0,  # Bottom-left
     1.0, -1.0, -1.0, 1.0,  # Bottom-right
     1.0,  1.0, -1.0, 1.0,  # Top-right
     1.0, -1.0,  1.0, 1.0,  # Bottom-left
     1.0,  1.0, -1.0, 1.0,  # Top-right
     1.0,  1.0,  1.0, 1.0,

    # color
    1.0, 0.0, 0.0, 1.0,  # Bottom-left
    1.0, 0.0, 0.0, 1.0,  # Bottom-right
    1.0, 0.0, 0.0, 1.0,  # Top-right
    1.0, 0.0, 0.0, 1.0,  # Bottom-left
    1.0, 0.0, 0.0, 1.0,  # Top-right
    1.0, 0.0, 0.0, 1.0,

    0.0, 1.0, 0.0, 1.0,  # Bottom-left
    0.0, 1.0, 0.0, 1.0,  # Bottom-right
    0.0, 1.0, 0.0, 1.0,  # Top-right
    0.0, 1.0, 0.0, 1.0,  # Bottom-left
    0.0, 1.0, 0.0, 1.0,  # Top-right
    0.0, 1.0, 0.0, 1.0,

    # Top face (blue)
    0.0, 0.0, 1.0, 1.0,  # Bottom-left
    0.0, 0.0, 1.0, 1.0,  # Bottom-right
    0.0, 0.0, 1.0, 1.0,  # Top-right
    0.0, 0.0, 1.0, 1.0,  # Bottom-left
    0.0, 0.0, 1.0, 1.0,  # Top-right
    0.0, 0.0, 1.0, 1.0,  # Top-left

# Bottom face (yellow)
    1.0, 1.0, 0.0, 1.0,  # Bottom-left
    1.0, 1.0, 0.0, 1.0,  # Bottom-right
    1.0, 1.0, 0.0, 1.0,  # Top-right
    1.0, 1.0, 0.0, 1.0,  # Bottom-left
    1.0, 1.0, 0.0, 1.0,  # Top-right
    1.0, 1.0, 0.0, 1.0,  # Top-left

    # Left face (magenta)
    1.0, 0.0, 1.0, 1.0,  # Bottom-left
    1.0, 0.0, 1.0, 1.0,  # Bottom-right
    1.0, 0.0, 1.0, 1.0,  # Top-right
    1.0, 0.0, 1.0, 1.0,  # Bottom-left
    1.0, 0.0, 1.0, 1.0,  # Top-right
    1.0, 0.0, 1.0, 1.0,  # Top-left

    # Right face (cyan)
     0.0, 1.0, 1.0, 1.0,  # Bottom-left
     0.0, 1.0, 1.0, 1.0,  # Bottom-right
     0.0, 1.0, 1.0, 1.0,  # Top-right
     0.0, 1.0, 1.0, 1.0,  # Bottom-left
     0.0, 1.0, 1.0, 1.0,  # Top-right
     0.0, 1.0, 1.0, 1.0,
], dtype=np.float32)


def vertData():
    return np.array([
        # Blue background rectangle (2 triangles)
        -0.55, -0.4, 0.0, 1.0,  # Bottom-left corner
        0.55, -0.4, 0.0, 1.0,  # Bottom-right corner
        0.55, 0.4, 0.0, 1.0,
        # Top-right corner
        -0.55, -0.4, 0.0, 1.0,  # Bottom-left corner
        0.55, 0.4, 0.0, 1.0,  # Top-right corner
        -0.55, 0.4, 0.0, 1.0,  # Top-left corner

        # Yellow cross rectangles (4 triangles)
        # Horizontal part of the cross
        -0.55, -0.05, 0.0, 1.0,  # Left bottom corner
        0.55, -0.05, 0.0, 1.0,  # Right bottom corner
        0.55, 0.05, 0.0, 1.0,  # Right top corner

        -0.55, -0.05, 0.0, 1.0,  # Left bottom corner
        0.55, 0.05, 0.0, 1.0,  # Right top corner
        -0.55, 0.05, 0.0, 1.0,  # left top corner

        # Vertical part of the cross
        -0.3, -0.4, 0.0, 1.0,  # Bottom left corner
        -0.2, -0.4, 0.0, 1.0,  # Bottom right corner
        -0.2, 0.4, 0.0, 1.0,  # Top right corner

        -0.3, -0.4, 0.0, 1.0,  # bottom left corner
        -0.2, 0.4, 0.0, 1.0,  # Top right corner
        -0.3, 0.4, 0.0, 1.0,  # Top left corner

        #RGB
        # R   G    B
        0.0, 0.0, 1.0, 1.0,
        0.0, 0.0, 1.0, 1.0,
        0.0, 0.0, 1.0, 1.0,
        0.0, 0.0, 1.0, 1.0,
        0.0, 0.0, 1.0, 1.0,
        0.0, 0.0, 1.0, 1.0,

        # yellow
        1.0, 1.0, 0.0, 1.0,
        1.0, 1.0, 0.0, 1.0,
        1.0, 1.0, 0.0, 1.0,
        1.0, 1.0, 0.0, 1.0,
        1.0, 1.0, 0.0, 1.0,
        1.0, 1.0, 0.0, 1.0,

        1.0, 1.0, 0.0, 1.0,
        1.0, 1.0, 0.0, 1.0,
        1.0, 1.0, 0.0, 1.0,
        1.0, 1.0, 0.0, 1.0,
        1.0, 1.0, 0.0, 1.0,
        1.0, 1.0, 0.0, 1.0,

    ])