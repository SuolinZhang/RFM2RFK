from MayaBase.modules.nodel import Dag_Node as Dag

from Rfm2Rfk import utils

import maya.cmds as cmds

import unittest


class TEST_RFM2RFK_UTILS_BASE(unittest.TestCase):

    def setUp(self):
        self.endNodeName = "NWM_END"
        self.upstreamNodeName = "NWM_UP"
        self.shadingEngineName = "test_SG"

        self.endNode = Dag(cmds.shadingNode("PxrSurface", name=self.endNodeName, asShader=True))
        self.upstreamNode = Dag(cmds.shadingNode("PxrChecker", name=self.upstreamNodeName, asShader=True))
        self.shadingEngine = Dag(cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=self.shadingEngineName))

        cmds.connectAttr(self.upstreamNode.a.resultRGB, self.endNode.a.diffuseColor)
        cmds.connectAttr(self.endNode.a.outColor, self.shadingEngine.a.rman__surface)


    def tearDown(self):
        if self.endNode.exists():
            self.endNode.delete()

        if self.upstreamNode.exists():
            self.upstreamNode.delete()

        if self.shadingEngine.exists():
            self.shadingEngine.delete()



class TEST_RFM2RFK_UTILS(TEST_RFM2RFK_UTILS_BASE):

    def test_m2k_utils_getNodeAttributes(self):
        end_attrs_dict = utils.getNodeAttributes(self.endNode.fullPath)
        self.assertIn('specularRoughness', end_attrs_dict)
        self.assertIsInstance(end_attrs_dict['specularFaceColor'], list)

    def test_m2k_utils_getInputConnctions(self):
        connections = utils.getInputConnctions(self.endNode)

        self.assertEqual(len(connections), 1)
        self.assertIn('diffuseColor', connections)
        self.assertEqual(connections['diffuseColor'], self.upstreamNode.a.resultRGB.path)

    def test_m2k_utils_connectionInputIsChild(self):

        self.assertFalse(utils.connectionInputIsChild(self.endNode.fullPath, "diffuseColor"))

    def test_m2k_utils_checkIfParent(self):

        self.assertTrue(utils.checkIfParent(self.endNode.fullPath))
        self.assertFalse(utils.checkIfParent(self.upstreamNode.fullPath))

    def test_m2k_utils_checkOrphaned(self):
        cmds.shadingNode("PxrTexture", name='test_texture', asShader=True)
        self.assertTrue(utils.checkOrphaned("test_texture"))
        cmds.delete('test_texture')

if __name__ == "__main__":
    unittest.main()