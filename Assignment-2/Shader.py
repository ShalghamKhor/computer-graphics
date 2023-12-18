def vertShader():
    return """
    #version 330
    layout (location=0) in vec4 position;
    layout (location=1) in vec4 colour;
    smooth out vec4 theColour;
    uniform mat4 MVP;
    void main()
    {
        gl_Position = MVP * position;
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
