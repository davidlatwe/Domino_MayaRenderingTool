#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#
#	    ___       ___       ___       ___       ___       ___
#	   /\  \     /\  \     /\__\     /\  \     /\__\     /\  \
#	  /::\  \   /::\  \   /::L_L_   _\:\  \   /:| _|_   /::\  \
#	 /:/\:\__\ /:/\:\__\ /:/L:\__\ /\/::\__\ /::|/\__\ /:/\:\__\
#	 \:\/:/  / \:\/:/  / \/_/:/  / \::/\/__/ \/|::/  / \:\/:/  /
#	  \::/  /   \::/  /    /:/  /   \:\__\     |:/  /   \::/  /
#	   \/__/     \/__/     \/__/     \/__/     \/__/     \/__/
#
#
#		@ Author     David Power
#		@ Email 	 david962041@gmail.com
#
#		@ File       dp_Domino.py
#		@ FileVer	 1.0.0-Beta
#		@ MayaVer 	 2014, 2015 (other version not tested yet)
#		@ Platform 	 Windows (other platform not tested yet)
#		@ Date       2015-02-16
#
#		@ Brief      rendering frame by frame inside renderView with V-ray, MentalRay and other mayaRenderer.
#					 Press ESC to stop render.
#					 (other renderer not tested yet)
#					
#					 *For more details, please visit my github page.
#
#		@ GitHub	 https://github.com/davidpower/Domino-MayaRenderingTool
#
#		@ Thanks     PXFLY
#
#
#
#
#
#
#
#	Instalation:
#
#		1. Put this file (dp_Domino.py) into your Maya script folder, restart maya if necessary.
#
#		2. Copy the following code as a python shelf button (do not copy the line with triple single quotes)

'''
import dp_Domino
reload(dp_Domino)
dp_Domino.init_dp_Domino.dp_init()

'''
#
#		3. Have a nice render.
#
#










''' some boolean variables for custom change '''

# checking or not checking vrayDR slave's on/off status
vrayDR_check_Slave = 1

# kick out offline vrayDR slave
vrayDR_kick_Slave = 1

# make ui to pyQt style
set_QtStyle = 1

# if off, sceneQueue function will disable
can_uniqueTag = 1

# collapse Range setting frame in mainWindow when startup
rangeFm_collapse = 0

# for testing progressWindow's ui layout, skip mainWindow when startup
directly_Show_domino_ProgressUI_forTest = 0

# for testing progressWindow's ui layout, show all hidden ui in progressWindow
show_Hidden_UI_in_domino_ProgressUI = 0


















''' don't touch below, unless you know what you are doing '''
''' vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv '''

import maya.cmds as cmds
import maya.mel as mel

from functools import partial
from datetime import datetime

import smtplib
import email
import email.mime.application

import cPickle
import platform
import subprocess
import sys
import os
import math
import re
import socket

# Try import pySide module
try:
	from maya.OpenMayaUI import MQtUtil
	from shiboken import wrapInstance
	import PySide.QtGui as QtGui
	import PySide.QtCore as QtCore
	print 'dp_Domino: pySide can work.'
except:
	set_QtStyle = 0








class UI:


	def dp_mainWindow(self, *args):

		window = 'domino_mainUI'

		if cmds.window(window, ex= 1):
			cmds.deleteUI(window)

		cmds.window(window, t= 'dp_Domino', s= 0, mxb= 0, mnb= 0, ret= 1)

		global unRenderableLayers
		unRenderableLayers = []

		#''' scriptJob here '''
		cmds.scriptJob(ac= ['defaultRenderGlobals.animation', UI_Controls.dp_animationOnOffStatus], p= window)
		cmds.scriptJob(ac= ['defaultRenderGlobals.currentRenderer', UI_Controls.dp_getRendererName], p= window)
		cmds.scriptJob(ac= ['defaultResolution.width', UI_Controls.dp_changeResolution], p= window)
		cmds.scriptJob(ac= ['defaultResolution.height', UI_Controls.dp_changeResolution], p= window)
		cmds.scriptJob(ac= ['defaultRenderGlobals.startFrame', partial(UI_Controls.dp_getAttrSync, 'defaultRenderGlobals.startFrame', 'strFrm')], p= window)
		cmds.scriptJob(ac= ['defaultRenderGlobals.endFrame', partial(UI_Controls.dp_getAttrSync, 'defaultRenderGlobals.endFrame', 'endFrm')], p= window)
		cmds.scriptJob(ac= ['defaultRenderGlobals.byFrameStep', partial(UI_Controls.dp_getAttrSync, 'defaultRenderGlobals.byFrameStep', 'stpFrm')], p= window)
		cmds.scriptJob(ac= ['defaultRenderGlobals.modifyExtension', partial(UI_Controls.dp_getAttrSync, 'defaultRenderGlobals.modifyExtension', 'renumF')], p= window)
		cmds.scriptJob(ac= ['defaultRenderGlobals.startExtension', partial(UI_Controls.dp_getAttrSync, 'defaultRenderGlobals.startExtension', 'strNum')], p= window)
		cmds.scriptJob(ac= ['defaultRenderGlobals.byExtension', partial(UI_Controls.dp_getAttrSync, 'defaultRenderGlobals.byExtension', 'stpNum')], p= window)
		cmds.scriptJob(con= ['defaultRenderGlobals.startFrame', partial(UI_Controls.dp_getAttrSync, 'defaultRenderGlobals.startFrame', 'strFrm')], p= window)
		cmds.scriptJob(con= ['defaultRenderGlobals.endFrame', partial(UI_Controls.dp_getAttrSync, 'defaultRenderGlobals.endFrame', 'endFrm')], p= window)
		cmds.scriptJob(con= ['defaultRenderGlobals.byFrameStep', partial(UI_Controls.dp_getAttrSync, 'defaultRenderGlobals.byFrameStep', 'stpFrm')], p= window)
		cmds.scriptJob(con= ['defaultRenderGlobals.modifyExtension', partial(UI_Controls.dp_getAttrSync, 'defaultRenderGlobals.modifyExtension', 'renumF')], p= window)
		cmds.scriptJob(con= ['defaultRenderGlobals.startExtension', partial(UI_Controls.dp_getAttrSync, 'defaultRenderGlobals.startExtension', 'strNum')], p= window)
		cmds.scriptJob(con= ['defaultRenderGlobals.byExtension', partial(UI_Controls.dp_getAttrSync, 'defaultRenderGlobals.byExtension', 'stpNum')], p= window)
		cmds.scriptJob(e= ['timeUnitChanged', UI_Controls.dp_rangeCtrlGetLayerAttr], p= window)
		cmds.scriptJob(e= ['renderLayerManagerChange', UI_Controls.dp_layerMenuSync], p= window)
		cmds.scriptJob(e= ['renderLayerChange', UI_Controls.dp_refreshLayerMenu], p= window)
		cmds.scriptJob(ac= ['defaultRenderLayer.renderable', partial(UI_Controls.dp_layerRenderableTracker, 'defaultRenderLayer')], p= window)
		
		#''' rendFrame '''
		cmds.columnLayout(adj= 1)
		cmds.frameLayout('rendFrame', l= '', bgc= [.85, 0.45, 0.2], li= 0, bs= 'out', w= 192, h = 190)
		cmds.formLayout('renderForm')
		cmds.button('resetBtn', l= '', w= 6, h= 6, bgc= [.3, .2, .2], ann= 'Reset domino_mainUI when error occurred. DO NOT press while rendering.', c= resetEnvironment.dp_resetVar)
		cmds.button('delAtBtn', l= '', w= 6, h= 6, bgc= [.2, .2, .4], ann= 'Delete logs and settings. DO NOT press while rendering.', c= resetEnvironment.dp_deletePRAttr)
		cmds.checkBox('backChk', l= 'Backward', cc= UI_Controls.dp_changeBackwardStatus, ann= 'Render frames backward. *Note: if "Frame Priority" is on, this change to global backward.')
		cmds.checkBox('fProChk', l= 'Frame Priority', cc= UI_Controls.dp_changeFramePrioStatus, ann= 'Render one frame in each layers than go to next frame.\nBest for STEREO preview.')
		cmds.text('gBackMk', l= '', h= 33, w= 2, bgc= [0.8, 0.4, 0.1], vis= 0)
		cmds.checkBox('animChk', l= 'Animation', v= cmds.getAttr('defaultRenderGlobals.animation'), cc= UI_Controls.dp_changeAnimationStatus, ann= 'When rendering animation, this checkBox should turn on.')
		cmds.checkBox('delJChk', l= 'Delete Jobs', cc= UI_Controls.dp_changeDeleteJobStatus, ann= 'delete all renderJob layers after render is finished.')
		cmds.iconTextButton('clrFixBtn', w= 25, h= 25, image= 'removeRenderable.png', ann= 'delete all renderJob layers RIGHT NOW.', c= Render_Controls.dp_deleteJobsAfterRender)
		mel.eval('setTestResolutionVar(1)')
		cmds.text('ResTextB', l= '', h= 9, w= 106, bgc= [0.1, 0.1, 0.1])
		vraySet = 0
		if cmds.objExists('vraySettings'):
			if cmds.attributeQuery('width', node= 'vraySettings', ex= 1): vraySet = 1
		cmds.text('ResTextW', l= str(cmds.getAttr('vraySettings.width' if vraySet else 'defaultResolution.width')), fn= 'smallPlainLabelFont')
		cmds.text('ResTextX', l= ' x ', fn= 'smallPlainLabelFont')
		cmds.text('ResTextH', l= str(cmds.getAttr('vraySettings.height' if vraySet else 'defaultResolution.height')), fn= 'smallPlainLabelFont')
		cmds.optionMenu('ResMenu', l= '', cc= UI_Controls.dp_changeResolution)
		cmds.menuItem(l= 'Render Settings')
		cmds.menuItem(l= '  Camera Panel')
		cmds.menuItem(l= '  10% Settings')
		cmds.menuItem(l= '  25% Settings')
		cmds.menuItem(l= '  50% Settings')
		cmds.menuItem(l= '  75% Settings')
		cmds.menuItem(l= '110% Settings')
		cmds.menuItem(l= '125% Settings')
		cmds.menuItem(l= '150% Settings')
		cmds.iconTextButton('rvOpenBtn', image= 'rvOpenWindow.png', w= 25, h= 25, ann= 'open renderView window', c= UI_Controls.dp_openRenderView)
		cmds.iconTextButton('ImgDirBtn', image= 'rvKeepIt.png', w= 22, h= 22, ann= 'open images folder', c= partial(UI_Controls.dp_openImageFolder, '__imgRoot__'))
		cmds.button('renderBtn', l= 'R E A D Y', bgc= [.85, .45, .2], w= 100, h= 30, c= self.dp_ProgressWindow)

		cmds.formLayout('renderForm', e= 1, af= [('resetBtn' , 'top',  2 ), ('resetBtn' , 'left', 3)])
		cmds.formLayout('renderForm', e= 1, af= [('delAtBtn' , 'top',  12), ('delAtBtn' , 'left', 3)])
		cmds.formLayout('renderForm', e= 1, af= [('animChk'  , 'top',  5 ), ('animChk'  , 'left' , 58)])
		cmds.formLayout('renderForm', e= 1, af= [('backChk'  , 'top', 25 ), ('backChk'  , 'left' , 58)])
		cmds.formLayout('renderForm', e= 1, af= [('fProChk'  , 'top', 45 ), ('fProChk'  , 'left' , 58)])
		cmds.formLayout('renderForm', e= 1, af= [('gBackMk'  , 'top', 27 ), ('gBackMk'  , 'left' , 52)])
		cmds.formLayout('renderForm', e= 1, af= [('delJChk'  , 'top', 65 ), ('delJChk'  , 'left' , 58)])
		cmds.formLayout('renderForm', e= 1, af= [('clrFixBtn', 'top', 62 ), ('clrFixBtn', 'left' , 134)])
		cmds.formLayout('renderForm', e= 1, af= [('ResTextB'  , 'top', 89 ), ('ResTextB'  , 'left' ,42)])
		cmds.formLayout('renderForm', e= 1, af= [('ResTextW'  , 'top', 87 ), ('ResTextW'  , 'right' ,100)])
		cmds.formLayout('renderForm', e= 1, af= [('ResTextX'  , 'top', 87 ), ('ResTextX'  , 'left' , 90)])
		cmds.formLayout('renderForm', e= 1, af= [('ResTextH'  , 'top', 87 ), ('ResTextH'  , 'left' , 101)])
		cmds.formLayout('renderForm', e= 1, af= [('ResMenu'  , 'top', 87+14 ), ('ResMenu'  , 'left' , 42)])
		cmds.formLayout('renderForm', e= 1, af= [('renderBtn', 'top', 112+16), ('renderBtn', 'left' , 45)])
		cmds.formLayout('renderForm', e= 1, af= [('rvOpenBtn', 'top', 87+11), ('rvOpenBtn', 'left' , 15)])
		cmds.formLayout('renderForm', e= 1, af= [('ImgDirBtn', 'top', 87+12), ('ImgDirBtn', 'left' , 152)])
		cmds.setParent( '..' )
		cmds.setParent( '..' )

		#''' rangeFrame '''
		cmds.frameLayout('rangeFrame', l= 'Range Check', bgc= [0.31, 0.45, 0.20], cll= 1, cl= rangeFm_collapse, li= 33, bs= 'out', w= 192, h= 20 if rangeFm_collapse else 246)
		cmds.formLayout('rangeCheckForm')
		cmds.optionMenu('layerMenu', l= '', w= 147, ann= 'Layer menu, won\'t change current render layer.', cc= UI_Controls.dp_rangeCtrlGetLayerAttr)
		cmds.iconTextButton('layerTime', w= 20, h= 20, image= 'out_time.png', ann= 'Show Rendering Time Log', c= self.dp_layerMenuToRenderLog)
		cmds.button('refresBtn', l= '', w= 6, h= 6, bgc= [.2, .3, .2], ann= 'Refresh layer optionMenu when error occurred.', c= resetEnvironment.dp_refreshLayerMenu_warning)
		cmds.text('strFrmTxt', l= 'S', fn= 'tinyBoldLabelFont')
		cmds.text('endFrmTxt', l= 'E', fn= 'tinyBoldLabelFont')
		cmds.text('stpFrmTxt', l= 'B', fn= 'tinyBoldLabelFont')
		cmds.floatField('strFrmFfd', w= 70, pre= 3, ann= 'Start frame.', cc= partial(UI_Controls.dp_setAttrSync, 'defaultRenderGlobals.startFrame', 'strFrm'))
		cmds.popupMenu('startFrame_popupMenu', p= 'strFrmFfd', pmc= partial(UI_Controls.dp_frameRangePopupMenuPostCmd, 'defaultRenderGlobals.startFrame', 'strFrmTxt'))
		cmds.floatField('endFrmFfd', w= 70, pre= 3, ann= 'End frame.', cc= partial(UI_Controls.dp_setAttrSync, 'defaultRenderGlobals.endFrame', 'endFrm'))
		cmds.popupMenu('endFrame_popupMenu', p= 'endFrmFfd', pmc= partial(UI_Controls.dp_frameRangePopupMenuPostCmd, 'defaultRenderGlobals.endFrame', 'endFrmTxt'))
		cmds.floatField('stpFrmFfd', w= 70, pre= 3, ann= 'By frame.', cc= partial(UI_Controls.dp_setAttrSync, 'defaultRenderGlobals.byFrameStep', 'stpFrm'))
		cmds.popupMenu('byFrameStep_popupMenu', p= 'stpFrmFfd', pmc= partial(UI_Controls.dp_frameRangePopupMenuPostCmd, 'defaultRenderGlobals.byFrameStep', 'stpFrmTxt'))
		cmds.separator ('renumFSpt', st= 'in', h= 68, hr= 0)
		cmds.text('renumFTxt', l= 'Re-Num', ann= 'Renumber frames.')
		cmds.popupMenu('modifyExtension_popupMenu', p= 'renumFTxt', pmc= partial(UI_Controls.dp_frameRangePopupMenuPostCmd, 'defaultRenderGlobals.modifyExtension', 'renumFTxt'))
		cmds.checkBox('renumFChk', l= '', cc= partial(UI_Controls.dp_setAttrSync, 'defaultRenderGlobals.modifyExtension', 'renumF'))
		cmds.text('strNumTxt', l= 'S', fn= 'smallPlainLabelFont', en= 0)
		cmds.text('stpNumTxt', l= 'B', fn= 'smallPlainLabelFont', en= 0)
		cmds.floatField('strNumFfd', w= 56, pre= 3, ann= 'Start number.', cc= partial(UI_Controls.dp_setAttrSync, 'defaultRenderGlobals.startExtension', 'strNum'), en= 0)
		cmds.popupMenu('startExtension_popupMenu', p= 'strNumFfd', pmc= partial(UI_Controls.dp_frameRangePopupMenuPostCmd, 'defaultRenderGlobals.startExtension', 'strNumTxt'))
		cmds.floatField('stpNumFfd', w= 56, pre= 3, ann= 'By frame.', cc= partial(UI_Controls.dp_setAttrSync, 'defaultRenderGlobals.byExtension', 'stpNum'), en= 0)
		cmds.popupMenu('byExtension_popupMenu', p= 'stpNumFfd', pmc= partial(UI_Controls.dp_frameRangePopupMenuPostCmd, 'defaultRenderGlobals.byExtension', 'stpNumTxt'))
		cmds.text('custmText', l= 'Custom range', fn= 'smallPlainLabelFont', ann= 'input single frame(x,) or a range(x-y,) or a step range(x-y@z).\nex: 1, 2, 5, 8-14, 13-6@2')
		cmds.textField('custmTxtF', w= 147, text= '', ann= 'input single frame(x,) or a range(x-y,) or a step range(x-y@z).\n' +
														   'ex: 1, 2, 5, 8-14, 13-6@2'
													,  cc= partial(UI_Controls.dp_changeCustomFrame, '', 1))
		cmds.popupMenu()
		cmds.menuItem(l= 'Set All', c= UI_Controls.dp_changeCustomFrameAll)
		cmds.iconTextButton('clrDtaBtn', w= 20, h= 20, image= 'removeRenderable.png', ann= 'clear current layers\'s custom render range data.'
																					, c= partial(UI_Controls.dp_clearAllCustomFrameData, 0))
		cmds.popupMenu()
		cmds.menuItem(l= 'Clear All', c= partial(UI_Controls.dp_clearAllCustomFrameData, 1))

		cmds.text('cameraTxt', l= 'Render Camera list', fn= 'smallPlainLabelFont')
		cmds.textScrollList('cameraScr', w= 147, h= 57, fn= 'smallFixedWidthFont', dcc= 'print "camrea look"')
		cmds.iconTextButton('overriBtn', w= 20, h= 20, image= 'overrideSettings_dim.png', ann= 'Set override or remove override.',
										 c= 'cmds.iconTextButton("overriBtn", e= 1, ' +
											'image= "overrideSettings" + ("" if "_dim" in cmds.iconTextButton("overriBtn", q= 1, image= 1) ' +
											'and cmds.optionMenu("layerMenu", q= 1, v= 1) != "masterLayer" else "_dim") + ".png")')
		cmds.popupMenu('removeOverride_popupMenu', p= 'overriBtn', pmc= ('if cmds.optionMenu("layerMenu", q= 1, v= 1) == "masterLayer":\n' +
																		'	cmds.menuItem("removeOverride_item", e= 1, en= 0)\n' +
																		'else:\n' +
																		'	cmds.menuItem("removeOverride_item", e= 1, en= 1)'))
		cmds.menuItem('removeAllOverride_item', l= 'Remove all override', c= partial(UI_Controls.dp_removeCamOverride, 1))
		cmds.menuItem('removeOverride_item', l= 'Remove override', c= partial(UI_Controls.dp_removeCamOverride, 0))
		cmds.iconTextButton('addCamBtn', w= 20, h= 20, image= 'openAttribute.png', ann= 'List not renderable camera. Press green button to set selected renderable.', c= UI_Controls.dp_disrenderableCameraList)
		cmds.iconTextButton('delCamBtn', w= 20, h= 20, image= 'closeAttribute.png', ann= 'Remove renderable camera from list.', c= partial(UI_Controls.dp_adjRenderCamera, 0))

		st, et, bt = 36, 72-12 ,108-24
		cmds.formLayout('rangeCheckForm', e= 1, af= [('layerMenu', 'top', 10 ), ('layerMenu', 'left', 16)])
		cmds.formLayout('rangeCheckForm', e= 1, af= [('layerTime', 'top', 10 ), ('layerTime', 'left', 162)])
		cmds.formLayout('rangeCheckForm', e= 1, af= [('refresBtn', 'top', 3 ), ('refresBtn', 'left', 3)])
		cmds.formLayout('rangeCheckForm', e= 1, af= [('strFrmTxt', 'top', st+5), ('strFrmTxt', 'left', 86)])
		cmds.formLayout('rangeCheckForm', e= 1, af= [('endFrmTxt', 'top', et+5), ('endFrmTxt', 'left', 86)])
		cmds.formLayout('rangeCheckForm', e= 1, af= [('stpFrmTxt', 'top', bt+5), ('stpFrmTxt', 'left', 86)])
		cmds.formLayout('rangeCheckForm', e= 1, af= [('strFrmFfd', 'top', st), ('strFrmFfd', 'left', 15)])
		cmds.formLayout('rangeCheckForm', e= 1, af= [('endFrmFfd', 'top', et), ('endFrmFfd', 'left', 15)])
		cmds.formLayout('rangeCheckForm', e= 1, af= [('stpFrmFfd', 'top', bt), ('stpFrmFfd', 'left', 15)])
		cmds.formLayout('rangeCheckForm', e= 1, af= [('renumFSpt', 'top', st), ('renumFSpt', 'left', 99)])
		cmds.formLayout('rangeCheckForm', e= 1, af= [('renumFTxt', 'top', st+2), ('renumFTxt', 'left', 126)])
		cmds.formLayout('rangeCheckForm', e= 1, af= [('renumFChk', 'top', st+2), ('renumFChk', 'left', 108)])
		cmds.formLayout('rangeCheckForm', e= 1, af= [('strNumFfd', 'top', et), ('strNumFfd', 'left', 106)])
		cmds.formLayout('rangeCheckForm', e= 1, af= [('stpNumFfd', 'top', bt), ('stpNumFfd', 'left', 106)])
		cmds.formLayout('rangeCheckForm', e= 1, af= [('strNumTxt', 'top', et+3), ('strNumTxt', 'left', 163)])
		cmds.formLayout('rangeCheckForm', e= 1, af= [('stpNumTxt', 'top', bt+3), ('stpNumTxt', 'left', 163)])
		cmds.formLayout('rangeCheckForm', e= 1, af= [('custmText', 'top', 84 + 22), ('custmText', 'left',  17)])
		cmds.formLayout('rangeCheckForm', e= 1, af= [('custmTxtF', 'top', 98 + 22), ('custmTxtF', 'left',  15)])
		cmds.formLayout('rangeCheckForm', e= 1, af= [('clrDtaBtn', 'top',98 + 22), ('clrDtaBtn', 'left', 164)])
		cmds.formLayout('rangeCheckForm', e= 1, af= [('cameraTxt', 'top', 142), ('cameraTxt', 'left', 17)])
		cmds.formLayout('rangeCheckForm', e= 1, af= [('cameraScr', 'top', 142 + 14), ('cameraScr', 'left', 15)])
		cmds.formLayout('rangeCheckForm', e= 1, af= [('overriBtn', 'top', 142 + 14), ('overriBtn', 'left', 163)])
		cmds.formLayout('rangeCheckForm', e= 1, af= [('addCamBtn', 'top', 142 + 33), ('addCamBtn', 'left', 165)])
		cmds.formLayout('rangeCheckForm', e= 1, af= [('delCamBtn', 'top', 142 + 52), ('delCamBtn', 'left', 165)])
		cmds.setParent( '..' )
		cmds.setParent( '..' )

		#''' fQueueFrame '''
		cmds.frameLayout('fQueueFrame', l= 'Scenes Queue', bgc= [0.2, 0.4, 0.55], cll= 1, cl= 1, li= 32, bs= 'out', w= 192)
		cmds.formLayout('fQueueForm')
		cmds.textScrollList('fileScrollList', w= 189, h= 90, fn= 'smallFixedWidthFont', ams= 1, dkc= partial(UI_Controls.dp_sceneQueueAction, 'delete'),
																						sc= 'if cmds.file(q= 1, sn= 1, shn= 1):\n	cmds.textScrollList("fileScrollList", e= 1, dii= 1)')
		cmds.button('fileAddBtn', l= ' Add Scene', w= 117, h= 22, ann= 'Add one scene into render queue.', c= partial(UI_Controls.dp_sceneQueueAction, 'add'))
		cmds.button('fileDelBtn', l= ' X', w= 24, h= 22, ann= 'Remove selected scene from queue.', c= partial(UI_Controls.dp_sceneQueueAction, 'delete'))
		cmds.button('fileUpBtn', l= '', en= 0, w= 22, h= 22)
		cmds.button('fileDnBtn', l= '', en= 0, w= 22, h= 22)
		cmds.iconTextButton('fileUpArrowBtn', image= 'arrowUp.png', w= 22, h= 22, ann= 'Move selected scene\'s render priority up.', c= partial(UI_Controls.dp_sceneQueueAction, 'moveUP'))
		cmds.iconTextButton('fileDownArrowBtn', image= 'arrowDown.png', w= 22, h= 22, ann= 'Move selected scene\'s render priority down.', c= partial(UI_Controls.dp_sceneQueueAction, 'moveDown'))
		cmds.separator ('fileGapSpt', st= 'in', w= 186)
		cmds.checkBox('saveSceneChk', l= 'Save Scene', ann= 'Save scene before switch to next.', cc= 'sv = cmds.checkBox("saveSceneChk", q= 1, v= 1)\ncmds.checkBox("saveTmLogChk", e= 1, en= sv, v= sv)')
		cmds.checkBox('saveTmLogChk', l= 'Save Time Log', ann= 'Save scene with time log.', en= 0)
		cmds.formLayout('fQueueForm', e= 1, af= [('fileScrollList', 'top', 0), ('fileScrollList', 'left', 0)])
		cmds.formLayout('fQueueForm', e= 1, af= [('fileDelBtn', 'top', 92), ('fileDelBtn', 'left', 0)])
		cmds.formLayout('fQueueForm', e= 1, af= [('fileAddBtn', 'top', 92), ('fileAddBtn', 'left', 25)])
		cmds.formLayout('fQueueForm', e= 1, af= [('fileUpBtn', 'top', 92), ('fileUpBtn', 'left', 143)])
		cmds.formLayout('fQueueForm', e= 1, af= [('fileDnBtn', 'top', 92), ('fileDnBtn', 'left', 166)])
		cmds.formLayout('fQueueForm', e= 1, af= [('fileUpArrowBtn', 'top', 92), ('fileUpArrowBtn', 'left', 143)])
		cmds.formLayout('fQueueForm', e= 1, af= [('fileDownArrowBtn', 'top', 92), ('fileDownArrowBtn', 'left', 166)])
		cmds.formLayout('fQueueForm', e= 1, af= [('fileGapSpt', 'bottom', 24), ('fileGapSpt', 'left', 2)])
		cmds.formLayout('fQueueForm', e= 1, af= [('saveSceneChk', 'bottom', 4), ('saveSceneChk', 'left', 5)])
		cmds.formLayout('fQueueForm', e= 1, af= [('saveTmLogChk', 'bottom', 4), ('saveTmLogChk', 'left', 92)])
		cmds.setParent( '..' )
		cmds.setParent( '..' )

		#''' noticeFrame '''
		settings = MailSending.dp_loadMailSetting()
		emailFrom = settings[0]
		emailPass = settings[1]
		emailTo = settings[2]
		emailSmtp = settings[3]
		mailFrequency = 10
		
		cmds.frameLayout('noticeFrame', l= 'Sending Notice', bgc= [0.4, 0.2, 0.2], cll= 1, cl= 1, li= 30, bs= 'out', w= 192)

		cmds.columnLayout(adj= 1)

		''' emailFrame '''
		cmds.frameLayout('emailFrame', l= 'Email Setting', bgc= [0.35, 0.3, 0.3], cll= 1, cl= 0, li= 35, bs= 'out', fn= 'smallBoldLabelFont', h= 203)
		
		cmds.formLayout('emailForm')
		cmds.checkBox('getMailChk', l= 'Get Email Notice', ann= 'Get email notice.')
		cmds.checkBox('getMailChk', e= 1, onc= 'cmds.textField("mailToTxtF", e= 1, en= 1)\ncmds.iconTextButton("mailTesBtn", e= 1, en= 1)\ncmds.textField("mailToTxtF", e= 1, en= 1)\n' +
											   'cmds.textField("mailFromTxtF", e= 1, en= 1)\ncmds.textField("mailPassTxtF", e= 1, en= 1)\ncmds.textField("mailSmtpTxtF", e= 1, en= 1)\n' +
											   'cmds.checkBox("showCompChk", e= 1, en= 1)\ncmds.checkBox("startMalChk", e= 1, en= 1)\ncmds.checkBox("layerMalChk", e= 1, en= 1)\n' +
											   'cmds.checkBox("doneMailChk", e= 1, en= 1)\ncmds.checkBox("stopMailChk", e= 1, en= 1)\ncmds.checkBox("sendTLogChk", e= 1, en= 0)\n' +
											   'cmds.text("mailToText", e= 1, en= 1)\ncmds.text("NoticeText", e= 1, en= 1)\n' +
											   'cmds.intField("hoursGapInt", e= 1, en= 1 if cmds.checkBox("hourMailChk", q= 1, v= 1) else 0)\n' +
											   'cmds.checkBox("hourMailChk", e= 1, en= 1)')
		cmds.checkBox('getMailChk', e= 1, ofc= 'cmds.textField("mailToTxtF", e= 1, en= 0)\ncmds.iconTextButton("mailTesBtn", e= 1, en= 0)\ncmds.textField("mailToTxtF", e= 1, en= 0)\n' +
											   'cmds.textField("mailFromTxtF", e= 1, en= 0)\ncmds.textField("mailPassTxtF", e= 1, en= 0)\ncmds.textField("mailSmtpTxtF", e= 1, en= 0)\n' +
											   'cmds.checkBox("showCompChk", e= 1, en= 0)\ncmds.checkBox("startMalChk", e= 1, en= 0)\ncmds.checkBox("layerMalChk", e= 1, en= 0)\n' +
											   'cmds.checkBox("doneMailChk", e= 1, en= 0)\ncmds.checkBox("stopMailChk", e= 1, en= 0)\ncmds.checkBox("sendTLogChk", e= 1, en= 0)\n' +
											   'cmds.text("mailToText", e= 1, en= 0)\ncmds.text("NoticeText", e= 1, en= 0)\ncmds.intField("hoursGapInt", e= 1, en= 0)\n' +
											   'cmds.checkBox("hourMailChk", e= 1, en= 0)')
		cmds.checkBox('showCompChk', l= 'Show Computer Name', ann= 'Show render computer name in mail title.', v= 0, en= 0)
		cmds.checkBox('sendTLogChk', l= 'Send Time Log (Next release)', ann= 'Sending render time log with mail.', v= 0, en= 0, vis= 0)
		cmds.text('mailToText', l= 'Send To :', ann= 'email address for getting mails', en= 0)
		cmds.textField('mailToTxtF', w= 150, text= emailTo, ann= 'email address for getting mails', cc= MailSending.dp_saveMailSetting, en= 0)
		cmds.iconTextButton('mailTesBtn', w= 25, h= 25, image= 'echoCommands.png', ann= 'send a testing mail.', c= partial(MailSending.dp_sendEmail, 'TEST'), en= 0)
		cmds.text('NoticeText', l= 'Get Notice When :', en= 0)
		cmds.checkBox('startMalChk', l= 'Render Start', ann= 'Get notice when render start.', v= 0, en= 0)
		layerOnOff = 0
		for layer in cmds.ls(et= 'renderLayer'):
			if cmds.getAttr(layer + '.renderable'):
				layerOnOff += 0.5
		cmds.checkBox('layerMalChk', l= 'Layer Finish', ann= 'Get notice when one layer finished.', v= int(layerOnOff), en= 0)
		cmds.checkBox('doneMailChk', l= 'Render Done', ann= 'Get notice when rendering is done.', v= 1, en= 0)
		cmds.checkBox('stopMailChk', l= 'User Stop', ann= 'Get notice when render stopped.', v= 0, en= 0)
		cmds.checkBox('hourMailChk', l= 'Every            Hour', ann= 'Get notice when the time has come.', v= 0,
									 cc= 'cmds.intField("hoursGapInt", e= 1, en= cmds.checkBox("hourMailChk", q= 1, v= 1))', en= 0)
		cmds.intField('hoursGapInt', s= 1, min= 1, max= 999, v= 1, h= 16, en= 0)
		cmds.intField('hoursGapInt', e= 1, cc= 'cmds.checkBox("hourMailChk", e= 1, l= "Every            Hours" if cmds.intField("hoursGapInt", q= 1, v= 1) > 1 else "Every            Hour")')
		cmds.formLayout('emailForm', e= 1, af= [('getMailChk', 'top',  9 ), ('getMailChk', 'left', 12)])
		cmds.formLayout('emailForm', e= 1, af= [('showCompChk', 'top', 28), ('showCompChk', 'left', 12)])
		cmds.formLayout('emailForm', e= 1, af= [('sendTLogChk', 'top', 47), ('sendTLogChk', 'left', 12)])
		cmds.formLayout('emailForm', e= 1, af= [('mailToText', 'top',  73 - 20), ('mailToText', 'left', 12)])
		cmds.formLayout('emailForm', e= 1, af= [('mailToTxtF', 'top',  89 - 20), ('mailToTxtF', 'left', 10)])
		cmds.formLayout('emailForm', e= 1, af= [('mailTesBtn', 'top',  87 - 20), ('mailTesBtn', 'left', 161)])
		cmds.formLayout('emailForm', e= 1, af= [('NoticeText' , 'top', 119 - 20), ('NoticeText' , 'left', 12)])
		cmds.formLayout('emailForm', e= 1, af= [('startMalChk', 'top', 137 - 20), ('startMalChk', 'left', 12)])
		cmds.formLayout('emailForm', e= 1, af= [('layerMalChk', 'top', 137 - 20), ('layerMalChk', 'left', 105)])
		cmds.formLayout('emailForm', e= 1, af= [('doneMailChk', 'top', 156 - 20), ('doneMailChk', 'left', 12)])
		cmds.formLayout('emailForm', e= 1, af= [('stopMailChk', 'top', 156 - 20), ('stopMailChk', 'left', 105)])
		cmds.formLayout('emailForm', e= 1, af= [('hourMailChk', 'top', 176 - 20), ('hourMailChk', 'left', 12)])
		cmds.formLayout('emailForm', e= 1, af= [('hoursGapInt', 'top', 177 - 20), ('hoursGapInt', 'left', 62)])
		cmds.setParent( '..' )
		cmds.setParent( '..' )

		''' severFrame '''
		cmds.frameLayout('severFrame', l= 'Sever Setting', bgc= [0.35, 0.3, 0.3], cll= 1, cl= 1, li= 34, bs= 'out', fn= 'smallBoldLabelFont')

		cmds.formLayout('severForm')
		cmds.text('mailFromText', l= 'Send From :', ann= 'email address for sending mails')
		cmds.textField('mailFromTxtF', w= 167, text= emailFrom, ann= 'email address for sending mails', cc= MailSending.dp_saveMailSetting, en= 0)
		cmds.text('mailPassText', l= 'Password :', ann= 'email password for login sever')
		cmds.textField('mailPassTxtF', w= 167, text= emailPass, ann= 'email password for login sever', cc= MailSending.dp_saveMailSetting, en= 0)
		cmds.text('mailSmtpText', l= 'SMTP Sever :', ann= 'email smpt sever and port setting. input sever:port\nex : smtp.gmail.com:587')
		cmds.textField('mailSmtpTxtF', w= 167, text= emailSmtp, ann= 'email smpt sever and port setting. input sever:port\nex : smtp.gmail.com:587', cc= MailSending.dp_saveMailSetting, en= 0)
		cmds.formLayout('severForm', e= 1, af= [('mailFromText', 'top',  9 ), ('mailFromText', 'left', 12)])
		cmds.formLayout('severForm', e= 1, af= [('mailFromTxtF', 'top', 23 ), ('mailFromTxtF', 'left', 10)])
		cmds.formLayout('severForm', e= 1, af= [('mailPassText', 'top', 50 ), ('mailPassText', 'left', 12)])
		cmds.formLayout('severForm', e= 1, af= [('mailPassTxtF', 'top', 64 ), ('mailPassTxtF', 'left', 10)])
		cmds.formLayout('severForm', e= 1, af= [('mailSmtpText', 'top', 91 ), ('mailSmtpText', 'left', 12)])
		cmds.formLayout('severForm', e= 1, af= [('mailSmtpTxtF', 'top',105 ), ('mailSmtpTxtF', 'left', 10)])
		cmds.setParent( '..' )
		cmds.setParent( '..' )
		cmds.setParent( '..' )
		cmds.setParent( '..' )

		#''' FrameADJ '''
		cmds.frameLayout('rangeFrame', e= 1, cc= partial(UI_Controls.dp_fCRW_2015, '', 'rangeFrame', 1)
										   , ec= partial(UI_Controls.dp_fCRW_2015, '', 'rangeFrame', 0))

		cmds.frameLayout('fQueueFrame',e= 1, cc= partial(UI_Controls.dp_fCRW_2015, '', 'fQueueFrame', 1)
										   , ec= partial(UI_Controls.dp_fCRW_2015, '', 'fQueueFrame', 0))

		cmds.frameLayout('noticeFrame',e= 1, cc= partial(UI_Controls.dp_fCRW_2015, '', 'noticeFrame', 1)
										   , ec= partial(UI_Controls.dp_fCRW_2015, '', 'noticeFrame', 0))

		cmds.frameLayout('emailFrame', e= 1, cc= partial(UI_Controls.dp_fCRW_2015, '', 'emailFrame', 1)
										   , ec= partial(UI_Controls.dp_fCRW_2015, '', 'emailFrame', 0))

		cmds.frameLayout('severFrame', e= 1, cc= partial(UI_Controls.dp_fCRW_2015, '', 'severFrame', 1)
										   , ec= partial(UI_Controls.dp_fCRW_2015, '', 'severFrame', 0))

		Render_Controls.dp_postSceneReadJob()

		#''' makeQtStyle'''
		if set_QtStyle: self.dp_mainWindow_Qt()

		if not can_uniqueTag:
			cmds.formLayout('fQueueForm', e= 1, en= 0)
			cmds.warning('dp_Domino: Current Maya version can\'t use textScrollList\'s uniqueTag flag. SceneQueue function OFF.')

		if not set_QtStyle:
			cmds.warning('dp_Domino: This machine can\'t not use PySide.')

		cmds.window(window, e= 1, w= 10, h= 10)
		cmds.showWindow(window)


	def dp_mainWindow_Qt(self):

		UI_Controls.dp_makePySideUI('rendFrame', 'QWidget {color: #2B2B2B; background-color: #3B3B3B}')
		UI_Controls.dp_makePySideUI('renderForm', 'QWidget {color: None; background-color: None}')
		UI_Controls.dp_makePySideUI('resetBtn', 'QPushButton {border: 1px solid FireBrick; border-radius: 2px;}')
		UI_Controls.dp_makePySideUI('delAtBtn', 'QPushButton {border: 1px solid SteelBlue; border-radius: 2px;}')
		UI_Controls.dp_makePySideUI('renderBtn', 'QPushButton {border: 1px solid DarkOrange; color: DarkOrange; background-color: #3B3B3B; border-radius: 3px;}')
		UI_Controls.dp_makePySideUI('refresBtn', 'QPushButton {border: 1px solid OliveDrab; border-radius: 2px;}')


	def dp_ProgressWindow(self, *args):
		
		global dp_Rendering
		window = 'domino_ProgressUI'
		
		if cmds.window(window, ex= 1):
			if dp_Rendering:
				cmds.showWindow(window)
			else:
				cmds.deleteUI(window)

		if not dp_Rendering or not cmds.window(window, ex= 1):

			cmds.window(window, title= 'Missions Progress', w= 100, h= 100, s= 0, mxb= 0, mnb= 0, ret= 1)

			default_pbWindowWidth = 280
			default_proBarLength = 160
			default_longestLayerName = 60
			
			letterSize = 7
			digiSize = 6.5
			slashSize = 4

			global renderMissionLayerSort
			global allFrameRange

			Render_Controls.dp_layerSort()
			Render_Controls.dp_storeAllFrameRange()

			if renderMissionLayerSort:

				pbWindowWidth = default_pbWindowWidth
				proBarLength = default_proBarLength
				newLayerName = {}

				for layer in renderMissionLayerSort:
					#get layer status length
					rangeData = allFrameRange[layer]
					rangeData.sort()
					count_layerTxtLength = 0
					count_proBarLength = 0

					# layer name length
					newLayerName[layer] = dataGetFormat.dp_layerNameAdjust(1, layer, 0)
					if mel.eval('gmatch ' + layer.upper() + ' \"*_RENDERJOB*\"'):
						num = layer.upper().split('_RENDERJOB')
						if num[1]:
							newLayerName[layer] = '(RenJob' + num[1] + ') ' + newLayerName[layer]
						else:
							newLayerName[layer] = '(RenJob) ' + newLayerName[layer]
					if layer == 'defaultRenderLayer':
						newLayerName[layer] = 'masterLayer'

					count_layerTxtLength += len(newLayerName[layer]) * letterSize
					# layer frame count down length
					tmp = len(str(Render_Controls.dp_jobsCaculator(2, layer))) * digiSize * 2 + 12 # xxx / xxx
					count_layerTxtLength = count_layerTxtLength if count_layerTxtLength > tmp else tmp

					count_proBarLength += len(str(rangeData[0])) * digiSize
					count_proBarLength += len(str(rangeData[-1])) * digiSize
					tmp = str(rangeData[0] if cmp(abs(rangeData[0]), abs(rangeData[-1])) + 1 else rangeData[-1])
					count_proBarLength += (len('00:00:00') if (len('= = ') + len(tmp)) < len('00:00:00') else len(tmp)) * digiSize
					count_proBarLength += 100

					if count_proBarLength <= proBarLength:
						count_layerTxtLength += proBarLength
						proBarLength = proBarLength
					else:
						count_layerTxtLength += count_proBarLength
						proBarLength = count_proBarLength
					
					count_layerTxtLength += 80

					if count_layerTxtLength > pbWindowWidth:
						pbWindowWidth = count_layerTxtLength

					#find longest layer name
					if len(newLayerName[layer]) * letterSize > default_longestLayerName:
						default_longestLayerName = len(newLayerName[layer]) * letterSize

				mainLayerNum = Render_Controls.dp_jobsCaculator(3, '')
				mainFrameNum = Render_Controls.dp_jobsCaculator(1, '')
				missionStringSize = len(' Frames') * letterSize + len(str(mainLayerNum)) * digiSize + len(' Layers, ') * letterSize + len(str(mainFrameNum)) * digiSize
				missionStringSize = missionStringSize / 2 + ((pbWindowWidth - 250) / 2) - 40
				proLabelIndent = (pbWindowWidth - 84) / 2

				# for maya 2015, window won't auto resize
				cmds.window(window, e= 1, w= pbWindowWidth, h= 100)

				cmds.columnLayout(adj= 1)
				
				#Main ProgressBar
				cmds.frameLayout('mainProFrame', l= 'Main Progress', li= proLabelIndent, bs= 'out', w= pbWindowWidth, h= 80, bgc= [0.3, 0.3, 0.3])
				cmds.columnLayout('mainProColumn', columnAttach= ['both', 25], rowSpacing= 2, columnWidth= (pbWindowWidth - 4))
				cmds.formLayout('myForm')
				cmds.rowLayout('myRow', numberOfColumns= 4)
				cmds.text('mainLayerNum', l= mainLayerNum, fn= 'boldLabelFont')
				cmds.text('myLayerText', l= ' Layers, ', fn= 'fixedWidthFont')
				cmds.text('mainFrameNum', l= mainFrameNum, fn= 'boldLabelFont')
				cmds.text('myFrameText', l= ' Frames', fn= 'fixedWidthFont')
				cmds.setParent( '..' )
				cmds.formLayout('myForm', e= 1, af= ['myRow', 'left', missionStringSize])
				cmds.setParent( '..' )

				value = mainFrameNum
				cmds.progressBar('mainProBar', h= 12, maxValue= value, step= 1)
				cmds.formLayout('myBtnForm')
				cmds.rowLayout('myBtnRow')
				cmds.button('goPauseBtn', l= 'S T A R T', bgc= [0.2, 0.9, 1.0], w= pbWindowWidth - 56, h= 18, c= Render.dp_kickDomino)
				cmds.setParent( '..' )
				cmds.formLayout('myBtnForm', e= 1, af= [('myBtnRow', 'top', 1)])
				cmds.setParent( '..' )
				
				cmds.setParent( '..' )
				cmds.setParent( '..' )

				#Jobs ProgressBar
				proBarHeight = 30
				cmds.frameLayout('jobsProFrame', l= 'Jobs Progress', li= proLabelIndent, bs= 'out', w= pbWindowWidth, bgc= [0.3, 0.3, 0.3])
				cmds.formLayout('jobsProForm')
				
				#layer Up Down Arrow
				layerSwitchVis = 0
				if len(renderMissionLayerSort) > 1:
					layerSwitchVis = 1
				cmds.iconTextButton('layerUpArrowBtn', image= 'arrowUp.png', w= 20, h= 20, en= 0, vis= layerSwitchVis, c= partial(UI_Controls.dp_changeLayerProgressOrder, 'UP'))
				cmds.iconTextButton('layerDownArrowBtn', image= 'arrowDown.png', w= 20, h= 20, en= 0, vis= layerSwitchVis, c= partial(UI_Controls.dp_changeLayerProgressOrder, 'DOWN'))
				cmds.formLayout('jobsProForm', e= 1, af = [('layerUpArrowBtn', 'top', 10), ('layerUpArrowBtn', 'right', 3)])
				cmds.formLayout('jobsProForm', e= 1, af = [('layerDownArrowBtn', 'top', 32), ('layerDownArrowBtn', 'right', 3)])
				cmds.radioCollection('layerCollection')
				
				#each layers control
				proBarTop = 25
				proTxtTop = 10
				proBarTopGap = 45
				proBarLeft = 90

				for layer in renderMissionLayerSort:
					rangeData = allFrameRange[layer]
					rangeData.sort()
					startFrameStr = ''
					endFrameStr = ''

					if not (cmds.checkBox('fProChk', q= 1, v= 1) if not directly_Show_domino_ProgressUI_forTest else 0):
						if cmds.attributeQuery('dp_userAttr_backward', node= layer, ex= 1) and cmds.getAttr(layer + '.dp_userAttr_backward'):
							startFrameStr = rangeData[len(rangeData) - 1]
							endFrameStr = rangeData[0]
						else:
							startFrameStr = rangeData[0]
							endFrameStr = rangeData[len(rangeData) - 1]
					else:
						if cmds.attributeQuery('dp_userAttr_backwardInFramePrio', node= 'defaultRenderLayer', ex= 1) and cmds.getAttr('defaultRenderLayer.dp_userAttr_backwardInFramePrio'):
							startFrameStr = rangeData[len(rangeData) - 1]
							endFrameStr = rangeData[0]
						else:
							startFrameStr = rangeData[0]
							endFrameStr = rangeData[len(rangeData) - 1]
					
					#render star *
					starPos = proBarLength + 38
					cmds.text((layer + 'ProStar'), l= '', h= 8, w= len(newLayerName[layer]) * letterSize * 0.8, bgc= [0.22, 0.43, 0.79], vis= show_Hidden_UI_in_domino_ProgressUI)
					cmds.formLayout('jobsProForm', e= 1, af= [((layer + 'ProStar'), 'top', (proBarTop + 5)), ((layer + 'ProStar'), 'right', starPos)])
					#layer name
					textPos = proBarLength + 40
					cmds.text((layer + 'ProTxtName'), l= newLayerName[layer], al= 'right', fn= 'fixedWidthFont')
					cmds.formLayout('jobsProForm', e= 1, af= [((layer + 'ProTxtName'), 'top', proBarTop - 2), ((layer + 'ProTxtName'), 'right', textPos)])
					#radioButton
					cmds.radioButton((layer + 'RadioBn'), l= '', vis= layerSwitchVis, cl= 'layerCollection',
						onc= 'cmds.iconTextButton("layerUpArrowBtn", e= 1, en= 1)\ncmds.iconTextButton("layerDownArrowBtn", e= 1, en= 1)')
					cmds.formLayout('jobsProForm', e= 1, af= [((layer + 'RadioBn'), 'top', proBarTop), ((layer + 'RadioBn'), 'left', 6)])
					#current frame
					numberStr = '= ' + str(int(startFrameStr) if commonTool.dp_canThisFloatBeInt(startFrameStr) else startFrameStr) + ' ='
					curFmPos = (proBarLength / 2) - ((len(numberStr) * digiSize) / 2) + 30 + 4
					cmds.text((layer + 'ProCurrFrame'), l= numberStr, fn= 'smallBoldLabelFont', vis= show_Hidden_UI_in_domino_ProgressUI)
					cmds.formLayout('jobsProForm', e= 1, af= [((layer + 'ProCurrFrame'), 'top', (proTxtTop - 7)), ((layer + 'ProCurrFrame'), 'right', curFmPos)])
					#last frame time
					lfTmPos = (proBarLength / 2) - ((len('00:00:00') * (digiSize - 2.5)) / 2) + 30
					cmds.text((layer + 'lastFrameTime'), l= '00:00:00', ann= 'last frame render time.', fn= 'smallPlainLabelFont')
					cmds.formLayout('jobsProForm', e= 1, af= [((layer + 'lastFrameTime'), 'top', (proTxtTop + 3)), ((layer + 'lastFrameTime'), 'right', lfTmPos)])
					#elapsed time
					epTmPos = (proBarLength / 2) - ((len('00:00:00:00') * digiSize) / 2) + 30
					cmds.text((layer + 'elapsedTime'), l= '0.0', ann= 'this layer render time.',fn= 'fixedWidthFont', vis= 0)
					cmds.formLayout('jobsProForm', e= 1, af= [((layer + 'elapsedTime'), 'top', proTxtTop), ((layer + 'elapsedTime'), 'right', epTmPos)])
					#layer frame sum
					layerFramesSum = Render_Controls.dp_jobsCaculator(2, layer)
					sumPos = textPos + 2
					cmds.text((layer + 'ProTxtNum'), l= str(layerFramesSum), fn= 'fixedWidthFont')
					cmds.formLayout('jobsProForm', e= 1, af= [((layer + 'ProTxtNum'), 'top', proTxtTop), ((layer + 'ProTxtNum'), 'right', sumPos)])
					#slash
					slashPos = sumPos + (len(str(layerFramesSum)) * digiSize) + 6
					cmds.text((layer + 'ProTxtSlash'), l= '/', fn= 'fixedWidthFont')
					cmds.formLayout('jobsProForm', e= 1, af= [((layer + 'ProTxtSlash'), 'top', proTxtTop), ((layer + 'ProTxtSlash'), 'right', slashPos)])
					#layer render status
					statPos = slashPos + (slashSize / 2) + 9
					cmds.text((layer + 'ProTxtStatus'), l= str(layerFramesSum), fn= 'boldLabelFont')
					cmds.formLayout('jobsProForm', e= 1, af= [((layer + 'ProTxtStatus'), 'top', proTxtTop), ((layer + 'ProTxtStatus'), 'right', statPos)])
					#layer start frame
					pBarPos = pbWindowWidth - proBarLength - 28
					numberStr = str(int(startFrameStr) if commonTool.dp_canThisFloatBeInt(startFrameStr) else startFrameStr)
					cmds.text((layer + 'ProTxtStart'), l= numberStr, fn= 'fixedWidthFont')
					cmds.formLayout('jobsProForm', e= 1, af= [((layer + 'ProTxtStart'), 'top', proTxtTop), ((layer + 'ProTxtStart'), 'left', pBarPos)])
					#layer end frame
					numberStr = str(int(endFrameStr) if commonTool.dp_canThisFloatBeInt(endFrameStr) else endFrameStr)
					cmds.text((layer + 'ProTxtEnd'), l= numberStr, fn= 'fixedWidthFont')
					cmds.formLayout('jobsProForm', e= 1, af= [((layer + 'ProTxtEnd'), 'top', proTxtTop), ((layer + 'ProTxtEnd'), 'right', 32)])
					#progressBar
					pBarPos = 30
					value = Render_Controls.dp_jobsCaculator(2, layer)
					cmds.progressBar((layer + 'ProBar'), maxValue= value, w= proBarLength, h= 12, step= 1)
					cmds.formLayout('jobsProForm', e= 1, af= [((layer + 'ProBar'), 'top', proBarTop + 1), ((layer + 'ProBar'), 'right', pBarPos)])
					#folder link
					cmds.iconTextButton((layer + 'folderBtn'), image= 'SP_DirIcon.png', w= 20, h= 20, vis= show_Hidden_UI_in_domino_ProgressUI, c= partial(UI_Controls.dp_openImageFolder, layer))# navButtonBrowse
					cmds.formLayout('jobsProForm', e= 1, af= [((layer + 'folderBtn'), 'top', proBarTop - 4), ((layer + 'folderBtn'), 'right', 5)])
					#rendering time sheet
					cmds.iconTextButton((layer + 'timeShBtn'), image= 'out_time.png', w= 20, h= 20, c= partial(self.dp_timeLogWindow, layer), vis= show_Hidden_UI_in_domino_ProgressUI)
					cmds.formLayout('jobsProForm', e= 1, af= [((layer + 'timeShBtn'), 'top', (proBarTop - 18)), ((layer + 'timeShBtn'), 'left', 2)])

					proTxtTop += proBarTopGap
					proBarTop += proBarTopGap
					proBarHeight += proBarTopGap

					cmds.frameLayout('jobsProFrame', e= 1, h= proBarHeight)
				
				cmds.setParent( '..' )
				cmds.setParent( '..' )

				if set_QtStyle: self.dp_ProgressWindow_Qt()
				
				cmds.showWindow(window)
				if cmds.window('domino_mainUI', ex= 1):
					cmds.window(window, e= 1, le= cmds.window('domino_mainUI', q= 1, le= 1) - cmds.window(window, q= 1, w= 1) - 18, te= cmds.window('domino_mainUI', q= 1, te= 1))
			
			else:
				if cmds.window(window, ex= 1):
					cmds.deleteUI(window)
				cmds.confirmDialog( title='dp_Domino: Error', message= 'No layers are set to render.', button= ['Confirm'], defaultButton= 'Confirm', icon= 'warning')


	def dp_ProgressWindow_Qt(self):

		global renderMissionLayerSort

		QProgressBarStyle =('QProgressBar::chunk {background-color: #006080; width: 1px; margin: 1px;}' +
							'QProgressBar {border: 1px solid DimGray; border-radius: 3px; text-align: center; color: Turquoise;font: 10px; font-weight: normal;}')
		
		UI_Controls.dp_makePySideUI('mainProBar', QProgressBarStyle)
		UI_Controls.dp_makePySideUI('goPauseBtn', 'QPushButton {border: 1px solid Cyan; color: Cyan; background-color: #424242; border-radius: 3px;}')
		
		for layer in renderMissionLayerSort:
			UI_Controls.dp_makePySideUI(layer + 'ProCurrFrame', 'QLabel {color: #6A6A6A}')
			UI_Controls.dp_makePySideUI(layer + 'lastFrameTime', 'QLabel {color: #6A6A6A}')
			UI_Controls.dp_makePySideUI(layer + 'elapsedTime', 'QLabel {color: #1A1A1A}')
			UI_Controls.dp_makePySideUI(layer + 'ProTxtNum', 'QLabel {color: #1A1A1A}')
			UI_Controls.dp_makePySideUI(layer + 'ProTxtSlash', 'QLabel {color: #1A1A1A}')
			UI_Controls.dp_makePySideUI(layer + 'ProTxtStatus', 'QLabel {color: #6A6A6A}')
			UI_Controls.dp_makePySideUI(layer + 'ProTxtStart', 'QLabel {color: #1A1A1A}')
			UI_Controls.dp_makePySideUI(layer + 'ProTxtEnd', 'QLabel {color: #1A1A1A}')
			UI_Controls.dp_makePySideUI(layer + 'ProBar', QProgressBarStyle)


	def dp_timeLogWindow(self, layer, *args):

		# showing data: frame range
		#				total time
		#				average time
		#				normal time
		#				time gap

		global renderStartDate

		window = 'domino_timeLogUI'

		if cmds.window(window, ex= 1):
			cmds.deleteUI(window)

		cmds.window(window, t= ('Time Log :  ' + layer), w= 300, h= 500, mxb= 0, mnb= 0)
		cmds.tabLayout('prLogTab', dcc= partial(UI_Controls.dp_logTabSaveOrRename, layer), psc= partial(self.dp_timeLogTab, layer))

		prLogTabList = []

		#get renderLog attr list
		if cmds.attributeQuery('dp_userAttr_timeLog_Tmp', node= layer, ex= 1):
			if 'renderStartDate' in globals() and 'saved' not in cmds.getAttr(layer + '.dp_userAttr_timeLog_Tmp'):
				prLogTabList.append('dp_userAttr_timeLog_Tmp')
		if cmds.attributeQuery('dp_userAttr_logList', node= layer, ex= 1):
			prLogList = cmds.getAttr(layer + '.dp_userAttr_logList')
			if prLogList:
				prLogTabList.extend(prLogList.split(','))

		if prLogTabList:
			#make tabs
			for prLogName in prLogTabList:
				prLogData = ''
				if cmds.attributeQuery(prLogName, node= layer, ex= 1):
					prLogData = cmds.getAttr(layer + '.' + prLogName)
				if prLogData:
					cmds.formLayout(('prLogForm__' + prLogName + '__' + layer), p= 'prLogTab')
					if prLogTabList.index(prLogName) == 0: self.dp_timeLogTab(layer)
					if prLogName == 'dp_userAttr_timeLog_Tmp':
						date_YMD = renderStartDate.split(' ')[3]
						date_HMS = renderStartDate.split(' ')[5]
						cmds.tabLayout('prLogTab', e= 1, tabLabel= [(('prLogForm__' + prLogName + '__' + layer), (date_YMD + ' # ' + date_HMS + '*'))])
					else:
						tabLabel = ''
						if not cmds.attributeQuery(prLogName + '_tabLabel', node= layer, ex= 1):
							date_YMD = prLogName.split('_')[3][0:4] + '/' + prLogName.split('_')[3][4:6] + '/' + prLogName.split('_')[3][6:8]
							date_HMS = prLogName.split('_')[3][8:10] + ':' + prLogName.split('_')[3][10:12] + ':' + prLogName.split('_')[3][12:14]
							tabLabel = date_YMD + ' # ' + date_HMS
						else:
							tabLabel = cmds.getAttr(layer + '.' + prLogName + '_tabLabel').split('@')[0]
						cmds.tabLayout('prLogTab', e= 1, tabLabel= [(('prLogForm__' + prLogName + '__' + layer), tabLabel)])

			cmds.showWindow(window)
			if cmds.window('domino_ProgressUI', ex= 1):
				cmds.window(window, e= 1, le= cmds.window('domino_ProgressUI', q= 1, le= 1) - cmds.window(window, q= 1, w= 1) - 18, te= cmds.window('domino_ProgressUI', q= 1, te= 1))
			cmds.window(window, e= 1, w= 300, h= 500)

		else:
			if cmds.window(window, ex= 1):
				cmds.deleteUI(window)
			cmds.confirmDialog( title='dp_Domino: Error', message='No rendering time logs\nhave been saved yet.', button=['Confirm'], defaultButton='Confirm', icon= 'warning')


	def dp_timeLogTab(self, layer, *args):

		# logAttr format: [ frameRange ; frameNum1 = frameTime1 ; frameNum2 = frameTime2 ; ... ; TotalTime ]
		#					frameRange : ' startFrame - endFrame @ byFrame' or ' customFrame, customFrame, customFrame - customFrame @ byFrame'
		#					TotalTime  : ' TT=#### '
		
		prLogTabForm = cmds.tabLayout('prLogTab', q= 1, st= 1)
		if not cmds.formLayout(prLogTabForm, q= 1, ca= 1):
			prLogData_FrameRange = ''
			prLogData_TotalTime = ''
			prLogName = prLogTabForm.split('__')[1]
			prLogData = cmds.getAttr(layer + '.' + prLogName)

			# if formatte is old, update
			if ';' not in prLogData or 'TT=' not in prLogData or '$' not in prLogData:
				log = prLogData
				log = log.replace('@', ';')
				log = log.replace(':', '=')
				log = log.replace('TT_', 'TT=')
				log = '[' + log.replace(';', '];', 1)
				logarr = []
				for f in log.split(';'):
					if '=' in f and not 'TT=' in f and not '$' in f:
						f = f + '$0'
					logarr.append(f)
				prLogData = ';'.join(logarr)
				cmds.setAttr(layer + '.' + prLogName, prLogData, type= 'string')

			prLogDataSplit = prLogData.split(';')

			#delete tab button
			cmds.iconTextButton(('prLogBtnDelete__' + prLogName + '__' + layer), w= 16, h= 16, image= 'SP_MessageBoxCritical.png', c= partial(UI_Controls.dp_logTabDelete, layer), p= prLogTabForm)
			cmds.formLayout(prLogTabForm, e= 1, af= [(('prLogBtnDelete__' + prLogName + '__' + layer), 'top', 5), (('prLogBtnDelete__' + prLogName + '__' + layer), 'right', 5)])
			
			#get frame range     ------------------------------------------------------------------------------ # custom render range didn't show 
			if prLogDataSplit[0].startswith('[') and prLogDataSplit[0].endswith(']'):
				prLogData_FrameRange = prLogDataSplit[0].strip('[]')
				prLogDataSplit.pop(0)
			else:
				prLogData_FrameRange = 'unknown'
			
			#get total render time
			try:
				if 'TT' in prLogDataSplit[len(prLogDataSplit) - 1]:
					prLogData_TotalTime = dataGetFormat.dp_getFormattedRenderTime(float(prLogDataSplit[len(prLogDataSplit) - 1].split('=')[1]), 1)
					prLogDataSplit.pop()
				else:
					prLogData_TotalTime = '-- : -- : -- : --'
			except:
				# for error when the first frame not rendering done yet
				prLogData_TotalTime = '-- : -- : -- : --'

			cmds.text(('prLogTextRange__' + prLogName + '__' + layer), l= 'Frame Range : ', p= prLogTabForm)
			cmds.text(('prLogTextRangeData__' + prLogName + '__' + layer), l= prLogData_FrameRange, ann= prLogData_FrameRange, fn= 'boldLabelFont', p= prLogTabForm)
			cmds.text(('prLogTextTotalTime__' + prLogName + '__' + layer), l= 'Total Time : ', p= prLogTabForm)
			cmds.text(('prLogTextTotalTimeData__' + prLogName + '__' + layer), l= prLogData_TotalTime, fn= 'boldLabelFont', p= prLogTabForm)
			cmds.formLayout(prLogTabForm, e= 1, af= [(('prLogTextRange__' + prLogName + '__' + layer), 'top', 10), (('prLogTextRange__' + prLogName + '__' + layer), 'left', 15)])
			cmds.formLayout(prLogTabForm, e= 1, af= [(('prLogTextRangeData__' + prLogName + '__' + layer), 'top', 10), (('prLogTextRangeData__' + prLogName + '__' + layer), 'left', 90)])
			cmds.formLayout(prLogTabForm, e= 1, af= [(('prLogTextTotalTime__' + prLogName + '__' + layer), 'top', 30), (('prLogTextTotalTime__' + prLogName + '__' + layer), 'left', 31)])
			cmds.formLayout(prLogTabForm, e= 1, af= [(('prLogTextTotalTimeData__' + prLogName + '__' + layer), 'top', 30), (('prLogTextTotalTimeData__' + prLogName + '__' + layer), 'left', 90)])

			#calculate each frames render time scale for frameLayout color
			timeSheet = []
			for frameData in prLogDataSplit:
				timeSheet.append(float(frameData.split('=')[1].split('$')[0]))
			
			MidValue = UI_Controls.dp_findAverageRenderTime(timeSheet) if timeSheet else 0
			AvgValue = sum(timeSheet) / len(timeSheet) if timeSheet else 0
			GapValue = max(timeSheet) - min(timeSheet) if timeSheet else 0

			MidValueTime = dataGetFormat.dp_getFormattedRenderTime(MidValue, 0)
			AvgValueTime = dataGetFormat.dp_getFormattedRenderTime(AvgValue, 0)
			GapValueTime = dataGetFormat.dp_getFormattedRenderTime(GapValue, 0)

			cmds.text(('prLogTextAverageTime__' + prLogName + '__' + layer), l= 'Average Time : ', p= prLogTabForm)
			cmds.text(('prLogTextAverageTimeData__' + prLogName + '__' + layer), l= AvgValueTime, fn= 'boldLabelFont', p= prLogTabForm)
			cmds.text(('prLogTextNormalTime__' + prLogName + '__' + layer), l= 'Normal Time : ', p= prLogTabForm)
			cmds.text(('prLogTextNormalTimeData__' + prLogName + '__' + layer), l= MidValueTime, fn= 'boldLabelFont', p= prLogTabForm)
			cmds.text(('prLogTextGapTime__' + prLogName + '__' + layer), l= 'Time Gap : ', p= prLogTabForm)
			cmds.text(('prLogTextGapTimeData__' + prLogName + '__' + layer), l= GapValueTime, fn= 'boldLabelFont', p= prLogTabForm)
			cmds.formLayout(prLogTabForm, e= 1, af= [(('prLogTextAverageTime__' + prLogName + '__' + layer), 'top', 50), (('prLogTextAverageTime__' + prLogName + '__' + layer), 'left', 13)])
			cmds.formLayout(prLogTabForm, e= 1, af= [(('prLogTextAverageTimeData__' + prLogName + '__' + layer), 'top', 50), (('prLogTextAverageTimeData__' + prLogName + '__' + layer), 'left', 90)])
			cmds.formLayout(prLogTabForm, e= 1, af= [(('prLogTextNormalTime__' + prLogName + '__' + layer), 'top', 70), (('prLogTextNormalTime__' + prLogName + '__' + layer), 'left', 21)])
			cmds.formLayout(prLogTabForm, e= 1, af= [(('prLogTextNormalTimeData__' + prLogName + '__' + layer), 'top', 70), (('prLogTextNormalTimeData__' + prLogName + '__' + layer), 'left', 90)])
			cmds.formLayout(prLogTabForm, e= 1, af= [(('prLogTextGapTime__' + prLogName + '__' + layer), 'top', 90), (('prLogTextGapTime__' + prLogName + '__' + layer), 'left', 35)])
			cmds.formLayout(prLogTabForm, e= 1, af= [(('prLogTextGapTimeData__' + prLogName + '__' + layer), 'top', 90), (('prLogTextGapTimeData__' + prLogName + '__' + layer), 'left', 90)])

			hueMax = 0.0
			hueMid = 0.335
			hueMin = 0.67
			hueRangeGap = 30.0
			scaleGate = 3.0
			
			if GapValue < hueRangeGap:
				hueMax = hueMax + ((hueMid - hueMax) / 2)
				hueMin = hueMin - ((hueMin - hueMid) / 2)
			
			#make frame sheet
			cmds.scrollLayout(('prLogScroll__' + prLogName + '__' + layer), cr= 1, p= prLogTabForm)
			cmds.formLayout(('prLogFormForFrame__' + prLogName + '__' + layer), p= ('prLogScroll__' + prLogName + '__' + layer))
			topPos = 0
			for frameData in prLogDataSplit:
				frameNum = frameData.split('=')[0]
				floatTime = float(frameData.split('=')[1].split('$')[0])
				frameTime = dataGetFormat.dp_getFormattedRenderTime(floatTime, 0)
				vrayDRNum = int(frameData.split('=')[1].split('$')[1])
				vrayDRStr = str(vrayDRNum) + ' slave' + ('s' if vrayDRNum > 1 else '')
				# get Frame color and set frameLayout
				hueValue = hueMid
				if floatTime > MidValue:
					if floatTime / MidValue >= scaleGate:
						hueValue = hueMax
					else:
						hueValue = hueMid - ((hueMid - hueMax) * (((floatTime / MidValue) - 1) / (scaleGate - 1)))
						if hueValue < hueMax:
							hueValue = hueMax
				if floatTime < MidValue:
					if MidValue / floatTime >= scaleGate:
						hueValue = hueMin
					else:
						hueValue = hueMin - ((hueMin - hueMid) * (((scaleGate - 1) / (MidValue / floatTime) - 1)))
						if hueValue > hueMin:
							hueValue = hueMin

				RGB = mel.eval('hsv_to_rgb <<' + str(hueValue) + ', 1.0, 0.5>>')
				# frame's frameLayout
				textName = 'prLogFrame__' + prLogName + '__' + layer + str(int(float(frameNum)))
				infoLabel = ' #' + frameNum.ljust(8) + vrayDRStr.rjust(12) + frameTime.rjust(12) + ' '
				cmds.text(textName, l= infoLabel, al= 'center', fn= 'smallFixedWidthFont', h= 20, bgc= [RGB[0], RGB[1], RGB[2]], p= ('prLogFormForFrame__' + prLogName + '__' + layer))
				cmds.formLayout(('prLogFormForFrame__' + prLogName + '__' + layer), e= 1, af= [(textName, 'top', topPos), (textName, 'left', 0), (textName, 'right', 0)])
				topPos += 20

			global dp_Rendering
			if prLogDataSplit == [] and dp_Rendering:
				frameNum = str(cmds.currentTime(q= 1) - 1) # vray jump 1 frame?
				textName = 'prLogFrame__' + prLogName + '__' + layer + str(int(float(frameNum)))
				infoLabel = ' #' + frameNum.ljust(8) + 'Rendering...'.rjust(12) + '--:--:--'.rjust(12) + ' '
				cmds.text(textName, l= infoLabel, al= 'center', fn= 'smallFixedWidthFont', h= 20, bgc= [.1, .1, .1], p= ('prLogFormForFrame__' + prLogName + '__' + layer))
				cmds.formLayout(('prLogFormForFrame__' + prLogName + '__' + layer), e= 1, af= [(textName, 'top', topPos), (textName, 'left', 0), (textName, 'right', 0)])


			if set_QtStyle:
				UI_Controls.dp_makePySideUI('prLogScroll__' + prLogName + '__' + layer, 'QLabel {color: Silver}')

			cmds.formLayout(prLogTabForm, e= 1, af= [(('prLogScroll__' + prLogName + '__' + layer), 'top', 115), (('prLogScroll__' + prLogName + '__' + layer), 'bottom', 0),
													 (('prLogScroll__' + prLogName + '__' + layer), 'left', 0), (('prLogScroll__' + prLogName + '__' + layer), 'right', 0)])


	def dp_layerMenuToRenderLog(self, *args):

		layer = cmds.optionMenu('layerMenu', q= 1, v= 1)
		if layer != 'No Renderable Layer':
			if layer == 'masterLayer': layer = 'defaultRenderLayer'
			self.dp_timeLogWindow(layer)





class UI_Controls:


	def dp_animationOnOffStatus(self):

		cmds.checkBox('animChk', e= 1, v= cmds.getAttr('defaultRenderGlobals.animation'))


	def dp_getRendererName(self):

		def dp_rendName_InfoFormat(qType):
	
			if cmds.getAttr('defaultRenderGlobals.currentRenderer') == 'mentalRay' :
				if qType == 'name' : return 'Mental Ray'
				if qType == 'space' : return '56'
			elif cmds.getAttr('defaultRenderGlobals.currentRenderer') == 'mayaVector' :
				if qType == 'name' : return 'Maya Vector'
				if qType == 'space' : return '53'
			elif cmds.getAttr('defaultRenderGlobals.currentRenderer') == 'mayaHardware2' :
				if qType == 'name' : return 'Maya Hardware 2.0'
				if qType == 'space' : return '36'
			elif cmds.getAttr('defaultRenderGlobals.currentRenderer') == 'mayaHardware' :
				if qType == 'name' : return 'Maya Hardware'
				if qType == 'space' : return '47'
			elif cmds.getAttr('defaultRenderGlobals.currentRenderer') == 'mayaSoftware' :
				if qType == 'name' : return 'Maya Software'
				if qType == 'space' : return '48'
			elif cmds.getAttr('defaultRenderGlobals.currentRenderer') == 'vray' :
				if qType == 'name' : return 'V-Ray'
				if qType == 'space' : return '74'
			elif cmds.getAttr('defaultRenderGlobals.currentRenderer') == 'arnold' :
				if qType == 'name' : return 'Arnold'
				if qType == 'space' : return '71'
			else :
				if qType == 'name' : return 'my Render'
				if qType == 'space' : return '59'

		cmds.frameLayout('rendFrame', e= 1, l= dp_rendName_InfoFormat('name'), li= int(dp_rendName_InfoFormat('space')))


	def dp_layerMenuSync(self, *args):

		# get current layer, direct using pyhton cmd when sceneQueue changing file will cause error, reason unknow.
		try:
			currentLayer = cmds.editRenderLayerGlobals(q= 1, currentRenderLayer= 1)
		except:
			currentLayer = mel.eval('editRenderLayerGlobals -q -currentRenderLayer')
		
		try:
			cmds.optionMenu('layerMenu', e= 1, v= currentLayer if currentLayer != 'defaultRenderLayer' else 'masterLayer')
		except:
			pass

		if cmds.optionMenu('layerMenu', q= 1, v= 1) == 'masterLayer': cmds.iconTextButton('overriBtn', e= 1, image= 'overrideSettings_dim.png')
		
		self.dp_rangeCtrlGetLayerAttr()


	def dp_changeAnimationStatus(self, *args):
		
		cmds.setAttr('defaultRenderGlobals.animation', cmds.checkBox('animChk', q= 1, v= 1))


	def dp_changeResolution(self, *args):

		resVar = cmds.optionMenu('ResMenu', q= 1, v= 1).strip()
		resMut = 1
		if resVar == 'Camera Panel':
			mel.eval('setTestResolutionVar(0)')
			resMut = 0
		elif resVar == 'Render Settings':
			mel.eval('setTestResolutionVar(1)')
		elif resVar == '10% Settings':
			mel.eval('setTestResolutionVar(2)')
			resMut = 0.1
		elif resVar == '25% Settings':
			mel.eval('setTestResolutionVar(3)')
			resMut = 0.25
		elif resVar == '50% Settings':
			mel.eval('setTestResolutionVar(4)')
			resMut = 0.5
		elif resVar == '75% Settings':
			mel.eval('setTestResolutionVar(5)')
			resMut = 0.75
		elif resVar == '110% Settings':
			mel.eval('setTestResolutionVar(6)')
			resMut = 1.1
		elif resVar == '125% Settings':
			mel.eval('setTestResolutionVar(7)')
			resMut = 1.25
		elif resVar == '150% Settings':
			mel.eval('setTestResolutionVar(8)')
			resMut = 1.5
		else:
			mel.eval('setTestResolutionVar(1)')

		if cmds.attributeQuery('dp_userAttr_Resolution', node= 'defaultRenderLayer', ex= 1):
			cmds.setAttr(('defaultRenderLayer.dp_userAttr_Resolution'), cmds.optionMenu('ResMenu', q= 1, v= 1), type= 'string')
		else:
			cmds.addAttr('defaultRenderLayer', ln= 'dp_userAttr_Resolution', dt= 'string', h= 1)
			cmds.setAttr(('defaultRenderLayer.dp_userAttr_Resolution'), cmds.optionMenu('ResMenu', q= 1, v= 1), type= 'string')

		cmds.text('ResTextB', e= 1, bgc= [0.3, 0.4, 0.1] if resMut != 1 else [0.1, 0.1, 0.1])
		cmds.text('ResTextW', e= 1, l= str(int(cmds.getAttr('defaultResolution.width') * resMut)))
		cmds.text('ResTextH', e= 1, l= str(int(cmds.getAttr('defaultResolution.height') * resMut)))


	def dp_changeCustomFrame(self, layer, currentLayer, *args):
		# input custom range data
		#
		if currentLayer:
			layer = cmds.optionMenu('layerMenu', q= 1, v= 1)
			if layer == 'No Renderable Layer': layer = 'masterLayer'
			layer = 'defaultRenderLayer' if layer == 'masterLayer' else layer

		# if customFrameRange field has data, disable frame range field
		if dataGetFormat.dp_checkCustomFrameRangeInputFormat():
			en = 0
			if cmds.textField('custmTxtF', q= 1, text= 1):
				if not cmds.attributeQuery('dp_userAttr_customFrameRange', node= layer, ex= 1):
					cmds.addAttr(layer, ln= 'dp_userAttr_customFrameRange', dt= 'string', h= 1)
				cmds.setAttr((layer + '.dp_userAttr_customFrameRange'), cmds.textField('custmTxtF', q= 1, text= 1), type= 'string')
			else:
				en = 1
			cmds.floatField('strFrmFfd', e= 1, en= en)
			cmds.floatField('endFrmFfd', e= 1, en= en)
			cmds.floatField('stpFrmFfd', e= 1, en= en)
			cmds.text('strFrmTxt', e= 1, en= en)
			cmds.text('endFrmTxt', e= 1, en= en)
			cmds.text('stpFrmTxt', e= 1, en= en)
			return 1
		else:
			return 0


	def dp_changeCustomFrameAll(self, *args):
		
		for layer in cmds.ls(et= 'renderLayer'):
			if cmds.getAttr(layer + '.renderable'):
				if not self.dp_changeCustomFrame(layer, 0):
					break


	def dp_changeLayerProgressOrder(self, direction, *args):

		def dp_moveLayerProgressCtrls(layer, proBarTop, proTxtTop):
		
			#render star *
			cmds.formLayout('jobsProForm', e= 1, af= [((layer + 'ProStar'), 'top', (proBarTop + 5))])
			#layer name
			cmds.formLayout('jobsProForm', e= 1, af= [((layer + 'ProTxtName'), 'top', proBarTop - 2)])
			#radioButton
			cmds.formLayout('jobsProForm', e= 1, af= [((layer + 'RadioBn'), 'top', (proBarTop + 2))])
			#current frame
			cmds.formLayout('jobsProForm', e= 1, af= [((layer + 'ProCurrFrame'), 'top', (proTxtTop - 7))])
			#last frame time
			cmds.formLayout('jobsProForm', e= 1, af= [((layer + 'lastFrameTime'), 'top', (proTxtTop + 3))])
			#elapsed time
			cmds.formLayout('jobsProForm', e= 1, af= [((layer + 'elapsedTime'), 'top', proTxtTop)])
			#layer frame sum
			cmds.formLayout('jobsProForm', e= 1, af= [((layer + 'ProTxtNum'), 'top', proTxtTop)])
			#slash
			cmds.formLayout('jobsProForm', e= 1, af= [((layer + 'ProTxtSlash'), 'top', proTxtTop)])
			#layer render status
			cmds.formLayout('jobsProForm', e= 1, af= [((layer + 'ProTxtStatus'), 'top', proTxtTop)])
			#layer start frame
			cmds.formLayout('jobsProForm', e= 1, af= [((layer + 'ProTxtStart'), 'top', proTxtTop)])
			#layer end frame
			cmds.formLayout('jobsProForm', e= 1, af= [((layer + 'ProTxtEnd'), 'top', proTxtTop)])
			#progressBar
			cmds.formLayout('jobsProForm', e= 1, af= [((layer + 'ProBar'), 'top', proBarTop + 1)])
			#folder link
			cmds.formLayout('jobsProForm', e= 1, af= [((layer + 'folderBtn'), 'top', proBarTop - 4)])
			#rendering time sheet
			cmds.formLayout('jobsProForm', e= 1, af= [((layer + 'timeShBtn'), 'top', (proBarTop - 18))])

		
		global renderMissionLayerSort

		radioButtonSelected = cmds.radioCollection('layerCollection', q= 1, sl= 1)
		layerToMove = renderMissionLayerSort.index(radioButtonSelected.split('RadioBn')[0])

		proBarTop = 25
		proTxtTop = 10
		proBarTopGap = 45

		if direction == 'UP':
			if layerToMove > 0:
				proBarTopFix = proBarTop + (proBarTopGap * (layerToMove - 1))
				proTxtTopFix = proTxtTop + (proBarTopGap * (layerToMove - 1))
				dp_moveLayerProgressCtrls(renderMissionLayerSort[layerToMove], proBarTopFix, proTxtTopFix)
				proBarTopFix = proBarTop + (proBarTopGap * layerToMove)
				proTxtTopFix = proTxtTop + (proBarTopGap * layerToMove)
				dp_moveLayerProgressCtrls(renderMissionLayerSort[layerToMove - 1], proBarTopFix, proTxtTopFix)

				renderMissionLayerSort.insert((layerToMove - 1) ,renderMissionLayerSort.pop(layerToMove))

		if direction == 'DOWN':
			if layerToMove < len(renderMissionLayerSort) - 1:
				proBarTopFix = proBarTop + (proBarTopGap * (layerToMove + 1))
				proTxtTopFix = proTxtTop + (proBarTopGap * (layerToMove + 1))
				dp_moveLayerProgressCtrls(renderMissionLayerSort[layerToMove], proBarTopFix, proTxtTopFix)
				proBarTopFix = proBarTop + (proBarTopGap * layerToMove)
				proTxtTopFix = proTxtTop + (proBarTopGap * layerToMove)
				dp_moveLayerProgressCtrls(renderMissionLayerSort[layerToMove + 1], proBarTopFix, proTxtTopFix)

				renderMissionLayerSort.insert((layerToMove + 1) ,renderMissionLayerSort.pop(layerToMove))

		for count, layer in enumerate(renderMissionLayerSort):
			if not cmds.attributeQuery('dp_userAttr_renderOrder', node= layer, ex= 1):
				cmds.addAttr(layer, ln= 'dp_userAttr_renderOrder', at= 'long', h= 1)
			cmds.setAttr(layer + '.dp_userAttr_renderOrder', count)


	def dp_changeFramePrioStatus(self, *args):

		if cmds.attributeQuery('dp_userAttr_FramePrio', node= 'defaultRenderLayer', ex= 1):
			cmds.setAttr(('defaultRenderLayer.dp_userAttr_FramePrio'), cmds.checkBox('fProChk', q= 1, v= 1))
		else:
			cmds.addAttr('defaultRenderLayer', ln= 'dp_userAttr_FramePrio', at= 'bool', h= 1)
			cmds.setAttr(('defaultRenderLayer.dp_userAttr_FramePrio'), cmds.checkBox('fProChk', q= 1, v= 1))

		self.dp_GlobalBackwardInFramePrio()


	def dp_changeBackwardStatus(self, *args):
		
		if not cmds.checkBox('fProChk', q= 1, v= 1):
			layer = cmds.optionMenu('layerMenu', q= 1, v= 1)
			if layer == 'No Renderable Layer': layer = 'masterLayer'
			layer = 'defaultRenderLayer' if layer == 'masterLayer' else layer
			if cmds.attributeQuery('dp_userAttr_backward', node= layer, ex= 1):
				cmds.setAttr((layer + '.dp_userAttr_backward'), cmds.checkBox('backChk', q= 1, v= 1))
			else:
				cmds.addAttr(layer, ln= 'dp_userAttr_backward', at= 'bool', h= 1)
				cmds.setAttr((layer + '.dp_userAttr_backward'), 1)
		else:
			if cmds.attributeQuery('dp_userAttr_backwardInFramePrio', node= 'defaultRenderLayer', ex= 1):
				cmds.setAttr(('defaultRenderLayer.dp_userAttr_backwardInFramePrio'), cmds.checkBox('backChk', q= 1, v= 1))
			else:
				cmds.addAttr('defaultRenderLayer', ln= 'dp_userAttr_backwardInFramePrio', at= 'bool', h= 1)
				cmds.setAttr(('defaultRenderLayer.dp_userAttr_backwardInFramePrio'), 1)

	
	def dp_changeDeleteJobStatus(self, *args):

		if cmds.attributeQuery('dp_userAttr_DeleteJobs', node= 'defaultRenderLayer', ex= 1):
			cmds.setAttr(('defaultRenderLayer.dp_userAttr_DeleteJobs'), cmds.checkBox('delJChk', q= 1, v= 1))
		else:
			cmds.addAttr('defaultRenderLayer', ln= 'dp_userAttr_DeleteJobs', at= 'bool', h= 1)
			cmds.setAttr(('defaultRenderLayer.dp_userAttr_DeleteJobs'), cmds.checkBox('delJChk', q= 1, v= 1))


	def dp_init_DeleteJobs(self):

		if cmds.attributeQuery('dp_userAttr_DeleteJobs', node= 'defaultRenderLayer', ex= 1):
			cmds.checkBox('delJChk', e= 1, v= cmds.getAttr('defaultRenderLayer.dp_userAttr_DeleteJobs'))
		else:
			cmds.checkBox('delJChk', e= 1, v= 0)


	def dp_init_Resolution(self):

		setDefaultRes = 1
		if cmds.attributeQuery('dp_userAttr_Resolution', node= 'defaultRenderLayer', ex= 1):
			res = cmds.getAttr('defaultRenderLayer.dp_userAttr_Resolution')
			if res and res != 'Render Settings':
				cmds.optionMenu('ResMenu',e= 1, v= res)
				self.dp_changeResolution()
				setDefaultRes = 0
		if setDefaultRes:
			cmds.optionMenu('ResMenu',e= 1, v= 'Render Settings')
			mel.eval('setTestResolutionVar(1)')
			cmds.text('ResTextB', e= 1, bgc= [0.1, 0.1, 0.1])
			cmds.text('ResTextW', e= 1, l= str(cmds.getAttr('defaultResolution.width')))
			cmds.text('ResTextH', e= 1, l= str(cmds.getAttr('defaultResolution.height')))


	def dp_init_Backward_FramePrio(self):
		
		if cmds.attributeQuery('dp_userAttr_FramePrio', node= 'defaultRenderLayer', ex= 1):
			cmds.checkBox('fProChk', e= 1, v= cmds.getAttr('defaultRenderLayer.dp_userAttr_FramePrio'))
		else:
			cmds.checkBox('fProChk', e= 1, v= 0)

		self.dp_GlobalBackwardInFramePrio()


	def dp_layerRenderableTracker(self, layerOldName):

		global unRenderableLayers

		try:
			layer = cmds.undoInfo(q= 1, un= 1).split()[-2].split('"')[1]
			value = cmds.undoInfo(q= 1, un= 1).split()[-1].split('"')[1]
		except:
			layer = 'defaultRenderLayer' if cmds.optionMenu('layerMenu', q= 1, v= 1) == 'masterLayer' else cmds.optionMenu('layerMenu', q= 1, v= 1)
			value = cmds.getAttr(layer + '.renderable')
			if 'layerMenuItem_' + layer in cmds.optionMenu('layerMenu', q=1, ils= 1):
				cmds.deleteUI('layerMenuItem_' + layer)
			if cmds.optionMenu('layerMenu', q= 1, ni= 1) == 0:
				cmds.menuItem('layerMenuItem_NoRenderableLayer', l= 'No Renderable Layer', p= 'layerMenu')
				cmds.optionMenu('layerMenu', e= 1, en= 0)

		if int(value):
			if cmds.optionMenu('layerMenu', q= 1, v= 1) == 'No Renderable Layer':
				cmds.deleteUI('layerMenuItem_NoRenderableLayer')
				cmds.optionMenu('layerMenu', e= 1, en= 1)
			if layer in unRenderableLayers: unRenderableLayers.remove(layer)
			cmds.menuItem('layerMenuItem_' + layer, l= layer if layer != 'defaultRenderLayer' else 'masterLayer', p= 'layerMenu')
			if layer != 'defaultRenderLayer':
				cmds.scriptJob(ro= 1, ac= [layer + '.renderable', partial(self.dp_layerRenderableTracker, layer)], p= 'layerMenuItem_' + layer)
				cmds.scriptJob(nodeNameChanged= [layer, partial(self.dp_layerReNameTracker, layer)], p= 'layerMenuItem_' + layer)
			if layer == cmds.editRenderLayerGlobals(q= 1, currentRenderLayer= 1):
				cmds.optionMenu('layerMenu', e= 1, v= layer if layer != 'defaultRenderLayer' else 'masterLayer')
		else:
			cmds.deleteUI('layerMenuItem_' + layerOldName)
			if layer not in unRenderableLayers: unRenderableLayers.append(layer)
			if layer != 'defaultRenderLayer':
				cmds.scriptJob(ro= 1, ac= [layer + '.renderable', partial(self.dp_layerRenderableTracker, layer)], p= 'domino_mainUI')
			if cmds.optionMenu('layerMenu', q= 1, ni= 1) == 0:
				cmds.menuItem('layerMenuItem_NoRenderableLayer', l= 'No Renderable Layer', p= 'layerMenu')
				cmds.optionMenu('layerMenu', e= 1, en= 0)

		self.dp_layerMenuSync()


	def dp_layerReNameTracker(self, layerOldName):

		layer = cmds.undoInfo(q= 1, un= 1).split()[-1].split('"')[1]
		cmds.menuItem('layerMenuItem_' + layerOldName, e= 1, l= layer)


	def dp_refreshLayerMenu(self, *args):

		global unRenderableLayers
		
		# if I don't print something, scriptJob [renderLayerChange] may not work sometimes, ex: deleting the only (v)renderLayer except (x)masterLayer 
		print 'dp_Domino: Refreshing layer optionMenu...'

		if cmds.optionMenu('layerMenu',q= 1, ni= 1):
			for item in cmds.optionMenu('layerMenu', q= 1, ils= 1):
				cmds.deleteUI(item)

		for layer in cmds.ls(et= 'renderLayer'):
			if cmds.getAttr(layer + '.renderable'):
				if layer in unRenderableLayers: unRenderableLayers.remove(layer)
				cmds.menuItem('layerMenuItem_' + layer, l= layer if layer != 'defaultRenderLayer' else 'masterLayer', p= 'layerMenu')
				if layer != 'defaultRenderLayer':
					cmds.scriptJob(ro= 1, ac= [layer + '.renderable', partial(self.dp_layerRenderableTracker, layer)], p= 'layerMenuItem_' + layer)
					cmds.scriptJob(nodeNameChanged= [layer, partial(self.dp_layerReNameTracker, layer)], p= 'layerMenuItem_' + layer)
			else:
				if layer not in unRenderableLayers: unRenderableLayers.append(layer)
				if layer != 'defaultRenderLayer':
					cmds.scriptJob(ro= 1, ac= [layer + '.renderable', partial(self.dp_layerRenderableTracker, layer)], p= 'domino_mainUI')

		currentLayer = cmds.editRenderLayerGlobals(q= 1, currentRenderLayer= 1)
		if cmds.optionMenu('layerMenu', q= 1, ni= 1):
			if 'layerMenuItem_' + currentLayer in cmds.optionMenu('layerMenu', q= 1, ils= 1):
				cmds.optionMenu('layerMenu', e= 1, v= currentLayer if currentLayer != 'defaultRenderLayer' else 'masterLayer')
			cmds.optionMenu('layerMenu', e= 1, en= 1)
		else:
			cmds.menuItem('layerMenuItem_NoRenderableLayer', l= 'No Renderable Layer', p= 'layerMenu')
			cmds.optionMenu('layerMenu', e= 1, en= 0)

		self.dp_layerMenuSync()


	def dp_GlobalBackwardInFramePrio(self):

		layer = cmds.optionMenu('layerMenu', q= 1, v= 1)
		if layer == 'No Renderable Layer': layer = 'masterLayer'
		layer = 'defaultRenderLayer' if layer == 'masterLayer' else layer
		
		if not cmds.checkBox('fProChk', q= 1, v= 1):
			cmds.text('gBackMk', e= 1, vis= 0)
			if cmds.attributeQuery('dp_userAttr_backward', node= layer, ex= 1):
				cmds.checkBox('backChk', e= 1, v= cmds.getAttr(layer + '.dp_userAttr_backward'))
			else:
				cmds.checkBox('backChk', e= 1, v= 0)
		else:
			cmds.text('gBackMk', e= 1, vis= 1)
			if cmds.attributeQuery('dp_userAttr_backwardInFramePrio', node= 'defaultRenderLayer', ex= 1):
				cmds.checkBox('backChk', e= 1, v= cmds.getAttr('defaultRenderLayer.dp_userAttr_backwardInFramePrio'))
			else:
				cmds.checkBox('backChk', e= 1, v= 0)


	def dp_clearAllCustomFrameData(self, clearAll, *args):

		if clearAll:
			for layer in cmds.ls(et= 'renderLayer'):
				if cmds.attributeQuery('dp_userAttr_customFrameRange', node= layer, ex= 1):
					cmds.deleteAttr(layer, at= 'dp_userAttr_customFrameRange')
		else:
			layer = cmds.optionMenu('layerMenu', q= 1, v= 1)
			if layer == 'No Renderable Layer': layer = 'masterLayer'
			layer = 'defaultRenderLayer' if layer == 'masterLayer' else layer
			if cmds.attributeQuery('dp_userAttr_customFrameRange', node= layer, ex= 1):
				cmds.deleteAttr(layer, at= 'dp_userAttr_customFrameRange')

		cmds.textField('custmTxtF', e= 1, text= '')

		cmds.floatField('strFrmFfd', e= 1, en= 1)
		cmds.floatField('endFrmFfd', e= 1, en= 1)
		cmds.floatField('stpFrmFfd', e= 1, en= 1)
		cmds.text('strFrmTxt', e= 1, en= 1)
		cmds.text('endFrmTxt', e= 1, en= 1)
		cmds.text('stpFrmTxt', e= 1, en= 1)


	def dp_openImageFolder(self, layer, *args):
		
		filePath = []
		imgPrefix = ''

		if layer != '__imgRoot__':

			currentRenderer = commonTool.dp_getOverrideData('defaultRenderGlobals.currentRenderer', layer)

			if currentRenderer == 'vray':
				imgPrefix = commonTool.dp_getOverrideData('vraySettings.fileNamePrefix', layer)
			else:
				imgPrefix = commonTool.dp_getOverrideData('defaultRenderGlobals.imageFilePrefix', layer)
			tmpPrefix = cmds.getAttr('defaultRenderGlobals.imageFilePrefix')
			if imgPrefix:
				cmds.setAttr('defaultRenderGlobals.imageFilePrefix', imgPrefix, type= 'string')
			if currentRenderer == 'vray':
				filePath = cmds.renderSettings(lyr= layer, fp= 1, fin= 1)
			else:
				#maya renderer storage images in tmp folder
				filePath = cmds.renderSettings(lyr= layer, fpt= 1, fin= 1)
			if tmpPrefix:
				cmds.setAttr('defaultRenderGlobals.imageFilePrefix', tmpPrefix, type= 'string')
		
		path = os.path.dirname(filePath[0]) if layer != '__imgRoot__' else cmds.workspace(q= 1, rd= 1) + cmds.workspace("images", q= 1, fre= 1)

		try:
			if cmds.file(path, q= 1, ex= 1):
				path = os.path.normcase(path)
				if platform.system() == 'Windows':
					subprocess.Popen(['explorer', path])
				elif platform.system() == 'Darwin':
					subprocess.Popen(['open', path])
				else:
					subprocess.Popen(['xdg-open', path])
		except:
			cmds.error('dp_Domino: Sorry, the image folder link is not support your OS yet. Please contact me.')


	def dp_openRenderView(self):

		if cmds.getAttr('defaultRenderGlobals.currentRenderer') != 'vray':
			mel.eval("RenderViewWindow;")
		else:
			mel.eval("vray showVFB;")


	def dp_logTabSaveOrRename(self, layer, *args):

		global dp_Rendering
		global renderStartDate
		attrName = ''
		if 'renderStartDate' in globals():
			attrName = 'dp_userAttr_timeLog_' + ''.join(renderStartDate.split(' ')[3].split('/')) + ''.join(renderStartDate.split(' ')[5].split(':'))

		if not dp_Rendering:

			tabIndex = cmds.tabLayout('prLogTab', q= 1, sti= 1)
			tabName = cmds.tabLayout('prLogTab', q= 1, tabLabel = 1)[tabIndex - 1]

			if tabName.endswith('*'):
				#save function tab
				if not cmds.attributeQuery(attrName, node= layer, ex= 1) and attrName:
					self.dp_logSaving(layer, attrName)
					#remove unsaved mark '*'
					cmds.tabLayout('prLogTab', e= 1, tabLabel= [(('prLogForm__' + 'dp_userAttr_timeLog_Tmp__' + layer), tabName.split('*')[0])])
			else:
				#give a new name
				rename = cmds.promptDialog(
						title= 'Name this renderAction',
						message= 'Enter Name:',
						button= ['OK', 'Cancel'],
						defaultButton= 'OK',
						cancelButton= 'Cancel',
						dismissString= 'Cancel')

				newName = cmds.promptDialog(q= 1, text= 1) if rename == 'OK' else ''
				if newName:
					forbidden = u'!"#%\'()*+,-./:;<=>?@[\]^_`{|}~'
					trantab = dict((ord(char), u'_') for char in forbidden)
					newName = newName.translate(trantab)
					prLogName = cmds.tabLayout('prLogTab', q= 1, st= 1).split('__')[1]
					if prLogName == 'dp_userAttr_timeLog_Tmp':
						prLogName = attrName
					if not cmds.attributeQuery(prLogName + '_tabLabel', node= layer, ex= 1):
						cmds.addAttr(layer, ln= prLogName + '_tabLabel', dt= 'string', h= 1)
					else:
						tabName = cmds.getAttr(layer + '.' + prLogName + '_tabLabel').split('@')[1]
					cmds.setAttr(layer + '.' + prLogName + '_tabLabel', newName + '@' + tabName, type= 'string')
					cmds.tabLayout('prLogTab', e= 1, tabLabel= [(cmds.tabLayout('prLogTab', q= 1, st= 1), newName)])


	def dp_logTabDelete(self, layer, *args):

		#delete function tab
		uiName = cmds.tabLayout('prLogTab', q= 1, st= 1)
		prLogName = uiName.split('__')[1]
		if cmds.attributeQuery(prLogName + '_tabLabel', node= layer, ex= 1):
			cmds.deleteAttr(layer, at= prLogName + '_tabLabel')
		if cmds.attributeQuery(prLogName, node= layer, ex= 1):
			cmds.deleteAttr(layer, at= prLogName)
		if cmds.attributeQuery('dp_userAttr_logList', node= layer, ex= 1):
			logList = cmds.getAttr(layer + '.dp_userAttr_logList').split(',')
			logList.remove(prLogName)
			cmds.setAttr((layer + '.dp_userAttr_logList'), (','.join(logList)), type= 'string')
		#check if any tabs still there
		isTabs = cmds.tabLayout('prLogTab', q= 1, tabLabel = 1)
		if len(isTabs) > 1:
			cmds.deleteUI(uiName)
		else:
			cmds.window('domino_timeLogUI', e= 1, vis= 0)


	def dp_logSaving(self, layer, attrName):

		tmpLogData = ''
		if cmds.attributeQuery('dp_userAttr_timeLog_Tmp', node= layer, ex= 1):
			tmpLogData = cmds.getAttr(layer + '.dp_userAttr_timeLog_Tmp')
		cmds.addAttr(layer, ln= attrName, dt= 'string', h= 1)
		cmds.setAttr(layer + '.' + attrName, tmpLogData, type= 'string')
		cmds.setAttr(layer + '.' + 'dp_userAttr_timeLog_Tmp', 'saved', type= 'string')
		#add attrLogName into logList
		if cmds.attributeQuery('dp_userAttr_logList', node= layer, ex= 1):
			otherAttrName = cmds.getAttr(layer + '.dp_userAttr_logList')
			attrName = attrName + ',' + (otherAttrName if otherAttrName else '') # <otherAttrName> might get NoneType
			cmds.setAttr((layer + '.dp_userAttr_logList'), attrName, type= 'string')
		else:
			cmds.addAttr(layer, ln= 'dp_userAttr_logList', dt= 'string', h= 1)
			cmds.setAttr((layer + '.dp_userAttr_logList'), attrName, type= 'string')


	def dp_findAverageRenderTime(self, timeSheet):

		timeSheet.sort()
		
		# get all frames renderTime Average
		meanValue = sum(timeSheet) / len(timeSheet)

		timeAvgGap = []
		for time in timeSheet:
			timeAvgGap.append(time - meanValue)

		timeAvgGapPow = []
		for timeGap in timeAvgGap:
			timeAvgGapPow.append(math.pow(timeGap, 2))

		stDev = math.sqrt(sum(timeAvgGapPow) / len(timeAvgGapPow))

		timeSheetTMP = []
		timeSheetTMP.extend(timeSheet)
		timeSheet.reverse()
		for time in timeSheet:
			if time > (meanValue + stDev):
				timeSheetTMP.pop()
			else:
				break
		timeSheetTMP.reverse()
		timeSheet.reverse()
		for time in timeSheet:
			if time < (meanValue - stDev):
				timeSheetTMP.pop()
			else:
				break

		superAvg = sum(timeSheetTMP) / len(timeSheetTMP)

		return superAvg


	def dp_sceneQueueAction(self, action, *args):

		if cmds.textScrollList('fileScrollList', q= 1, ni= 1) > 0 or action == 'add':
			if cmds.textScrollList('fileScrollList', q= 1, ni= 1) > 0 and cmds.file(q= 1, sn= 1, shn= 1):
				cmds.textScrollList('fileScrollList', e= 1, dii= 1)
			slIndex = cmds.textScrollList('fileScrollList', q= 1, sii= 1)
			queueTail = cmds.textScrollList('fileScrollList', q= 1, ni= 1)
			if action == 'add':
				multipleFilters = 'Maya Files (*.ma *.mb);;Maya ASCII (*.ma);;Maya Binary (*.mb);;All Files (*.*)'
				scenePath = cmds.fileDialog2(ff= multipleFilters, dir= cmds.workspace(q= 1, dir= 1), ds=2, fm=1)
				scene = os.path.basename(scenePath[0]) if scenePath else ''
				if scene:
					try:
						#maya2014
						cmds.textScrollList('fileScrollList', e= 1, a= scene, utg= scenePath, da= 1, si= scene)
						#cmds.textScrollList('fileScrollList', e= 1, a= scene, da= 1, si= scene)
					except:
						# normally, you get here by error with double scene in queue
						cmds.textScrollList('fileScrollList', e= 1, da= 1, si= scene)

			if action == 'delete' and slIndex:
				for idx in slIndex:
					cmds.textScrollList('fileScrollList', e= 1, rii= idx)
					for i in slIndex:
						if i != idx:
							slIndex[slIndex.index(i)] = i - 1

			if 'move' in action and slIndex:
				slItems = cmds.textScrollList('fileScrollList', q= 1, si= 1)
				slUQtag = cmds.textScrollList('fileScrollList', q= 1, sut= 1)
				self.dp_sceneQueueAction('delete')
				if action == 'moveUP':
					for i in slIndex:
						if slIndex.index(i) == 0:
							topLimit = 2 if cmds.file(q= 1, sn= 1, shn= 1) else 1
							slIndex[0] = slIndex[0] - 1 if slIndex[0] > topLimit else topLimit
							i = slIndex[0]
						slIndex[slIndex.index(i)] = slIndex[0] + slIndex.index(i)

				if action == 'moveDown':
					slIndex.reverse()
					for i in slIndex:
						if slIndex.index(i) == 0:
							slIndex[0] = slIndex[0] + 1 if slIndex[0] < queueTail else queueTail
							i = slIndex[0]
						slIndex[slIndex.index(i)] = slIndex[0] - slIndex.index(i)
					slIndex.reverse()
				
				for i in range(len(slIndex)):
					#maya2014
					cmds.textScrollList('fileScrollList', e= 1, ap= [slIndex[i], slItems[i]], utg= slUQtag[i], si= slItems[i])
					#cmds.textScrollList('fileScrollList', e= 1, ap= [slIndex[i], slItems[i]], si= slItems[i])
		else:
			if action == 'addCurrentScene':
				if cmds.file(q= 1, sn= 1):
					currentScenePath = cmds.file(q= 1, sn= 1)
					currentScene = os.path.basename(currentScenePath)
					#maya2014
					cmds.textScrollList('fileScrollList', e= 1, a= currentScene, utg= currentScenePath)
					#cmds.textScrollList('fileScrollList', e= 1, a= currentScene)


	def dp_lockUIControls(self, en):

		cmds.checkBox('backChk', e= 1, en= en)
		cmds.checkBox('fProChk', e= 1, en= en)
		cmds.checkBox('animChk', e= 1, en= en)
		cmds.optionMenu('ResMenu', e= 1, en= en)
		cmds.frameLayout('rangeFrame', e= 1, en= en)
		cmds.textScrollList('fileScrollList', e= 1, en= en)
		cmds.button('fileDelBtn', e= 1, en= en)
		cmds.iconTextButton('fileUpArrowBtn', e= 1, en= en)
		cmds.iconTextButton('fileDownArrowBtn', e= 1, en= en)


	def dp_frameRangePopupMenuPostCmd(self, attrName, textName, *args):

		layer = cmds.optionMenu('layerMenu', q= 1, v= 1)
		if layer == 'No Renderable Layer': layer = 'masterLayer'
		if layer != 'masterLayer':
			cmds.popupMenu(attrName.split('.')[1] + '_popupMenu', e= 1, dai= 1)
			if commonTool.dp_hasOverride(attrName, layer):
				cmds.menuItem(l= 'Remove Layer Override', c= partial(self.dp_frameRangeMenuItemCmd, attrName, textName, layer, 1), p= attrName.split('.')[1] + '_popupMenu')
			else:
				cmds.menuItem(l= 'Create Layer Override', c= partial(self.dp_frameRangeMenuItemCmd, attrName, textName, layer, 0), p= attrName.split('.')[1] + '_popupMenu')


	def dp_frameRangeMenuItemCmd(self, attrName, textName, layer, remove, *args):

		if remove:
			cmds.editRenderLayerAdjustment(attrName, lyr= layer, r= 1)
			self.dp_tintOverrideColor(textName, 0)
		else:
			cmds.editRenderLayerAdjustment(attrName, lyr= layer)
			self.dp_tintOverrideColor(textName, 1)


	def dp_tintOverrideColor(self, textName, tint, *args):

		#pySide
		if tint:
			if textName == 'renumFTxt': cmds.text('renumFTxt', e= 1, fn= 'boldLabelFont')
			if set_QtStyle:
				self.dp_makePySideUI(textName, 'QLabel {color: Chocolate}')
			else:
				pass
		else:
			if textName == 'renumFTxt': cmds.text('renumFTxt', e= 1, fn= 'plainLabelFont')
			if set_QtStyle:
				self.dp_makePySideUI(textName, 'QLabel {color: None}')
			else:
				pass


	def dp_setAttrSync(self, attrName, ctrlPrefix, *args):

		layer = cmds.optionMenu('layerMenu', q= 1, v= 1)
		if layer == 'No Renderable Layer': layer = 'masterLayer'
		layer = 'defaultRenderLayer' if layer == 'masterLayer' else layer
		if ctrlPrefix != 'renumF':
			commonTool.dp_setOverrideData(attrName, layer, cmds.floatField(ctrlPrefix + 'Ffd', q= 1, v= 1))
			cmds.floatField(ctrlPrefix + 'Ffd', e= 1, v= commonTool.dp_getOverrideData(attrName, layer))
		else:
			commonTool.dp_setOverrideData(attrName, layer, cmds.checkBox(ctrlPrefix + 'Chk', q= 1, v= 1))
			cmds.checkBox(ctrlPrefix + 'Chk', e= 1, v= commonTool.dp_getOverrideData(attrName, layer))
			en = 0
			if cmds.checkBox(ctrlPrefix + 'Chk', q= 1, v= 1):
				en = 1
			cmds.text('strNumTxt', e= 1, en= en)
			cmds.text('stpNumTxt', e= 1, en= en)
			cmds.floatField('strNumFfd', e= 1, en= en)
			cmds.floatField('stpNumFfd', e= 1, en= en)


	def dp_rangeCtrlGetLayerAttr(self, *args):

		self.dp_getAttrSync('defaultRenderGlobals.startFrame', 'strFrm')
		self.dp_getAttrSync('defaultRenderGlobals.endFrame', 'endFrm')
		self.dp_getAttrSync('defaultRenderGlobals.byFrameStep', 'stpFrm')
		self.dp_getAttrSync('defaultRenderGlobals.modifyExtension', 'renumF')
		self.dp_getAttrSync('defaultRenderGlobals.startExtension', 'strNum')
		self.dp_getAttrSync('defaultRenderGlobals.byExtension', 'stpNum')
		self.dp_getCameraList()
		# textField: custmTxtF
		layer = cmds.optionMenu('layerMenu', q= 1, v= 1)
		if layer == 'No Renderable Layer' or layer == 'masterLayer': layer = 'defaultRenderLayer'
		if cmds.attributeQuery('dp_userAttr_customFrameRange', node= layer, ex= 1):
			cmds.textField('custmTxtF', e= 1, text= cmds.getAttr(layer + '.dp_userAttr_customFrameRange'))
		else:
			cmds.textField('custmTxtF', e= 1, text= '')
		en = 0 if cmds.textField('custmTxtF', q= 1, text= 1) != '' else 1
		cmds.floatField('strFrmFfd', e= 1, en= en)
		cmds.floatField('endFrmFfd', e= 1, en= en)
		cmds.floatField('stpFrmFfd', e= 1, en= en)
		cmds.text('strFrmTxt', e= 1, en= en)
		cmds.text('endFrmTxt', e= 1, en= en)
		cmds.text('stpFrmTxt', e= 1, en= en)
		cmds.textField('custmTxtF', e= 1, bgc= [0.16, 0.16, 0.16])
		self.dp_changeCustomFrame('', 1)

		self.dp_init_Backward_FramePrio()


	def dp_getAttrSync(self, attrName, ctrlPrefix):
		
		layer = cmds.optionMenu('layerMenu', q= 1, v= 1)
		if layer == 'No Renderable Layer' or layer == 'masterLayer': layer = 'defaultRenderLayer' 
		
		if layer == cmds.editRenderLayerGlobals(q= 1, currentRenderLayer= 1):
			# Reason for doing this is because when layerOptionMenu query overrided frame value in current layer,
			# the value(sec) store in '.value' and '.plug' have a slightly different.
			# Still not very clearly why, but for now, this way do well. 
			value = cmds.getAttr(attrName)
		else:
			value = commonTool.dp_getOverrideData(attrName, layer)

		if ctrlPrefix != 'renumF':
			cmds.floatField(ctrlPrefix + 'Ffd', e= 1, v= value)
		else:
			cmds.checkBox(ctrlPrefix + 'Chk', e= 1, v= value)
			en = 0
			if cmds.checkBox(ctrlPrefix + 'Chk', q= 1, v= 1):
				en = 1
			cmds.text('strNumTxt', e= 1, en= en)
			cmds.text('stpNumTxt', e= 1, en= en)
			cmds.floatField('strNumFfd', e= 1, en= en)
			cmds.floatField('stpNumFfd', e= 1, en= en)
		if layer != 'defaultRenderLayer' and commonTool.dp_hasOverride(attrName, layer):
			self.dp_tintOverrideColor(ctrlPrefix + 'Txt', 1)
		else:
			self.dp_tintOverrideColor(ctrlPrefix + 'Txt', 0)


	def dp_getCameraList(self):

		cmds.iconTextButton('addCamBtn', e= 1, image= 'openAttribute.png', c= self.dp_disrenderableCameraList)
		cmds.formLayout('rangeCheckForm', e= 1, af= [('addCamBtn', 'top', 142 + 33), ('addCamBtn', 'left', 165)])
		#pySide
		if set_QtStyle:
			self.dp_makePySideUI('cameraScr', 'QListView {color: None}')
		else:
			pass
		layer = cmds.optionMenu('layerMenu', q= 1, v= 1)
		if layer == 'No Renderable Layer': layer = 'masterLayer'
		layer = 'defaultRenderLayer' if layer == 'masterLayer' else layer
		cmds.textScrollList('cameraScr', e= 1, ra= 1)
		for cam in cmds.ls(ca= 1):
			if commonTool.dp_getOverrideData(cam + '.renderable', layer):
				cmds.textScrollList('cameraScr', e= 1, a= cmds.listRelatives(cam, p= 1))


	def dp_disrenderableCameraList(self, *args):

		cmds.iconTextButton('addCamBtn', e= 1, image= 'currentNamespace.png', c= partial(self.dp_adjRenderCamera, 1))
		cmds.formLayout('rangeCheckForm', e= 1, af= [('addCamBtn', 'top', 142 + 34), ('addCamBtn', 'left', 163)])
		#pySide
		if set_QtStyle:
			self.dp_makePySideUI('cameraScr', 'QListView {color: MediumSpringGreen; border-radius: 3px; border: 2px solid SeaGreen;}')
		else:
			pass
		layer = cmds.optionMenu('layerMenu', q= 1, v= 1)
		if layer == 'No Renderable Layer': layer = 'masterLayer'
		layer = 'defaultRenderLayer' if layer == 'masterLayer' else layer
		cmds.textScrollList('cameraScr', e= 1, ra= 1)
		for cam in cmds.ls(ca= 1):
			if not commonTool.dp_getOverrideData(cam + '.renderable', layer):
				cmds.textScrollList('cameraScr', e= 1, a= cmds.listRelatives(cam, p= 1))


	def dp_adjRenderCamera(self, value, *args):

		layer = cmds.optionMenu('layerMenu', q= 1, v= 1)
		if layer == 'No Renderable Layer': layer = 'masterLayer'
		layer = 'defaultRenderLayer' if layer == 'masterLayer' else layer
		override = 0 if '_dim' in cmds.iconTextButton('overriBtn', q= 1, image= 1) else 1
		# geather selected camera
		camerAdjList = cmds.textScrollList('cameraScr', q= 1, si= 1)
		if camerAdjList:
			for cam in camerAdjList:
				cmaShapeAttr = cmds.listRelatives(cam, s= 1)[0] + '.renderable'
				if override and layer != 'defaultRenderLayer': cmds.editRenderLayerAdjustment(cmaShapeAttr, lyr= layer)
				commonTool.dp_setOverrideData(cmaShapeAttr, layer, value)

		self.dp_getCameraList()


	def dp_removeCamOverride(self, allLayer, *args):

		camerAdjList = cmds.textScrollList('cameraScr', q= 1, si= 1)
		if camerAdjList:
			for cam in camerAdjList:
				cmaShapeAttr = cmds.listRelatives(cam, s= 1)[0] + '.renderable'
				if allLayer:
					for layer in cmds.listConnections(cmaShapeAttr, p= 1):
						layer = layer.split('.')[0]
						if layer != 'defaultRenderLayer':
							cmds.editRenderLayerAdjustment(cmaShapeAttr, lyr= layer, r= 1)
				else:
					layer = cmds.optionMenu('layerMenu', q= 1, v= 1)
					if layer == 'No Renderable Layer': layer = 'masterLayer'
					if layer != 'masterLayer':
						cmds.editRenderLayerAdjustment(cmaShapeAttr, lyr= layer, r= 1)

			self.dp_getCameraList()


	def dp_makePySideUI(self, ctrlName, myStyle):

		# thanks to Nathan Horne
		ctrlName = long(MQtUtil.findControl(ctrlName))
		qObj = wrapInstance(ctrlName, QtCore.QObject)
		metaObj = qObj.metaObject()
		cls = metaObj.className()
		superCls = metaObj.superClass().className()

		if hasattr(QtGui, cls):
			base = getattr(QtGui, cls)
		elif hasattr(QtGui, superCls):
			base = getattr(QtGui, superCls)
		else:
			base = QtGui.QWidget

		uiPySide = wrapInstance(ctrlName, base)
		uiPySide.setStyleSheet(myStyle)


	def dp_fCRW_2015(self, mainLayout, PRenderFrame, collapse, *args):
		# frame_Collapse_Resize_Window   ForMaya2015
		if mainLayout:
			derCmd = (  'height = 2\n' +
						'for frameChild in cmds.columnLayout("' + mainLayout + '", q= 1, ca= 1):\n' +
						'	if frameChild == "ViceFunFrame":\n' +
						'		if not cmds.frameLayout("ViceFunFrame", q= 1, cl= 1):\n' +
						'			height += 24\n' +
						'			for vfchild in cmds.columnLayout(cmds.frameLayout("ViceFunFrame", q= 1, ca= 1)[0], q= 1, ca= 1):\n' +
						'				height += cmds.frameLayout(vfchild, q= 1, h= 1)\n' +
						'		else:\n' +
						'			height += cmds.frameLayout(frameChild, q= 1, h= 1)\n' +
						'	else:\n' +
						'		height += cmds.frameLayout(frameChild, q= 1, h= 1)\n' +
						'cmds.window("domino_infoUI", e= 1, h= height)')
			cmds.evalDeferred(derCmd)
		else:
			if PRenderFrame == 'rangeFrame':
				if collapse:
					cmds.frameLayout('rangeFrame', e= 1, h= 20)
				else:
					cmds.frameLayout('rangeFrame', e= 1, h= 246)

			if PRenderFrame == 'fQueueFrame':
				if collapse:
					cmds.frameLayout('fQueueFrame', e= 1, h= 20)
				else:
					cmds.frameLayout('fQueueFrame', e= 1, h= 165)

			if PRenderFrame == 'noticeFrame':
				if collapse:
					cmds.frameLayout('noticeFrame', e= 1, h= 20)
				else:
					cmds.frameLayout('noticeFrame', e= 1, h= (24 + cmds.frameLayout('emailFrame', q= 1, h= 1) + cmds.frameLayout('severFrame', q= 1, h= 1)))

			if PRenderFrame == 'emailFrame':
				if collapse:
					cmds.frameLayout('emailFrame', e= 1, h= 19)
					cmds.frameLayout('noticeFrame', e= 1, h= (24 + 19 + cmds.frameLayout('severFrame', q= 1, h= 1)))
				else:
					cmds.frameLayout('emailFrame', e= 1, h= 203)
					cmds.frameLayout('noticeFrame', e= 1, h= (24 + 203 + cmds.frameLayout('severFrame', q= 1, h= 1)))

			if PRenderFrame == 'severFrame':
				if collapse:
					cmds.frameLayout('severFrame', e= 1, h= 19)
					cmds.frameLayout('noticeFrame', e= 1, h= (24 + 19 + cmds.frameLayout('emailFrame', q= 1, h= 1)))
				else:
					cmds.frameLayout('severFrame', e= 1, h= 160)
					cmds.frameLayout('noticeFrame', e= 1, h= (24 + 160 + cmds.frameLayout('emailFrame', q= 1, h= 1)))

			cmds.evalDeferred('cmds.window("domino_mainUI", e= 1, h= (192 + cmds.frameLayout("rangeFrame", q= 1, h= 1)' +
																  ' + cmds.frameLayout("fQueueFrame", q= 1, h= 1)' +
																  ' + cmds.frameLayout("noticeFrame", q= 1, h= 1)))')





class Render:


	def dp_kickDomino(self, *args):

		# start queue
		if Render_Controls.dp_getSceneList():
			UI_Controls.dp_lockUIControls(0)
			Render_Controls.dp_mayaPref_uiConfig('init')
			if can_uniqueTag:
				self.dp_renderDomino()
			else:
				self.dp_renderDomino_Scene()
		else:
			cmds.confirmDialog( title='dp_Domino: Error', message='SceneQueue is empty.\nSave at least one scene to render.', button=['Confirm'], defaultButton='Confirm', icon= 'warning')


	def dp_renderDomino(self):

		global dp_Rendering
		global dp_RenderAbort
		global renderMissionLayerSort
		global renderStartDate
		global dp_sceneQueueBox
		dp_RenderAbort = 0
		dp_Rendering = 1


		if cmds.file(q= 1, sn= 1, shn= 1):

			if cmds.textScrollList('fileScrollList', q= 1, sii= 1) != [1]:
				# renderSetting
				#mel.eval('unifiedRenderGlobalsWindow')
				#if cmds.window('unifiedRenderGlobalsWindow', ex= 1): cmds.window('unifiedRenderGlobalsWindow', e= 1, vis= 0)
				Render_Controls.dp_mayaPref_uiConfig('restore')
				if cmds.window('domino_ProgressUI', ex= 1): cmds.deleteUI('domino_ProgressUI')
				mel.eval('python("dp_Domino.UI.dp_ProgressWindow()")')

			self.dp_renderDomino_Scene()

			dp_sceneQueueBox.pop(0)

			if cmds.checkBox('saveSceneChk', q= 1, v= 1):
				if cmds.checkBox('saveTmLogChk', q= 1, v= 1):
					attrName = ''
					if 'renderStartDate' in globals():
						attrName = 'dp_userAttr_timeLog_' + ''.join(renderStartDate.split(' ')[3].split('/')) + ''.join(renderStartDate.split(' ')[5].split(':'))
					for layer in renderMissionLayerSort:
						if not cmds.attributeQuery(attrName, node= layer, ex= 1) and attrName:
							UI_Controls.dp_logSaving(layer, attrName)
				mel.eval('file -s -f')


		cmds.textScrollList('fileScrollList', e= 1, da= 1)

		if not dp_RenderAbort and dp_sceneQueueBox:
			Render_Controls.dp_mayaPref_uiConfig('off')
			cmds.textScrollList('fileScrollList', e= 1, si= dp_sceneQueueBox[0])
			scenePath = cmds.textScrollList('fileScrollList', q= 1, sut= 1)
			cmds.file(scenePath[0], o= 1, f= 1)
		else:
			Render_Controls.dp_mayaPref_uiConfig('restore')
			dp_Rendering = 0
			# unlock controls
			UI_Controls.dp_lockUIControls(1)


	def dp_renderDomino_Scene(self):
		
		global dp_SJ_idleEvent
		global dp_outputLogPath
		global dp_RenderAbort
		global renderMissionLayerSort
		global renderStartDate
		global server_list
		global server_status
		dp_SJ_idleEvent = 0
		server_list = []
		server_status = []
		pbWindowWidth = cmds.window('domino_ProgressUI', q= 1, w= 1)

		cmds.button('goPauseBtn', e= 1, l= 'S T O P', bgc= [0.5, 0.2, 0.2], c= 'cmds.button("goPauseBtn", e= 1, l= "[  E S C  ]")\ndp_Domino.dp_RenderAbort = 1')
		if set_QtStyle:
			UI_Controls.dp_makePySideUI('goPauseBtn', 'QPushButton {color: Salmon; background-color: #2A2A2A; border-radius: 3px;}')

		currentFrame = cmds.currentTime(q= 1)

		# hide layer moving controls
		cmds.iconTextButton('layerDownArrowBtn', e= 1, vis= 0)
		cmds.iconTextButton('layerUpArrowBtn', e= 1, vis= 0)
		for layer in renderMissionLayerSort:
			cmds.radioButton((layer + 'RadioBn'), e= 1, vis= 0)

		# record scriptEditor output for vrayRD
		animBatchOnly = 0
		if cmds.objExists('vraySettings'):
			if cmds.attributeQuery('animBatchOnly', node= 'vraySettings', ex= 1):
				animBatchOnly = cmds.getAttr('vraySettings.animBatchOnly')
				if not animBatchOnly: cmds.setAttr('vraySettings.animBatchOnly', 1)
				if vrayDR_check_Slave:
					vrayDRSupervisor.dp_vrayDRGetSlaveIPAndCheckStatus()
					cmds.cmdFileOutput(o= dp_outputLogPath)

		# start main timer
		labelIndent = (pbWindowWidth - 185) / 2
		renderStartDate = cmds.date(format='Start :  YYYY/MM/DD - hh:mm:ss')
		cmds.frameLayout('mainProFrame',e= 1, bgc= [0.4, 0.6, 0.8], l= renderStartDate, li= labelIndent)
		cmds.timer(s= 1, n= 'dp_MainTimer')

		# start hour timer
		if cmds.checkBox('hourMailChk', q= 1, v= 1):
			cmds.timer(s= 1, n= 'dp_HourTimer')

		# send start mail
		if cmds.checkBox('getMailChk', q= 1, v= 1):
			if cmds.checkBox('startMalChk', q= 1, v= 1):
				MailSending.dp_sendEmail('START')

		# S T A R T
		if cmds.checkBox('fProChk', q= 1, v= 1):
			self.dp_renderDomino_byFrames()
		else:
			self.dp_renderDomino_byLayers()

		if cmds.checkBox('delJChk', q= 1, v= 1):
			if dp_RenderAbort == 0:
				Render_Controls.dp_deleteJobsAfterRender()

		cmds.currentTime(currentFrame)

		# stop main timer
		mainEndTime = cmds.timer(e= 1, n= 'dp_MainTimer')
		labelIndent = (pbWindowWidth - 135) / 2
		proLabelIndent = (pbWindowWidth - 84) / 2
		cmds.frameLayout('mainProFrame', e= 1, l= 'Elapsed -  ' + dataGetFormat.dp_getFormattedRenderTime(int(mainEndTime), 1), li= labelIndent)
		cmds.frameLayout('jobsProFrame', e= 1, l= 'Jobs Progress', li= proLabelIndent, bgc= [0.3, 0.3, 0.3])

		# stop hour timer
		if cmds.checkBox('hourMailChk', q= 1, v= 1):
			cmds.timer(e= 1, n= 'dp_HourTimer')

		# send mail
		if dp_RenderAbort == 0:
			if cmds.checkBox('getMailChk', q= 1, v= 1):
				if cmds.checkBox('doneMailChk', q= 1, v= 1):
					MailSending.dp_sendEmail('DONE')
			cmds.frameLayout('mainProFrame', e= 1, bgc= [0.16, 0.7, 0.16])
			cmds.button('goPauseBtn', e= 1, l= 'D O N E', bgc= [0.16, 0.7, 0.16], c= 'pass', en= 0)
			if set_QtStyle:
				UI_Controls.dp_makePySideUI('goPauseBtn', 'QPushButton {border: 1px solid LimeGreen; color: LimeGreen; background-color: #2A2A2A; border-radius: 3px;}')
		else:
			if cmds.checkBox('getMailChk', q= 1, v= 1):
				if cmds.checkBox('stopMailChk', q= 1, v= 1):
					MailSending.dp_sendEmail('STOP')
			cmds.frameLayout('mainProFrame', e= 1, bgc= [0.8, 0.2, 0.2])
			cmds.button('goPauseBtn', e= 1, l= 'A B O R T E D', bgc= [0.8, 0.2, 0.2], c= 'pass', en= 0)
			if set_QtStyle:
				UI_Controls.dp_makePySideUI('goPauseBtn', 'QPushButton {border: 1px solid Crimson; color: Crimson; background-color: #2A2A2A; border-radius: 3px;}')

		# close scriptEditor output record
		descriptor = cmds.cmdFileOutput(q= 1, o= dp_outputLogPath)
		if -1 != descriptor:
			cmds.cmdFileOutput(c= descriptor)
		if cmds.file(dp_outputLogPath, q= 1, ex= 1):
			os.remove(dp_outputLogPath)

		if cmds.objExists('vraySettings'):
			if cmds.attributeQuery('animBatchOnly', node= 'vraySettings', ex= 1):
				cmds.setAttr('vraySettings.animBatchOnly', animBatchOnly)


	def dp_renderDomino_byFrames(self):

		global dp_RenderAbort
		global renderMissionLayerSort
		global allFrameRange
		global layerWithSort

		startFrameMin, endFrameMax = 0.0, 0.0

		#get major frame list
		majorFrameList = []
		for layer in renderMissionLayerSort: majorFrameList.extend(allFrameRange[layer])
		majorFrameList = list(set(majorFrameList))
		majorFrameList.sort()
		if cmds.checkBox('backChk', q= 1, v= 1): majorFrameList.reverse()

		#sorted and non-sorted
		jobLine = 1
		jobEnd = 2 if len(layerWithSort) > 0 else 1

		while jobLine <= jobEnd:
			renderMissionLayer = []
			if jobEnd == 2:
				if jobLine == 1: renderMissionLayer = layerWithSort
				if jobLine == 2: renderMissionLayer = [ly for ly in renderMissionLayerSort if ly not in layerWithSort]
			else:
				renderMissionLayer = renderMissionLayerSort

			#frame loop
			for thisFrame in majorFrameList:
				if dp_RenderAbort == 0:
					#layer loop
					for layer in renderMissionLayer:
						startFrame = commonTool.dp_getOverrideData('defaultRenderGlobals.startFrame', layer)
						endFrame = commonTool.dp_getOverrideData('defaultRenderGlobals.endFrame', layer)
						rangeData = allFrameRange[layer]

						currentRenderer = commonTool.dp_getOverrideData('defaultRenderGlobals.currentRenderer', layer)

						#if backward - for query Next Frame
						rangeData.sort()
						if cmds.checkBox('backChk', q= 1, v= 1): rangeData.reverse()

						#add or flush renderTimeLogTmp attr in first loop
						if not cmds.attributeQuery('dp_userAttr_timeLog_Tmp', node= layer, ex= 1):
							cmds.addAttr(layer, ln= 'dp_userAttr_timeLog_Tmp', dt= 'string', h= 1)
						if thisFrame == rangeData[0]:
							cmds.setAttr(layer + '.dp_userAttr_timeLog_Tmp', dataGetFormat.dp_formattedFrameRange(layer), type= 'string')

						#check if current render frame in this layer's render range
						if thisFrame in rangeData:
							
							cmds.text((layer + 'ProCurrFrame'), e= 1, vis= 1)

							#prepare for check if user hit stop render (for maya renderers) - this part is for progressWindow to init and set Max value
							if currentRenderer != 'vray':
								maxValue = 1
								cmds.progressWindow(title= 'rendering frames', progress= 0, max= maxValue, status= '     Rendering....', isInterruptable= 1)
								cmds.progressBar('mainProBar', e= 1, step= 1)
								cmds.progressBar('mainProBar', e= 1, step= -1)

							nextFrame = 0.0
							if len(rangeData) - 1 == rangeData.index(thisFrame):
								nextFrame = thisFrame
							else:
								nextFrame = rangeData[rangeData.index(thisFrame) + 1]

							#show folder button
							if not cmds.iconTextButton((layer + 'folderBtn'), q= 1, vis= 1):
								cmds.iconTextButton((layer + 'folderBtn'), e= 1, vis= 1)

							#RENDER
							self.dp_renderDomino_frame(thisFrame, layer, startFrame, endFrame, nextFrame) #get Cameras, set Layer, set Frame, Render!


						#prepare for check if user hit stop render (for maya renderers)
						if currentRenderer != 'vray':
							cmds.progressWindow(endProgress= 1)

						# if stop
						if dp_RenderAbort == 1:
							cmds.text((layer + 'ProStar'), e= 1, vis= 1)
							cmds.text((layer + 'ProStar'), e= 1, bgc= [0.9, 0.2, 0.2])
							break
				else:
					break

			jobLine += 1

		#mission end


	def dp_renderDomino_byLayers(self):

		global dp_RenderAbort
		global renderMissionLayerSort
		global allFrameRange

		#layer loop
		for layer in renderMissionLayerSort:
			if dp_RenderAbort == 0:
				startFrame = commonTool.dp_getOverrideData('defaultRenderGlobals.startFrame', layer)
				endFrame = commonTool.dp_getOverrideData('defaultRenderGlobals.endFrame', layer)
				rangeData = allFrameRange[layer]

				cmds.text((layer + 'ProCurrFrame'), e= 1, vis= 1)

				#add or flush renderTimeLogTmp attr in first loop
				if not cmds.attributeQuery('dp_userAttr_timeLog_Tmp', node= layer, ex= 1):
					cmds.addAttr(layer, ln= 'dp_userAttr_timeLog_Tmp', dt= 'string', h= 1)
				cmds.setAttr(layer + '.dp_userAttr_timeLog_Tmp', dataGetFormat.dp_formattedFrameRange(layer), type= 'string')

				currentRenderer = commonTool.dp_getOverrideData('defaultRenderGlobals.currentRenderer', layer)

				#prepare for check if user hit stop render (for maya renderers) - this part is for progressWindow to init and set Max value
				if currentRenderer != 'vray':
					maxValue = len(rangeData)
					cmds.progressWindow(title= 'rendering frames', progress= 0, max= maxValue, status= '     Rendering....', isInterruptable= 1)
					cmds.progressBar('mainProBar', e= 1, step= 1)
					cmds.progressBar('mainProBar', e= 1, step= -1)

				#frame loop
				for thisFrame in rangeData:
					nextFrame = 0.0
					if len(rangeData) - 1 == rangeData.index(thisFrame):
						nextFrame = thisFrame
					else:
						nextFrame = rangeData[rangeData.index(thisFrame) + 1]

					#show folder button
					if not cmds.iconTextButton((layer + 'folderBtn'), q= 1, vis= 1) and dp_RenderAbort == 0:
						cmds.iconTextButton((layer + 'folderBtn'), e= 1, vis= 1)

					#RENDER
					self.dp_renderDomino_frame(thisFrame, layer, startFrame, endFrame, nextFrame) #get Cameras, set Layer, set Frame, Render!


					#if stop
					if dp_RenderAbort == 1:
						cmds.text((layer + 'ProStar'), e= 1, vis= 1)
						cmds.text((layer + 'ProStar'), e= 1, bgc= [0.9, 0.2, 0.2])
						break

				#prepare for check if user hit stop render (for maya renderers)
				if currentRenderer != 'vray':
					cmds.progressWindow(endProgress= 1)

				if dp_RenderAbort == 0:
					cmds.text((layer + 'ProStar'), e= 1, vis= 0)

				cmds.iconTextButton((layer + 'timeShBtn'), e= 1, vis= 1)

			else:
				break

		#mission end


	def dp_renderDomino_frame(self, thisFrame, layer, startFrame, endFrame, nextFrame):

		global dp_RenderAbort
		global dp_SJ_idleEvent

		#set current layer
		cmds.editRenderLayerGlobals(currentRenderLayer= layer)
		cmds.text((layer + 'ProStar'), e= 1, vis= 1)

		currentRenderer = commonTool.dp_getOverrideData('defaultRenderGlobals.currentRenderer', layer)

		# if current renderer is vray, check 'render animation only in batch mode' checkBox
		vrayAniBatchOnly = 0
		if currentRenderer == 'vray' and cmds.getAttr('vraySettings.animBatchOnly'):
			vrayAniBatchOnly = 1
			cmds.setAttr('vraySettings.animBatchOnly', 0)

		#set current frame
		cmds.setAttr('defaultRenderGlobals.startFrame', thisFrame)
		cmds.setAttr('defaultRenderGlobals.endFrame', thisFrame)
		cmds.currentTime(thisFrame)

		if currentRenderer != 'vray':
			cmds.text((layer + 'ProCurrFrame'), e= 1, l= ('- ' + str(int(nextFrame) if commonTool.dp_canThisFloatBeInt(nextFrame) else nextFrame) + ' -'))
		else:
			cmds.text((layer + 'ProCurrFrame'), e= 1, l= ('- ' + str(int(thisFrame) if commonTool.dp_canThisFloatBeInt(thisFrame) else thisFrame) + ' -'))

		#Renumber frames
		startExtension = 0.0
		renumber = int(commonTool.dp_getOverrideData('defaultRenderGlobals.modifyExtension', layer))
		if renumber:
			startExtension = float(commonTool.dp_getOverrideData('defaultRenderGlobals.startExtension', layer))
			renderCount = (thisFrame - startFrame) / float(commonTool.dp_getOverrideData('defaultRenderGlobals.byFrameStep', layer)) + 1
			renumberFrame = float(commonTool.dp_getOverrideData('defaultRenderGlobals.startExtension', layer)) + (float(commonTool.dp_getOverrideData('defaultRenderGlobals.byExtension', layer)) * (renderCount - 1))
			cmds.setAttr('defaultRenderGlobals.startExtension', renumberFrame)

		#get all renderable camera
		Cams = cmds.ls(ca= 1)
		renderCams = []
		for cam in Cams:
			if cmds.getAttr(cam + '.renderable'):
				tmpCam = cmds.listRelatives(cam, p= 1)
				renderCams.append(tmpCam[0])

		sj2VrayCmd = 'scriptJob -ro true -ie \"python(\\\"dp_Domino.dp_SJ_idleEvent = 0\\\"); pause -sec 3; if(`progressBar -q -ic $gMainProgressBar`) python(\\\"dp_Domino.dp_RenderAbort = 1\\\");\"'
		
		#start timer(Frame)
		cmds.timer(s= 1, n= 'dp_FrameTimer')
		
		for rCam in renderCams:
			#check if user hit stop render (for vray)
			if currentRenderer == 'vray':
				if dp_SJ_idleEvent == 0: dp_SJ_idleEvent = mel.eval(sj2VrayCmd)
				if dp_RenderAbort == 1:
					break

			#check if user hit stop render (for maya renderers)
			if currentRenderer != 'vray':
				if cmds.progressWindow(q= 1, isCancelled= 1):
					dp_RenderAbort = 1
					break

			#frame start date
			labelIndent = (cmds.window('domino_ProgressUI', q= 1, w= 1) - 184) / 2
			renderStartDate = cmds.date(format='Frame Start :   -/DD - hh:mm:ss')
			cmds.frameLayout('jobsProFrame', e= 1, l= renderStartDate, li= labelIndent, bgc= [.3, .4, .6])

			#adjust layer and RENDER!!
			layer = dataGetFormat.dp_layerNameAdjust(1, layer, 1)

			# R E N D E R
			self.dp_doRender(rCam)


			layer = dataGetFormat.dp_layerNameAdjust(2, layer, 1)

			#check if user hit stop render (for vray) - double check
			if currentRenderer == 'vray':
				if dp_SJ_idleEvent == 0: dp_SJ_idleEvent = mel.eval(sj2VrayCmd)
				if dp_RenderAbort == 1:
					break

			#check if user hit stop render (for maya renderers) - double check
			if currentRenderer != 'vray':
				if cmds.progressWindow(q= 1, isCancelled= 1):
					cmds.text((layer + 'ProCurrFrame'), e= 1, l= ('- ' + str(int(thisFrame) if commonTool.dp_canThisFloatBeInt(thisFrame) else thisFrame) + ' -'))
					dp_RenderAbort = 1
					break

		#stop timer(Frame)
		thisFrameTime = cmds.timer(e= 1, n= 'dp_FrameTimer')
		cmds.text((layer + 'lastFrameTime'), e= 1, l= dataGetFormat.dp_getFormattedRenderTime(int(thisFrameTime), 0))
		if set_QtStyle: UI_Controls.dp_makePySideUI(layer + 'lastFrameTime', 'QLabel {color: SteelBlue}')

		#restore frame range
		Render_Controls.dp_restoreFrameRange(startFrame, endFrame)
		if renumber: cmds.setAttr('defaultRenderGlobals.startExtension', startExtension)
		if vrayAniBatchOnly: cmds.setAttr('vraySettings.animBatchOnly', 1)

		# check if progress window is off
		if not cmds.window('domino_ProgressUI', q= 1, vis= 1): cmds.window('domino_ProgressUI', e= 1, vis= 1)

		if dp_RenderAbort == 0:
			progressStep = int(cmds.text((layer + 'ProTxtStatus'), q= 1, l= 1)) - 1
			cmds.text((layer + 'ProTxtStatus'), e= 1, l= progressStep)

			if currentRenderer != 'vray':
				cmds.progressWindow(e= 1, step= 1)
			cmds.progressBar('mainProBar', e= 1, step= 1)
			cmds.progressBar((layer + 'ProBar'), e= 1, step= 1)
		
		#add frame render time data to renderTimeLogTmp
		renderTimeLogTmp = cmds.getAttr(layer + '.dp_userAttr_timeLog_Tmp')
		slaveNum = str(vrayDRSupervisor.dp_vrayDRNodeNumber(currentRenderer, layer)) if vrayDR_check_Slave else '0'
		cmds.setAttr(layer + '.dp_userAttr_timeLog_Tmp', renderTimeLogTmp + ';' + str(thisFrame) + '=' + str(thisFrameTime) + '$' + slaveNum, type= 'string')

		#update layer render time
		layerElapTime = thisFrameTime + float(cmds.text((layer + 'elapsedTime'),q= 1, l= 1))
		if cmds.progressBar((layer + 'ProBar'), q= 1, progress= 1) == cmds.progressBar((layer + 'ProBar'), q= 1, max= 1):
			cmds.text((layer + 'ProCurrFrame'), e= 1, vis= 0)
			cmds.text((layer + 'lastFrameTime'),e= 1, vis= 0)
			cmds.iconTextButton((layer + 'timeShBtn'), e= 1, vis= 1)
			cmds.text((layer + 'elapsedTime'),e= 1, l= dataGetFormat.dp_getFormattedRenderTime(int(layerElapTime), 1), vis= 1)
			#add layer total render time data to renderTimeLogTmp
			renderTimeLogTmp = cmds.getAttr(layer + '.dp_userAttr_timeLog_Tmp')
			cmds.setAttr(layer + '.dp_userAttr_timeLog_Tmp', renderTimeLogTmp + ';TT=' + str(layerElapTime), type= 'string')
			if cmds.checkBox('getMailChk', q= 1, v= 1) and cmds.checkBox('layerMalChk', q= 1, v= 1): MailSending.dp_sendEmail(layer)
		else:
			cmds.text((layer + 'elapsedTime'),e= 1, l= str(layerElapTime))

		cmds.text((layer + 'ProStar'), e= 1, vis= 0)

		# check if over an hour since last notice
		if dp_RenderAbort == 0 and cmds.checkBox('hourMailChk', q= 1, v= 1):
			try:
				lapTime = cmds.timer(lap= 1, n= 'dp_HourTimer')
				if lapTime / 3600 >= cmds.intField('hoursGapInt', q= 1, v= 1):
					MailSending.dp_sendEmail('HOUR')
					cmds.timer(e= 1, n= 'dp_HourTimer')
					cmds.timer(s= 1, n= 'dp_HourTimer')
			except:
				cmds.timer(s= 1, n= 'dp_HourTimer')

		# vrayDR off-line check
		if currentRenderer == 'vray' and vrayDR_check_Slave:
			vrayDRSupervisor.dp_vrayDRNodeOfflineCheck()
			vrayDRSupervisor.dp_vrayDRGetSlaveIPAndCheckStatus()


	def dp_doRender(self, rCam):

		renderPanels = cmds.getPanel(scriptType= 'renderWindowPanel')
		mel.eval('renderWindowRenderCamera render ' + renderPanels[0] + ' ' + rCam)





class Render_Controls:


	def dp_postSceneReadJob(self):

		global dp_Rendering
		
		UI_Controls.dp_refreshLayerMenu()
		UI_Controls.dp_getRendererName()
		UI_Controls.dp_init_DeleteJobs()
		UI_Controls.dp_init_Resolution()
		cmds.checkBox('animChk', e= 1, v= cmds.getAttr('defaultRenderGlobals.animation'))

		# scenes switching engine
		cmds.scriptJob(e= ['PostSceneRead', Render_Controls.dp_postSceneReadJob], ro= 1, p= 'domino_mainUI')
		
		if not dp_Rendering:
			cmds.textScrollList('fileScrollList', e= 1, ra= 1)
			if can_uniqueTag: UI_Controls.dp_sceneQueueAction('addCurrentScene')
			if cmds.button('goPauseBtn', ex= 1):
				cmds.button('goPauseBtn', e= 1, l= 'R E F R E S H', bgc= [0.3, 0.3, 0.35], c= UI.dp_ProgressWindow)
				if set_QtStyle:
					UI_Controls.dp_makePySideUI('goPauseBtn', 'QPushButton {color: Goldenrod; background-color: Cornsilk; border-radius: 3px;}')
		else:
			Render.dp_renderDomino()


	def dp_getSceneList(self, *args):

		global dp_sceneQueueBox

		dp_sceneQueueBox = cmds.textScrollList('fileScrollList', q= 1, ai= 1)
		cmds.textScrollList('fileScrollList', e= 1, da= 1)
		if dp_sceneQueueBox:
			cmds.textScrollList('fileScrollList', e= 1, si= dp_sceneQueueBox[0])
			return 1
		else:
			return 0


	def dp_layerSort(self):

		global renderMissionLayerSort
		global layerWithSort
		renderMissionLayerSort = []
		layerWithSort = []
		layerWithNoSort = []

		for layer in cmds.ls(et= 'renderLayer'):
			if cmds.getAttr(layer + '.renderable'):
				if cmds.attributeQuery('dp_userAttr_renderOrder', node= layer, ex= 1):
					layerWithSort.append(str(cmds.getAttr(layer + '.dp_userAttr_renderOrder')) + '#' + layer)
				else:
					layerWithNoSort.append(layer)

		layerWithSort.sort()
		for count, layer in enumerate(layerWithSort):
			layerWithSort[count] = layer.split('#')[1]
		layerWithSort.extend(layerWithNoSort)
		renderMissionLayerSort.extend(layerWithSort)


	def dp_jobsCaculator(self, action, querylayer):

		value = 0
		global renderMissionLayerSort
		global allFrameRange
		
		#query total frame number
		if action == 1:
			for layer in renderMissionLayerSort:
				#get frame range and byframe
				rangeData = allFrameRange[layer]
				value += len(rangeData)
			return value

		#query frame number in one layer
		if action == 2:
			rangeData = allFrameRange[querylayer]
			value = len(rangeData)
			return value

		#query layer number
		if action == 3:
			for layer in renderMissionLayerSort:
				value += 1
			return value


	def dp_storeAllFrameRange(self):

		global renderMissionLayerSort
		global allFrameRange
		allFrameRange = {}

		for layer in renderMissionLayerSort:
			allFrameRange[layer] = self.dp_getFrameRange(layer)


	def dp_getFrameRange(self, querylayer):

		rangeDataArr = []
		noCustom = 0
		back = 0

		if cmds.attributeQuery('dp_userAttr_backward', node= querylayer, ex= 1):
			back = 1 if cmds.getAttr(querylayer + '.dp_userAttr_backward') else 0
		else:
			back = 0

		if cmds.attributeQuery('dp_userAttr_customFrameRange', node= querylayer, ex= 1):
			customRange = cmds.getAttr(querylayer + '.dp_userAttr_customFrameRange')
			if customRange:
				for rangeData in customRange.split(','):
					rangeData = rangeData.strip()
					if '-' in rangeData and not (rangeData.startswith('-') and rangeData.count('-') == 1):
						startFrame, endFrame = dataGetFormat.dp_frameRangeStringCleanUp(rangeData)
						startFrame = float(startFrame)
						endFrame = float(endFrame)
						byFrame = float(rangeData.split('@')[1] if '@' in rangeData else '1' if startFrame < endFrame else '-1')
						if startFrame < endFrame:
							F = startFrame
							while F <= endFrame:
								rangeDataArr.append(int(F) if commonTool.dp_canThisFloatBeInt(F) else F)
								F += byFrame
						elif startFrame > endFrame:
							F = startFrame
							while F >= endFrame:
								rangeDataArr.append(int(F) if commonTool.dp_canThisFloatBeInt(F) else F)
								F -= byFrame
						else:
							rangeDataArr.append(int(startFrame) if commonTool.dp_canThisFloatBeInt(startFrame) else float(startFrame))
					else:
						rangeDataArr.append(int(rangeData) if commonTool.dp_canThisFloatBeInt(rangeData) else float(rangeData))
				if back:
					rangeDataArr.reverse()
			else:
				noCustom = 1
		else:
			noCustom = 1

		if noCustom:
			startFrame = commonTool.dp_getOverrideData('defaultRenderGlobals.startFrame', querylayer)
			endFrame = commonTool.dp_getOverrideData('defaultRenderGlobals.endFrame', querylayer)
			byframe = commonTool.dp_getOverrideData('defaultRenderGlobals.byFrameStep', querylayer)
			
			for F in commonTool.dp_frange(startFrame, endFrame+1, byframe):
				rangeDataArr.append(int(F) if commonTool.dp_canThisFloatBeInt(F) else F)

			if back:
				rangeDataArr.reverse()

		return rangeDataArr


	def dp_deleteJobsAfterRender(self):

		layerToDelete = []
		for layer in cmds.ls(et= 'renderLayer'):
			if cmds.getAttr(layer + '.renderable') and mel.eval('gmatch ' + layer.upper() + ' \"*_RENDERJOB*\"'):
				layerToDelete.append(layer)

		if layerToDelete:
			if not cmds.objExists('dp_renderJobLayer_deleting_buff'):
				cmds.createRenderLayer(e= 1, mc= 1, n= 'dp_renderJobLayer_deleting_buff')
				cmds.scriptJob(ro= 1, e= ['renderLayerManagerChange', 'cmds.delete("dp_renderJobLayer_deleting_buff")'])
			for layer in layerToDelete:
				cmds.delete(layer)

		cmds.editRenderLayerGlobals(currentRenderLayer= 'defaultRenderLayer')


	def dp_restoreFrameRange(self, startFrame, endFrame):
		
		#set render setting frame range back to origen
		cmds.setAttr('defaultRenderGlobals.startFrame', startFrame)
		cmds.setAttr('defaultRenderGlobals.endFrame', endFrame)


	def dp_mayaPref_uiConfig(self, action):

		global gUseScenePanelConfig
		global file_uc

		if action == 'init':
			gUseScenePanelConfig = mel.eval('$tmp = $gUseScenePanelConfig')
			file_uc = mel.eval('$tmp = `file -q -uc`')

		if action == 'off':
			if gUseScenePanelConfig:
				mel.eval('$gUseScenePanelConfig = false') # reset if stop or resetEnv
			if file_uc:
				mel.eval('file -uc false')

		if action == 'restore':
			if gUseScenePanelConfig:
				mel.eval('$gUseScenePanelConfig = true')
			if file_uc:
				mel.eval('file -uc true')





class dataGetFormat:


	def dp_layerNameAdjust(self, action, layerToAdj, doRename):
		#ex : s1_myLayer###_object$$$_renderJob1
		newLayerName = ''
		hasExtraJob = ''

		# remove prefix and suffix, than save prefix and suffix
		if action == 1:
			Buffer = layerToAdj.split('_')
			for bufId in range(len(Buffer)):
				if not Buffer[bufId].isdigit() and Buffer[bufId]:
					if not mel.eval('gmatch ' + Buffer[bufId].upper() + ' \"RENDERJOB*\"'):
						if bufId == len(Buffer) - 1:
							newLayerName += Buffer[bufId]
						else:
							if mel.eval('gmatch ' + Buffer[bufId + 1].upper() + ' \"RENDERJOB*\"') if not Buffer[bufId + 1].isdigit() and Buffer[bufId + 1] else 0:
								newLayerName += Buffer[bufId]
							else:
								newLayerName += Buffer[bufId] + '_'
				else:
					if bufId == len(Buffer) - 1:
						newLayerName += Buffer[bufId]
					else:
						newLayerName += Buffer[bufId] + '_'
				#check suffix
				if not Buffer[bufId].isdigit() and Buffer[bufId]:
					if mel.eval('gmatch ' + Buffer[bufId].upper() + ' \"RENDERJOB*\"'):
						hasExtraJob = Buffer[bufId]

			if doRename:
				#set Attr mark
				if hasExtraJob:
					if not cmds.attributeQuery('dp_userAttr_hasExtraJob', node= layerToAdj, ex= 1):
						cmds.addAttr(layerToAdj, ln= 'dp_userAttr_hasExtraJob', dt= 'string', h= 1)
					cmds.setAttr(layerToAdj + '.dp_userAttr_hasExtraJob', hasExtraJob, type= 'string')

				#rename Layer
				for layer in cmds.ls(et= 'renderLayer'):
					if layer == newLayerName and layer != layerToAdj:
						cmds.rename(layer, 'giveMeOneFrameRenderTimeAndIWillGetYourNameBack')

				if layerToAdj != 'defaultRenderLayer':
					cmds.rename(layerToAdj, newLayerName)

				mel.eval('updateEditorRenderLayer(\"RenderLayerTab\")') # maya will pop up ERROR, if you don't update renderLayerTab after renaming renderLayer.

			return newLayerName

		# restore suffix to layerName
		if action == 2:
			newLayerName = layerToAdj
			if cmds.attributeQuery('dp_userAttr_hasExtraJob', node= layerToAdj, ex= 1):
				newLayerName = newLayerName + '_' + cmds.getAttr(layerToAdj + '.dp_userAttr_hasExtraJob')
				cmds.deleteAttr(layerToAdj, at= 'dp_userAttr_hasExtraJob')

			#rename Layer
			if layerToAdj != 'defaultRenderLayer':
				cmds.rename(layerToAdj, newLayerName)

			for layer in cmds.ls(et= 'renderLayer'):
				if layer == 'giveMeOneFrameRenderTimeAndIWillGetYourNameBack':
					cmds.rename(layer, layerToAdj)

			mel.eval('updateEditorRenderLayer(\"RenderLayerTab\")') # maya will pop up ERROR, if you don't update renderLayerTab after renaming renderLayer.

			return newLayerName


	def dp_checkCustomFrameRangeInputFormat(self):

		errorFormat = 0
		errorLogic = 0
		startFrame, endFrame, byFrame = 0, 0, 0
		message = ''
		customRange = cmds.textField('custmTxtF', q= 1, text= 1).strip()
		formattedCustomRange = []
		if customRange:
			try:
				for rangeData in customRange.split(','):
					rangeData = rangeData.strip()
					origenInput = rangeData
					message = '{' + origenInput + '}'
					if '-' in rangeData and not (rangeData.startswith('-') and rangeData.count('-') == 1):
						if rangeData.count('-') in range(1, 5):
							if rangeData.startswith('-'):
								rangeData = rangeData.replace('-', ' ', 2).replace(' ', '-', 1)
							else:
								rangeData = rangeData.replace('-', ' ', 1)
							startFrame, endFrame = self.dp_frameRangeStringCleanUp(rangeData)
							startFrame = int(startFrame) if commonTool.dp_canThisFloatBeInt(startFrame) else float(startFrame)
							endFrame = int(endFrame) if commonTool.dp_canThisFloatBeInt(endFrame) else float(endFrame)
							byFrame = rangeData.split('@')[1] if '@' in rangeData else '1' if startFrame < endFrame else '-1'
							byFrame = int(byFrame) if commonTool.dp_canThisFloatBeInt(byFrame) else float(byFrame)
							inputStr = str(startFrame) + '- ' + str(endFrame) + ('@ ' + str(byFrame) if byFrame != 1 and byFrame != -1 else '') if startFrame != endFrame else str(startFrame)
							formattedCustomRange.append(inputStr)

							if startFrame < endFrame and byFrame < 0:
								message = '{' + origenInput + '} : [byFrame] can\'t be Negative, when [startFrame] is Smaller than [endFrame]'
								errorLogic = 1
							if startFrame > endFrame and byFrame > 0:
								message = '{' + origenInput + '} : [byFrame] can\'t be Positive, when [startFrame] is Bigger than [endFrame]'
								errorLogic = 1
							if byFrame == 0:
								message = '{' + origenInput + '} : [byFrame] can\'t be Zero'
								errorLogic = 1
							if errorLogic:
								break
						else:
							errorFormat = 1
							break
					else:
						rangeData = float(rangeData) if '.' in rangeData else int(rangeData)
						formattedCustomRange.append(str(rangeData))
			except:
				errorFormat = 1

		if not errorFormat:
			if not errorLogic:
				cmds.textField('custmTxtF', e= 1, bgc= [0.16, 0.16, 0.16], text= ', '.join(formattedCustomRange))
				return 1
			else:
				cmds.textField('custmTxtF', e= 1, bgc= [0.0, 0.0, 0.3])
				cmds.warning('dp_Domino: Custom_Range Error, please check input LOGIC. -> ' + message)
				return 0
		else:
			cmds.textField('custmTxtF', e= 1, bgc= [0.3, 0.0, 0.0])
			cmds.warning('dp_Domino: Custom_Range Error, please check input FORMAT. -> ' + message)
			return 0


	def dp_formattedFrameRange(self, querylayer):

		frameRangeString = ''
		noCustom = 0

		if cmds.attributeQuery('dp_userAttr_backward', node= querylayer, ex= 1):
			frameRangeString += 'B' if cmds.getAttr(querylayer + '.dp_userAttr_backward') else ''

		if cmds.attributeQuery('dp_userAttr_customFrameRange', node= querylayer, ex= 1):
			customRange = cmds.getAttr(querylayer + '.dp_userAttr_customFrameRange')
			if customRange:
				frameRangeString += customRange
			else:
				noCustom = 1
		else:
			noCustom = 1

		if noCustom:
			frameRangeString += str(commonTool.dp_getOverrideData('defaultRenderGlobals.startFrame', querylayer)) + '- ' + str(commonTool.dp_getOverrideData('defaultRenderGlobals.endFrame', querylayer))
			byFrame = commonTool.dp_getOverrideData('defaultRenderGlobals.byFrameStep', querylayer)
			frameRangeString += '@ ' + str(byFrame) if byFrame != 1 and byFrame != -1 else ''

		return '[' + frameRangeString + ']'


	def dp_getFormattedRenderTime(self, elapsedTime, includeDay):

		HH = '%02d' %(int(elapsedTime / 3600) % 24)
		MM = '%02d' %(int(elapsedTime / 60) % 60)
		SS = '%02d' %(elapsedTime % 60)

		if includeDay:
			
			DD = '%02d' %(int(elapsedTime / 86400))
			return DD + ':' + HH + ':' + MM + ':' + SS

		else:
			
			return HH + ':' + MM + ':' + SS


	def dp_frameRangeStringCleanUp(self, rangeData):

		return re.findall(r"[-]?\d*\.\d+|[-]?\d+", rangeData.split('@')[0] if '@' in rangeData else rangeData)


	def dp_LayerNameForMail(self, layer, *args):

		newLayerName = self.dp_layerNameAdjust(1, layer, 0)
		if mel.eval('gmatch ' + layer.upper() + ' \"*_RENDERJOB*\"'):
			num = layer.upper().split('_RENDERJOB')
			if num[1]:
				newLayerName = newLayerName + ' (RenJob' + num[1] + ')'
			else:
				newLayerName = newLayerName + ' (RenJob)'

		return newLayerName





class vrayDRSupervisor:


	def dp_vrayDRGetSeversFile(self, fileName):
		
		listarr = []
		filePath = mel.eval('vrayFindServersFile("' + fileName + '")')
		if cmds.file(filePath, q= 1, ex= 1):
			flistarr = open(filePath, 'r')
			for line in flistarr:
				listarr.append(line.strip())
			flistarr.close()
		return listarr


	def dp_vrayDRGetSlaveIPAndCheckStatus(self):

		global server_list
		global server_status
		global dp_timeOut
		server_list = self.dp_vrayDRGetSeversFile('server_list.tmp')
		if server_list:
			server_status = self.dp_vrayDRGetSeversFile('server_status.tmp')
			server_ports = self.dp_vrayDRGetSeversFile('server_ports.tmp')
			offlineIP = []
			for count, status in enumerate(server_status):
				if status == 'Enable':
					try:
						port = int(server_ports[count])
					except:
						port = mel.eval('getDefaultDRPort()')
					prSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					prSocket.settimeout(dp_timeOut)
					try:
						result = prSocket.connect_ex((server_list[count], port))
						if result == 0:
							server_list[count] = socket.gethostbyname(server_list[count])
						else:
							offlineIP.append(server_list[count])
					except:
						offlineIP.append(server_list[count])
					prSocket.close()
			self.dp_vrayDRturnSlaveOff(offlineIP)


	def dp_vrayDRNodeNumber(self, currentRenderer, layer):
		#if vray, check distributed rendering node off-line
		global server_status
		slaveNum = 0
		if currentRenderer == 'vray':
			if commonTool.dp_getOverrideData('vraySettings.sys_distributed_rendering_local', layer):
				slaveNum += 1
			if commonTool.dp_getOverrideData('vraySettings.sys_distributed_rendering_on', layer):
				slaveNum += server_status.count('Enable')
		else:
			slaveNum = 1

		return slaveNum


	def dp_vrayDRNodeOfflineCheck(self):

		global dp_outputLogPath
		if cmds.file(dp_outputLogPath, q= 1, ex= 1):
			outputLog = open(dp_outputLogPath, 'r')
			offlineIP = []
			for line in outputLog:
				# ex->  // Warning: Could not connect to host 192.168.xx.xxx:20207: Connection timeout //
				# ex-> 	// Warning: line 1: Render host xthisHostnamex (192.168.xx.xxx:20207) is not responding // 
				if 'Warning: Could not connect to host' in line:
					offlineIP.append(line.split('host')[1].strip().split(' ')[0].split(':')[0])
				if 'Render host' and 'is not responding' in line:
					offlineIP.append(line.split('(')[1].split(')')[0].split(':')[0])
			outputLog.close()
			if offlineIP:
				self.dp_vrayDRturnSlaveOff(offlineIP)
				outputLog = open(dp_outputLogPath, 'w')
				outputLog.write('')
				outputLog.close()


	def dp_vrayDRturnSlaveOff(self, offlineIP):

		global server_list
		global server_status
		if vrayDR_kick_Slave:
			offlineIP = list(set(offlineIP))
			for IP in offlineIP:
				try:
					server_status[server_list.index(IP)] = 'Disable'
					if cmds.getAttr('vraySettings.sys_distributed_rendering_on'):
						cmds.warning('dp_Domino: vrayDR slave off-line : [' + IP + '], setted to [Disable]')
				except:
					pass
			statusFile = open(mel.eval('vrayFindServersFile("server_status.tmp")'), 'w')
			statusInfo = ''
			for status in server_status:
				statusInfo += status + '\n'
			statusFile.write(statusInfo)
			statusFile.close()
			mel.eval('if(`window -ex VRayDR`){ vraySwitchServerStatus(); }')





class commonTool:


	def dp_setOverrideData(self, setValue, setlayer, value):
		# set override value without switching layers : it can set everything! (setValue = 'object.attribute' or 'fps') # dataType problem
		destination = setValue
		overrideList = cmds.listConnections(setValue, p= 1) if setValue != 'fps' else []
		setFrame = 1 if setValue == 'defaultRenderGlobals.startFrame' or setValue == 'defaultRenderGlobals.endFrame' else 0
		atCurrentLayer = 1 if cmds.editRenderLayerGlobals(q= 1, currentRenderLayer= 1) == setlayer else 0
		goWithMaster = 1 if cmds.editRenderLayerGlobals(q= 1, currentRenderLayer= 1) == 'defaultRenderLayer' and not self.dp_hasOverride(setValue, setlayer) else 0
		# if this attr has override by some layer(s)
		if overrideList and not atCurrentLayer and not goWithMaster:
			# find override
			setLayerProx = setlayer
			findOverride = 0

			while findOverride == 0:
				for override in overrideList:
					Buffer = override.split('.')
					if Buffer[0] == setLayerProx:
						destination = Buffer[0] + '.' + Buffer[1] + '.value'
						findOverride = 1
						break
				# if this layer has no override, change setlayer to defaultLayer(masterLayer)
				setLayerProx = 'defaultRenderLayer' if findOverride == 0 else setLayerProx
		
		if setFrame and destination.endswith('.value'):
			timeUnit = cmds.currentUnit(q= 1, t= 1) # mel.eval('currentTimeUnitToFPS')
			if timeUnit[-3:] == 'fps':
				value = round(value * (6000.0 / float(timeUnit.split('fps')[0])), 0) / 6000.0
			value = {		# maya stores 'ticks/tps' behind, vvv-> value = int(frame * tpf) / tps
					'game' : round(value * 400, 0) / 6000.0,
					'film' : round(value * 250, 0) / 6000.0,
					 'pal' : round(value * 240, 0) / 6000.0,
					'ntsc' : round(value * 200, 0) / 6000.0,
					'show' : round(value * 125, 0) / 6000.0,
					'palf' : round(value * 120, 0) / 6000.0,
				   'ntscf' : round(value * 100, 0) / 6000.0,
				'millisec' : round(value *   6, 0) / 6000.0,
					 'sec' : round(value * 6000, 0) / 6000.0,
					 'min' : round(value * 360000, 0) / 6000.0,
					'hour' : round(value * 21600000, 0) / 6000.0,
			}.get(timeUnit, value)
		
		if setValue == 'fps':
			try:
				cmds.currentUnit(t= value)
				return 1
			except:
				timeUnitList = ['game', 'film', 'pal', 'ntsc', 'show', 'palf', 'ntscf', 'millisec', 'sec', 'min', 'hour',
								'2fps', '3fps', '4fps', '5fps', '6fps', '8fps', '10fps', '12fps', '16fps', '20fps', '40fps',
								'75fps', '80fps', '100fps', '120fps', '125fps', '150fps', '200fps', '240fps', '250fps', '300fps',
								'375fps', '400fps', '500fps', '600fps', '750fps', '1200fps', '1500fps', '2000fps', '3000fps', '6000fps']
				print '\nTime Unit List:'
				print '	' + '\n	'.join(timeUnitList)
				cmds.warning('dp_Domino: def dp_setOverrideData:: \'fps\' value input error, for more info please check scriptEditor.')
				return 0
		else:
			try:
				cmds.setAttr(destination, value)
				return 1
			except:
				cmds.warning('dp_Domino: def dp_setOverrideData:: attribute setting failed, maybe attr is locked or else...')
				return 0


	def dp_getOverrideData(self, queryValue, queryLayer):
		# query override value without switching layers : it can query everything! (queryValue = 'object.attribute' or 'fps') # dataType problem?
		value = ''
		overrideList = cmds.listConnections(queryValue, p= 1) if queryValue != 'fps' else ['fps']
		# if this attr has override by some layer(s)
		if overrideList:
			# find override
			queryLayerProx = queryLayer
			findOverride = 0
			
			while findOverride == 0 and queryValue != 'fps':
				for override in overrideList:
					Buffer = override.split('.')
					if Buffer[0] == queryLayerProx:
						value = cmds.getAttr(Buffer[0] + '.' +Buffer[1] + '.plug')
						if cmds.editRenderLayerGlobals(q= 1, currentRenderLayer= 1) == 'defaultRenderLayer':
							if self.dp_hasOverride(queryValue, queryLayer) and queryLayer != 'defaultRenderLayer':
								value = cmds.getAttr(Buffer[0] + '.' +Buffer[1] + '.value')
						else:
							if self.dp_hasOverride(queryValue, queryLayerProx) and cmds.editRenderLayerGlobals(q= 1, currentRenderLayer= 1) != queryLayer:
								if self.dp_hasOverride(queryValue, queryLayer) or self.dp_hasOverride(queryValue, cmds.editRenderLayerGlobals(q= 1, currentRenderLayer= 1)):
									if queryLayer != 'defaultRenderLayer':
										value = cmds.getAttr(Buffer[0] + '.' +Buffer[1] + '.value')
									else:
										if self.dp_hasOverride(queryValue, cmds.editRenderLayerGlobals(q= 1, currentRenderLayer= 1)):
											value = cmds.getAttr(Buffer[0] + '.' +Buffer[1] + '.value')
						findOverride = 1
						break		
				# if this layer has no override, change queryLayer to defaultLayer(masterLayer)
				queryLayerProx = 'defaultRenderLayer' if findOverride == 0 else queryLayerProx
			# return value
			if queryValue == 'defaultRenderGlobals.startFrame' or queryValue == 'defaultRenderGlobals.endFrame' or queryValue == 'fps':
				timeUnit = cmds.currentUnit(q= 1, t= 1) # mel.eval('currentTimeUnitToFPS')
				if timeUnit[-3:] == 'fps':
					value = round(round(value * 6000, 0) / (6000 / float(timeUnit.split('fps')[0])), 3) if queryValue != 'fps' else float(timeUnit.split('fps')[0])
				return {		# maya stores 'ticks/tps'(sec) behind, vvv-> frame = int(sec * tps) / tpf
						'game' : round(round(value * 6000, 0) / 400, 3)	if queryValue != 'fps' else 15.0,
						'film' : round(round(value * 6000, 0) / 250, 3)	if queryValue != 'fps' else 24.0,
						 'pal' : round(round(value * 6000, 0) / 240, 3)	if queryValue != 'fps' else 25.0,
						'ntsc' : round(round(value * 6000, 0) / 200, 3)	if queryValue != 'fps' else 30.0,
						'show' : round(round(value * 6000, 0) / 125, 3)	if queryValue != 'fps' else 48.0,
						'palf' : round(round(value * 6000, 0) / 120, 3)	if queryValue != 'fps' else 50.0,
					   'ntscf' : round(round(value * 6000, 0) / 100, 3)	if queryValue != 'fps' else 60.0,
					'millisec' : round(round(value * 6000, 0) /   6, 3) if queryValue != 'fps' else 1000.0,
						 'sec' : round(round(value * 6000, 0) / 6000, 3) if queryValue != 'fps' else (1/1.0),
						 'min' : round(round(value * 6000, 0) / 360000, 3) if queryValue != 'fps' else (1/60.0),
						'hour' : round(round(value * 6000, 0) / 21600000, 3) if queryValue != 'fps' else (1/3600.0),
				}.get(timeUnit, value)
			else:
				return value
		else:
			return cmds.getAttr(queryValue)


	def dp_hasOverride(self, queryValue, queryLayer):
		# checking value has overrided or not
		attrList = cmds.editRenderLayerAdjustment(queryLayer, q= 1, lyr= 1)
		has = 0
		if attrList:
			for attr in attrList:
				if attr == queryValue:
					has = 1 
					break
		return has


	def dp_canThisFloatBeInt(self, strNumber):

		if '.' in str(strNumber):
			return 1 if int(str(strNumber).split('.')[1]) == 0 else 0
		else:
			return 1


	def dp_frange(self, start, stop, step):

		i = start
		while i < stop:
			yield i
			i += step


	def dp_prScriptJobList(self, *args):

		for sj in cmds.scriptJob(lj= 1):
			if 'domino_mainUI' in sj and 'PostSceneRead' in sj:
				print sj.strip()





class MailSending:


	def dp_sendEmail(self, mode, *args):
			
		msg = email.mime.Multipart.MIMEMultipart()
		msg['From'] = cmds.textField('mailFromTxtF', q= 1, text= 1)
		msg['To'] = cmds.textField('mailToTxtF', q= 1, text= 1)
		password = cmds.textField('mailPassTxtF', q= 1, text= 1)
		smtp = cmds.textField('mailSmtpTxtF', q= 1, text= 1)
		scene = cmds.file(q= 1, sn= 1, shn= 1)
		hour = str(cmds.intField('hoursGapInt', q= 1, v= 1)) + 'Hour' + ('s' if cmds.intField('hoursGapInt', q= 1, v= 1) > 1 else '')
		#user = '{' + os.getenv('USERNAME') + '}'
		computer = ''
		body = ''

		if cmds.checkBox('showCompChk', q= 1, v= 1):
			computer = '[' + os.getenv('COMPUTERNAME') + ']'

		if mode == 'TEST':
			msg['Subject'] = 'PR -%s Testing Email' %(computer)
			body = email.mime.Text.MIMEText("""
			Hi!
			This is a <dp_Domino> testing mail.
			Email Notice is working.
			""")
		elif mode == 'START':
			msg['Subject'] = 'PR -%s Rendering Start - %s' %(computer, scene)
			body = email.mime.Text.MIMEText(self.dp_makeMailBody(mode))
		
		elif mode == 'DONE':
			msg['Subject'] = 'PR -%s Finished - %s' %(computer, scene)
			body = email.mime.Text.MIMEText(self.dp_makeMailBody(mode))
		
		elif mode == 'STOP':
			msg['Subject'] = 'PR -%s User Cancelled - %s' %(computer, scene)
			body = email.mime.Text.MIMEText(self.dp_makeMailBody(mode))

		elif mode == 'HOUR':
			msg['Subject'] = 'PR -%s %s Check - %s' %(computer, hour, scene)
			body = email.mime.Text.MIMEText(self.dp_makeMailBody(mode))
		
		else:
			newLayerName = dataGetFormat.dp_LayerNameForMail(mode)
			msg['Subject'] = 'PR -%s Layer: <%s> Done - %s' %(computer, newLayerName, scene)
			body = email.mime.Text.MIMEText(self.dp_makeMailBody(mode))
		
		msg.attach(body)
		
		try:
			s = smtplib.SMTP(smtp)
			s.starttls()
			s.login(msg['From'],password)
			s.sendmail(msg['From'],[msg['To']], msg.as_string())
			s.quit()
		except:
			cmds.warning('dp_Domino: E-mail sanding failed, might have internet connection problem...')


	def dp_makeMailBody(self, mode, *args):

		def dp_makeMailBody_frameRange(layer):

			frameRange = ''
			if cmds.attributeQuery('dp_userAttr_customFrameRange', node= layer, ex= 1):
				frameRange = cmds.getAttr(layer + '.dp_userAttr_customFrameRange')
			else:
				frameRange = cmds.text((layer + 'ProTxtStart'), q= 1, l= 1) + ' - ' + cmds.text((layer + 'ProTxtEnd'), q= 1, l= 1)
			return frameRange

		global renderMissionLayerSort

		scene = cmds.file(q=True, sn=True, shn=True)
		body = 'Scene :  ' + scene + '\n'
		if cmds.checkBox('fProChk', q= 1, v= 1):
			body += '*Mode :  Frame Priority\n'
		else:
			body += '*Mode :  Layer Priority\n'

		if mode == 'START':
			body += '*Mission :  ' + str(Render_Controls.dp_jobsCaculator(3, '')) + ' Layers, ' + str(Render_Controls.dp_jobsCaculator(1, '')) + ' Frames\n'
			body += '\n*Layers :  \n'
			for layer in renderMissionLayerSort:
				newLayerName = dataGetFormat.dp_LayerNameForMail(layer)
				frameRange = dp_makeMailBody_frameRange(layer)
				body += '             ' + newLayerName + '\n'
				body += '             ' + frameRange + '\n'
				body += '              -\n'
		
		elif mode == 'DONE' or mode == 'STOP':
			body += '*Mission ' + cmds.frameLayout('mainProFrame',q= 1, l= 1)
			body += '\n*Layers :  \n'
			for layer in renderMissionLayerSort:
				newLayerName = dataGetFormat.dp_LayerNameForMail(layer)
				frameRange = dp_makeMailBody_frameRange(layer)
				progress = int(float(cmds.progressBar(layer + 'ProBar', q= 1, pr= 1)) / float(cmds.progressBar(layer + 'ProBar', q= 1, max= 1)) * 100.0)
				currentFrame = cmds.text(layer + 'ProCurrFrame', q= 1, l= 1) if progress > 0 else ''
				elpTime = cmds.text((layer + 'elapsedTime'), q= 1, l= 1)
				if ':' not in elpTime:
					elpTime = dataGetFormat.dp_getFormattedRenderTime(int(float(elpTime)), 1) if elpTime != '0.0' else '--:--:--:--'
				if cmds.text((layer + 'ProStar'), q= 1, vis= 1):
					body += '     !!!  - ' + newLayerName + '\n'
				else:
					body += '             ' + newLayerName + '\n'
				body += '             ' + frameRange + '\n'
				body += '             ' + str(progress) + '%	' + currentFrame + '\n'
				body += '             ' + elpTime + '\n'
				body += '              -\n'

		elif mode == 'HOUR':
			body += '*Mission ' + cmds.frameLayout('mainProFrame',q= 1, l= 1)
			body += '\n*Layers :  \n'
			for layer in renderMissionLayerSort:
				newLayerName = dataGetFormat.dp_LayerNameForMail(layer)
				frameRange = dp_makeMailBody_frameRange(layer)
				progress = int(float(cmds.progressBar(layer + 'ProBar', q= 1, pr= 1)) / float(cmds.progressBar(layer + 'ProBar', q= 1, max= 1)) * 100.0)
				currentFrame = cmds.text(layer + 'ProCurrFrame', q= 1, l= 1) if progress > 0 else ''
				elpTime = cmds.text((layer + 'elapsedTime'), q= 1, l= 1)
				if ':' not in elpTime:
					elpTime = dataGetFormat.dp_getFormattedRenderTime(int(float(elpTime)), 1) if elpTime != '0.0' else '--:--:--:--'
				body += '             ' + newLayerName + '\n'
				body += '             ' + frameRange + '\n'
				body += '             ' + str(progress) + '%	' + currentFrame + '\n'
				body += '             ' + elpTime + '\n'
				body += '              -\n'

		else:
			mainEndTime = cmds.timer(lap= 1, n= 'dp_MainTimer')
			newLayerName = dataGetFormat.dp_LayerNameForMail(mode)
			frameRange = dp_makeMailBody_frameRange(mode)
			body += '*Mission Elapsed -  ' + dataGetFormat.dp_getFormattedRenderTime(int(mainEndTime), 1)
			body += '\n*Layer < ' + newLayerName + ' > is rendering done.'
			body += '\n*Frame : ' + frameRange + '\n'
			body += '*This layer\'s rendering time :  ' + cmds.text((mode + 'elapsedTime'), q= 1, l= 1)

		return body


	def dp_saveMailSetting(self, *args):

		config = 'superRenderMail.settings'

		if os.path.exists(config) is True:
			os.remove(config)
			
		sendFrom = cmds.textField('mailFromTxtF', q= 1, text= 1)
		password = cmds.textField('mailPassTxtF', q= 1, text= 1)
		sendTo = cmds.textField('mailToTxtF', q= 1, text= 1)
		smtp = cmds.textField('mailSmtpTxtF', q= 1, text= 1)
		
		password = password.encode('base64')
		
		dagConfig = {'sendFrom':sendFrom,'password':password, 'sendTo':sendTo, 'smtp':smtp}
		
		settingOutput = open(config, 'wb')
		cPickle.dump(dagConfig, settingOutput)
		settingOutput.close()

		#print 'Settings saved at ' + os.path.realpath(config)


	def dp_loadMailSetting(self, *args):

		config = 'superRenderMail.settings'
			
		if os.path.exists(config) is False:
			sendFrom =  'powerRenderMail@gmail.com'
			password = 'chucknorrisrender'
			sendTo = ''
			smtp = 'smtp.gmail.com:587'
		else:
			settingInput=open(config, 'rb')
			dagConfig = cPickle.load(settingInput)
			settingInput.close()
				
			sendFrom =  dagConfig['sendFrom']
			password = dagConfig['password'].decode('base64')
			sendTo = dagConfig['sendTo']
			smtp = dagConfig['smtp']

		return [sendFrom, password, sendTo, smtp]





class resetEnvironment:


	def dp_resetVar(self, *args):

		print '+ * + . + * + . + * + . + * + . + * + . + * + . + * + . + * + . + * + . + * + . + * + . + * + . + * + . + * +\n'
		
		global dp_Rendering
		dp_Rendering = 0
		print '		  Var: {dp_Rendering} Reseted to 0.'

		try:
			cmds.timer(e= 1, n= 'dp_MainTimer')
			print '		Timer: [dp_MainTimer] Reseted.'
		except:
			print '		Timer: [dp_MainTimer] was not started.'
		try:
			cmds.timer(e= 1, n= 'dp_HourTimer')
			print '		Timer: [dp_HourTimer] Reseted.'
		except:
			print '		Timer: [dp_HourTimer] was not started.'
		try:
			cmds.timer(e= 1, n= 'dp_FrameTimer')
			print '		Timer: [dp_FrameTimer] Reseted.'
		except:
			print '		Timer: [dp_FrameTimer] was not started.'

		#unlock controls
		UI_Controls.dp_lockUIControls(1)

		#close scriptEditor output record
		cmds.cmdFileOutput(ca= 1)
		print 'cmdFileOutput: All closed.'
		try:
			if cmds.file(dp_outputLogPath, q= 1, ex= 1):
				os.remove(dp_outputLogPath)
				print '	outputLog: file deleted.'
			else:
				print '	outputLog: no log file exists.'
		except:
			outputLog = open(dp_outputLogPath, 'w')
			outputLog.write('')
			outputLog.close()
			print '	outputLog: file cleared.'
		print 'outputLogPath: ' + dp_outputLogPath
		
		print '\n+ . + * + . + * + . + * + . + * + . + * + . + * + . + * + . + * + . + * + . + * + . + * + . + * + . + * + . +'
		cmds.warning('dp_Domino: Reseted. For more Info please check scriptEditor.')


	def dp_deletePRAttr(self, *args):

		print '+ * + . + * + . + * + . + * + . + * + . + * + . + * + . + * + . + * + . + * + . + * + . + * + . + * + . + * +\n'
		
		attrList = ['dp_userAttr_renderOrder',
					'dp_userAttr_hasExtraJob',
					'dp_userAttr_customFrameRange',
					'dp_userAttr_backward',
					'dp_userAttr_backwardInFramePrio',
					'dp_userAttr_FramePrio',
					'dp_userAttr_logList',
					'dp_userAttr_timeLog_Tmp',
					'dp_userAttr_timeLog_yyyymmddhhmmss',
					'dp_userAttr_timeLog_yyyymmddhhmmss_tabLabel',
					'dp_userAttr_DeleteJobs',
					'dp_userAttr_Resolution']
		
		print 'Deleteing [dp_userAttr_..] attributes...\n'
		print '--+--+--+--+--+--+--+--+--+--+--\n'

		for layer in cmds.ls(et= 'renderLayer'):
			print '	<' + layer + '> :'
			attrInNode = cmds.listAttr(layer, r= 1, ud= 1)
			attrDeleted = []
			if attrInNode:
				for attr in attrInNode:
					if attr in attrList or attr.startswith('dp_userAttr_timeLog_'):
						cmds.deleteAttr(layer, at= attr)
						attrDeleted.append(attr)
				if attrDeleted:
					print '			' + '\n			'.join(attrDeleted)
				else:
					print '			none'
			else:
				print '			none'

			print '\n--+--+--+--+--+--+--+--+--+--+--\n'

		print '+ . + * + . + * + . + * + . + * + . + * + . + * + . + * + . + * + . + * + . + * + . + * + . + * + . + * + . +'
		cmds.warning('dp_Domino: [dp_userAttr_..] attributes deleted. For more Info please check scriptEditor.')


	def dp_refreshLayerMenu_warning(self, *args):

		cmds.warning('dp_Domino: Refreshing layer optionMenu...')
		UI_Controls.dp_refreshLayerMenu()
		cmds.warning('dp_Domino: Layer optionMenu refreshed.')





class init_dp_Domino:


	def dp_envTest_uniqueTag(self):

		# Test the ui control 'textScrollList -uniqueTag'
		try:
			if cmds.window('utgFlagTest', ex= 1): cmds.deleteUI('utgFlagTest')
			cmds.window('utgFlagTest')
			cmds.paneLayout()
			cmds.textScrollList('textScrollListTest', a= ['can uniqueTag work?'], utg= ['dp_Domino: textScrollList -uniqueTag can work.'], sii= 1)
			print cmds.textScrollList('textScrollListTest', q= 1, sut= 1)[0]
			cmds.deleteUI('utgFlagTest')
		except:
			can_uniqueTag = 0


	def dp_deleteAndShowWindows(self):

		for window in ['domino_mainUI', 'domino_ProgressUI', 'domino_timeLogUI', 'domino_infoUI']:
			if cmds.window(window, ex= 1):
				cmds.deleteUI(window)
		if directly_Show_domino_ProgressUI_forTest:
			UI.dp_ProgressWindow()
		else:
			UI.dp_mainWindow()


	def dp_init(self):

		global dp_Rendering
		global dp_timeOut
		global dp_outputLogPath
		global dp_sceneQueueBox

		self.dp_envTest_uniqueTag()

		if 'dp_Rendering' not in globals():
			dp_Rendering = 0
			dp_timeOut = 0.01 # sec
			sceneName = cmds.file(q= 1, sn= 1, shn= 1) if cmds.file(q= 1, sn= 1, shn= 1) else 'untitled'
			worksPath = cmds.workspace(q= 1, fn= 1)
			thisDate = cmds.date(format='YYYYMMDDhhmmss')
			dp_outputLogPath = worksPath + '/scriptEditor_output_' + sceneName + '_' + thisDate + '.log'
			dp_sceneQueueBox = []
			self.dp_deleteAndShowWindows()
		else:
			if dp_Rendering:
				cmds.showWindow('domino_mainUI')
			else:
				self.dp_deleteAndShowWindows()







#_init classes

UI = UI()

UI_Controls = UI_Controls()

Render = Render()

Render_Controls = Render_Controls()

dataGetFormat = dataGetFormat()

vrayDRSupervisor = vrayDRSupervisor()

commonTool = commonTool()

MailSending = MailSending()

resetEnvironment = resetEnvironment()

init_dp_Domino = init_dp_Domino()




'''/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/'''
'''/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/ E N D /\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/'''
'''/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/'''
'''/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\ D O M I N O \/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/'''
'''/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/'''
'''/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\ by D A V I D .p \/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/'''
'''/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/'''