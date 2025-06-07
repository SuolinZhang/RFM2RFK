"""
Author:SuoLin Zhang
Created:2023
About: All common needed functions.
"""
import maya.cmds as cmds 


def matchMove(selection, point=False, orient=False):
    """Takes a driver location object and a list of driven items to move in that order.
        The default option is to use a parentConstraint to move both translate and rotate
        unless point or orient are set to true.
        Args:
            selection(List): A list of items in the scene
            point(Bool): Toggle the type of constraint to create.
            orient(Bool): Toggle the type of constraint to create.
        Example: matchMove()

    """
    parentObj = selection.pop(0)
    
    for obj in selection:
        try:
            if point or orient:
                if point:
                    constraint = cmds.pointConstraint(parentObj, obj, mo=False)
                if orient:
                    constraint = cmds.orientConstraint(parentObj, obj, mo=False)
            else:
                constraint = cmds.parentConstraint(parentObj, obj, mo=False)

            cmds.delete(constraint)

        except Exception as e:
            print(">>> matchMove Error:{0}:{1}".format(type(e).__name__, e))


def createOffset(selection, grpName="_OFF_GRP"):
    """Takes the selection passed in the scene or the selection passed
        and creates the offset groups in their locations.
        Args:
            selection(list):A list of items in the scene.
            grpName(str):Name of the offset group suffix.

        Returns:
            list: List of the off groups that have been created.

        Example:
              createOffset("sphere_GEO")
              Output: ["sphere_GEO_OFF_GRP"]
    """
    newlyCreatedGroups = []
    offsetGrpNames = [
        grpName, "_PLACER_GRP", "_PLACER_OFF_GRP", "_SUB_GRP", "_SUB_OFF_GRP",
        "_ZERO_GRP", "_ZERO_OFF_GRP", "_BASE_GRP", "_BASE_OFF_GRP",
    ]

    for num, item in enumerate(selection):
        if not cmds.objExists(item):
            print(">>> Could not create Offset group as item does not exist:{}".format(item))
            continue

        offGrpParent = cmds.pickWalk(item, d="up")[0]

        # If the current item ends with the grpName, remove the first name from the
        # offsetGrpNames list, and also remove the grpName from the current item name

        if item.endswith(grpName):
            offsetGrpNames.pop(0)
            newItemName = item.replace(grpName, "")
        else:
            # If item doesn't end up with the grpName, keep the item name as it is
            newItemName = item

        # Creating a new group name by appending the first available name from the names list

        groupName = next((newItemName + suffix for suffix in offsetGrpNames
                          if not cmds.objExists(newItemName + suffix)), None)

        # If a group name was created successfully, create a new group
        if groupName:
            offGrp = cmds.group(em=1, w=1, n=groupName)
            matchMove([item, offGrp])

            cmds.parent(item, offGrp)

            if str(offGrpParent) != str(item):
                cmds.parent(offGrp, offGrpParent)

            newlyCreatedGroups.append(offGrp)

        else:
            print(">>>Could not create offset group for: {0}".format(item))

    return newlyCreatedGroups






















