"""
Author:SuoLin Zhang
Created:2023
About: Colour Functionality
"""

from MayaBase.modules import six

import maya.cmds as cmds

from MayaBase.modules.utils.common_names import COLOURS_DICT


def getColourFromInteger(colour):
    """ Takes an integer of a colour and returns the string name for the colour

    Args:
        colour(int): The integer of colour string to get

    Returns:
        str: The colour index name if found

    Example:
        getColourFromInteger(3)
        # Output: "light grey"
    """
    return [i for i in COLOURS_DICT if COLOURS_DICT[i] == colour][0]


def getColourFromString(colour):
    """ Takes a string of a colour and returns maya's index for the overrideColor attribute.

        Args:
            colour (str):  The curve colour to get

        Returns:
            int: The colour index if found.

        Example:
            getColourFromString("Blue")
            # Output: 6
    """
    if colour.lower() in COLOURS_DICT:
        return COLOURS_DICT[colour.lower().replace("_", " ")]

    raise ValueError("Sorry but the name you entered was not found for a colour")


def getColour(item):
    """ Gets the color of the object shape item passed.

            Args:
                item (str):  The object to get the colour from

            Returns:
                int: The colour index name if found.

            Example:
                getColour("hand_CTRL")
                # Output: 26
    """
    # Extend objects with its shapes and filter the selection by Types
    objectRelatives = cmds.listRelatives(item, shapes=True, noIntermediate=True, fullPath=True) or []
    objectRelatives.append(item)

    allObjects = cmds.ls(objectRelatives, type=['nurbsCurve', 'joint', 'locator'])

    for obj in allObjects:
        if cmds.getAttr("{}.overrideEnabled".format(obj)):
            return cmds.getAttr("{}.overrideColor".format(obj))


def setColour(objects, colour):
    """ Takes a list of objects and sets their colours.

            Args:
                objects (list):  The controllers to change the color of
                colour (int/str):  The controllers colour to set

            Example:
                setColour(24)
                # Output: Item colour changed.
        """
    if not colour:
        raise ValueError("Please pass either the colour number or name: '{}' not understood".format(colour))

    if isinstance(colour, six.string_types):
        colour = getColourFromString(colour)

    elif type(colour) != int:
        raise TypeError("Format not understood: Please pass either the colour number or name.")

    # Force objects to be a list

    objectsList = objects if type(objects) == list else [objects]

    # Extend objects with its shapes and filter the selection by Types

    extendedSelection = []
    shapes = cmds.listRelatives(objectsList, s=True, ni=True, f=True) or []
    extendedSelection.extend(cmds.ls(objectsList, l=True))
    extendedSelection.extend(shapes)

    allObjects = cmds.ls(extendedSelection, type=['joint', 'nurbsCurve', 'locator'])

    for obj in allObjects:
        if cmds.objExists(obj + ".overrideEnabled") and cmds.objExists(obj + ".overrideColor"):
            cmds.setAttr("{0}.overrideEnabled".format(obj), 1)
            cmds.setAttr("{0}.overrideColor".format(obj), colour)
