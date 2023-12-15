
import numpy

def vertShader():
    return """
    #version 330
    uniform float offsetX;
    uniform float offsetY;
    
    layout (location=0) in vec4 position;
    layout (location=1) in vec4 colour;
    smooth out vec4 theColour;
    void main()
    {
        vec4 modifiedPosition = position + vec4(offsetX, offsetY, 0.0, 0.0);
        gl_Position = modifiedPosition;
        theColour = colour;     
    }
    
    """


def fragShader():
    return """
    #version 330
    smooth in vec4 theColour;
    out vec4 outputColour;
    void main()
    {
        outputColour = theColour;
    }
    """


def vertData():
    return numpy.array([
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


def danishLag():
    return numpy.array([
        # Blue background rectangle (2 triangles)
        -0.55, -0.4, 0.0, 1.0,  # Bottom-left corner
        0.55, -0.4, 0.0, 1.0,  # Bottom-right corner
        0.55, 0.4, 0.0, 1.0,  # Top-right corner
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

        # Vertex Colours blue
        #r    g    b
        1.0, 0.0, 0.0, 1.0,
        1.0, 0.0, 0.0, 1.0,
        1.0, 0.0, 0.0, 1.0,
        1.0, 0.0, 0.0, 1.0,
        1.0, 0.0, 0.0, 1.0,
        1.0, 0.0, 0.0, 1.0,

        1.0, 1.0, 1.0, 1.0,
        1.0, 1.0, 1.0, 1.0,
        1.0, 1.0, 1.0, 1.0,
        1.0, 1.0, 1.0, 1.0,
        1.0, 1.0, 1.0, 1.0,
        1.0, 1.0, 1.0, 1.0,

        1.0, 1.0, 1.0, 1.0,
        1.0, 1.0, 1.0, 1.0,
        1.0, 1.0, 1.0, 1.0,
        1.0, 1.0, 1.0, 1.0,
        1.0, 1.0, 1.0, 1.0,
        1.0, 1.0, 1.0, 1.0,

    ])
