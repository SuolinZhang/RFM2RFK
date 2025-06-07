"""
Author:SuoLin Zhang
Created:2023
About: All common needed tools.
"""
from MayaBase.modules.nodel import Joint, Curve, Dag_Node as Dag
import maya.cmds as cmds


def lips_shape(control, rootJoint, headCtrl, jawCtrl, primAxis='z', secAxis='x', upAxis='y', invertY=False):
    ctrl = Curve(control)
    root_Jnt = Joint(rootJoint)
    end_Jnt = root_Jnt.children[0]
    mid_loc = Dag(cmds.spaceLocator(n=control + '_loc')[0])
    mid_loc_offset = mid_loc.createOffset()
    mid_loc_offset.moveTo(end_Jnt, point=1)
    if Curve(headCtrl).exists():
        if 'low' in ctrl.node:
            mid_loc_offset.parentTo(jawCtrl)
        else:
            mid_loc_offset.parentTo(headCtrl)

    loc_tSec_root_rUp_mdl = (mid_loc.a['tx'] * 50).node
    loc_tSec_root_rUp_mdl.a.output >> root_Jnt.a['r' + upAxis]
    if invertY:
        loc_tUp_root_rSec_mdl = (mid_loc.a['t' + upAxis] * 50).node
        loc_tUp_root_rSec_mdl.a.output * (-1) >> root_Jnt.a['r' + secAxis]
    else:
        loc_tUp_root_rSec_mdl = (mid_loc.a['t' + upAxis] * 50).node
        loc_tUp_root_rSec_mdl.a.output >> root_Jnt.a['r' + secAxis]

    hrz_gradient_node = (mid_loc.a['tx'] * 1).node
    offset_node = ((hrz_gradient_node.a.output * mid_loc.a['tx']) - end_Jnt.a['t' + primAxis].get()).node
    offset_node.a.output1D * (-1) >> end_Jnt.a['t' + primAxis]

    ctrl.a.add(ln="Gradient", at='double', dv=1, k=1)
    ctrl.a.add(ln='Offset', at='double', dv=0, k=1)
    ctrl.a.add(ln='OrientX', at='double', dv=5, k=1)
    ctrl.a.add(ln='OrientY', at='double', dv=5, k=1)
    ctrl.a["Gradient"] >> hrz_gradient_node.a.input2
    ctrl.a['Offset'] >> offset_node.a['input1D[3]']
    ctrl.a['OrientX'] >> loc_tSec_root_rUp_mdl.a.input2
    ctrl.a['OrientY'] >> loc_tUp_root_rSec_mdl.a.input2
    ctrl.pointConstraint(mid_loc, mo=1)
    cmds.select(cl=1)


def twistJointsSetUp(prefix, moduleObjs, partType, startJoint, midJoint, endJoint, clavicleJnt, baseGrp):
    """make twist joints setup"""

    partPrefixes = ['Upper', 'Lower']
    jointAlist = [startJoint, midJoint]
    jointBlist = [midJoint, endJoint]
    differenceJointList = [clavicleJnt, endJoint]

    if partType == 'leg':
        differenceJointList = [baseGrp, endJoint]

    for partPrefix, jointA, jointB, differJoint in zip(partPrefixes, jointAlist, jointBlist, differenceJointList):
        ikJnt = Joint(jointA).duplicate(n=prefix + partPrefix + 'TwistIk1_jnt', parentOnly=1)
        ikJnt.a.r.set(0, 0, 0)
        ikJntEnd = Joint(jointB).duplicate(n=prefix + partPrefix + 'TwistIk2_jnt', parentOnly=1)
        ikJntEnd.parentTo(ikJnt)
        ikJntEnd.a.r.set(0, 0, 0)
        ikJntEnd.a.jo.set(0, 0, 0)

        twistSetupGrp = Dag(cmds.group(n=prefix + partPrefix + 'TwistSetup_grp', em=1, p=jointA))
        twistSetupGrp.parentTo(moduleObjs['partsGrp'])
        Joint(jointA).parentConstraint(twistSetupGrp, mo=1)
        ikJnt.parentTo(twistSetupGrp)

        twistIk = Dag(cmds.ikHandle(n=prefix + partPrefix + 'Twist_ikh', sol='ikSCsolver', sj=ikJnt, ee=ikJntEnd)[0])
        twistIk.parentTo(twistSetupGrp)
        Joint(differJoint).parentConstraint(twistIk, mo=1)

        twistJointsNum = 2

        for i in range(twistJointsNum):
            twistJoint = ikJntEnd.duplicate(n=prefix + partPrefix + 'TwistPart%d_jnt' % (i + 1))
            radius = twistJoint.a.radius.get()
            twistJoint.a.radius.set(radius * 2)
            twistJoint.setColour(14)
            twistJoint.parentTo(jointA)

            jntPointCons = Dag(cmds.pointConstraint(jointA, jointB, twistJoint.fullPath)[0])
            jntPointConsWeights = cmds.pointConstraint(jntPointCons.fullPath, q=1, weightAliasList=1)

            # adjust position of joint by setting constraint weights
            jntPointCons.a[jntPointConsWeights[0]].set(i + 1)
            jntPointCons.a[jntPointConsWeights[1]].set(twistJointsNum - i)

            ikJnt.a.rx * ((twistJointsNum - i) / (twistJointsNum + 1)) >> twistJoint.a.rx


if __name__ == "__main__":
    lips_shape()
