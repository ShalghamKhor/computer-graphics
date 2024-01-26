import numpy as np
import glm

class Scene:
    def __init__(self, objects, camera):
        self.objects = objects
        self.camera = camera


    def display(self):
        view_matrix = self.camera.get_view_matrix()
        projection_matrix = self.camera.projection_matrix

        for obj in self.objects:
            obj.display(view_matrix, projection_matrix)

    def set_camera(self, position, target, up_vector):
        self.camera.set_position(position)
        self.camera.set_target(target)
        self.camera.set_up_vector(up_vector)

    def setup_perspective(self, fov, aspect_ratio, near_plane, far_plane):
        self.camera.set_perspective(fov, aspect_ratio, near_plane, far_plane)

        

class Camera:
    def __init__(self):
        self.position = np.array([0.0, 0.0, 0.0])
        self.target = np.array([0.0, 0.0, -1.0])
        self.up_vector = np.array([0.0, 1.0, 0.0])
        self.projection_matrix = np.identity(4)

    def set_position(self, position):
        self.position = position

    def set_target(self, target):
        self.target = target

    def set_up_vector(self, up_vector):
        self.up_vector = up_vector

    def set_perspective(self, fov, aspect_ratio, near_plane, far_plane):
        self.projection_matrix = glm.perspective(glm.radians(fov), aspect_ratio, near_plane, far_plane)

    def get_view_matrix(self):
        return glm.lookAt(self.position, self.target, self.up_vector)
