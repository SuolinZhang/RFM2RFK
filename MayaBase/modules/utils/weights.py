"""
Author:SuoLin Zhang
Created:2023
About: functions for working with deformer weights
"""

import maya.cmds as cmds
import json
import os.path

weightsFileExt = '.xml'
influencesFileExt = '.infs'


def saveWeights(geoObject, weightsFolder, geoSkinClusterNode, influences):
    weightsFileName = geoObject + weightsFileExt
    cmds.deformerWeights(weightsFileName, path=weightsFolder, export=True, deformer=geoSkinClusterNode)

    influencesFileName = geoObject + influencesFileExt
    influencesPath = os.path.join(weightsFolder, influencesFileName)
    fileObj = open(influencesPath, mode='w')
    json.dump(influences, fileObj, sort_keys=True, indent=4, separators=(',', ': '))


def loadWeights(geoObject, weightsFolder):
    weightsFileName = geoObject + weightsFileExt
    weightsFilepath = os.path.join(weightsFolder, weightsFileName)

    influencesFileName = geoObject + influencesFileExt
    influencesFilePath = os.path.join(weightsFolder, influencesFileName)

    if not os.path.exists(weightsFilepath):
        print('# weights file not found for %s, skipping loading weights from %s' % (geoObject, weightsFilepath))
        return

    if not os.path.exists(influencesFilePath):
        print('# influences file not found for %s, skipping loading weights from %s' % (geoObject, influencesFilePath))
        return
    # get influences
    fileObj = open(influencesFilePath, mode='rb')
    fileObjStr = fileObj.read()
    influences = json.loads(fileObjStr)
    fileObj.close()

    # create skinCluster
    sc = cmds.skinCluster(geoObject, influences, tsb=True)[0]

    # load skin weights
    cmds.deformerWeights(weightsFileName, path=weightsFolder, im=True, deformer=sc)

    return weightsFilepath






















