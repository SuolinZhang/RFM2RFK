"""
Author:SuoLin Zhang
Created:2025

Common Utility functions needed for tool
"""

import logging

import maya.cmds as cmds
from MayaBase.modules.nodel import Dag_Node as Dag

log = logging.getLogger("clip")


def getNodeAttributes(node):
    """
    Retrieves all exportable attributes from a Maya node and their values.

    Filters out internal attributes (starting with '__') and child attributes.
    Converts attribute values to appropriate Python types for serialization.

    Args:
        node (str): maya individual node fullpath

    Returns:
        dict: dict contains node's all needed attributes and their values

    Examples:
        >>> dict = getNodeAttribute('PxrSurface1')
        >>> print(dict)
        {
        "diffuseColor" : [0, 0, 0],
        "specularRoughness": 0.3,
        ...
        }
    """

    attributes_list = cmds.listAttr(node, visible=True, settable=True) or []
    exported_node = Dag(node)
    attr_dict = {}
    for attr in attributes_list:
        if attr.startswith('__') or exported_node.a[attr].isChild:
            continue

        type = exported_node.a[attr].get(type=True)

        try:
            if type in ["float", "double", "int"]:
                val = exported_node.a[attr].get()
            elif type == "bool":
                val = int(exported_node.a[attr].get())
            elif type in ["float3", "double3"]:
                val = list(exported_node.a[attr].get()[0])
            elif type == "enum":
                val = int(exported_node.a[attr].get())
            elif type == "string":
                val = exported_node.a[attr].get()
            else:
                continue
            attr_dict[attr] = val

        except RuntimeError:
            continue



    return attr_dict



def getInputConnctions(node):
    """
    Retrieves all input connections for a Maya node.

    Args:
        node (str): Fullpath of the Maya node to inspect

    Returns:
        dict: Dictionary mapping destination attributes to source connections.
              Example:
              {
                  "diffuseColor": "PxrTexture.outColor",
                  ...
              }
    """

    connections = {}

    node_connections = cmds.listConnections(node, source=True, destination=False, connections=True, plugs=True) or []
    if node_connections:
        for i in range(len(node_connections) // 2):
            dest_attr = node_connections[i * 2]
            dest_attr = dest_attr[dest_attr.find(".") + 1 :]
            src_fullPath = node_connections[i * 2 + 1]
            connections[dest_attr] = src_fullPath

    return connections

# def getInputNodes(node_dict):
#     """
#     Gets all upstream nodes connected to the specified node.
#
#     Args:
#         node_dict (dict): Node dictionary containing "fullPath" and "connections"
#
#     Returns:
#         list: Names of all directly connected upstream nodes
#               Example: ["PxrTexture1", "PxrBump1"]
#     """
#
#     node_list = set()
#     current_node = Dag(node_dict["fullPath"])
#     for attribute in node_dict["connections"]:
#         input_node = current_node.a[attribute].connectionInput.node.name
#         node_list.add(input_node)
#
#     return list(node_list)



def connectionInputIsChild(node_path, attribute):
    """
       Checks if a connection's source is a child attribute.

       Args:
           node_path (str): Full path to the Maya node
           attribute (str): Name of the attribute to check

       Returns:
           bool: True if the connection input is a child attribute
    """
    node = Dag(node_path)
    if node.a[attribute].connectionInput.isChild:
        return True

    else:
        return False

def checkIfParent(node_name):
    """
        Determines if a node is a terminal node in the material network.

        A node is considered terminal if its only downstream connection is to a shadingEngine.

        Args:
            node_name (str): Name of the node to check

        Returns:
            bool: True if node is terminal (only connects to shadingEngine)
    """
    down_list = cmds.listConnections(node_name, source=False, destination=True) or []
    print(down_list)
    for node in down_list:
        if Dag(node).type == "shadingEngine":
            return True

    return False

def checkOrphaned(node_name):
    """
    Identifies orphaned nodes that aren't properly connected in the network.

    Args:
        node_name (str): Fullpath of the node to check

    Returns:
        bool: True if node is only connected to default Maya nodes
              None if node has valid connections
    """

    connection = cmds.listConnections(node_name)

    if len(connection) == 1 and 'default' in connection[0]:
        return True

    return None





