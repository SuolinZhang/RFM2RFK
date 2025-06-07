from MayaBase.modules.nodel import Dag_Node as Dag

import maya.cmds as cmds

from Rfm2Rfk import m2k, ET
import unittest

from Rfm2Rfk.m2k import buildXML

_XML_CACHE = {}


class TEST_RFM2RFK_M2K_BASE(unittest.TestCase):

    def setUp(self):
        self.endNodeName = "NWM_END"
        self.upstreamNodeName = "NWM_UP"
        self.shadingEngineName = "test_SG"

        self.endNode = Dag(cmds.shadingNode("PxrSurface", name=self.endNodeName, asShader=True))
        self.upstreamNode = Dag(cmds.shadingNode("PxrChecker", name=self.upstreamNodeName, asShader=True))
        self.shadingEngine = Dag(cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=self.shadingEngineName))

        cmds.connectAttr(self.upstreamNode.a.resultRGB, self.endNode.a.diffuseColor)
        cmds.connectAttr(self.endNode.a.outColor, self.shadingEngine.a.rman__surface)

        test_template = """
        <node baseType="PrmanShadingNode" name="PxrSurface" selected="true" ns_fromContext="networkMaterial" type="PrmanShadingNode">
            <group_parameter name="PxrSurface">
                <string_parameter name="name" value="PxrSurface"/>
                <string_parameter name="nodeType" value="PxrSurface"/>
                <string_parameter name="__lastValue" value="wzdrtwzyk2ycgyj54dqoqlfewy7mkpvlbdw7px5mskhduq4w6fniFalse"/>
                <string_parameter name="__showHiddenParams" value="False"/>
                <group_parameter name="parameters"> 
                    <group_parameter name="diffuseColor">
                        <number_parameter name="enable" value="0"/>
                        <numberarray_parameter name="value" size="3" tupleSize="3">
                          <number_parameter name="i0" value="0.18"/>
                          <number_parameter name="i1" value="0.18"/>
                          <number_parameter name="i2" value="0.18"/>
                        </numberarray_parameter>
                        <string_parameter name="type" value="FloatAttr"/>
                    </group_parameter> 
                    <group_parameter name="specularRoughness">
                        <number_parameter name="enable" value="0"/>
                        <number_parameter name="value" value="0.2"/>
                        <string_parameter name="type" value="FloatAttr"/>
                    </group_parameter>
                </group_parameter>
            </group_parameter>
        </node>
        """
        test_checker = """
        <node baseType="PrmanShadingNode" name="PxrChecker" ns_fromContext="networkMaterial" ns_viewState="2" selected="true" type="PrmanShadingNode" x="-1257.93" y="-480.358">
            <group_parameter name="PxrChecker">
                <string_parameter name="name" value="PxrChecker"/>
                <string_parameter name="nodeType" value="PxrChecker"/>
                <string_parameter name="__lastValue" value="jbuclgyjarjrbxo64bar4tasxeclhi3mqbh7jk43cvmfalneu6zqFalse"/>
                <string_parameter name="__showHiddenParams" value="False"/>
                <group_parameter name="parameters">
                  <group_parameter name="colorA">
                    <number_parameter name="enable" value="0"/>
                    <numberarray_parameter name="value" size="3" tupleSize="3">
                      <number_parameter name="i0" value="1"/>
                      <number_parameter name="i1" value="1"/>
                      <number_parameter name="i2" value="1"/>
                    </numberarray_parameter>
                    <string_parameter name="type" value="FloatAttr"/>
                  </group_parameter>
                </group_parameter>
            </group_parameter>
        </node>
        """
        # Parse directly from string
        global _XML_CACHE
        _XML_CACHE['PxrSurface'] = ET.ElementTree(ET.fromstring(test_template))
        _XML_CACHE['PxrChecker'] = ET.ElementTree(ET.fromstring(test_checker))


    def tearDown(self):
        if self.endNode.exists():
            self.endNode.delete()

        if self.upstreamNode.exists():
            self.upstreamNode.delete()

        if self.shadingEngine.exists():
            self.shadingEngine.delete()
        _XML_CACHE.clear()

class TEST_RFM2RFK_CONVERSION(TEST_RFM2RFK_M2K_BASE):

    def test_getAllNodes(self):
        list = m2k.getAllNodes([self.endNodeName])
        self.assertEqual(len(list), 2)

    def test_generateNode(self):
        dict = m2k.generateNode(self.endNode.fullPath)
        self.assertEqual(dict["name"], self.endNodeName)

    def test_compareParameter(self):
        self.endNode.a.specularRoughness.set(1.0)
        dict = m2k.generateNode(self.endNode.fullPath)
        self.assertEqual(1.0, m2k.compareParameter("specularRoughness", dict))

    def test_iterateMapping(self):
        self.endNode.a.specularRoughness.set(1.0)
        dict = m2k.generateNode(self.endNode.fullPath)
        dict["X"] = 0
        dict["Y"] = 0
        xml_tree = m2k.iterateMapping(dict)
        xml = xml_tree.getroot()
        param_element= xml.find(".//group_parameter[@name='specularRoughness']")
        self.assertEqual("1.0", param_element.find("*[@name='value']").get('value'))

    def test_copy_workflow(self):
        dict = {}
        up_dict = m2k.generateNode(self.upstreamNode.fullPath)
        dict[self.upstreamNodeName]= up_dict
        tree = m2k.buildTree(dict)
        self.assertEqual(1, len(tree["terminal_nodes"]))

        xml_tree = m2k.buildXML(tree)
        xml_str= ET.tostring(xml_tree.getroot())
        print(f"Gnerated xml: {xml_str}")

if __name__ == "__main__":
    unittest.main()