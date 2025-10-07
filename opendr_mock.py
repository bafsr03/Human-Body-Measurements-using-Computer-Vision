"""
Mock opendr module to replace the problematic opendr installation.
This provides minimal functionality to allow the code to run without 3D rendering.
"""

import numpy as np

class ProjectPoints:
    def __init__(self, f=None, rt=None, t=None, k=None, c=None):
        self.f = f if f is not None else np.ones(2)
        self.rt = rt if rt is not None else np.zeros(3)
        self.t = t if t is not None else np.zeros(3)
        self.k = k if k is not None else np.zeros(5)
        self.c = c if c is not None else np.zeros(2)

class ColoredRenderer:
    def __init__(self):
        self.camera = None
        self.frustum = {}
        self.v = None
        self.f = None
        self.vc = None
        self.background_image = None
        self.r = None
    
    def set(self, v=None, f=None, vc=None, bgcolor=None):
        self.v = v
        self.f = f
        self.vc = vc
        if bgcolor is not None:
            self.bgcolor = bgcolor

def LambertianPointLight(f=None, v=None, num_verts=None, light_pos=None, vc=None, light_color=None):
    """Mock LambertianPointLight function"""
    if vc is not None:
        return vc
    return np.ones((num_verts, 3)) if num_verts else np.ones((100, 3))

