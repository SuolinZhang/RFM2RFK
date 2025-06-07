# MayaBase
## Description
A utility toolkit for Autodesk Maya that provides an object-oriented abstraction layer over Maya's native commands and API. The library restructures Maya's functionality by introducing custom node classes built upon Dependency Graph (DG) nodes and Directed Acyclic Graph (DAG) nodes as base classes.

I learned how to write the main body of this module from Nick Hughes, you can find his course here: https://www.udemy.com/course/python-for-maya-beginner-to-advanced-rigging-automation
## Classes
### Dep Node
Dep Node is base class for all classes in this module, contains basic functions like retrieve name and type, delete and rename the node.
### Dag Node
A dag node allows user to retrieve the full path of a node, query attributes like shape, parent, and children. It contains methods such as creating constraints, moveto, setting colors, and creating offset groups.
### Attributes & Attribute
The Attribute class, associated with both DepNode and DagNode classes, retrieves the attributes of Maya nodes. In addition to setting and getting attributes, it enables the quick creation of connections, conditional nodes, and arithmetic nodes through Python's dunder methods.
### Dag Dimension
Dag Dimension class mainly involves utilizing the xform command from the Maya cmds module to retrieve node's three-dimensional spatial attributes and functionalities related to pivot transformations.
### Mesh
Mesh class primarily involves functionalities related to weight processing.
### Curve, Joint
Several related properties were added.
## Bugs
When using `>>` or `<<` to connect attributes, some unexpected errors in connection orders may occur when the destination attribute has multi-indices.

LoadSkinWeight method in mesh_node class will lead to mess for skin weights. 

Controller lib is banned for now as it causes a short lag when loading pymel.

## Tests
`from MayaBase.modules.utils import testing` 

`testing.testAllModules()`
