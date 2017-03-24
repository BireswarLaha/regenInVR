#DK2 demo
import viz
import oculus
import steamvr
import vizfx
import globals
from globals import *
import vector3
from vector3 import *
import steamvr
import vizshape

#######################################################
#LOADING A BASIC SCENE FOR TESTING
viz.go()

#viz.add('piazza.osgb')
viz.add('models/rockHall.osgb')
#viz.add('piazza_animations.osgb')
#######################################################

# Setup Oculus Rift HMD
headTracker = None
hmd = oculus.Rift()
headTracker = hmd.getSensor()

if not headTracker:
	hmd = steamvr.HMD()
	headTracker = hmd.getSensor()
else:
	globals.hmdType = "RIFT"

# Setup navigation node and link to main view
navigationNode = viz.addGroup()
viewLink = viz.link(navigationNode, viz.MainView)

if headTracker is None:
	print "Rift is not connected!"
else:
	globals.headTrackingActive = True
	# Setup heading reset key
	vizact.onkeydown(KEYS['reset'], hmd.getSensor().reset)
	viewLink.preMultLinkable(headTracker)

# Apply user profile eye height to view
profile = None
if globals.hmdType == "RIFT":
	profile = hmd.getProfile()
	if profile:
		viewLink.setOffset([0,profile.eyeHeight,0])
	else:
		viewLink.setOffset([0,1.8,0])

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

#adding a video
video = viz.addVideo('media/movie1.avi')

#Adding a quad to show a movie
videoRenderingBoard = viz.addTexQuad()
videoRenderingBoard.texture(video)
#videoRenderingBoard.setPosition([0.0, 0.0, 0.0], mode = viz.REL_PARENT)
videoRenderingBoard.setPosition([0.0, 1.0, 1.0])
video.loop()
video.play()

videoRenderingBoard.visible(False)

#Adding a sphere to show a movie
DEFAULT_SPHERE_RADIUS = 0.5
DEFAULT_SPHERE_POSITION = [2.0, 1.0, 1.0]
videoRenderingSphere = vizshape.addSphere(radius=DEFAULT_SPHERE_RADIUS, slices = 32, stacks = 32, flipFaces=True, cullFace=True, lighting=True)
videoRenderingSphere.texture(video)
videoRenderingSphere.setPosition(DEFAULT_SPHERE_POSITION)
videoRenderingSphere.visible(False)
sphereLink = viz.link(headTracker, videoRenderingSphere)
sphereLink.setMask(viz.LINK_POS)
sphereLink.disable()

def unlinkAndResetSphere():
	global sphereLink, DEFAULT_SPHERE_POSITION, videoRenderingSphere
	sphereLink.disable()
	videoRenderingSphere.setPosition(DEFAULT_SPHERE_POSITION)

#Adding a box to show a movie
DEFAULT_BOX_SIDE_LENGTH = 1.0
DEFAULT_BOX_POSITION = [-2.0, 1.0, 1.0]
videoRenderingBox = vizshape.addBox(size=[DEFAULT_BOX_SIDE_LENGTH, DEFAULT_BOX_SIDE_LENGTH, DEFAULT_BOX_SIDE_LENGTH], flipFaces=True, cullFace=True, lighting=True)
videoRenderingBox.texture(video)
videoRenderingBox.setPosition(DEFAULT_BOX_POSITION)
videoRenderingBox.visible(False)
boxLink = viz.link(headTracker, videoRenderingBox)
boxLink.setMask(viz.LINK_POS)
boxLink.disable()

def unlinkAndResetBox():
	global boxLink, DEFAULT_BOX_POSITION, videoRenderingBox
	boxLink.disable()
	videoRenderingBox.setPosition(DEFAULT_BOX_POSITION)

def onKeyDown(key):
	global videoRenderingBoard, videoRenderingSphere, videoRenderingBox, keysToBeIgnored
	global sphereLink, boxLink, DEFAULT_SPHERE_POSITION, DEFAULT_BOX_POSITION
	print "key = " + str(key)

	if key in keysToBeIgnored:
		print "ignoring the key press in onKeyDown function"
#	elif key is 'p':
#		print "videoRenderingBoard.getPosition(viz.ABS_GLOBAL) = " + str(videoRenderingBoard.getPosition(viz.ABS_GLOBAL))
#		print "videoRenderingBoard.getPosition(viz.ABS_PARENT) = " + str(videoRenderingBoard.getPosition(viz.ABS_PARENT))
#		print "videoRenderingBoard.getPosition(viz.ABS_LOCAL) = " + str(videoRenderingBoard.getPosition(viz.ABS_LOCAL))
	elif key is '1': #visibility toggle
		unlinkAndResetBox()
		unlinkAndResetSphere()
		print "toggling the visibility of the stimulus screens"
		videoRenderingBoard.visible(viz.TOGGLE)
		videoRenderingSphere.visible(viz.TOGGLE)
		videoRenderingBox.visible(viz.TOGGLE)
	elif key is '2': #box viewing
		unlinkAndResetSphere()
		if boxLink.getEnabled():
			print "disabling the box link now ..."
			unlinkAndResetBox()
		else:
			print "enabling the box link now ..."
			boxLink.enable()
#			boxLink.postTrans([0.0, 0.0, 0.4])
#			boxLink.setOffset([0.0, 0.0, 0.4])
	elif key is '3': #sphere link
		unlinkAndResetBox()
		if sphereLink.getEnabled():
			print "disabling the sphere link now ..."
			unlinkAndResetSphere()
		else:
			print "enabling the sphere link now ..."
			sphereLink.enable()
#		print "setting parent of the infoboard as the headtracker ..."
#		videoRenderingBoard.setParent(headTracker)
#		videoRenderingBoard.setPosition(0.0, 0.0, -1.0, viz.ABS_PARENT)
#	elif key is '3':
#		print "setting parent of the infoboard as the WORLD ..."
#		videoRenderingBoard.clearParents()
#		videoRenderingBoard.setParent(viz.WORLD)
#		videoRenderingBoard.setPosition([0.0, 1.0, 0.0])

viz.callback(viz.KEYDOWN_EVENT, onKeyDown, priority=-10)
