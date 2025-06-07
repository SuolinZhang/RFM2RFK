"""
Author:SuoLin Zhang
Created:2023
About: Tests for our Dag Dimension Functionality
"""

from MayaBase.modules.nodel import Dag_Node as Dag

import maya.cmds as cmds

import unittest


class Test_Object_Dimension(unittest.TestCase):
    def setUp(self):
        self.attrs = ["tx", "ty", "tz", "rx", "ry", "rz"]

        self.sphereName = "sphere_GEO"
        self.sphere = Dag(cmds.polySphere(n=self.sphereName)[0])

        self.cubeName = "cube_GEO"
        self.cube = Dag(cmds.polyCube(n=self.cubeName, w=1, h=2, d=3)[0])

    def tearDown(self) -> None:
        self.sphere.delete()
        self.cube.delete()

    def test_dag_dimension_worldMatrix_pass(self):
        self.assertTrue(self.sphere.o.worldMatrix)

    def test_dag_dimension_worldMatrix_fail(self):
        calc = (self.sphere.a.tx == self.cube.a.tx)

        with self.assertRaises(ValueError):
            self.assertFalse(calc.node.o.worldMatrix)

        calc.node.delete()

    def test_dag_dimension_xformBoundingBox(self):
        expectedResult = [-1.0, -1.0, -1.0, 1.0, 1.0, 1.0]
        self.assertEqual([round(i, 4) for i in self.sphere.o.xformBoundingBox], expectedResult)

    def test_dag_dimension_bb(self):
        expectedResult = lambda x: self.sphere.o.xformBoundingBox
        testResult = lambda x: self.sphere.o.bb
        self.assertEqual(expectedResult.__code__.co_code, testResult.__code__.co_code)

    def test_dag_dimension_width(self):
        self.assertEqual(round(self.sphere.o.width, 2), 2.0)
        self.assertEqual(round(self.cube.o.width, 2), 1.0)

    def test_dag_dimension_height(self):
        self.assertEqual(round(self.sphere.o.height, 2), 2.0)
        self.assertEqual(round(self.cube.o.height, 2), 2.0)

    def test_dag_dimension_depth(self):
        self.assertEqual(round(self.sphere.o.depth, 2), 2.0)
        self.assertEqual(round(self.cube.o.depth, 2), 3.0)

    def test_dag_dimension_centre(self):
        self.assertEqual([round(i, 2) for i in self.sphere.o.centre], [0, 0, 0])
        self.assertEqual([round(i, 2) for i in self.cube.o.centre], [0, 0, 0])

    def test_dag_dimension_center(self):
        expectedResult = lambda x: self.sphere.o.centre
        testResult = lambda x: self.sphere.o.center
        self.assertEqual(expectedResult.__code__.co_code, testResult.__code__.co_code)

    def test_dag_dimension_position(self):
        self.assertEqual(self.sphere.o.position, [0, 0, 0, 0, 0, 0])
        [self.sphere.a[i].set(1) for i in self.attrs]
        self.assertEqual(self.sphere.o.position, [1, 1, 1, 1, 1, 1])

    def test_dag_dimension_copyPivotTo(self):
        tempDag = Dag(cmds.group(em=1, w=1))
        self.sphere.a.tx.set(1)
        self.sphere.a.ty.set(2)
        self.sphere.a.tz.set(3)

        tempDag.moveTo(self.sphere)
        self.assertEqual(tempDag.o.centre, [1, 2, 3])

        self.cube.o.copyPivotTo(self.sphere)
        tempDag.moveTo(self.sphere)
        self.assertEqual(tempDag.o.centre, [0, 0, 0])
        tempDag.delete()

    def test_dag_dimension_copyPivotFrom(self):
        tempDag = Dag(cmds.group(em=1, w=1))
        self.sphere.a.tx.set(1)
        self.sphere.a.ty.set(2)
        self.sphere.a.tz.set(3)

        tempDag.moveTo(self.sphere)
        self.assertEqual(tempDag.o.centre, [1, 2, 3])

        self.sphere.o.copyPivotFrom(self.cube)
        tempDag.moveTo(self.sphere)
        self.assertEqual(tempDag.o.centre, [0, 0, 0])
        tempDag.delete()

    def test_dag_dimension_centrePivot(self):
        tempDag = Dag(cmds.group(em=1, w=1))

        self.sphere.a.tx.set(1)
        self.sphere.a.ty.set(2)
        self.sphere.a.tz.set(3)

        self.assertEqual([round(i, 2) for i in self.sphere.o.pivot], [0, 0, 0, 0, 0, 0])

        self.sphere.o.copyPivotFrom(self.cube)
        self.assertEqual([round(i, 2) for i in self.sphere.o.pivot], [-1, -2, -3, 0, 0, 0])
        tempDag.moveTo(self.sphere)
        self.assertEqual(tempDag.o.centre, [0, 0, 0])

        self.sphere.o.centerPivot()
        self.assertEqual([round(i, 2) for i in self.sphere.o.pivot], [0, 0, 0, 0, 0, 0])
        tempDag.moveTo(self.sphere)
        self.assertEqual([round(i, 4) for i in tempDag.o.centre], [1, 2, 3])

        tempDag.delete()

    def test_dag_dimension_distanceTo(self):
        self.cube.a.t.set(0, 10, 0)
        self.assertEqual(self.sphere.o.distanceTo(self.cube), 10)

        self.cube.a.t.set(150, 0, 0)
        self.assertEqual(self.sphere.o.distanceTo(self.cube), 150)


if __name__ == "__main__":
    unittest.main()
