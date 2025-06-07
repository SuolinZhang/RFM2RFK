"""
Author:SuoLin Zhang
Created:2023
About: Tests for our Dag_Node Functionality
"""

from MayaBase.modules.nodel import Dag_Node as Dag

import maya.cmds as cmds

import unittest

from MayaBase.modules.nodel.base.attribute_base import Attribute


class Test_Attributes_Base(unittest.TestCase):
    def setUp(self):
        self.attrs = ["tx", "ty", "tz", "rx", "ry", "rz"]

        self.sphereName = "sphere_GEO"
        self.sphere = Dag(cmds.polySphere(n=self.sphereName)[0])
        self.sphere.createOffset()
        [self.sphere.a[i].set(1) for i in self.attrs]

        self.cubeName = "cube_GEO"
        self.cube = Dag(cmds.polyCube(n=self.cubeName)[0])
        self.cube.createOffset()
        [self.cube.a[i].set(2) for i in self.attrs]

        self.planeName = "plane_GEO"
        self.plane = Dag(cmds.polyPlane(n=self.planeName)[0])

    def tearDown(self) -> None:
        self.sphere.offset.delete()
        self.cube.offset.delete()
        self.plane.delete()


class Test_Attributes(Test_Attributes_Base):

    def test_attributes__repr__(self):
        expectedResult = "Attributes('{0}')".format(self.sphereName)
        self.assertEqual(expectedResult, self.sphere.a.__repr__())

    def test_attributes__getitem__(self):
        self.assertTrue(isinstance(self.sphere.a["rx"], Attribute))

    def test_attributes__getattr__(self):
        self.assertTrue(isinstance(self.sphere.a.rx, Attribute))

    def test_attributes_list(self):
        expectedResult = ["message", "caching"]
        expectedResultLength = 200

        self.assertEqual(self.sphere.a.list()[0].attr, expectedResult[0])
        self.assertEqual(self.sphere.a.list()[1].attr, expectedResult[1])
        self.assertGreater(len(self.sphere.a.list()), expectedResultLength)

    def test_attributes_add_exists_delete(self):
        self.assertFalse(self.sphere.a.attr_item_1.exists())

        self.sphere.a.add(ln="attr_item_1", nn="attr item", at="long", min=0, max=12, dv=9, k=1)
        self.assertTrue(self.sphere.a.attr_item_1.exists())

        self.sphere.a.attr_item_1.delete()
        self.assertFalse(self.sphere.a.attr_item_1.exists())

    def test_attributes_zeroAttributes(self):
        self.assertEqual(self.sphere.a.rx.get(), 1)
        self.sphere.a.zeroAttributes()
        self.assertEqual(self.sphere.a.rx.get(), 0)


class Test_Attribute_Base(Test_Attributes_Base):

    def test_attribute__str__(self):
        expectedResult = "|{0}_OFF_GRP|{0}.rx".format(self.sphereName)
        self.assertEqual(str(self.sphere.a["rx"]), expectedResult)

        expectedResult = "|{0}_OFF_GRP|{0}.rotateX".format(self.sphereName)
        self.assertEqual(expectedResult, str(self.sphere.a["rotateX"]))

    def test_attribute__repr__(self):
        expectedResult = "Attribute('{0}.tx')".format(self.sphereName)
        self.assertEqual(expectedResult, self.sphere.a.tx.__repr__())

    def test_attribute__lshift__(self):
        self.plane.a.tx << self.cube.a.tx
        self.assertEqual(self.plane.a.tx.get(), 2)

        self.cube.offset.a.t << self.cube.a.t
        self.assertEqual(self.cube.offset.a.t.get(), [(2, 2, 2)])

    def test_attribute__rshift__(self):
        self.sphere.a.tx >> self.cube.a.tx
        self.assertEqual(self.cube.a.tx.get(), 1)

    # -------------------------------------------------------------------------------------------------

    def test_attribute__eq__child_attributes(self):
        calc = (self.cube.a.scaleX == self.sphere.a.scaleX)

        self.assertEqual(calc.node.name, "{0}_{1}_eq_CD".format(self.sphere.name, self.cube.a.scaleX.attr))
        self.assertEqual(calc.attr, "outColorR")
        self.assertEqual(calc.get(), 0)
        self.assertEqual(calc.node.a.firstTerm.connectionInput.fullPath, self.cube.a.scaleX.fullPath)
        self.assertEqual(calc.node.a.secondTerm.connectionInput.fullPath, self.sphere.a.scaleX.fullPath)

        calc.node.delete()

    def test_attribute__eq__parent_attributes(self):
        calc = (self.cube.a.scale == self.sphere.a.scale)

        expectedResult = calc.node.type
        self.assertEqual("condition", expectedResult)

        self.assertTrue(calc.node.a.operation.get() == 0)
        self.assertTrue(calc.node.a.firstTerm.get() == 3)
        self.assertTrue(calc.node.a.secondTerm.get() == 3)
        calc.node.delete()

    def test_attribute__eq__setCondition(self):
        calc = (self.cube.a.sx == self.sphere.a.sx).setCondition(ifTrue=1, ifFalse=0)

        self.assertEqual(calc.node.a.outColorR.get(), 1)

        self.cube.a.sx.set(0)
        self.assertEqual(calc.node.a.outColorR.get(), 0)

        self.cube.a.sx.set(3)
        self.assertEqual(calc.node.a.outColorR.get(), 0)

        calc.node.delete()

    def test_attribute__ne__(self):
        calc = (self.cube.a.scaleX != self.sphere.a.scaleX)

        self.assertEqual(calc.get(), 1)
        self.assertEqual(calc.node.a.firstTerm.connectionInput.fullPath, self.cube.a.scaleX.fullPath)
        self.assertEqual(calc.node.a.secondTerm.connectionInput.fullPath, self.sphere.a.scaleX.fullPath)

        calc.node.delete()


    def test_attribute__gt__(self):
        calc = (self.cube.a.scaleX > self.sphere.a.scaleX)

        self.assertEqual(calc.get(), 1)
        self.assertEqual(calc.node.a.firstTerm.connectionInput.fullPath, self.cube.a.scaleX.fullPath)
        self.assertEqual(calc.node.a.secondTerm.connectionInput.fullPath, self.sphere.a.scaleX.fullPath)

        calc.node.delete()


    def test_attribute__ge__(self):
        calc = (self.cube.a.scaleX >= self.sphere.a.scaleX)

        self.assertEqual(calc.get(), 0)
        self.assertEqual(calc.node.a.firstTerm.connectionInput.fullPath, self.cube.a.scaleX.fullPath)
        self.assertEqual(calc.node.a.secondTerm.connectionInput.fullPath, self.sphere.a.scaleX.fullPath)

        calc.node.delete()


    def test_attribute__lt__(self):
        calc = (self.cube.a.scaleX < self.sphere.a.scaleX)

        self.assertEqual(calc.get(), 1)
        self.assertEqual(calc.node.a.firstTerm.connectionInput.fullPath, self.cube.a.scaleX.fullPath)
        self.assertEqual(calc.node.a.secondTerm.connectionInput.fullPath, self.sphere.a.scaleX.fullPath)

        calc.node.delete()


    def test_attribute__le__(self):
        calc = (self.cube.a.scaleX <= self.sphere.a.scaleX)

        self.assertEqual(calc.get(), 0)
        self.assertEqual(calc.node.a.firstTerm.connectionInput.fullPath, self.cube.a.scaleX.fullPath)
        self.assertEqual(calc.node.a.secondTerm.connectionInput.fullPath, self.sphere.a.scaleX.fullPath)

        calc.node.delete()


    # -------------------------------------------------------------------------------------------------

    def test_attribute__add__(self):
        calc = (self.sphere.a.tx + self.cube.a.tx)
        calc >> self.plane.a.tx
        self.assertEqual(self.plane.a.tx.get(), 3)

        calc.node.delete()

        calc = self.sphere.a.t + self.cube.a.t
        calc.node.delete()


    def test_attribute__sub__(self):
        calc = self.sphere.a.tx - self.cube.a.tx
        calc >> self.plane.a.tx
        self.assertEqual(self.plane.a.tx.get(), -1)

        calc.node.delete()
    def test_attribute__mul__(self):
        calc = self.sphere.a.tx * self.cube.a.tx
        calc >> self.plane.a.tx
        self.assertEqual(self.plane.a.tx.get(), 2)

        calc.node.delete()
    def test_attribute__div__(self):
        calc = self.sphere.a.tx / self.cube.a.tx
        calc >> self.plane.a.tx
        self.assertEqual(self.plane.a.tx.get(), 0.5)

        calc.node.delete()
    def test_attribute__pow__(self):
        self.sphere.a.tx.set(3)
        calc = self.sphere.a.tx ** self.cube.a.tx
        calc >> self.plane.a.tx
        self.assertEqual(self.plane.a.tx.get(), 9)

        calc.node.delete()
    # -------------------------------------------------------------------------------------------------

    def test_attribute_attr(self):
        self.assertTrue(self.sphere.a.sx.attr == "sx")
        self.assertTrue(self.sphere.a.scaleX.attr == "scaleX")
        self.assertTrue(self.sphere.a.shearXY.attr == "shearXY")

    def test_attribute_attribute(self):
        self.assertTrue(self.sphere.a.sx.attr == "sx")
        self.assertTrue(self.sphere.a.scaleX.attr == "scaleX")
        self.assertTrue(self.sphere.a.shearXY.attr == "shearXY")

    def test_attribute_path(self):
        self.assertEqual(self.sphere.path, "sphere_GEO")
        self.assertEqual(self.sphere.a.rx.path, "sphere_GEO.rx")

    def test_attribute_fullPath(self):
        self.assertEqual(self.sphere.fullPath, "|sphere_GEO_OFF_GRP|sphere_GEO")
        self.assertEqual(self.sphere.a.rx.fullPath, "|sphere_GEO_OFF_GRP|sphere_GEO.rx")

    def test_attribute_set(self):
        self.assertEqual(self.sphere.a.rx.get(), 1)
        self.sphere.a.rx.set(2)
        self.assertEqual(self.sphere.a.rx.get(), 2)


    def test_attribute_get(self):
        self.assertEqual(self.sphere.a.rx.get(), 1)
        self.assertEqual(self.cube.a.ry.get(), 2)

    def test_attribute_set_AttributeError(self):
        with self.assertRaises(AttributeError):
            self.sphere.set(2) # AttributeError: 'Dag_Node' object has no attribute 'set'

    def test_attribute_set_RuntimeError(self):
         with self.assertRaises(RuntimeError):
            self.sphere.a.s.set(2) # RuntimeError: setAttr: Error reading data element number 2

    def test_attribute_set_TypeError(self):
        with self.assertRaises(TypeError):
            self.sphere.a.sx.get(1) # TypeError: get() takes 1 positional argument but 2 were given

    def test_attribute_isParent(self):
        self.assertTrue(self.sphere.a.r.isParent)
        self.assertFalse(self.sphere.a.rx.isParent)

    def test_attribute_isChild(self):
        self.assertTrue(self.sphere.a.rx.isChild)
        self.assertFalse(self.sphere.a.r.isChild)

    def test_attribute_query(self):
        self.assertEqual(self.sphere.a.rx.query(lc=True), None)
        self.assertEqual(self.sphere.a.r.query(lc=True), ['rotateX', 'rotateY', 'rotateZ'])
        self.assertEqual(self.sphere.a.rx.query(nn=True), "Rotate X")

    def test_attribute_children(self):

        self.assertEqual(self.sphere.a.tx.children, [])
        self.assertEqual(str(self.sphere.a.r.children),
                         str([self.sphere.a.rotateX, self.sphere.a.rotateY, self.sphere.a.rotateZ]))

    def test_attribute_parent(self):
        self.assertEqual(self.sphere.a.r.parent, [])
        self.assertEqual(self.sphere.a.rx.parent, self.sphere.a.r)


    def test_attribute_connectionInput(self):
        self.cube.a.t >> self.sphere.a.t
        self.cube.a.t >> self.plane.a.t

        self.assertEqual(self.sphere.a.t.connectionInput,
                         self.cube.a.t.children)

        self.assertEqual(self.plane.a.t.connectionInput,
                         self.cube.a.t.children)

        self.assertEqual(self.sphere.a.t.connectionInput,
                         self.plane.a.t.connectionInput)

    def test_attribute_connectionOutputs(self):
        self.cube.a.t >> self.sphere.a.t
        self.cube.a.t >> self.plane.a.t

        self.assertEqual(self.cube.a.t.connectionOutputs,
                         self.sphere.a.t.children + self.plane.a.t.children)

    def test_attribute_connect(self):
        output = self.sphere.a.rz.connect(self.cube.a.rx)
        self.assertEqual(str(output), str(self.sphere.a.rz))

    def test_attribute_disconnect(self):
        self.cube.a.rx >> self.cube.a.rz
        self.assertEqual(str(self.cube.a.rz.connectionInput), str(self.cube.a.rotateX))

        self.cube.a.rz.disconnect()
        self.assertEqual(self.cube.a.rz.connectionInput, None)

if __name__ == "__main__":
    unittest.main()
