"""
Author:SuoLin Zhang
Created:2023
About: Tests for our Dep_Node Functionality
"""

from MayaBase.modules.nodel import Dep_Node

import maya.cmds as cmds

import unittest


class Test_Dep_Node(unittest.TestCase):
    def setUp(self) -> None:
        self.sphereName = "sphere_001"
        self.jointName = "joint_001"

        self.sphere = Dep_Node(cmds.polySphere(n=self.sphereName)[0])
        cmds.select(cl=True)
        self.joint = Dep_Node(cmds.joint(n=self.jointName))

        self.object = Dep_Node(self.sphereName)

    def tearDown(self) -> None:
        if cmds.objExists(self.sphereName):
            cmds.delete(self.sphereName)

        if cmds.objExists(self.jointName):
            cmds.delete(self.jointName)

    # __init__ will be inferred by create method

    def test_dep_node__str__(self):
        self.assertEqual(str(self.sphere), self.sphereName)

    def test_dep_node__repr__(self):
        self.assertEqual(
            repr(self.sphere),
            "Dep_Node('sphere_001')"
        )

    def test_dep_node__eq__(self):
        self.assertTrue(self.sphere == self.object)
        self.assertTrue(self.sphere.fullPath == self.sphereName)
        self.assertTrue(self.sphere.path == self.sphereName)
        self.assertFalse(self.sphere == self.joint)

    def test_dep_node_getter(self):
        self.assertEqual(self.sphere.node, self.sphereName)
        self.assertEqual(self.object.node, self.sphere.node)
        self.assertNotEqual(self.sphere.node, self.joint.node)

    def test_dep_node_setter(self):
        self.sphere.node = self.jointName
        self.assertEqual(self.sphere.node, self.jointName)
        cmds.delete(self.sphereName)

    def test_dep_node_path(self):
        self.assertEqual(self.sphere.fullPath, self.sphereName)

    def test_dep_node_fullpath(self):
        self.assertEqual(self.sphere.fullPath, self.sphereName)
        self.assertEqual(self.sphere.fullPath, self.sphere.path)
        self.assertNotEqual(self.sphere.fullPath, self.joint.fullPath)

    def test_dep_node_isReferenced(self):
        self.assertFalse(self.sphere.isReferenced())

    def test_dep_node_exists(self):
        self.assertTrue(self.sphere.exists())

        cmds.delete(self.sphere)

        self.assertFalse(self.sphere.exists())

    def test_dep_node_fake_object(self):
        self.assertFalse(Dep_Node("FAKE OBJECT").exists())

    def test_dep_node_typ(self):
        self.assertEqual(self.joint.typ, "joint")
        self.assertNotEqual(self.joint.typ, "nurbsCurve")

    def test_dep_node_name(self):
        group1 = cmds.group(n="group1", em=True)
        group2 = cmds.group(n="group2", em=True)
        cmds.parent(group2, group1)
        cmds.parent(self.sphere, group2)
        result = self.sphere.name
        self.assertTrue(result == self.sphereName)
        cmds.delete(group1)

    def test_dep_node_namespace(self):
        self.assertIsNone(self.sphere.namespace)

    def test_dep_node_namespace_is_NOT_None(self):
        cmds.namespace(add="Foo")
        namespace = "Foo:"
        self.sphere.rename(namespace + self.sphereName)
        self.assertEqual(self.sphere.namespace, "Foo")
        cmds.delete(self.sphere)
        cmds.namespace(rm="Foo")

    def test_dep_node_lock_and_islocked(self):
        self.assertFalse(self.sphere.isLocked)

        self.sphere.lock(True)
        self.assertTrue(self.sphere.isLocked)

        self.sphere.lock(False)
        self.assertFalse(self.sphere.isLocked)

    def test_dep_node_delete(self):
        self.assertTrue(self.object.exists())
        self.object.delete()
        self.assertFalse(self.object.exists())
        self.assertFalse(self.sphere.exists())

    def test_dep_node_create_mutiplyDivide_node(self):
        mdNode = Dep_Node("geo_md", "multiplyDivide")
        self.assertTrue(mdNode.exists())
        self.assertEqual(mdNode.type, "multiplyDivide")
        mdNode.delete()
        self.assertFalse(mdNode.exists())

    def test_dep_node_create_and_delete_vector_product_node(self):
        vectorProduct = Dep_Node(cmds.shadingNode('vectorProduct', asUtility=True, n="test_VP"))
        self.assertTrue(vectorProduct.exists())

        vectorProduct.delete()
        self.assertFalse(vectorProduct.exists())


if __name__ == "__main__":
    unittest.main()
