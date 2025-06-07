"""
Author:SuoLin Zhang
Created:2023
About: Our objects dimensions functionality
"""

import maya.cmds as cmds

from MayaBase.modules.utils.math import getDistanceBetween


class Object_Dimension(object):

    def __init__(self, node):
        self._node = node

        if not self.worldMatrix:
            raise ValueError(">>> No worldMatrix and therefore no dimension found for this project")

    @property
    def worldMatrix(self):
        return self._node.a.worldMatrix.exists()

    @property
    def xformBoundingBox(self):
        """ Xform Bounding Box

            Return:
                Output: [minTX,minTY,minTZ,maxTX,maxTY,maxTZ]
        """
        return cmds.xform(self._node, q=1, bbi=1)

    @property
    def bb(self):
        return self.xformBoundingBox

    @property
    def width(self):
        return self.bb[3] - self.bb[0]

    @property
    def height(self):
        return self.bb[4] - self.bb[1]

    @property
    def depth(self):
        return self.bb[5] - self.bb[2]

    @property
    def centre(self):
        """ Gathering the centre of the object in world space.

            Returns:
                Output: [x, y, z]
        """
        return [
            (self.bb[3] + self.bb[0]) / 2,
            (self.bb[4] + self.bb[1]) / 2,
            (self.bb[5] + self.bb[2]) / 2,
        ]

    @property
    def center(self):
        return self.centre

    @property
    def position(self):
        """Position will return the world space translate and rotate pivot of the object"""
        from MayaBase.modules.nodel import Dag_Node as Dag
        tempDag = Dag(cmds.group(em=1, w=1))
        tempDag.moveTo(self._node)

        position = [float(format(i, 'f'))
                    for i in cmds.xform(tempDag, ws=1, t=1, q=1) + cmds.xform(tempDag, ws=1, ro=1, q=1)]
        tempDag.delete()

        return position

    @property
    def pivot(self):
        """Returns the translation and object rotate value"""
        return cmds.xform(self._node.fullPath, q=1, piv=1)[:3] + cmds.xform(self._node.fullPath, q=1, ws=1, ro=1)

    # -------------------------------------------------------------------------------------------------
    def copyPivot(self, driverObject, drivenObject):
        """Copy the center pivot coordination of an object in maya from a driver to a driven object"""

        # Get the center pivot position from the source object translation
        source_translate = cmds.xform(driverObject, q=1, ws=1, t=1)

        # Move the pivot of the target object to the source pivot position
        cmds.xform(drivenObject, ws=1, pivots=source_translate)

    def copyPivotFromPivot(self, driverObject):
        """Copy the initial pivot value of an object in maya from a driver to a driven object"""

        # Get the pivot value of the source object
        piv = cmds.xform(driverObject, q=1, piv=1, ws=1)

        # Move the pivot of the target object to the source pivot position
        cmds.xform(self._node, ws=1, pivots=(piv[0], piv[1], piv[2]))

    def copyPivotTo(self, item):
        return self.copyPivot(self._node, item)

    def copyPivotFrom(self, item):
        return self.copyPivot(item, self._node)

    def centrePivot(self):
        cmds.xform(self._node.fullPath, cp=1)

    def centerPivot(self):
        return self.centrePivot()

    # -------------------------------------------------------------------------------------------------

    def distanceTo(self, item):
        """ Gets the distance in world space between two objects

            Returns:
                Output: float

            Example:
                3.434342342
        """
        distance = getDistanceBetween(str(self._node), str(item))
        return distance
