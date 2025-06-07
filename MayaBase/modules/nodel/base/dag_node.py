"""
Author:SuoLin Zhang
Created:2023
About: Our Dag Node functionality to deal with Maya
        node with or without dependency.
"""

import maya.cmds as cmds
from MayaBase.modules.nodel import Dep_Node
from MayaBase.modules.utils import open_maya_api, colour
from MayaBase.modules.common import matchMove, createOffset


class Dag_Node(Dep_Node):
    """Class based way of calling all the information that we need to
    deal with in the Maya node with dependency in a clean Python way.

        Args:
            node(node/str): Takes either a ready-made base node or the name of one to create
            nodeType(str): Used for creating a specified node type.(optional)

        Example:

            dag = Dap_Node("node_001")
            dag.rename("foobar_001")
            print(dag.fullPath)
    """

    def __init__(self, node, nodeType=None):
        self._dag = None

        Dep_Node.__init__(self, node)

        # Create on initiate if nodeType is passed
        if nodeType:
            self.create(nodeType)

    # -------------------------------------------------------------------------------------------------

    @property
    def node(self):
        return self._node

    @node.setter
    def node(self, node):
        self._dag = node

        if not Dep_Node.node.fset(self, node):
            return False

        self._dag = open_maya_api.toMDagPath(self.node)

    # -------------------------------------------------------------------------------------------------

    @property
    def dag(self):
        return self._dag

    # -------------------------------------------------------------------------------------------------

    @property
    def path(self):
        if self.dag:
            return self.dag.partialPathName()
        return Dep_Node.path.fget(self)

    @property
    def fullPath(self):
        if self.dag:
            return self.dag.fullPathName()
        else:
            return Dep_Node.fullPath.fget(self)

    # -------------------------------------------------------------------------------------------------
    @property
    def shapes(self):
        shapes = []
        for shape in cmds.listRelatives(self.fullPath, s=True, f=True, ni=True) or []:
            shapes.append(Dag_Node(shape))

        return shapes

    @property
    def shape(self):
        shapes = self.shapes
        return shapes[0] if len(shapes) else Dag_Node(None)

    # -------------------------------------------------------------------------------------------------
    @property
    def children(self):
        shapes = self.shapes
        children = []
        for child in cmds.listRelatives(self.fullPath, c=True, f=True, ni=True) or []:
            if child not in shapes:
                children.append(Dag_Node(child))

        return children

    @property
    def allChildren(self):
        allChildren = []
        for child in cmds.listRelatives(self.fullPath, ad=True, f=True, ni=True) or []:
            allChildren.append(Dag_Node(child))
        return allChildren

    @property
    def parent(self):
        parent = cmds.listRelatives(self.fullPath, p=True, f=True)
        if parent:
            return Dag_Node(parent[0])

    @property
    def allParents(self):
        parents = []
        parent = self.parent
        while parent:
            parents.append(parent)
            parent = parent.parent

        return parents

    # -------------------------------------------------------------------------------------------------

    @property
    def order(self):
        return self.parent.children.index(self)

    def reorder(self, index):
        cmds.reorder(self.name, r=index)

    # -------------------------------------------------------------------------------------------------

    def parentTo(self, item, **kwargs):
        cmds.parent(self.fullPath, item, **kwargs)

    def parentToWorld(self, **kwargs):
        cmds.parent(self.fullPath, w=True, **kwargs)

    def moveTo(self, item, **kwargs):
        matchMove([Dag_Node(item).name, self.fullPath], **kwargs)

    def moveHere(self, items, **kwargs):
        matchMove([self.fullPath] + [Dag_Node(i).name for i in items], **kwargs)

    # -------------------------------------------------------------------------------------------------

    @property
    def offset(self):
        return self.parent

    def createOffset(self, count=1, **kwargs):
        if self.exists():
            for i in range(count):
                offsetName = createOffset([self.name], **kwargs)[0]
            return Dag_Node(offsetName)

    # -------------------------------------------------------------------------------------------------
    def _getConstraint(self, constraintType):
        """Gathers the required type of constraint"""
        constraints = cmds.listConnections(self.fullPath, source=True, destination=False, type=constraintType)
        return Dag_Node(constraints[0] if constraints else Dag_Node(None))

    @property
    def getGeometryConstraint(self):
        return self._getConstraint("geometryConstraint")

    @property
    def getAimConstraint(self):
        return self._getConstraint("aimConstraint")

    @property
    def getOrientConstraint(self):
        return self._getConstraint("orientConstraint")

    @property
    def getPointConstraint(self):
        return self._getConstraint("pointConstraint")

    @property
    def getParentConstraint(self):
        return self._getConstraint("parentConstraint")

    @property
    def getScaleConstraint(self):
        return self._getConstraint("scaleConstraint")

    def constraintWeightingAttributes(self, constraintType):
        constraint = self._getConstraint(constraintType)
        return [constraint.fullPath + "." + i for i in cmds.listAttr(constraint, keyable=True, connectable=True) if
                "W" in (i[-2] or i[-3])]

    def geometryConstraint(self, *args, **kwargs):
        return Dag_Node(cmds.geometryConstraint(self.fullPath, *args, **kwargs)[0])

    def aimConstraint(self, *args, **kwargs):
        return Dag_Node(cmds.aimConstraint(self.fullPath, *args, **kwargs)[0])

    def orientConstraint(self, *args, **kwargs):
        return Dag_Node(cmds.orientConstraint(self.fullPath, *args, **kwargs)[0])

    def pointConstraint(self, *args, **kwargs):
        return Dag_Node(cmds.pointConstraint(self.fullPath, *args, **kwargs)[0])

    def parentConstraint(self, *args, **kwargs):
        return Dag_Node(cmds.parentConstraint(self.fullPath, *args, **kwargs)[0])

    def scaleConstraint(self, *args, **kwargs):
        return Dag_Node(cmds.scaleConstraint(self.fullPath, *args, **kwargs)[0])

    def parentScaleConstraint(self, *args, **kwargs):
        cmds.scaleConstraint(self.fullPath, *args, **kwargs)
        return Dag_Node(cmds.parentConstraint(self.fullPath, *args, **kwargs)[0])

    # -------------------------------------------------------------------------------------------------
    @property
    def colour(self):
        return colour.getColour(self.fullPath)

    @property
    def colourAsString(self):
        if self.colour is None:
            return None

        return colour.getColourFromInteger(self.colour)

    def setColour(self, value):
        colour.setColour(self.fullPath, value)
        return self

    # -------------------------------------------------------------------------------------------------

    def setVisibility(self, value):
        if self.exists():
            cmds.setAttr("{item}.v".format(item=self.fullPath), value)

    def show(self):
        self.setVisibility(1)

    def hide(self):
        self.setVisibility(0)

    # -------------------------------------------------------------------------------------------------
    @property
    def history(self):
        if self.exists():
            history = [Dag_Node(i) for i in cmds.listHistory(self.fullPath)]
            return history
        return []

    def deleteHistory(self):
        if self.exists():
            cmds.delete(self.fullPath, constructionHistory=True)

    def duplicate(self, **kwargs):
        if not self.exists():
            raise ValueError(">>> No maya node to duplicate")

        return Dag_Node(cmds.duplicate(self.fullPath, **kwargs)[0])

    def move(self, *args, **kwargs):
        cmds.select(self.fullPath, r=1)
        cmds.move(*args, **kwargs)
