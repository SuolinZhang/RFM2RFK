"""
Author:SuoLin Zhang
Created:2023
About: Tests for our Open Maya API Functionality
"""

import unittest

import maya.OpenMaya as om

import maya.cmds as cmds

from MayaBase.modules.utils.open_maya_api import toDependencyNode, toMObject


class Test_Maya_Open_API(unittest.TestCase):
    def setUp(self) -> None:
        self.jointName = "L_hand_JNT"
        self.joint = cmds.joint(n=self.jointName)

        self.baseGrp = cmds.group(n="BASE_GRP", em=1)
        self.subGrp = cmds.group(n="SUB_GRP", em=1)
        cmds.parent(self.subGrp, self.baseGrp)
        cmds.parent(self.joint, self.subGrp)

    def tearDown(self) -> None:
        cmds.delete(self.baseGrp)

    def test_toDependencyNode(self):
        obj = toDependencyNode(self.jointName)
        result = obj.typeName()
        expectedResult = "joint"
        self.assertEqual(result, expectedResult)

    def test_toMObject(self):
        obj = toMObject(self.jointName)
        fullPathName = om.MFnDagNode(obj).fullPathName()
        expectedResult = "|BASE_GRP|SUB_GRP|L_hand_JNT"
        self.assertEqual(fullPathName, expectedResult)


if __name__ == "__main__":
    unittest.main()
