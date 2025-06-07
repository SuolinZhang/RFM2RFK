"""
Author:SuoLin Zhang
Created:2023
About: A utility function that facilitates the conversion of Maya
        Nodes into various API objects like "MObject", or "MDagPath".
"""

import maya.OpenMaya as om


def toDependencyNode(node):
    """Convert a node into an OpenMaya Dependency Node.
    Args:
        node(str): The maya node.

    Returns:
        object: The OpenMaya Dependency Object.

    Example:
        name = "L_hand_JNT"
        obj = toDependencyNode(name)
        print(obj.typename())
        # Output:joint
    """

    obj = toMObject(node)
    return om.MFnDependencyNode(obj)


def toMObject(node):
    """Convert a node into an OpenMaya Object
    Args:
        node(str): The maya node

    Returns:
        object: The OpenMaya object.

    Example:
        name = "L_hand_JNT"
        obj = toMObject(name)
        print(obj.fullPathName())
        # Output: BASE_GRP|SUB_GRP|L_hand_JNT
    """
    selectionList = om.MSelectionList()
    selectionList.add(node)
    obj = om.MObject()
    selectionList.getDependNode(0, obj)
    return obj


def toMDagPath(node):
    """Convert a node into an OpenMaya Dag object.
    Args:
        node(str): The maya node.

    Returns:
        object: The OpenMaya Object.

    Example:
        name = "L_hand_JNT"
        obj = toMDagPath(name)
        print(obj.partialPathName())
        print(obj.fullPathName())
        # Output:L_hand_JNT
        # Output:BASE_GRP|SUB_GRP|L_hand_JNT
    """

    obj = toMObject(node)
    if obj.hasFn(om.MFn.kDagNode):
        dag = om.MDagPath.getAPathTo(obj)
        return dag
