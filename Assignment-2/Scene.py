import glm


class Scene:
    def __init__(self, objects, camera_position, camera_target, camera_up, fov, aspect, near, far):
        self.objects = objects
        self.camera_position = camera_position
        self.camera_target = camera_target
        self.camera_up = camera_up
        self.fov = fov
        self.aspect = aspect
        self.near = near
        self.far = far

    def initialize(self):
        for obj in self.objects:
            obj.initialize()

    def display(self):
        viewMatrix = glm.lookAt(self.camera_position, self.camera_target, self.camera_up)
        projectionMatrix = glm.perspective(glm.radians(self.fov), self.aspect, self.near, self.far)

        for obj in self.objects:
            # Combine model, view, and projection matrices
            MVP = projectionMatrix * viewMatrix * obj.modelMatrix
            obj.transform(MVP)
            obj.display()
