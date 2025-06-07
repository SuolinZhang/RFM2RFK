"""
Author:SuoLin Zhang
Created:2023
About: Tests for our Dag_Node Functionality
"""

from MayaBase.modules.nodel import Dag_Node

import maya.cmds as cmds

import unittest


class Test_Dag_Node_Base(unittest.TestCase):
    def setUp(self):
        self.sphereName = "sphere_GEO"
        self.jointName = "joint_j1"

        self.sphere = Dag_Node(cmds.polySphere(n=self.sphereName)[0])
        self.object = Dag_Node(self.sphereName)
        cmds.select(cl=True)

        self.joint = Dag_Node(cmds.joint(n=self.jointName))
        self.md = Dag_Node(cmds.shadingNode('multiplyDivide', asUtility=True, n="test_node"))

    def tearDown(self) -> None:
        if self.sphere.exists():
            self.sphere.delete()

        if self.joint.exists():
            self.joint.delete()

        if self.md.exists():
            self.md.delete()


class Test_Dag_Node(Test_Dag_Node_Base):

    def test_dep_node__str__(self):
        self.assertEqual(str(self.sphere), "|" + self.sphereName)

    def test_dep_node__repr__(self):
        self.assertEqual(
            repr(self.sphere),
            "Dag_Node('sphere_GEO')"
        )

    def test_dep_node__eq__(self):
        self.assertTrue(self.sphere == self.object)
        self.assertTrue(self.sphere.fullPath == "|" + self.sphereName)
        self.assertTrue(self.sphere.path == self.object.path)
        self.assertTrue(self.sphere.fullPath == self.object.fullPath)
        self.assertFalse(self.sphere == self.joint)

    def test_dag_node_getter(self):
        self.assertEqual(self.sphere.node, self.sphereName)
        self.assertEqual(self.object.node, self.sphere.node)
        self.assertNotEqual(self.sphere.node, self.joint.node)

    def test_dag_node_setter(self):
        self.sphere.node = self.jointName
        self.assertEqual(self.sphere.node, self.jointName)
        cmds.delete(self.sphereName)

    def test_dag_node_dag(self):
        grp = cmds.group(self.sphere, n="OFFSET_GRP")
        self.assertEqual(self.sphere.dag.fullPathName(), "|OFFSET_GRP|sphere_GEO")
        cmds.delete(grp)

    def test_dag_node_path(self):
        self.assertEqual(self.sphere.path, self.sphereName)
        self.assertNotEqual(self.sphere.path, "|" + self.sphereName)

    def test_dag_node_fullPath(self):
        grp = cmds.group(self.sphere, n="OFFSET_GRP")
        self.assertEqual(self.sphere.fullPath, "|OFFSET_GRP" + "|" + self.sphereName)
        cmds.delete(grp)

    def test_dag_node_shapes(self):
        self.assertEqual(len(self.sphere.shapes), 1)
        self.assertEqual(self.sphere.shapes[0].name, self.sphereName + "Shape")

    def test_dag_node_shape(self):
        self.assertEqual(self.sphere.shape.name, self.sphereName + "Shape")


class Test_Dag_Node_Hierarchy(Test_Dag_Node_Base):
    def setUp(self) -> None:
        super().setUp()

        self.grp1 = Dag_Node(cmds.group(self.sphere, n="OFFSET_1_GRP"))
        self.grp2 = cmds.group(em=1, n="OFFSET_2_GRP")
        self.grp3 = cmds.group(em=1, n="OFFSET_3_GRP")
        self.grp4 = cmds.group(em=1, n="OFFSET_4_GRP")
        self.grp5 = cmds.group(em=1, n="OFFSET_5_GRP")
        self.grp6 = cmds.group(self.grp5, n="OFFSET_6_GRP")

        cmds.parent(
            self.grp2,
            self.grp3,
            self.grp4,
            self.grp6,
            self.grp1
        )

        cmds.parent(self.grp5, self.grp4)

    def tearDown(self) -> None:
        super().tearDown()
        if self.grp1.exists():
            self.grp1.delete()

    def test_dag_node_children(self):
        self.assertEqual(len(self.grp1.children), 5)
        self.assertEqual(self.grp1.children[0], self.sphere)

    def test_dag_node_allChildren(self):
        self.assertEqual(len(self.grp1.allChildren), 7)

    def test_dag_node_parent(self):
        self.assertEqual(Dag_Node(self.grp5).parent, Dag_Node(self.grp4))

    def test_dag_node_allParents(self):
        self.assertEqual(Dag_Node(self.grp5).allParents, [Dag_Node(self.grp4), Dag_Node(self.grp1)])
        self.assertEqual(len(Dag_Node(self.grp4).allParents), 1)
        self.assertEqual(len(Dag_Node(self.grp5).allParents), 2)

    def test_dag_node_order_and_reorder(self):
        self.assertTrue(self.sphere.order == 0)
        self.sphere.reorder(3)
        self.assertTrue(self.sphere.order == 3)

    def test_dag_node_parentTo(self):
        self.sphere.parentTo(self.joint)
        self.assertEqual(self.sphere.parent, self.joint)

    def test_dag_node_parentToWorld(self):
        self.assertEqual(len(self.sphere.allParents), 1)
        self.sphere.parentToWorld()
        self.assertEqual(len(self.sphere.allParents), 0)

    def test_dag_node_moveTo(self):
        cmds.setAttr(self.sphere.fullPath + ".tz", 100)
        self.assertFalse(cmds.xform(self.sphere, worldSpace=True, translation=True, query=True) ==
                         cmds.xform(self.joint, ws=True, q=True, t=True))

        self.joint.moveTo(self.sphere)
        self.assertTrue(cmds.xform(self.sphere, ws=True, t=True, q=True) ==
                        cmds.xform(self.joint, ws=True, q=True, t=True))

    def test_dag_node_moveHere(self):
        cmds.setAttr(self.sphere.fullPath + ".tz", 100)
        self.assertFalse(cmds.xform(self.sphere, worldSpace=True, translation=True, query=True) ==
                         cmds.xform(self.joint, ws=True, q=True, t=True))
        self.sphere.moveHere([self.joint])
        self.assertTrue(cmds.xform(self.sphere, ws=True, t=True, q=True) ==
                        cmds.xform(self.joint, ws=True, q=True, t=True))

    def test_dag_node_offset(self):
        self.assertEqual(Dag_Node(self.grp5).offset, Dag_Node(self.grp4))

    def test_dag_node_createOffset(self):
        self.assertEqual(len(self.grp1.allParents), 0)
        self.grp1.createOffset()
        self.assertEqual(len(self.grp1.allParents), 1)
        self.grp1.offset.delete()

    def test_dag_node__getConstraint(self):
        expectedResults = cmds.parentConstraint(self.joint, self.sphere, mo=True)[0]
        constraint = self.sphere._getConstraint("parentConstraint")
        self.assertEqual(expectedResults, constraint)

    def test_dag_node_getGeometryConstraint_getter_setter(self):
        expectedResults = self.sphere.geometryConstraint(self.joint)
        constraint = self.joint.getGeometryConstraint
        self.assertEqual(expectedResults, constraint)

    def test_dag_node_getAimConstraint_getter_setter(self):
        expectedResults = self.sphere.aimConstraint(self.joint)
        constraint = self.joint.getAimConstraint
        self.assertEqual(expectedResults, constraint)

    def test_dag_node_getOrientConstraint_getter_setter(self):
        expectedResults = self.sphere.orientConstraint(self.joint)
        constraint = self.joint.getOrientConstraint
        self.assertEqual(expectedResults, constraint)

    def test_dag_node_getPointConstraint_getter_setter(self):
        expectedResults = self.sphere.pointConstraint(self.joint)
        constraint = self.joint.getPointConstraint
        self.assertEqual(expectedResults, constraint)

    def test_dag_node_getParentConstraint_getter_setter(self):
        expectedResults = self.sphere.parentConstraint(self.joint)
        constraint = self.joint.getParentConstraint
        self.assertEqual(expectedResults, constraint)

    def test_dag_node_getScaleConstraint_getter_setter(self):
        expectedResults = self.sphere.scaleConstraint(self.joint)
        constraint = self.joint.getScaleConstraint
        self.assertEqual(expectedResults, constraint)

    def test_dag_node_constraintWeightingAttributes(self):
        self.grp1.parentConstraint(self.grp2, self.grp3, self.grp4, self.grp5)
        constraintAttr = Dag_Node(self.grp5).constraintWeightingAttributes("parentConstraint")
        self.assertEqual(len(constraintAttr), 4)

    def test_dag_node_parentScaleConstraint_getter_setter(self):
        expectedResult = self.sphere.parentScaleConstraint(self.joint)
        constraint = self.joint.getParentConstraint
        self.assertEqual(constraint, expectedResult)
        self.assertEqual(self.joint.getScaleConstraint, "joint_j1_scaleConstraint1")

    def test_dag_node_colour(self):
        self.assertIsNone(self.joint.colour)
        self.joint.setColour("red")
        self.assertEqual(self.joint.colour, 13)

    def test_dag_node_colourAsString(self):
        self.joint.setColour(13)
        self.assertEqual(self.joint.colourAsString, "red")

    def test_dag_node_setColour(self):
        self.joint.setColour("light blue")
        self.assertEqual(self.joint.colourAsString, "light blue")

    def test_dag_node_setVisibility(self):
        self.sphere.setVisibility(1)
        self.assertEqual(cmds.getAttr(self.sphere.fullPath + ".v"), 1)

        self.sphere.setVisibility(0)
        self.assertEqual(cmds.getAttr(self.sphere.fullPath + ".v"), 0)

    def test_dag_node_hide(self):
        self.sphere.hide()
        self.assertEqual(cmds.getAttr(self.sphere.fullPath + ".v"), 0)

    def test_dag_show(self):
        self.sphere.hide()
        self.assertEqual(cmds.getAttr(self.sphere.fullPath + ".v"), 0)

        self.sphere.show()
        self.assertEqual(cmds.getAttr(self.sphere.fullPath + ".v"), 1)

    def test_dag_node_history(self):
        history = self.sphere.history
        self.assertIn('polySphere1', history)

    def test_dag_node_deleteHistory(self):
        self.sphere.deleteHistory()
        history = self.sphere.history
        self.assertNotIn('polySphere1', history)

    def test_dag_node_duplicate_pass(self):
        testItemName = "duplicated_ITEM_TEST"
        sphere2 = self.sphere.duplicate(n=testItemName)
        self.assertTrue(sphere2.exists())
        self.assertTrue(sphere2.fullPath == "|OFFSET_1_GRP|" + testItemName)

        sphere2.delete()
        self.assertFalse(sphere2.exists())

    def test_dag_node_move(self):
        self.sphere.move(5, y=1)
        value = cmds.getAttr(self.sphere.fullPath + '.ty')
        self.assertEqual(value, 5)


if __name__ == "__main__":
    unittest.main()
