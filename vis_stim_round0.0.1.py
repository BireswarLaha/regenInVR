﻿import viz
import oculus
import steamvr
import vizfx
import globals
from globals import *
import vector3
from vector3 import *
import steamvr
import vizshape

viz.go()

#loading scene
#viz.add('piazza.osgb')
#viz.add('models/rockHall.osgb')
viz.add('models/sydney_opera_house.osgb')

#initializing the HMD
hmd = steamvr.HMD()
headTracker = hmd.getSensor()

# Setup navigation node and link to main view
navigationNode = viz.addGroup()
viewLink = viz.link(navigationNode, viz.MainView)

if headTracker is None:
	print "HMD is not connected!"
else:
	globals.headTrackingActive = True
	# Setup heading reset key
	vizact.onkeydown(KEYS['reset'], hmd.getSensor().reset)
	viewLink.preMultLinkable(headTracker)

# Setup arrow key navigation
MOVE_SPEED = 2.0
def move():
	if globals.headTrackingActive:
		headForwardDir = headTracker.getLineForward().getDir()
		forwardDir = Vec3ToVizardFloatList(getProjectionOfVectorOnPlane(vizardFloatListToVec3(headForwardDir), UP_VECTOR))
		backDir = [-forwardDir[0], -forwardDir[1], -forwardDir[2]]
		rightDir = Vec3ToVizardFloatList(vizardFloatListToVec3(forwardDir).Cross(UP_VECTOR))
		leftDir = [-rightDir[0], -rightDir[1], -rightDir[2]]
		upDir = Vec3ToVizardFloatList(UP_VECTOR)
		downDir = [-upDir[0], -upDir[1], -upDir[2]]
	currentPos = navigationNode.getPosition(viz.ABS_GLOBAL)
	newPos = [currentPos[0], currentPos[1], currentPos[2]]
	yaw,pitch,roll = navigationNode.getEuler()
	m = viz.Matrix.euler(yaw,0,0)
	dm = viz.getFrameElapsed() * MOVE_SPEED
	deltaYaw = 0
	if viz.key.isDown(KEYS['forward']) or viz.key.isDown('w'):
		m.preTrans([0,0,dm])
		if globals.headTrackingActive:
			newPos = [currentPos[0] + forwardDir[0] * dm, currentPos[1] + forwardDir[1] * dm, currentPos[2] + forwardDir[2] * dm]
	if viz.key.isDown(KEYS['back']) or viz.key.isDown('s'):
		m.preTrans([0,0,-dm])
		if globals.headTrackingActive:
			newPos = [currentPos[0] + backDir[0] * dm, currentPos[1] + backDir[1] * dm, currentPos[2] + backDir[2] * dm]
	if viz.key.isDown(KEYS['left']) or viz.key.isDown('a'):
		m.preTrans([-dm,0,0])
		if globals.headTrackingActive:
			newPos = [currentPos[0] + leftDir[0] * dm, currentPos[1] + leftDir[1] * dm, currentPos[2] + leftDir[2] * dm]
	if viz.key.isDown(KEYS['right']) or viz.key.isDown('d'):
		m.preTrans([dm,0,0])
		if globals.headTrackingActive:
			newPos = [currentPos[0] + rightDir[0] * dm, currentPos[1] + rightDir[1] * dm, currentPos[2] + rightDir[2] * dm]
	if viz.key.isDown(' '):
		m.preTrans([0,dm,0])
		if globals.headTrackingActive:
			newPos = [currentPos[0] + upDir[0] * dm, currentPos[1] + upDir[1] * dm, currentPos[2] + upDir[2] * dm]
	if viz.key.isDown(viz.KEY_CONTROL_L):
		m.preTrans([0,-dm,0])
		if globals.headTrackingActive:
			newPos = [currentPos[0] + downDir[0] * dm, currentPos[1] + downDir[1] * dm, currentPos[2] + downDir[2] * dm]
	if viz.key.isDown('e'):
		yaw += 1
		deltaYaw = 1
	if viz.key.isDown('q'):
		yaw -= 1
		deltaYaw = -1
	if not globals.headTrackingActive:
		newPos = [currentPos[0] + m.getPosition()[0], currentPos[1] + m.getPosition()[1], currentPos[2] + m.getPosition()[2]]
		navigationNode.setEuler(yaw,pitch,roll)
	navigationNode.setPosition(newPos, viz.ABS_GLOBAL)
#	if (m.getPosition()[0] + m.getPosition()[0] + m.getPosition()[0] <> 0):
#		print m.getPosition()
vizact.ontimer(0,move)

keysToBeIgnored = []
keysToBeIgnored.append(KEYS['forward'])
keysToBeIgnored.append(KEYS['back'])
keysToBeIgnored.append(KEYS['left'])
keysToBeIgnored.append(KEYS['right'])
keysToBeIgnored.append(KEYS['reset'])
keysToBeIgnored.append(KEYS['camera'])
keysToBeIgnored.append(KEYS['help'])

