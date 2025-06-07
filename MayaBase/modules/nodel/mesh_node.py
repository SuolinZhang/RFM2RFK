"""
Author:SuoLin Zhang
Created:2023
About: Our Mesh Node functionality to deal with Maya
        node with or without dependency.
"""

import maya.cmds as cmds
import maya.mel as mel
from MayaBase.modules.nodel import Dag_Node
from MayaBase.modules.utils import weights


class Mesh(Dag_Node):

    def __init__(self, node):
        Dag_Node.__init__(self, node)

        # Check that we are on the transform and not the shape node
        if cmds.objectType(node) == "mesh":
            self.node = self.parent.node

    # ------------------------------------------------------------------------------------------------- FORMATION
    @property
    def vertices(self):
        return cmds.ls(self.fullPath + ".vtx[*]", fl=1)

    @property
    def edges(self):
        return cmds.ls(self.fullPath + ".e[*]", fl=1)

    @property
    def faces(self):
        return cmds.ls(self.fullPath + ".f[*]", fl=1)

    # ------------------------------------------------------------------------------------------------- TYPE

    @property
    def type(self):
        return cmds.objectType(self.shape)

    # ------------------------------------------------------------------------------------------------- SKINCLUSTER

    @property
    def skinCluster(self):
        skinCluster = mel.eval("findRelatedSkinCluster \"%s\"" % self.fullPath)
        return Dag_Node(skinCluster)

    @property
    def joints(self):
        if self.skinCluster.exists():
            influences = [Dag_Node(i) for i in cmds.skinCluster(self.skinCluster, q=1, inf=1)]
            return influences

    @property
    def blendShapes(self):
        history = self.history
        bs = [i for i in history if i.type == "blendShape"]
        return bs

    def weightTo(self, joints, **kwargs):
        if self.exists():
            cmds.skinCluster(self.fullPath, joints, **kwargs)

    def softWeightTo(self, joints, rui=0, mi=3, tsb=1, dr=2, **kwargs):
        self.weightTo(joints, rui=rui, mi=mi, tsb=tsb, dr=dr, **kwargs)

    def hardWeightTo(self, joints):
        self.weightTo(joints, rui=0, mi=1, tsb=1, dr=0.1)

    def copyWeightsTo(self, items):
        items = items if isinstance(items, (list, tuple)) else [items]
        if self.skinCluster.exists():
            joints = self.joints
            for item in [Mesh(i) for i in items]:
                if item.skinCluster:
                    item.skinCluster.delete()
                item.hardWeightTo(joints)
                cmds.copySkinWeights(
                    ss=self.skinCluster.name,
                    ds=item.skinCluster.name,
                    noMirror=1,
                    sa="closestPoint",
                    ia="oneToOne"
                )

    def copyWeightsFrom(self, item):
        Mesh(item).copyWeightsTo(self)

    def saveSkinWeights(self, weightsFolder):
        geoObject = str(self.node)
        geoSkinClusterNode = str(self.skinCluster)
        if not geoSkinClusterNode:
            print('# no skinCluster found on %s, skipping saving skin weights' % geoObject)
            return
        influences = [str(joint.node) for joint in self.joints]
        weights.saveWeights(geoObject, weightsFolder, geoSkinClusterNode, influences)

    def loadSkinWeights(self, weightsFolder):
        geoObject = str(self.node)
        weights.loadWeights(geoObject, weightsFolder)

    # ------------------------------------------------------------------------------------------------- TOPOLOGY
    def deleteTweaks(self):
        if self.exists():
            tweaks = list(set([i.name for i in self.history if cmds.objectType(i.name) == "tweak"]))

            if tweaks:
                cmds.delete(tweaks)

    # ------------------------------------------------------------------------------------------------- DUPLICATE
    def duplicate(self, **kwargs):
        if not self.exists():
            raise ValueError(">>> No item to duplicate")

        return Mesh(cmds.duplicate(self.fullPath, **kwargs)[0])
