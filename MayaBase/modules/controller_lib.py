"""
Author:SuoLin Zhang
Created:2023
About: Our Controller library to store all controller shapes
"""
import MayaBase.modules.utils.controllers as ctrl
import maya.cmds as cmds
from MayaBase.modules.utils import path


class Controller(object):
    def __init__(self, prefix, ctrlShape="ctrlCircle", size=1.0, **kwargs):
        """
        Create specified control shape by assigning specific value to arguments node, ctrlType, size.
        Args:
            prefix(str): prefix of controller name
            ctrlShape(str): name to create specified control type("ctrlCircle",
                                                                "io",
                                                                "spike",
                                                                "pyramid",
                                                                "pyramidUp"
                                                                "twoArrows",
                                                                "normalArrow",
                                                                "fatArrow",
                                                                "crossCircle",
                                                                "disc",
                                                                "waveCircle",
                                                                "rightEye",
                                                                "leftEye",
                                                                "rightFoot",
                                                                "leftFoot",
                                                                "sun",
                                                                "create")
            size(float): size of the control to create, basic shape of the control is less than 0.5 maya unit.
        """
        self.node = prefix + '_ctrl'
        self.size = size

        if not cmds.objExists(self.node):
            self.create(ctrlShape, **kwargs)
        else:
            raise RuntimeError(">>> Object already exists")

    def __repr__(self):
        return path.generateReprString(
            self.__class__.__name__,
            self.node
        )

    def ctrlCircle(self, **kwargs):
        return ctrl.ctrl_circle(name=self.node, curveScale=self.size, **kwargs)

    def io(self):
        return ctrl.ctrl_io(name=self.node, curveScale=self.size)

    def spike(self):
        return ctrl.ctrl_spike(name=self.node, curveScale=self.size)

    def pyramid(self, **kwargs):
        return ctrl.ctrl_pyramid(name=self.node, curveScale=self.size, **kwargs)

    def pyramidUp(self, **kwargs):
        return ctrl.ctrl_pyramidUp(name=self.node, curveScale=self.size, **kwargs)

    def twoArrows(self):
        return ctrl.ctrl_twoArrows(name=self.node, curveScale=self.size)

    def normalArrow(self):
        return ctrl.ctrl_normalArrow(name=self.node, curveScale=self.size)

    def fatArrow(self):
        return ctrl.ctrl_fatArrow(name=self.node, curveScale=self.size)

    def crossCircle(self):
        return ctrl.ctrl_crossCircle(name=self.node, curveScale=self.size)

    def disc(self):
        return ctrl.ctrl_disc(name=self.node, curveScale=self.size)

    def waveCircle(self):
        return ctrl.ctrl_waveCircle(name=self.node, curveScale=self.size)

    def rightEye(self):
        return ctrl.ctrl_rightEye(name=self.node, curveScale=self.size)

    def leftEye(self):
        return ctrl.ctrl_leftEye(name=self.node, curveScale=self.size)

    def rightFoot(self):
        return ctrl.ctrl_rightFoot(name=self.node, curveScale=self.size)

    def leftFoot(self):
        return ctrl.ctrl_leftFoot(name=self.node, curveScale=self.size)

    def sun(self):
        return ctrl.ctrl_sun(name=self.node, curveScale=self.size)

    def create(self, ctrlType, **kwargs):

        if cmds.objExists(self.node):
            print(">>> {} already exists, SHAPES MAY CRASH"
                  ">>> {} already exists, SHAPES MAY CRASH"
                  ">>> {} already exists, SHAPES MAY CRASH"
                  ">>> {} already exists, SHAPES MAY CRASH"
                  ">>> {} already exists, SHAPES MAY CRASH"
                  ">>> {} already exists, SHAPES MAY CRASH"
                  ">>> {} already exists, SHAPES MAY CRASH"
                  .format(self.node, self.node, self.node,
                          self.node, self.node, self.node, self.node))

        if ctrlType == "ctrlCircle":
            self.ctrlCircle(**kwargs)

        elif ctrlType == "io":
            return self.io()

        elif ctrlType == "spike":
            return self.spike()

        elif ctrlType == "pyramid":
            return self.pyramid(**kwargs)

        elif ctrlType == "pyramidUp":
            return self.pyramidUp(**kwargs)

        elif ctrlType == "twoArrows":
            return self.twoArrows()

        elif ctrlType == "normalArrow":
            return self.normalArrow()

        elif ctrlType == "fatArrow":
            return self.fatArrow()

        elif ctrlType == "crossCircle":
            return self.crossCircle()

        elif ctrlType == "disc":
            return self.disc()

        elif ctrlType == "waveCircle":
            return self.waveCircle()

        elif ctrlType == "rightEye":
            return self.rightEye()

        elif ctrlType == "leftEye":
            return self.leftEye()

        elif ctrlType == "rightFoot":
            return self.rightFoot()

        elif ctrlType == "leftFoot":
            return self.leftFoot()

        elif ctrlType == "sun":
            return self.sun()
        else:
            txt2 = ">>> INVALID TYPE"
            raise ValueError(txt2)
