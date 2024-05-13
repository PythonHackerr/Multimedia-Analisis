from re import L
import moderngl
import math
from pyrr import Matrix44

from base_window import BaseWindowConfig


class RobotWindow(BaseWindowConfig):

    def __init__(self, **kwargs):
        super(RobotWindow, self).__init__(**kwargs)
        self.model_load()

    def model_load(self):
        self.sphere = self.load_scene('sphere.obj')
        self.cube = self.load_scene('cube.obj')
        self.sphereVAO = self.sphere.root_nodes[0].mesh.vao.instance(self.program)
        self.cubeVAO = self.cube.root_nodes[0].mesh.vao.instance(self.program)

        self.parts = {
            'head': {
                'color': (0.0, 0.0, 1.0),
                'translation': (0.0, 0.0, 5.0),
            },
            'body': {
                'color': (1.0, 0.0, 0.0),
                'translation': (0.0, 0.0, 2.0),
                'scale': (1.0, 1.0, 2.0),
                'rotation': 0,
            },
            'right_arm': {
                'color': (0.5, 0.3, 0.0),
                'translation': (0.0, 3.0, 3.0),
                'scale': (0.5, 0.5, 1.25),
                'rotation': -math.pi/4,
            },
            'left_arm': {
                'color': (0.5, 0.3, 0.0),
                'translation': (0.0, -3.0, 3.0),
                'scale': (0.5, 0.5, 1.25),
                'rotation': math.pi/4,
            },
            'right_leg': {
                'color': (0.1, 0.4, 0.4),
                'translation': (0.0, 2.0, -1.5),
                'scale': (0.5, 0.5, 1.75),
                'rotation': -math.pi/6,
            },
            'left_leg': {
                'color': (0.1, 0.4, 0.4),
                'translation': (0.0, -2.0, -1.5),
                'scale': (0.5, 0.5, 1.75),
                'rotation': math.pi/6,
            }
        }

    def init_shaders_variables(self):
        self.col = self.program['col']
        self.pvm = self.program['pvm']

    def render(self, time: float, frame_time: float):

        self.ctx.clear(0.8, 0.8, 0.8, 0.0)
        self.ctx.enable(moderngl.DEPTH_TEST)

        projection = Matrix44.perspective_projection(45.0, self.aspect_ratio, 0.1, 1000.0)
        lookat = Matrix44.look_at(
            (-15.0, -18.0, 5.0),
            (0.0, 0.0, 1.0),
            (0.0, 0.0, 1.0),
        )
        
        # ----- render evetything -----
        for (part, data) in self.parts.items():
            if data['color'] is not None:
                self.col.value = data['color']
                
            trans = None

            if 'translation' in data:
                trans = Matrix44.from_translation(data['translation'])
            if 'rotation' in data:
                trans *= Matrix44.from_x_rotation(data['rotation'])
            if 'scale' in data:
                trans *= Matrix44.from_scale(data['scale'])

            self.pvm.write((projection*lookat*trans).astype("f4"))

            if part == 'head':
                self.sphereVAO.render()
            else:
                self.cubeVAO.render()
