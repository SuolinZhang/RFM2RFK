"""
Author:SuoLin Zhang
Created:2023
About: Our Joint Node functionality to deal with Maya
        node with or without dependency.
"""
from MayaBase.modules.controller_lib import Controller
from MayaBase.modules.nodel import Dag_Node
import maya.cmds as cmds


class Joint(Dag_Node):

    def __init__(self, node):
        Dag_Node.__init__(self, node)
        self.node = node

    @property
    def children(self):
        shapes = self.shapes
        children = []
        for child in cmds.listRelatives(self.fullPath, c=True, f=True, ni=True) or []:
            if child not in shapes:
                children.append(Joint(child))

        return children

    @property
    def allChildren(self):
        allChildren = []
        for child in cmds.listRelatives(self.fullPath, ad=True, f=True, ni=True) or []:
            allChildren.append(Joint(child))
        return allChildren

    @property
    def parent(self):
        parent = cmds.listRelatives(self.fullPath, p=True, f=True)
        if parent:
            if cmds.objectType(parent[0]) == 'joint':
                return Joint(parent[0])
            return Dag_Node(parent[0])

    @property
    def allParents(self):
        parents = []
        parent = self.parent
        while parent:
            parents.append(parent)
            parent = parent.parent

        return parents

    def createControl(self, prefix, typ="ctrlCircle", size=1.0, matchMove=False, **kwargs):
        """
                Args:
                    typ(str):controller type("ctrlCircle",
                                            "io",
                                            "pyramid",
                                            "pyramidUp",
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
                    size(float): size of controller
                    matchOS(bool): match offset group to joint
                Returns:
                    {
                    'c': globalCtrl,
                    'off': globalCtrlOffset
            }
                """
        from MayaBase.modules.nodel import Curve
        ctrlParent = self.parent
        ctrl = Curve(Controller(prefix, ctrlShape=typ, size=size, **kwargs).node)
        ctrl_offset = ctrl.createOffset()

        if matchMove:
            ctrl_offset.moveTo(self.fullPath)
        if ctrlParent:
            ctrl_offset.parentTo(ctrlParent)

        return {"c": ctrl,
                "off": ctrl_offset
                }

