from time import sleep

import moderngl
from pyrr import Matrix44

from base_window import BaseWindowConfig


class PhongWindow(BaseWindowConfig):
    def __init__(self, **kwargs):
        super(PhongWindow, self).__init__(**kwargs)

    def model_load(self):
        """Load an object to see the light on."""
        self.sphere_model = self.load_scene("sphere.obj")
        self.sphere_vao = self.sphere_model.root_nodes[0].mesh.vao.instance(
            self.program
        )

    def init_shaders_variables(self):
        # scene params
        self.var_projection = self.program["projection"]
        self.var_view_position = self.program["view_position"]
        self.var_view = self.program["view"]
        self.var_obj_color = self.program["obj_color"]

        # light
        self.var_light_color = self.program["light_color"]
        self.var_light_position = self.program["light_position"]

        # constants
        self.var_diffuse_param = self.program["diffuse_param"]
        self.var_shininess_param = self.program["shininess_param"]
        self.var_specular_param = self.program["specular_param"]
        self.var_ambient_param = self.program["ambient_param"]

    def render(self, time: float, frame_time: float):
        self.ctx.clear(1.0, 1.0, 1.0, 0.0)
        self.ctx.enable(moderngl.DEPTH_TEST | moderngl.CULL_FACE)

        proj = Matrix44.perspective_projection(
            45.0, self.aspect_ratio, 0.1, 1000.0)
        lookat = Matrix44.look_at(
            (3.0, 1.0, 5.0),
            (0.0, 0.0, 1.0),
            (0.0, 0.0, 1.0),
        )

        self.var_view.write(lookat.astype("f4"))
        self.var_projection.write(proj.astype("f4"))
        self.var_view_position.value = (5.0, 5.0, 0.0)

        self.var_light_color.value = (1, 1, 1)
        self.var_light_position.value = (10.0, 5.0, 15.0)
        self.var_specular_param.value = 0.75
        self.var_ambient_param.value = 0.5
        self.var_diffuse_param.value = 0.1
        self.var_shininess_param.value = 2.0

        self.var_obj_color.value = (0.2, 0.7, 0.5)
        self.sphere_vao.render()

        sleep(frame_time)
