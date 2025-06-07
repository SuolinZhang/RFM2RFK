"""
Author:SuoLin Zhang
Created:2023
About: Our Dag Node functionality to deal with
        our Maya attributes in a Pythonic way.
"""

import maya.cmds as cmds

from MayaBase.modules.utils import path

import string

from MayaBase.modules import six




class Attributes(object):
    def __init__(self, node):
        self.node = node

        if not node.exists():
            raise ValueError("Node does not exist:{}".format(node.name))

    def __repr__(self):
        return path.generateReprString(
            self.__class__.__name__,
            self.node.fullPath
        )

    def __getitem__(self, attr):
        """ Getting the attribute with a string input

            Example:
                print(cube.a["rotateX"])
                Output: "|cube_GEO.rotateX"
        """
        if attr in self.__dict__.keys():
            return self.__dict__[attr]

        return Attribute(self.node, attr)

    def __getattr__(self, attr):
        """ Getting the attribute with a string input

                   Example:
                       print(cube.a.rotateX)
                       Output: "|cube_GEO.rotateX"
        """
        if attr in self.__dict__.keys():
            return self.__dict__[attr]

        return Attribute(self.node, attr)

    # -------------------------------------------------------------------------------------------------
    def list(self, **kwargs):
        """ Using maya.cmds functionality to list all attributes.

            Example:
                print(cube.a.list())
                Output: list
        """
        return [Attribute(self.node, a) for a in cmds.listAttr(self.node, **kwargs)]

    def add(self, **kwargs):
        """ Using functionality from maya.cmds addAttr to add
                    an attribute to the current node.

                    Arg:
                        longName (str): Fixed code name
                        nn (str): Human readable name
                        attributeType (str): Type, Long, float, enum
                        en (str): "__________:__________"
                        dv (int/float):  Default Value to set
                        min (int/float): Min value to go to
                        max (int/float): Max value to go to
                        k (bool): Keyable
                        h (bool): Hidden

                    Example:
                        cube.a.add(ln="new_attr", nn="New Attr", at="float", k=1, dv=0)
                """
        cmds.addAttr(self.node, **kwargs)

    def zeroAttributes(self, **kwargs):
        """ Zeros out the transform attributes on the node.

            Example:
                print(cube.a.zeroAttributes())

        """
        cmds.makeIdentity(self.node.fullPath, **kwargs)


class Attribute(object):

    def __init__(self, node, attr):
        self.node = node
        self._attribute = attr

    def __str__(self):
        fullPath = self.fullPath
        if not fullPath:
            return ">>> INVALID OBJECT"

        return fullPath

    def __repr__(self):
        return path.generateReprString(
            self.__class__.__name__,
            self.fullPath
        )

    # -------------------------------------------------------------------------------------------------

    def __lshift__(self, attr):
        """ Connecting from the last item to the first.

            Example:
                node2.a.sx << node1.a.sy
        """
        attr.connect(self)

    def __rshift__(self, attr):
        """ Connecting from the first item to the last.

            Example:
                node1.a.sx >> node2.a.sy
        """
        self.connect(attr)

    # -------------------------------------------------------------------------------------------------
    def _conditionNodeName(self, value):
        return value.node.name if isinstance(value, type(self)) else self.node.name + "_" + str(value)

    def __eq__(self, value):
        """ Making a condition node and setting the first &
            second terms and the operation.

            Example 1:
                node1.a.sx == node2.a.sx
            Example 2:
                (node1.a.sx == node2.a.sx).setCondition( ifTrue=node1.a.sx, ifFalse=node2.a.sx ) >> node1.a.sz
            Example 3:
                calc = node1.a.sx == node2.a.sx
                calc.setCondition(ifTrue=node1.a.sx, ifFalse=node2.a.sx)
        """

        from MayaBase.modules.nodel.base.attribute_condition import Condition

        name = self._conditionNodeName(value)
        nodeName = "{0}_{1}_eq_CD".format(name, self.attr)

        return Condition(nodeName, self, value, 0).a.outColorR

    def __ne__(self, value):
        from MayaBase.modules.nodel.base.attribute_condition import Condition

        name = self._conditionNodeName(value)
        nodeName = "{0}_{1}_eq_CD".format(name, self.attr)

        return Condition(nodeName, self, value, 1).a.outColorR

    def __gt__(self, value):
        from MayaBase.modules.nodel.base.attribute_condition import Condition

        name = self._conditionNodeName(value)
        nodeName = "{0}_{1}_eq_CD".format(name, self.attr)

        return Condition(nodeName, self, value, 2).a.outColorR

    def __ge__(self, value):
        from MayaBase.modules.nodel.base.attribute_condition import Condition

        name = self._conditionNodeName(value)
        nodeName = "{0}_{1}_eq_CD".format(name, self.attr)

        return Condition(nodeName, self, value, 3).a.outColorR

    def __lt__(self, value):
        from MayaBase.modules.nodel.base.attribute_condition import Condition

        name = self._conditionNodeName(value)
        nodeName = "{0}_{1}_eq_CD".format(name, self.attr)

        return Condition(nodeName, self, value, 4).a.outColorR

    def __le__(self, value):
        from MayaBase.modules.nodel.base.attribute_condition import Condition

        name = self._conditionNodeName(value)
        nodeName = "{0}_{1}_eq_CD".format(name, self.attr)

        return Condition(nodeName, self, value, 5).a.outColorR

    def setCondition(self, **kwargs):
        from MayaBase.modules.nodel.base.attribute_condition import Condition

        return Condition(self.node).setCondition(**kwargs)

    # -------------------------------------------------------------------------------------------------
    def __add__(self, value):
        """ Using the plusMinus node for the connections.

            Example:
                calc = (node.a.sx + node.a.sy)
        """
        return self.plusMinusAverageNode(value)

    def __sub__(self, value):
        """ Subtracting the value passed or attribute

            Example:
                subNode = node.a.sx - node.a.sy
        """
        return self.plusMinusAverageNode(value, operationType=2)

    def __mul__(self, value):
        """ Multiplying the value passed or attribute.

            Example:
                mulNode = node.a.sx * node.a.sy
        """
        return self.multiplyDivideNode(value, operationType=1)

    def __div__(self, value):
        """ Dividing the value passed or attribute.

            Example:
                calc = node.a.sx / node.a.sy
        """
        return self.multiplyDivideNode(value, operationType=2)

    def __truediv__(self, value):
        """ Dividing the value passed or attribute.

            Example:
                calc = node.a.sx / node.a.sy
        """
        return self.multiplyDivideNode(value, operationType=2)

    def __pow__(self, value):
        """ Power the value passed or attribute.

            Example:
                calc = node.a.sx ** node.a.sy
        """
        return self.multiplyDivideNode(value, operationType=3)

    def plusMinusAverageNode(self, value, operationType=1):
        """ Adding or Subtracting the value passed or attribute.

                    Args
                        value (int/float/str/attributeObject): The value to use.
                        operationType (int): The operation to use.
                            operationType = 1 (sum)
                            operationType = 2 (subtract)
                            operationType = 3 (average)
                    Returns:
                        object: self

                    Example 1:
                        addNode = node.a.sx + node.a.sy
                    Example 2:
                        calc = ((node.a.sx + node.a.sy) + node.a.sz) + 10
                        calc.a.output >> node.a.sx
                """
        nodeType = "plusMinusAverage"
        nodeName = self.createNodeName(value, nodeType)

        # Check whether the connections are both parent plugs or children
        attribute = "input3D" if self.checkConnectionAttribute(value) else "input1D"

        # This makes the addition to a current plusMinus node if is self
        if cmds.objectType(self.node) == nodeType and cmds.getAttr(self.node.a.operation) == operationType:
            self.addToPlusMinusAverage(attribute, value)

        else:
            return self.createPlusMinusAverage(nodeName, nodeType, operationType, attribute, value)

        return self

    def createNodeName(self, value, suffix):
        """Create a new node name. """
        suffixCut = (suffix[0] + "".join([i for i in suffix if i.isupper()])).upper()
        nodesAttached = "{0}_{1}_{2}_{3}".format(self.node.name, self.attr, value, suffixCut)
        nodeName = "".join(["_" if i in string.punctuation else i for i in nodesAttached])
        return nodeName

    def checkConnectionAttribute(self, inputValue):
        """Check whether the connections are both parent or child plugs. """
        inputIsParent = True if isinstance(inputValue, Attribute) and inputValue.isParent else False
        return True if self.isParent and inputIsParent else False

    def addToPlusMinusAverage(self, attribute, value):
        """ Find the end attribute to add to.

                    Args:
                        attribute (int/float/str/attributeObject): The maya node.
                        value (int/float/str/attributeObject): The maya node.
                """
        connectionIndex = cmds.getAttr(self.node.a[attribute], size=1)
        if isinstance(value, (float, int)):
            self.node.a["%s[%s]" % (attribute, connectionIndex)].set(value)
        else:
            self.node.a["%s" % (attribute)] << value

    def createPlusMinusAverage(self,
                               nodeName,
                               nodeType,
                               operationType,
                               attribute,
                               value):
        """ Creating the new plug and make the connections to the node.

                    Args:
                        nodeName (str): The full node name to use.
                        nodeType (str): The type of object to use.
                        operationType (int): The index of the node type to use.
                        attribute (str): The attribute name to use.
                        value (int/float/str/attributeObject):  The value to use.

                    Returns:
                        class: The attribute nodal name and class.
                """
        from MayaBase.modules.nodel import Dep_Node
        plusMinusAverage = Dep_Node(nodeName, nodeType)
        plusMinusAverage.a.operation.set(operationType)

        plusMinusAverage.a[attribute] << self

        if isinstance(value, (float, int)):
            plusMinusAverage.a[attribute].addToPlusMinusAverage(attribute, value)

        elif isinstance(value, six.string_types) or isinstance(value, Attribute):
            plusMinusAverage.a[attribute] << value

        if self.checkConnectionAttribute(value):
            return plusMinusAverage.a.output3D

        return plusMinusAverage.a.output1D

    def multiplyDivideNode(self, value, operationType=1):
        nodeType = "multiplyDivide"
        nodeName = self.createNodeName(value, nodeType)
        # multi
        if operationType == 1:
            # if parent
            if self.checkConnectionAttribute(value):
                return self.createMultiDivide(nodeName, nodeType, operationType, value)

            # if child
            else:
                return self.createMultDoubleLinear(nodeName, value)
        # div/pow
        else:

            # If parent
            if self.checkConnectionAttribute(value):
                return self.createDivideParent(nodeName, nodeType, operationType, value)

            # If child
            else:
                return self.createDivideChildren(nodeName, nodeType, operationType, value)

    def createMultiDivide(self, nodeName, nodeType, operationType, value):
        """ Create the multi divide node that we need to work with.

            Args:
                nodeName (str): The full node name to use.
                nodeType (str): The naming of type to use.
                operationType (int): The index of the node type to use.
                value (int/float/str/attributeObject):  The value to use.

            Returns
                class: The attribute nodal class.
        """
        from MayaBase.modules.nodel import Dep_Node
        md = Dep_Node(nodeName, nodeType)
        md.a.operation = operationType

        md.a.input1 << self
        md.a.input2 << value

        return md.a.output

    def createMultDoubleLinear(self, nodeName, value):
        """ Make a multi double linear node to work with.

            Args:
                nodeName (str): The full node name to use.
                value (int/float/str/attributeObject): The value to use.

            Returns
                str/class: The attribute nodal name and class.
        """
        from MayaBase.modules.nodel import Dep_Node
        mdl = Dep_Node(nodeName[:-2] + "MDL", "multDoubleLinear")
        mdl.a.input1 << self

        if isinstance(value, (float, int)):
            mdl.a.input2.set(value)
        else:
            mdl.a.input2 << value

        return mdl.a.output

    def createDivideChildren(self, nodeName, nodeType, operationType, value):
        """ Create the multi divide node to work with parent attributes

                   Args:
                       nodeName (str): The full node name to use.
                       nodeType (str): The node to use.
                       operationType (int): The index of the node type to use.
                       value (int/float/str/attributeObject): The value to use.
                   Returns:
                        class: The attribute object output.
               """
        from MayaBase.modules.nodel import Dep_Node
        divide = Dep_Node(nodeName, nodeType)
        divide.a.operation.set(operationType)

        divide.a.input1X << self

        if isinstance(value, (float, int)):
            divide.a.input2X.set(value)
        else:
            divide.a.input2X << value

        return divide.a.outputX

    def createDivideParent(self, nodeName, nodeType, operationType, value):
        """ Create the multi divide node to work with parent attributes

                   Args:
                       nodeName (str): The full node name to use.
                       nodeType (str): The node to use.
                       operationType (int): The index of the node type to use.
                       value (int/float/str/attributeObject): The value to use.
                   Returns:
                        class: The attribute object output.
               """
        from MayaBase.modules.nodel import Dep_Node
        divide = Dep_Node(nodeName, nodeType)
        divide.a.operation.set(operationType)

        divide.a.input1 << self

        if isinstance(value, (float, int)):
            divide.a.input2.set(value)
        else:
            divide.a.input2 << value

        return divide.a.output

    # -------------------------------------------------------------------------------------------------
    @property
    def attr(self):
        """ Object attribute string.

            Example:
                print(sohere.a.rotateX.attr)
                Output: "RotateX"
        """
        return self._attribute

    @property
    def attribute(self):
        """Object attribute string

            Example:
                print(sphere.a.rotateX.attribute)
                Output:"RotateX"
        """
        return self._attribute

    @property
    def path(self):
        """ Object attribute string path with node name and attr.

            Example:
                print(sphere.a.rotateX.path)
                Output:"sphere_Geo.rotateX"
        """
        nodePath = "{}.{}".format(self.node.path, self.attribute)
        if self.node.path and cmds.objExists(nodePath):
            return nodePath

    @property
    def fullPath(self):
        """ Object attribute string full path with node full path, name and attr.

            Example:
                print(sphere.a.rotateX.path)
                Output:"|BASE_GRP|SUB_GRP|sphere_Geo.rotateX"
        """
        nodePath = "{}.{}".format(self.node.fullPath, self.attribute)
        if self.node.fullPath and cmds.objExists(nodePath):
            return nodePath

    def exists(self):
        """ Checks whether our attribute exists

            Example:
                print(sphere.a.rx.exists())
                Output:True
        """
        if self.fullPath:
            return True
        return False

    # -------------------------------------------------------------------------------------------------

    def set(self, *args, **kwargs):
        """ Sets our attribute using functionality from maya.cmds

            Example:
                print(sphere.a.rx.set(1))
        """
        cmds.setAttr(self.fullPath, *args, **kwargs)

    def get(self, **kwargs):
        """ Gets our attribute value using functionality from maya.cmds

            Example:
                print(sphere.a.rx.get())
                Output: 1
        """
        return cmds.getAttr(self.fullPath, **kwargs)

    def query(self, **kwargs):
        """ Query our attribute's value using functionality from maya.cmds

            Example:
                print(sphere.a.rx.query(listParent=True))
                Output: ['rotate']
        """
        return cmds.attributeQuery(self.attribute, node=self.node, **kwargs)

    # -------------------------------------------------------------------------------------------------

    @property
    def isParent(self):
        """ Check whether the connection is a parent."""
        return bool(self.children)

    @property
    def isChild(self):
        """ Check whether the connection is a child."""
        return bool(self.parent)

    # -------------------------------------------------------------------------------------------------
    @property
    def children(self):
        """ Returns a list of the children attributes if there are some.

            Example:
                print(sphere.a.rotate.children)
                Output: [
                            Attribute('sphere_GEO.rotateX'),
                            Attribute('sphere_GEO.rotateY'),
                            Attribute('sphere_GEO.rotateZ')
                        ]
                print(sphere.a.rx.children)
                Output: []
        """
        if self.query(indexMatters=True, multi=True):
            multiIndices = cmds.getAttr(self, multiIndices=True)
            index = len(multiIndices) if multiIndices else 0
            lc = self.query(listChildren=True)

            # If children, return all the multi indices attrs
            if lc:
                return [self.node.a["%s[%s].%s" % (self.attr, index, a)] for a in lc]

            # return the single multi index item
            else:
                return [self.node.a["%s[%s]" % (self.attr, index)]]

        return [self.node.a[attr] for attr in self.query(listChildren=True) or []]  # NoneType is not iterable,
        # iterate [] returns None

    @property
    def parent(self):
        """ Returns a list of the parent attributes if there are some.

            Example:
                print(sphere.a.rotateX.parent)
                Output: [Attribute('sphere_GEO.rotate')]
                print(sphere.a.rotate.parent)
                Output: []
        """
        a = self.query(listParent=True)
        if a:
            return Attribute(self.node, a[0]) or []
        return []

    # -------------------------------------------------------------------------------------------------

    @property
    def connectionInput(self):
        """ Returns the input connection of an attribute.

                      Example:
                          print(sphere.a.rx.connectionInput)
                          Output: Attribute('cube_GEO.rotateX')
        """
        from MayaBase.modules.nodel import Dag_Node
        attrs = cmds.listConnections(self.fullPath, p=1, d=0) or []

        if self.children:
            for child in self.children:
                childAttrs = cmds.listConnections(child.fullPath, plugs=True, destination=False)
                if childAttrs:
                    attrs += childAttrs

        inputs = []

        if attrs:
            for attr in attrs:
                nodeName = Dag_Node(attr.split(".")[0])
                attrName = attr.split(".")[-1]
                inputs.append(Attribute(nodeName, attrName))
            return inputs[0] if len(attrs) == 1 else inputs

        return None

    @property
    def connectionOutputs(self):
        """ Returns all the output connections of an attribute.

                              Example:
                                  print(cube.a.rx.connectionOutputs)
                                  Output: Attribute('cube_GEO.rotateX')
        """
        from MayaBase.modules.nodel import Dag_Node
        attrs = cmds.listConnections(self.fullPath, p=1, s=0) or []

        if self.children:
            for child in self.children:
                childAttrs = cmds.listConnections(child.fullPath, plugs=True)
                if childAttrs:
                    attrs += childAttrs

        if attrs:
            attrNodes = [Attribute(Dag_Node(attr.split(".")[0]), attr.split(".")[-1]) for attr in attrs]
            return attrNodes

        return None

    # -------------------------------------------------------------------------------------------------
    def connect(self, attr):
        """ Connects this attribute to the passed item.

            Example:
                sphere.a.rx.connect(cube.a.rx)
        """
        if not cmds.isConnected(self, attr):

            if (self.query(listChildren=True) != None) and (attr.query(listChildren=True) == None):
                raise ValueError(
                    "The driving of these values might be a parent value such"
                    "as scale and the driven cannot then be a child, this must be handled on the"
                    "input side.")

            try:
                drivingAttrs = self.children or [self] * 3
                drivenAttrs = attr.children or [attr]

                for driver, driven in zip(drivingAttrs, drivenAttrs):
                    cmds.connectAttr(driver, driven, force=True)

            except (RuntimeError, AttributeError):  # if attr is locked or not allowed to force
                cmds.connectAttr(self, attr, force=True)

            return self

    def disconnect(self):
        """ Disconnects this attribute to the passed item.

            Example:
                cube.a.rx.disconnect()
        """
        CHILDREN_ELSE_SELF = self.children if self.children else self

        allAttrs = CHILDREN_ELSE_SELF
        connections = cmds.listConnections(allAttrs, p=True)

        if not connections:
            return None
        
        if self.children:
            for child_attr in self.children:
                conn_attr = cmds.listConnections(child_attr, p=True)
                if not conn_attr:
                    continue

                if cmds.isConnected(conn_attr[0], child_attr):
                    cmds.disconnectAttr(conn_attr[0], child_attr)

        else:
            for attr in connections:
                if cmds.isConnected(attr, self.fullPath):
                    cmds.disconnectAttr(attr, self.fullPath)

    def delete(self):
        """ Removes and deletes the attribute

            Example:
                 cube.a.geo_vis.delete()
        """
        cmds.deleteAttr(self.fullPath)
