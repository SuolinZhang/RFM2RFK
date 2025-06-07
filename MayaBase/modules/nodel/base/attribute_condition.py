"""
Author:SuoLin Zhang
Created:2023
About: Our Dag Node functionality to deal with Maya
        node with or without dependency.
"""

from MayaBase.modules.nodel import Dep_Node


class Condition(Dep_Node):
    """ The class that will carry our condition node information. """

    def __init__(self, node, firstTerm=None, secondTerm=None, operation=None):
        Dep_Node.__init__(self, node, "condition")

        # Set the attribute that we are working with that will set the condition
        if firstTerm:
            self.setFirstTerm(firstTerm)

        if secondTerm:
            self.setSecondTerm(secondTerm)

        if operation:
            self.a.operation.set(operation)

    def setFirstTerm(self, firstTerm):
        """ Set the first term that we will use to drive the true or false. """
        return self.setConditionTerm(firstTerm, "firstTerm")

    def setSecondTerm(self, secondTerm):
        """ Set the second term that we will use to drive the true or false. """
        return self.setConditionTerm(secondTerm, "secondTerm")

    def setConditionTerm(self, value, term):
        """ Set the terms and the value of the terms that will drive the condition. """
        # Direct input to node of value float or int
        if isinstance(value, (float, int)):
            self.a[term].set(value)

        # Whole parent attr value like translate or rotate ( not rotateX )
        elif (value.__class__.__name__ == "Attribute") and value.children:
            valAttrX, valAttrY, valAttrZ = value.children
            (valAttrX + valAttrY + valAttrZ) >> self.a[term]
            return self.a.outColor

        # Single attr value
        else:
            self.a[term] << value

        return self.a.outColorR

    def setCondition(self, ifTrue=None, ifFalse=None, returnParent=False):
        """ Set the values of the true and the false in the condition node.
            Either use an int, float, list, tuple, or str ("scaleX" or "scale" or "sx").

            Args:
                ifTrue (int/float/list/tuple/str/attributeObject): The value to use.
                ifFalse (int/float/list/tuple/str/attributeObject): The value to use.
                returnParent (bool): Whether we return a parent or child attribute.

            Returns
                class attr: The class parent or child attr to work with.

            Example 1:
                (node1.a.sx <= node2.a.sx).setCondition( ifTrue=node1.a.sx, ifFalse=node2.a.sx)

            Example 2:
                (node1.a.sx <= node2.a.sx).setCondition( ifTrue=1, ifFalse=0 ) >> node1.a.sz

            Example 3:
                calc = node1.a.sx <= node2.a.sx
                calc.setCondition(ifTrue=[1,2,3], ifFalse=[10,3,4]) >> node1.a.sz
        """
        # Connect the value attr into the new node
        for attr, value in zip(["colorIfTrue", "colorIfFalse"], [ifTrue, ifFalse]):

            # Setting an integer/float
            if isinstance(value, (float, int)):
                self.a[attr + "R"].set(value)

            # Setting lists or tuples
            elif isinstance(value, (list, tuple)):
                self.a[attr].set(*value)
                returnParent = True

            else:
                # Setting parent attributes
                if (value.__class__.__name__ == "Attribute") and value.children:
                    self.a[attr] << value
                    returnParent = True

                # Setting a child attribute
                else:
                    self.a[attr + "R"] << value

        return self.a["outColor"] if returnParent else self.a["outColorR"]
