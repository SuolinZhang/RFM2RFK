"""
Author:SuoLin Zhang
Created:2023
About: Math calculations and functionality.
"""
import maya.cmds as cmds

import math

from MayaBase.modules import six


def getDistanceBetween(obj1, obj2):
    """ Measures the distance between the objects passed.

        A list can be passed if the x,y,z has already be ascertained.

        Args:
            obj1 (str/list): The item to gather the position from or the list of the X,Y,Z.
            obj2 (str/list): The item to gather the position from or the list of the X,Y,Z.

        Returns:
            float: The distance in the scene between the items.
    """

    objectDistance1 = cmds.xform(obj1, ws=1, t=1, q=1) if isinstance(obj1, six.string_types) else obj1
    objectDistance2 = cmds.xform(obj2, ws=1, t=1, q=1) if isinstance(obj2, six.string_types) else obj2

    return getDistanceBetweenCalculation(objectDistance1, objectDistance2)


def getDistanceBetweenCalculation(objectDistance1, objectDistance2):
    """ Return the 2D or 3D distance based on coordinates passed.

        Args:
            objectDistance1 (list): The item to gather the position from or the list of the X,Y,Z.
            objectDistance2 (list): The item to gather the position from or the list of the X,Y,Z.

        Returns:
            float: The distance in the scene between the items.
    """
    xDiff = objectDistance2[0] - objectDistance1[0]
    yDiff = objectDistance2[1] - objectDistance1[1]

    if len(objectDistance1) > 2:
        zDiff = objectDistance2[2] - objectDistance1[2]
        return math.sqrt(xDiff * xDiff + yDiff * yDiff + zDiff * zDiff)

    return math.sqrt(xDiff * xDiff + yDiff * yDiff)
