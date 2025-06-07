"""
Author:SuoLin Zhang
Created:2023
About: Tests for our Mesh Node Functionality
"""

from MayaBase.modules.nodel import Dag_Node as Dag
from MayaBase.modules.nodel import Dep_Node as Dep
from MayaBase.modules.nodel import Mesh

import maya.cmds as cmds

import unittest


class Test_Mesh(unittest.TestCase):
    def setUp(self):
        self.attrs = ["tx", "ty", "tz", "rx", "ry", "rz"]

        self.sphereName = "sphere_GEO"
        self.sphere = Mesh(cmds.polySphere(n=self.sphereName)[0])

        self.cubeName = "cube_GEO"
        self.cube = Mesh(cmds.polyCube(n=self.cubeName, w=1, h=2, d=3)[0])

        self.joint_Name1 = "body_j1"
        self.joint_Name2 = "body_j2"

        cmds.select(cl=True)
        self.body_j1 = Dag(cmds.joint(n=self.joint_Name1))
        cmds.select(cl=True)
        self.body_j2 = Dag(cmds.joint(n=self.joint_Name2))

        cmds.skinCluster(self.sphere.fullPath, [self.body_j1, self.body_j2], rui=0, mi=3, tsb=1, dr=2)

    def tearDown(self) -> None:
        self.sphere.delete()
        self.cube.delete()
        self.body_j1.delete()
        self.body_j2.delete()

    # ------------------------------------------------------------------------------------------------- FORMATION
    def test_mesh_node_vertices(self):
        self.assertEqual(self.sphere.vertices[0], self.sphereName + ".vtx[0]")
        self.assertEqual(self.sphere.vertices[1], self.sphereName + ".vtx[1]")

    def test_mesh_node_edges(self):
        self.assertEqual(self.sphere.edges[0], self.sphereName + ".e[0]")
        self.assertEqual(self.sphere.edges[1], self.sphereName + ".e[1]")

    def test_mesh_node_faces(self):
        self.assertEqual(self.sphere.faces[0], self.sphereName + ".f[0]")
        self.assertEqual(self.sphere.faces[1], self.sphereName + ".f[1]")

    # ------------------------------------------------------------------------------------------------- TYPE
    def test_mesh_node_type(self):
        self.assertEqual(self.sphere.type, "mesh")

    # ------------------------------------------------------------------------------------------------- SKINCLUSTER
    def test_mesh_node_skinCluster(self):
        self.assertTrue(self.sphere.skinCluster.exists())

    def test_mesh_node_joints(self):
        self.assertEqual(self.sphere.joints, [self.body_j1, self.body_j2])

    def test_mesh_node_weightTo(self):
        joints = [self.body_j1, self.body_j2]
        self.cube.weightTo(joints, rui=0, mi=3, tsb=1, dr=2)
        self.assertTrue(self.sphere.skinCluster.exists())
        self.assertTrue(self.cube.skinCluster.exists())

    def test_mesh_node_softWeightTo(self):
        joints = [self.body_j1, self.body_j2]
        self.cube.softWeightTo(joints)
        self.assertTrue(self.cube.skinCluster.exists())

    def test_mesh_node_hardWeightTo(self):
        joints = [self.body_j1, self.body_j2]
        self.cube.hardWeightTo(joints)
        self.assertTrue(self.cube.skinCluster.exists())

    def test_mesh_node_copyWeightsTo(self):
        self.sphere.copyWeightsTo(self.cube)
        self.assertTrue(self.cube.skinCluster.exists())

    def test_mesh_node_copyWeightsFrom(self):
        self.cube.copyWeightsFrom(self.sphere)
        self.assertTrue(self.cube.skinCluster.exists())

    # ------------------------------------------------------------------------------------------------- TOPOLOGY

    def test_mesh_node_deleteTweaks(self):
        sphere2 = Mesh(cmds.polySphere(n=self.sphereName)[0])
        cmds.move(0, 4, 0, self.body_j2, r=1)
        cmds.move(4, 4, 4, self.sphere.vertices[0:33], a=1)
        cmds.blendShape(sphere2, self.sphere, tc=0)

        self.assertTrue(Dep("tweak1").exists())

        self.sphere.deleteTweaks()

        self.assertFalse(Dep("tweak1").exists())

        sphere2.delete()

    # ------------------------------------------------------------------------------------------------- DUPLICATE
    def test_mesh_node_duplicate(self):
        sphere2 = self.sphere.duplicate(n="test_sphere")
        self.assertTrue(sphere2.exists())
        self.assertEqual(sphere2.name, "test_sphere")
        sphere2.delete()


if __name__ == "__main__":
    unittest.main()

