"""
Author:SuoLin Zhang
Created:2023
About: Our Mesh Node functionality to deal with Maya
        node with or without dependency.
"""

import maya.cmds as cmds
from MayaBase.modules.nodel import Dag_Node


class Curve(Dag_Node):

    def __init__(self, node):
        Dag_Node.__init__(self, node)
        self.node = node

    @property
    def cvs(self):
        return cmds.ls(self.node + ".cv[*]", fl=1)

    @property
    def cvPositions(self):
        positions = [cmds.xform(cv, q=True, t=True, ws=True) for cv in self.cvs]
        pos = [(pos[0], pos[1], pos[2]) for pos in positions]
        return pos

    @property
    def eps(self):
        return cmds.ls(self.node + ".ep[*]", fl=1)

    @property
    def epPosition(self):
        positions = [cmds.xform(ep, q=True, t=True, ws=True) for ep in self.eps]
        pos = [(pos[0], pos[1], pos[2]) for pos in positions]
        return pos

    @property
    def shapes(self):
        shapes = []
        for shape in cmds.listRelatives(self.fullPath, s=True, f=True, ni=True) or []:
            shapes.append(Curve(shape))

        return shapes

    @property
    def shape(self):
        shapes = self.shapes
        return Curve(shapes[0]) if len(shapes) else Dag_Node(None)

    def clsMove(self, *args, **kwargs):
        cls, clsHdl = cmds.cluster(self.fullPath)
        cmds.move(*args, clsHdl, **kwargs)
        self.deleteHistory()

    def clsRotate(self, *args, **kwargs):
        cls, clsHdl = cmds.cluster(self.fullPath)
        cmds.rotate(*args, clsHdl, **kwargs)
        self.deleteHistory()
