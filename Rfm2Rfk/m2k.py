"""
Author:SuoLin Zhang
Created:2025

Copy maya Material Network to Katana
"""

import maya.cmds as cmds

from PySide2.QtGui import QGuiApplication

CLIPBOARD = QGuiApplication.clipboard()

from pathlib import Path

from MayaBase.modules.nodel import Dag_Node as Dag

from Rfm2Rfk.utils import checkOrphaned
from . import ET

from Rfm2Rfk import utils

_XML_CACHE = {}
_TEMPLATE_DIR = Path(__file__).parent/"renderer"/"Prman"/"node"

def loadALLTEMPLATES():
    """
    Pre-load all katana nodes templates to cache

    """
    for file in _TEMPLATE_DIR.glob("*.xml"):
        node_type = file.stem
        _XML_CACHE[node_type] = ET.parse(file)

loadALLTEMPLATES()

KATANA_NODE_WIDTH = 200
KATANA_SPACE_WIDTH = 60
KATANA_ROW_HEIGHT = 100



def getAllNodes(nodes):
    """
    Get selected nodes and all nodes upstream

    Args:
        nodes (list)
    Returns:
        list : contains all needed node fullpath
    """

    result_nodes = []
    processed = set()
    while nodes:
        current = nodes.pop()
        if current in processed:
            continue
        result_nodes.append(current)
        processed.add(current)

        connections = cmds.listConnections(current, source=True, destination=False) or []
        nodes.extend([n for n in connections if n not in processed])

    return result_nodes


def generateNode(node):
    """
    Generate individual node dict

    Args:
        node (str) : node fullpath
    Returns:
        dict : {
        "name" : node name,
        "type" : node type,
        "attributes" : node attributes (dict {"diffuseColor" : [0, 0, 0], ...}),
        "connections" : node connections (dict {"diffuseColor": "PxrTexture.outColor",...}),
        "fullPath" : node fullPath
    }

    """
    node_attributes = utils.getNodeAttributes(node)
    node_connections = utils.getInputConnctions(node)
    node = Dag(node)
    node_name = node.name
    node_type = node.type
    node_fullPath = node.fullPath

    return {
        "name" : node_name,
        "type" : node_type,
        "attributes" : node_attributes,
        "connections" : node_connections,
        "fullPath" : node_fullPath
    }


def compareParameter(attr_name, node_dict):
    """
    This function retrieves a specified parameter's value from a Maya node and compares it
    against the matching parameter definition in an XML file.

    It supports both single values and array-type parameters (like float3/double3) with tolerance-based comparison for
    floating-point numbers.

    Args:
        attr_name (str): Name of the parameter to compare (e.g., "diffuseColor").
        node_dict (dict): Maya node dictionary

    Returns:
        any: The Maya parameter value if it differs from the XML definition
        None: If the Maya parameter matches the XML value (within tolerance for floats)

    Note:
        - For array parameters (like float3), compares each component with 0.0001 tolerance
        - Non-array parameters return the Maya value directly
    """

    node_type = node_dict["type"]

    template = _XML_CACHE[node_type]

    # deep copy template data to avoid contaminating template in cache
    tree = ET.ElementTree(ET.fromstring(ET.tostring(template.getroot())))
    root = tree.getroot()

    group_params_element = root.find(f".//group_parameter[@name='{node_type}']")
    param_element = group_params_element.find(f".//group_parameter[@name='{attr_name}']")
    param_value = node_dict["attributes"][attr_name]


    # compare value of specific attribute from maya to katana
    # if param type is float3 or double3
    # same return None, otherwise return param value from maya
    # other param type return maya value
    if param_element:
        if isinstance(param_value, list):
            new_values = []
            xml_values = []
            for index, value in enumerate(param_value):
                index = "i" + str(index)
                xml_val = float(param_element.find(f".//number_parameter[@name='{index}']").get("value"))
                xml_values.append(xml_val)
                if abs(value - xml_val) < 0.0001:
                    new_values.append(xml_val)
                    continue
                else:
                    new_values.append(value)

            if xml_values == new_values:
                return None

            else:
                return new_values

        elif isinstance(param_value, (int, float)):
            xml_value = float(param_element.find(".//number_parameter[@name='value']").get("value"))
            if abs(param_value - xml_value) < 0.0001:
                return None
            else:
                return param_value

        elif isinstance(param_value, str):
            print(param_value)
            return param_value

    return None

def iterateMapping(node):
    """
    Maps Maya node parameters to Katana XML parameters using cached templates.

     Args:
        node (dict): Maya node dictionary containing:
            - name (str): Node name
            - type (str): Node type (must match template filename)
            - attributes (dict): Parameter values
            - connections (dict): Input connections
            - fullPath (str): Full node path
            - X (int): pos X value
            - Y (int): pox Y value
    Returns:
        ET.ElementTree: Configured Katana node XML structure

    Raises:
        ValueError: If no matching template found or child attributes are connected
        RuntimeError: If XML processing fails

    """
    node_type=node["type"]

    template = _XML_CACHE[node_type]

    # deep copy template data to avoid contaminating template in cache
    tree = ET.ElementTree(ET.fromstring(ET.tostring(template.getroot())))
    root = tree.getroot()

    node_name = node["name"]

    params_root_element = root.find(f".//group_parameter[@name='{node_type}']")

    if params_root_element is None:
        raise ValueError(f"No matching node type '{node_type}' found in XML template")

    # Convert katana node name to maya node name
    root.set('name', node_name)
    params_root_element.set('name', node_name)
    params_root_element.find("string_parameter[@name='name']").set('value', node_name)

    # Set node position
    root.set('x', str(node["X"]))
    root.set('y', str(node["Y"]))

    # process all parameters(attributes)
    params_element = root.find(".//group_parameter[@name='parameters']")
    for param in params_element.findall("group_parameter"):
        param_name = param.get('name')


        if param_name not in node['attributes']:
            continue

        value = compareParameter(param_name, node)
        if value is None:
            continue
        # print(f"{param_name} : {value}")
        # Handle different parameter types
        enable_param = param.find("*[@name='enable']")
        value_param = param.find("*[@name='value']")
        if value_param is not None:
            # print(f"find param : {param_name}")
            enable_param.set('value', str("1"))
            if isinstance(value, (int, float)):
                value_param.set('value', str(value))

            elif isinstance(value, str):
                value_param.set('value', value)

            elif isinstance(value, list) and int(value_param.get('tupleSize')) == len(value):
                for i in range(len(value)):
                    val = value[i]
                    index = 'i' + str(i)
                    array_element = value_param.find(f"number_parameter[@name='{index}']")
                    array_element.set('value', str(val))

            else:
                continue

    # process connections
    connections = node["connections"]

    for attr, src_connection in connections.items():
        if utils.connectionInputIsChild(node["name"], attr):
            raise ValueError(f"Katana Do Not Support Child Attribute! Error Attribute: {src_connection}\n"
                             f"Please Use A Parent Attribute Connect")

        port_node = root.find(f".//port[@name='{attr}']")
        if port_node is not None:
            port_node.set("source", src_connection)
            utils.log.info("Connected: %s.%s to %s", node_name, attr, src_connection)
    return tree


def insertNode(nodes, node_name, branch, y_coord, level=0):
    """
       Recursively builds a hierarchical tree structure from node connections.

       Args:
           nodes (dict): Dictionary of all node data {node_name: node_dict}
           node_name (str): Current node to process
           branch (dict): Parent branch to attach to
           y_coord (int) : branch's y coordinate
           level (int): Current depth level (used for layout)

       """
    if node_name in nodes:

        current_node = nodes[node_name]

        new_branch = {
            "name" : node_name,
            "type" :current_node["type"],
            "X" : level * (KATANA_NODE_WIDTH + KATANA_SPACE_WIDTH),
            "Y": y_coord,
            "attributes" : current_node["attributes"],
            "connections" : current_node["connections"],
            "children" : []
        }
        print(new_branch)
        branch["children"].append(new_branch)

        # find nodes downstream
        downstream_nodes = [name for name, dict in nodes.items() if any(node_name == conn.split('.')[0] for conn in dict["connections"].values())]
        print(downstream_nodes)

        for down_node in downstream_nodes:
            insertNode(nodes, down_node, new_branch, y_coord, level=level + 1)





def buildTree(nodes):
    """
    Build a material tree from nodes list for generating XML data.

    Args:
        nodes (dict): Dictionary of all nodes data {node_name: node_dict}

    Returns:
        dict: Tree structure containing:
            - name: "root"
            - children: Hierarchical node structure
            - terminal_nodes: List of terminal nodes (e.g. shaders)
            - orphaned_nodes: List of unconnected nodes

    """

    tree = {"name" : "root", "children" : [], "terminal_nodes" : [], "orphaned_nodes" : [], "branch_Y_coords": {}}

    # deal with orphaned nodes
    for orphaned_name in nodes:
        if checkOrphaned(orphaned_name):
            orphaned_node = nodes[orphaned_name]
            orphaned_node.update({
                "X" : 0,
                "Y" : 0
            })
            tree["orphaned_nodes"].append(nodes[orphaned_name])

    # find all terminal nodes(like shader nodes e.g.PxrSurface)
    terminal_nodes = [name for name in nodes if not any(name in n["connections"].values() for n in nodes.values())]
    tree["terminal_nodes"] = terminal_nodes

    # find nodes most upstream(has no input connections)
    started_nodes = [name for name in nodes if not nodes[name].get("connections")]

    # start to build the nodes tree in order
    for branch_index, node_name in enumerate(started_nodes):
        y_coord = branch_index * (KATANA_ROW_HEIGHT + KATANA_SPACE_WIDTH)
        insertNode(nodes, node_name, tree, y_coord)

    return tree


def buildXML(tree):
    """
    Build katana XML

    Args:
        tree (dict): material tree structure
    Returns:
        ET.ElementTree: Complete Katana XML document
    """
    print("Building XML from tree:", tree)  # check input tree

    katana_root = ET.Element("katana")
    xml_exported_nodes = ET.SubElement(katana_root, "node")
    xml_exported_nodes.attrib["name"] = "__SAVE_exportedNodes"
    xml_exported_nodes.attrib["type"] = "Group"

    # Calculate maximum depths for all nodes
    node_depths = {}
    getMaxDepths(tree["children"], node_depths)

    # Get global maximum depth
    max_level = max(node_depths.values()) if node_depths else 0

    # Add orphaned nodes first
    if tree["orphaned_nodes"]:
        for orphaned_node in tree.get("orphaned_nodes", []):
            xml_exported_nodes.append(iterateMapping(orphaned_node).getroot())


    # Recursively build the tree by levels using max depth of each node
    processed_nodes=set()
    for current_level in range(0, max_level+1):
        processTreeLevel(tree["children"], current_level, xml_exported_nodes, node_depths, processed_nodes)


    # xml_str = ET.tostring(katana_root, encoding='unicode')
    # print("Final XML output:", xml_str) # test XML

    return ET.ElementTree(katana_root)

def processTreeLevel(nodes, target_level, parent_xml, depth_dict, processed_nodes):
    """
    Processes nodes at specific target level based on pre-calculated depths.

    Args:
        nodes: List of node dictionaries
        target_level: Current processing level
        parent_xml: Parent XML element
        depth_dict: Node depth mapping {name: max_depth}
        processed_nodes : a set to store processed nodes which have connections
    """
    for node in nodes:
        node_name = node["name"]
        if (depth_dict[node_name] == target_level and node_name not in processed_nodes):
            leaf = iterateMapping(node)
            parent_xml.append(leaf.getroot())
            processed_nodes.add(node_name)

        processTreeLevel(node["children"], target_level, parent_xml, depth_dict, processed_nodes)


def getMaxDepths(nodes, depth_dict, level=0):
    """
       Recursively calculates maximum depth for each node across all branches.

       Args:
           nodes: List of node dictionaries
           depth_dict: Dictionary stores each node's max depth {node_name: max_depth}
           level: Current recursion depth
       """

    for node in nodes:
        node_name = node["name"]
        if node_name not in depth_dict or level > depth_dict[node_name]:
            depth_dict[node_name] = level
        getMaxDepths(node["children"], depth_dict, level+1)


def copy():
    """
    Copy xml data to clipboard

    """
    if not CLIPBOARD:
        utils.log.info("Clipboard not available, sorry")
        return
    selected_nodes = cmds.ls(selection=True)
    all_nodes = getAllNodes(selected_nodes)
    print(f"Collected {len(all_nodes)} nodes: {all_nodes}") # output test

    nodes_dict = {}
    for node_name in all_nodes:
        nodes_dict[node_name] = generateNode(node_name)
    print("Generated nodes dict:", nodes_dict) # output test

    tree = buildTree(nodes_dict)
    xml = buildXML(tree)
    xml_str = ET.tostring(xml.getroot(), encoding='unicode')
    if xml_str:
        CLIPBOARD.setText(xml_str)
        utils.log.info(
            "Successfully copied nodes to clipboard. "
            "You can paste them to Katana now."
        )
    else:
        utils.log.info("Nothing copied")







