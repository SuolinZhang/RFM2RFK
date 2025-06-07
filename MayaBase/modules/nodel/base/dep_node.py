"""
Author:SuoLin Zhang
Created:2023
About: Our Dep Node functionality to deal with Maya
        base Nodes with no object dependency.
"""

import maya.cmds as cmds

from MayaBase.modules.utils import open_maya_api, path

from MayaBase.modules.nodel.base.attribute_base import Attributes

from MayaBase.modules.nodel.base.dag_dimension import Object_Dimension


class Dep_Node(object):
    """Class based way of calling all the information that we need to
    deal with in the Maya from base nodes with no object dependency.

        Args:
            node(node/str): Takes either a ready-made base node or the name of one to create
            nodetype(str): Used for creating a specified node type.(optional)

        Example:

            dep = Dep_Node("node_001")
            dep.rename("foobar_001")
            dep.delete()
    """

    def __init__(self, node, nodeType=None):
        self._dep = None
        self.node = node

        # Create on initiate if nodeType is passed
        if nodeType and not self.exists():
            self.create(nodeType)

    # -------------------------------------------------------------------------------------------------

    def __str__(self):
        fullPath = self.fullPath
        if not fullPath:
            return "INVALID OBJECT"

        return fullPath

    def __repr__(self):
        return path.generateReprString(
            self.__class__.__name__,
            self.fullPath
        )

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.fullPath == other.fullPath
        elif self.fullPath == other:
            return True
        elif self.path == other:
            return True
        return False

    # -------------------------------------------------------------------------------------------------

    @property
    def node(self):
        return self._node

    @node.setter
    def node(self, node):
        self._dep = None
        self._node = str(node) if node is not None else None

        if not self.node or not cmds.objExists(self.node):
            return False

        self._dep = open_maya_api.toDependencyNode(self.node)
        return True

    # -------------------------------------------------------------------------------------------------

    @property
    def dep(self):
        return self._dep

    # -------------------------------------------------------------------------------------------------

    @property
    def a(self):
        return Attributes(self)

    @property
    def o(self):
        return Object_Dimension(self)
    # -------------------------------------------------------------------------------------------------

    @property
    def path(self):
        if self.dep:
            return self.dep.name()

    @property
    def fullPath(self):
        return self.path

    # -------------------------------------------------------------------------------------------------

    def isReferenced(self):
        return cmds.referenceQuery(
            self.fullPath,
            isNodeReferenced=True
        )

    # -------------------------------------------------------------------------------------------------

    def exists(self):
        if self.fullPath and cmds.objExists(self.fullPath):
            return True
        return False

    # -------------------------------------------------------------------------------------------------

    @property
    def type(self):
        return self.dep.typeName()

    @property
    def typ(self):
        return self.type

    @property
    def name(self):
        return path.baseName(self.fullPath)

    @property
    def namespace(self):
        return path.namespace(self.fullPath)

    # -------------------------------------------------------------------------------------------------

    def rename(self, name):
        cmds.rename(self, name)
        return self

    def lock(self, state=True):
        cmds.lockNode(self.fullPath, lock=state)

    @property
    def isLocked(self):
        return cmds.lockNode(self.fullPath, query=True, lock=True)[0]

    # -------------------------------------------------------------------------------------------------
    def delete(self):
        if self.fullPath and cmds.objExists(self.fullPath):
            cmds.delete(self.fullPath)
        self._dep = None

    def create(self, nodeType):
        if self.fullPath:
            txt = ">>> This node already exists: \n\tName: \"{}\"\n\tType:{}".format(self.node, nodeType)
            raise ValueError(txt)

        self.node = cmds.createNode(nodeType, n=self.node)
        return self


