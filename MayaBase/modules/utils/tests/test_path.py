"""
Author:SuoLin Zhang
Created:2023
About: Tests for our path module.
"""

import unittest

from MayaBase.modules.utils.path import (
    generateReprString,
    rootName,
    baseName,
    namespace
)


class Test_Path(unittest.TestCase):
    def test_generateReprString(self):
        cls = "Dep_Node"
        name = "sphere_Grp"

        expectedResult = "Dep_Node('sphere_Grp')"

        result = generateReprString(cls, name)

        self.assertEqual(result, expectedResult)

    def test_rootName(self):
        name = "namespace:base_GRP|namespace:sub_GRP|namespace:sphere_GEO"
        result = rootName(name)
        expectedResult = "namespace:sphere_GEO"
        self.assertEqual(result, expectedResult)

    def test_baseName(self):
        name = "namespace:base_GRP|namespace:sub_GRP|namespace:sphere_GEO"
        result = baseName(name)
        expectedResult = "sphere_GEO"
        self.assertEqual(result, expectedResult)

    def test_namespace(self):
        name = "namespace:base_GRP|namespace:sub_GRP|namespace:sphere_GEO"
        result = namespace(name)
        expectedResult = "namespace"
        self.assertEqual(result, expectedResult)


if __name__ == "__main__":
    unittest.main()