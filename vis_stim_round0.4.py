#Developed on Vizard sample code, titled 'steamvrExample.py'
#Bireswar Laha, Huberman Lab, Department of Neurobiology, Stanford University
#Dated: March-May, 2017

import sys
import viz
import vizfx
import vizact
import vizinfo
import viztask
import steamvr
import vector3
import vizcam
import view_fader

####saving data during the stimulation runs
import os
import csv
import time
import datetime

#create a data directory for writing data at runtime
dataDir = 'data/'
dataFile = 'random_data.csv'
#print(os.path.isdir("data"))
if not os.path.exists(dataDir):
	print "creating data directory"
	os.makedirs(dataDir)
else:
	print "data directory existing"

fieldnames = ['ID', 'stim1time', 'stim2time', 'stim3time', 'stim4time', 'stim5time', 'stim6time', 'stim7time', 'stim8time', 'stim9time', 'stim10time']

ID = int(time.time())
print "ID = " + str(ID)
print "time = " + str(datetime.datetime.utcfromtimestamp(ID))

stim1time = stim2time = stim3time = stim4time = stim5time = stim6time = stim7time = stim8time = stim9time = stim10time = 0

#open a CSV file at the beginning
dataFilePresent = os.path.isfile(dataDir + dataFile)

if not dataFilePresent:
	print "creating data file and writing the header"
	with open(dataDir + dataFile, 'w') as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()
		print "adding the first data line to the data file"
		writer.writerow({'ID': ID, 'stim1time': stim1time, 'stim2time': stim2time, 'stim3time': stim3time, 'stim4time': stim4time, 'stim5time': stim5time, 'stim6time': stim6time, 'stim7time': stim7time, 'stim8time': stim8time, 'stim9time': stim9time, 'stim10time': stim10time})
else:
	print "data file is present in the data folder already"
	with open(dataDir + dataFile, 'a') as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		print "appending another data line to the data file"
		writer.writerow({'ID': ID, 'stim1time': stim1time, 'stim2time': stim2time, 'stim3time': stim3time, 'stim4time': stim4time, 'stim5time': stim5time, 'stim6time': stim6time, 'stim7time': stim7time, 'stim8time': stim8time, 'stim9time': stim9time, 'stim10time': stim10time})

#write out data to the file at the start and end of stimulation, and flush the cache!
def writeData():
	print "Updating datafile"
	print "Datafile updated"

#close the file at the end of the program run

totalLengthOfEachStimulationSessionInSeconds = 180 #the length of each stimulation session in seconds
width = 0.11	#http://doc-ok.org/?p=1414 - Vive has approximately 100 degrees HFOV at 10 mm screen separation from the eyes
height = 0.11	#http://doc-ok.org/?p=1414 - Vive has approximately 110 degrees VFOV at 10 mm screen separation from the eyes
scale = 5.25
gapFromViveScreens = 0.43

# Initialize window
viz.setMultiSample(8)
viz.go()

colorSaturationValue = 0.5
viz.clearcolor(colorSaturationValue, colorSaturationValue, colorSaturationValue)

choices = ['experimental condition', 'control condition']
stimuliChoices = ['dense', 'sparse']
conditionChosen = viz.choose('Choose the condition for this run: ', choices)
print 'Group chosen:',choices[conditionChosen]

if 'experimental condition' == choices[conditionChosen]:
	stimChosen = viz.choose('Select stimulation: ', stimuliChoices)
	print 'Stimulation chosen:', stimuliChoices[stimChosen]

# Setup SteamVR HMD
hmd = None
hmd = steamvr.HMD()
if (hmd is not None) and (not hmd.getSensor()):
	sys.exit('SteamVR HMD not detected')

# Setup navigation node and link to main view
navigationNode = viz.addGroup()
viewLink = viz.link(navigationNode, viz.MainView)
if (hmd is not None) and (hmd.getSensor()):
	viewLink.preMultLinkable(hmd.getSensor())
else:
	tracker = vizcam.addKeyboard6DOF()
	tracker.setPosition([0,1.8,0])
	viz.link(tracker, viz.MainView)
	
# Load environment
gallery = vizfx.addChild('models/galleryWithoutPaintings.osgb')
gallery.hint(viz.OPTIMIZE_INTERSECT_HINT)
gallery.disable(viz.SHADOW_CASTING)

paintingsDictionary = {}

#load paintings
numberOfPaintings = 11
paintings = [None] * numberOfPaintings
positionOfTex = [None] * numberOfPaintings
eulerOfTex = [None] * numberOfPaintings
sizeOfTex = [None] * numberOfPaintings

#0-(numberOfPaintings-1) paintingsInTheBackground are the texquads for the paintings
#numberOfPaintings-(2*numberOfPaintings-1) paintingsInTheBackground are the black osgbs, hiding the main paintings
paintingsInTheBackground = [None] * (numberOfPaintings * 2)

pathToTextureForPainting = [None] * numberOfPaintings
pathToTextureForPainting[0] = 'textures/painting_picasso.png'
pathToTextureForPainting[1] = 'textures/painting_dali-memory.png'
pathToTextureForPainting[2] = 'textures/painting_van-gogh.png'
pathToTextureForPainting[3] = 'textures/painting_monet-venice.png'
pathToTextureForPainting[4] = 'textures/painting_scream.png'
pathToTextureForPainting[5] = 'textures/painting_starry-night.png'
pathToTextureForPainting[6] = 'textures/painting_harring-bestbuddies.png'
pathToTextureForPainting[7] = 'textures/painting_monalisa.png'
pathToTextureForPainting[8] = 'textures/painting_warhol_soup.png'
pathToTextureForPainting[9] = 'textures/painting_birth-of-venus.png'
pathToTextureForPainting[10] = 'textures/painting_magritte.png'

positionOfTex[0] = [-4.90514, 1.55, 0.32]
positionOfTex[1] = [-4.90389, 1.65, 2.53]
positionOfTex[2] = [-4.90372, 1.75, 4.8]
positionOfTex[3] = [-4.89718, 1.8, 6.71429]
positionOfTex[4] = [-3.3, 2.2, 9.05103]
positionOfTex[5] = [0.0, 2.1, 9.9]
positionOfTex[6] = [3.11735, 2.27, 9.2]
positionOfTex[7] = [4.80222, 2.3, 6.75]
positionOfTex[8] = [4.80513, 2.2, 4.65]
positionOfTex[9] = [4.80061, 2.4, 2.5]
positionOfTex[10] = [4.79488, 2.57, 0.29]

eulerOfTex[0] = [-90.0, 0.0, 0.0]
eulerOfTex[1] = [-90.0, 0.0, 0.0]
eulerOfTex[2] = [-90.0, 0.0, 0.0]
eulerOfTex[3] = [-90.0, 0.0, 0.0]
eulerOfTex[4] = [-30.0, 0.0, 0.0]
eulerOfTex[5] = [0.0, 0.0, 0.0]
eulerOfTex[6] = [30.0, 0.0, 0.0]
eulerOfTex[7] = [90.0, 0.0, 0.0]
eulerOfTex[8] = [90.0, 0.0, 0.0]
eulerOfTex[9] = [90.0, 0.0, 0.0]
eulerOfTex[10] = [90.0, 0.0, 0.0]

sizeOfTex[0] = [0.81, 1.09]
sizeOfTex[1] = [2.08, 1.37]
sizeOfTex[2] = [0.87, 1.23]
sizeOfTex[3] = [1.35, 0.90]
sizeOfTex[4] = [1.42, 1.90]
sizeOfTex[5] = [2.59, 1.63]
sizeOfTex[6] = [2.12, 1.52]
sizeOfTex[7] = [0.99, 1.41]
sizeOfTex[8] = [1.07, 1.65]
sizeOfTex[9] = [1.68, 1.21]
sizeOfTex[10] = [1.21, 1.71]

#backgroundBlackTex = viz.addTexture('textures/blackSquare.png')
#backgroundBlackTex = viz.addTexture('textures/skyBlue.png')
backgroundBlackTex = viz.addTexture('textures/blackSquare.png')
for i in range(numberOfPaintings):
	paintings[i] = viz.addTexQuad(size=sizeOfTex[i])
	textureForPainting = viz.addTexture(pathToTextureForPainting[i])
	paintings[i].texture(backgroundBlackTex)
	paintings[i].texture(textureForPainting,'',1)
	paintings[i].texblend(0.0, '', 1)
	paintings[i].setPosition(positionOfTex[i])
	paintings[i].setEuler(eulerOfTex[i])
	paintingsInTheBackground[i] = paintings[i]
	print "name of this tex quad node = " + str(paintingsInTheBackground[i].getNodeNames())

#painting_birth_of_venus = vizfx.addChild('models/painting_birth-of-venus.osgb')
#paintingsDictionary['painting_birth-of-venus'] = painting_birth_of_venus
#
#painting_dali_memory = vizfx.addChild('models/painting_dali-memory.osgb')
#paintingsDictionary['painting_dali-memory'] = painting_dali_memory
#
#painting_harring_bestbuddies = vizfx.addChild('models/painting_harring-bestbuddies.osgb')
#paintingsDictionary['painting_harring-bestbuddies'] = painting_harring_bestbuddies
#
#painting_magritte = vizfx.addChild('models/painting_magritte.osgb')
#paintingsDictionary['painting_magritte'] = painting_magritte
#
#painting_monalisa = vizfx.addChild('models/painting_monalisa.osgb')
#paintingsDictionary['painting_monalisa'] = painting_monalisa
#
#painting_monet_venice = vizfx.addChild('models/painting_monet-venice.osgb')
#paintingsDictionary['painting_monet-venice'] = painting_monet_venice
#
#painting_picasso = vizfx.addChild('models/painting_picasso.osgb')
#paintingsDictionary['painting_picasso'] = painting_picasso
#
#painting_scream = vizfx.addChild('models/painting_scream.osgb')
#paintingsDictionary['painting_scream'] = painting_scream
#
#painting_starry_night = vizfx.addChild('models/painting_starry-night.osgb')
#paintingsDictionary['painting_starry-night'] = painting_starry_night
#
#painting_van_gogh = vizfx.addChild('models/painting_van-gogh.osgb')
#paintingsDictionary['painting_van-gogh'] = painting_van_gogh
#
#painting_warhol_soup = vizfx.addChild('models/painting_warhol_soup.osgb')
#paintingsDictionary['painting_warhol_soup'] = painting_warhol_soup

#painting_birth_of_venus.visible(False)
#painting_dali_memory.visible(False)
#painting_harring_bestbuddies.visible(False)
#painting_magritte.visible(False)
#painting_monalisa.visible(False)
#painting_monet_venice.visible(False)
#painting_picasso.visible(False)
#painting_scream.visible(False)
#painting_starry_night.visible(False)
#painting_van_gogh.visible(False)
#painting_warhol_soup.visible(False)
#
painting_birth_of_venus_black = vizfx.addChild('models/painting_birth-of-venus_black.osgb')
paintingsDictionary['painting_birth-of-venus_black'] = painting_birth_of_venus_black
#paintingsDictionary['painting_birth-of-venus_black'].visible(False)
paintingsInTheBackground[0 + numberOfPaintings] = painting_birth_of_venus_black

painting_dali_memory_black = vizfx.addChild('models/painting_dali-memory_black.osgb')
paintingsDictionary['painting_dali-memory_black'] = painting_dali_memory_black
#paintingsDictionary['painting_dali-memory_black'].visible(False)
paintingsInTheBackground[1 + numberOfPaintings] = painting_dali_memory_black

painting_harring_bestbuddies_black = vizfx.addChild('models/painting_harring-bestbuddies_black.osgb')
paintingsDictionary['painting_harring-bestbuddies_black'] = painting_harring_bestbuddies_black
#paintingsDictionary['painting_harring-bestbuddies_black'].visible(False)
paintingsInTheBackground[2 + numberOfPaintings] = painting_harring_bestbuddies_black

painting_magritte_black = vizfx.addChild('models/painting_magritte_black.osgb')
paintingsDictionary['painting_magritte_black'] = painting_magritte_black
#paintingsDictionary['painting_magritte_black'].visible(False)
paintingsInTheBackground[3 + numberOfPaintings] = painting_magritte_black

painting_monalisa_black = vizfx.addChild('models/painting_monalisa_black.osgb')
paintingsDictionary['painting_monalisa_black'] = painting_monalisa_black
#paintingsDictionary['painting_monalisa_black'].visible(False)
paintingsInTheBackground[4 + numberOfPaintings] = painting_monalisa_black

painting_monet_venice_black = vizfx.addChild('models/painting_monet-venice_black.osgb')
paintingsDictionary['painting_monet-venice_black'] = painting_monet_venice_black
#paintingsDictionary['painting_monet-venice_black'].visible(False)
paintingsInTheBackground[5 + numberOfPaintings] = painting_monet_venice_black

painting_picasso_black = vizfx.addChild('models/painting_picasso_black.osgb')
paintingsDictionary['painting_picasso_black'] = painting_picasso_black
#paintingsDictionary['painting_picasso_black'].visible(False)
paintingsInTheBackground[6 + numberOfPaintings] = painting_picasso_black

painting_scream_black = vizfx.addChild('models/painting_scream_black.osgb')
paintingsDictionary['painting_scream_black'] = painting_scream_black
#paintingsDictionary['painting_scream_black'].visible(False)
paintingsInTheBackground[7 + numberOfPaintings] = painting_scream_black

painting_starry_night_black = vizfx.addChild('models/painting_starry-night_black.osgb')
paintingsDictionary['painting_starry-night_black'] = painting_starry_night_black
#paintingsDictionary['painting_starry-night_black'].visible(False)
paintingsInTheBackground[8 + numberOfPaintings] = painting_starry_night_black

painting_van_gogh_black = vizfx.addChild('models/painting_van-gogh_black.osgb')
paintingsDictionary['painting_van-gogh_black'] = painting_van_gogh_black
#paintingsDictionary['painting_van-gogh_black'].visible(False)
paintingsInTheBackground[9 + numberOfPaintings] = painting_van_gogh_black

painting_warhol_soup_black = vizfx.addChild('models/painting_warhol_soup_black.osgb')
paintingsDictionary['painting_warhol_soup_black'] = painting_warhol_soup_black
#paintingsDictionary['painting_warhol_soup_black'].visible(False)
paintingsInTheBackground[10 + numberOfPaintings] = painting_warhol_soup_black

#fader
#fader = view_fader.addFader()
#fader.fadeInTask()

#Create skylight
viz.MainView.getHeadLight().disable()
sky_light = viz.addDirectionalLight(euler=(0,90,0), color=viz.WHITE)
sky_light.setShadowMode(viz.SHADOW_DEPTH_MAP)

# Create effect for highlighting objects
code = """
Effect {
	Type Highlight
	Shader {
		BEGIN FinalColor
		gl_FragColor.rgb = mix(gl_FragColor.rgb, vec3(0.0, 1.0, 1.0), 0.5);
		END
	}
}
"""
highlightEffect = viz.addEffect(code)

# Map painting name to jump location
JUMP_LOCATIONS = {   'painting_picasso': [-3.4, -0.00000, 0.42632]
					,'painting_dali-memory': [-3.4, 0.00000, 2.61695]
					,'painting_van-gogh': [-3.4, -0.00000, 4.85902]
					,'painting_monet-venice': [-3.4, -0.00000, 6.79640]
					,'painting_scream': [-2.00545, 0.00000, 7.09077]
					,'painting_starry-night': [0.0, 0.00000, 8.0]
					,'painting_harring-bestbuddies': [2.35362, -0.00000, 7.05530]
					,'painting_monalisa': [3.4, 0.00000, 6.89882]
					,'painting_warhol_soup': [3.4, 0.00000, 4.62012]
					,'painting_birth-of-venus': [3.4, -0.00000, 2.19906]
					,'painting_magritte': [3.4, 0.00000, 0.07459]
}
paintingNames = []
dictionaryMappingPaintingNamesToVideoListIndex = {}

paintingNames.append('painting_picasso')
dictionaryMappingPaintingNamesToVideoListIndex['painting_picasso'] = 0

paintingNames.append('painting_dali-memory')
dictionaryMappingPaintingNamesToVideoListIndex['painting_dali-memory'] = 1

paintingNames.append('painting_van-gogh')
dictionaryMappingPaintingNamesToVideoListIndex['painting_van-gogh'] = 2

paintingNames.append('painting_monet-venice')
dictionaryMappingPaintingNamesToVideoListIndex['painting_monet-venice'] = 3

paintingNames.append('painting_scream')
dictionaryMappingPaintingNamesToVideoListIndex['painting_scream'] = 4

paintingNames.append('painting_starry-night')
dictionaryMappingPaintingNamesToVideoListIndex['painting_starry-night'] = 5

paintingNames.append('painting_harring-bestbuddies')
dictionaryMappingPaintingNamesToVideoListIndex['painting_harring-bestbuddies'] = 6

paintingNames.append('painting_monalisa')
dictionaryMappingPaintingNamesToVideoListIndex['painting_monalisa'] = 7

paintingNames.append('painting_warhol_soup')
dictionaryMappingPaintingNamesToVideoListIndex['painting_warhol_soup'] = 8

paintingNames.append('painting_birth-of-venus')
dictionaryMappingPaintingNamesToVideoListIndex['painting_birth-of-venus'] = 9

paintingNames.append('painting_magritte')
dictionaryMappingPaintingNamesToVideoListIndex['painting_magritte'] = 10

from random import randint
itemIndexWithNoStimulation = randint(0,10)
#itemIndexWithNoStimulation = 10
#print "itemIndexWithNoStimulation = " + str(itemIndexWithNoStimulation)
#print "painting without stimulation for this round is " + str(paintingNames[itemIndexWithNoStimulation])
print "\nPainting without stimulation is " + str(itemIndexWithNoStimulation) + "." + str(paintingNames[itemIndexWithNoStimulation])

# Create quad for flashing screen during jump
jump_flash = viz.addTexQuad(size=100, pos=[0,0,1], color=viz.BLACK)
jump_flash.setReferenceFrame(viz.RF_EYE)
jump_flash.disable([viz.LIGHTING, viz.INTERSECTION, viz.DEPTH_TEST, viz.SHADOW_CASTING])
jump_flash.blendFunc(viz.GL_ONE, viz.GL_ONE)
jump_flash.drawOrder(100)
jump_flash.visible(False)

def IntersectController(controller):
	"""Perform intersection using controller"""
	line = controller.model.getLineForward(viz.ABS_GLOBAL, length=100.0)
	return viz.intersect(line.begin, line.end)

def HighlightPainting(name, mode):
	"""Apply/Unapply highlight effect from specified painting"""
	if name:
		
		nameNew = name + "_black"
		splitNames = nameNew.split("-")
		
#		print "name = " + name
		
		global paintingsDictionary

#		if paintingsDictionary[nameNew].getVisible() == False:
#			nameNew = nameNew + "_black"

		if mode:
#			gallery.apply(highlightEffect, node=name)
			paintingsDictionary[nameNew].apply(highlightEffect, node=name)
		else:
#			gallery.unapply(highlightEffect, node=name)
			paintingsDictionary[nameNew].unapply(highlightEffect, node=name)

def HighlightTask(controller):
	"""Task that highlights jump locations pointed at by controller"""

	# Show controller pointer
	controller.line.visible(True)

	# Update highlight every frame
	last_highlight = ''
	try:
		while True:

			# Intersect pointer with scene
			info = IntersectController(controller)
			
#			if ((info.name != "drawable") and (info.name != "whitewall") and (info.name != "frame")):
#				print "name of object intersected with = " + str(info.name)
			
			# Check if name is a jump location painting
			node_name = info.name if info.name in JUMP_LOCATIONS else ''

			# Update highlight state if selected painting changed
			if last_highlight != node_name:
				controller.setVibration(0.001)
				HighlightPainting(last_highlight, False)
				last_highlight = node_name
				HighlightPainting(last_highlight, True)

			# Wait for next frame
			yield None

	finally:

		# Remove highlight when task finishes
		HighlightPainting(last_highlight, False)

		# Hide controller pointer
		controller.line.visible(False)

previousPaintingName = None
previousVidListIndex = -1
videoListIndex = None
def JumpTask(controller):
	"""Task that users trigger button press/release to jump to painting locations"""
	while True:

		# Wait for trigger to press
		yield viztask.waitSensorDown(controller, steamvr.BUTTON_TRIGGER)

		# Start highlighting task
		highlightTask = viztask.schedule(HighlightTask(controller))

		# Wait for trigger to release
		yield viztask.waitSensorUp(controller, steamvr.BUTTON_TRIGGER)

		# Stop highlighting task
		highlightTask.remove()

		# Intersect pointer with scene
		info = IntersectController(controller)
		if info.name in JUMP_LOCATIONS:
			
			nameToTest = info.name

			# Move navigation node to jump location
			jumpPos = list(JUMP_LOCATIONS[info.name])
			viewPos = viz.MainView.getPosition()
			navPos = navigationNode.getPosition()
			jumpPos[0] = jumpPos[0] - (viewPos[0] - navPos[0])
			jumpPos[2] = jumpPos[2] - (viewPos[2] - navPos[2])
			navigationNode.setPosition(jumpPos)
			
			# Display jump flash
			jump_flash.visible(True)
			jump_flash.runAction(vizact.fadeTo(viz.BLACK, begin=viz.WHITE, time=2.0, interpolate=vizact.easeOutStrong))
			jump_flash.addAction(vizact.method.visible(False))

			global itemIndexWithNoStimulation, paintingNames, canvasForStim, canvasWithoutStim, canvasForInitMsg, paintingsDictionary, dictionaryMappingPaintingNamesToVideoListIndex, sparseVideoPaths, fader
			global leftVideoRenderingBoard, rightVideoRenderingBoard, videoRenderingBoard, totalLengthOfEachStimulationSessionInSeconds, videoLoopsRemaining, maxNumberOfVideoLoops, trackpadState
			global paintings, stimulate, videoListIndex, paintingIndex, previousPaintingName, previousVidListIndex

			# Hide instruction canvasForInitMsg after first jump
			canvasForInitMsg.visible(False)

			separationOnHorizontalPlane = 0.8
			verticalPosOfCanvas = 0.6
			normalizedDirectionToShiftTheCanvas = vector3.Vec3ToVizardFloatList(vector3.vizardFloatListToVec3([-info.normal[0], 0.0, -info.normal[2]]).normalize())

			videoListIndex = dictionaryMappingPaintingNamesToVideoListIndex[info.name]
			paintingIndex = dictionaryMappingPaintingNamesToVideoListIndex[info.name]
			if videoListIndex > itemIndexWithNoStimulation: videoListIndex -= 1	#this is under the assumption that the indices of the videos associated to the canvases go up from 0 to 10, ignoring the index for the item to be ignored
			paintingsDictionary[info.name + "_black"].visible(False)

			if (info.name != paintingNames[itemIndexWithNoStimulation]):
				#visual stimulation ready to be taken
				stimulate = True
				print "\n==========================\nPainting: " + info.name + ". Video: " + sparseVideoPaths[videoListIndex] + ". Index# " + str(videoListIndex)
				printMessageAtTheStartOfCycle()
			else:
				#visual stimulation unavailable or already taken
				print "\n=========================\nPainting: " + info.name + ". The visual stimulation here is either unavailable, or is complete for this round. Please check other canvases."
				paintings[paintingIndex].texblend(1.0, '', 1)
				stimulate = False

			#show the previous empty canvas if the stimulation is incomplete there
			if (previousPaintingName is not None) and (previousVidListIndex != -1) and (previousPaintingName != paintingNames[itemIndexWithNoStimulation]) and (videoLoopsRemaining[previousVidListIndex] > 0):	#stimulation is not complete at the previous canvas
				paintingsDictionary[previousPaintingName + "_black"].visible(True)
			previousPaintingName = info.name
			previousVidListIndex = videoListIndex

# Add controllers
theControllerToUse = None
theControllerNOTtoUse = None

controllerModel = None

controllerCounter = 0
for controller in steamvr.getControllerList():

	# Create model for controller
	controller.model = controller.addModel(parent=navigationNode)
	controller.model.disable(viz.INTERSECTION)
	viz.link(controller, controller.model)
	controllerModel = controller.model

	# Create pointer line for controller
	viz.startLayer(viz.LINES)
	viz.vertexColor(viz.WHITE)
	viz.vertex([0,0,0])
	viz.vertex([0,0,100])
	controller.line = viz.endLayer(parent=controller.model)
	controller.line.disable([viz.INTERSECTION, viz.SHADOW_CASTING])
	controller.line.visible(False)

	# Setup task for triggering jumps using controller
	viztask.schedule(JumpTask(controller))

	if controllerCounter == 0:
		theControllerToUse = controller
	else:
		theControllerNOTtoUse = controller
	controllerCounter += 1

# Register callback for sensor down event
trackpadState = 0
stimulate = False
vidLoopsRemaining = -1

visibilityArray = [None] * (numberOfPaintings * 2)
def setBackgroundVisibility(visibility = False):
	global gallery, painting_birth_of_venus_black, painting_dali_memory_black, painting_harring_bestbuddies_black, painting_magritte_black
	global painting_monalisa_black, painting_monet_venice_black, painting_picasso_black, painting_scream_black, painting_starry_night_black
	global painting_van_gogh_black, painting_warhol_soup_black, paintingsInTheBackground, numberOfPaintings, visibilityArray
	global controllerModel, theControllerToUse, theControllerNOTtoUse
	
	gallery.visible(visibility)
#	controllerModel.visible(visibility)
	if theControllerToUse is not None: theControllerToUse.model.visible(visibility)
	if theControllerNOTtoUse is not None: theControllerNOTtoUse.model.visible(visibility)
	
	if visibility == False:
		#save the current visibility in a global array, and hide all paintingsInTheBackground
		for i in range(numberOfPaintings * 2):
			visibilityArray[i] = paintingsInTheBackground[i].getVisible()
			paintingsInTheBackground[i].visible(False)
	else:
		for i in range(numberOfPaintings * 2):
#			print "i = " + str(i)
			if visibilityArray[i] is not None: paintingsInTheBackground[i].visible(visibilityArray[i])

#	painting_birth_of_venus_black.visible(visibility)
#
#	painting_dali_memory_black.visible(visibility)
#
#	painting_harring_bestbuddies_black.visible(visibility)
#
#	painting_magritte_black.visible(visibility)
#
#	painting_monalisa_black.visible(visibility)
#
#	painting_monet_venice_black.visible(visibility)
#
#	painting_picasso_black.visible(visibility)
#
#	painting_scream_black.visible(visibility)
#
#	painting_starry_night_black.visible(visibility)
#
#	painting_van_gogh_black.visible(visibility)
#
#	painting_warhol_soup_black.visible(visibility)

videoToPlay = None
def onSensorUp(e):
	global theControllerToUse, theControllerNOTtoUse, trackpadState, stimulate
	global leftVideoRenderingBoard, rightVideoRenderingBoard, videoRenderingBoard, videoLoopsRemaining, vidLoopsRemaining, videoToPlay

#	print "e.button = " + str(e.button)
	if e.object is theControllerToUse:
		if e.button == steamvr.BUTTON_TRACKPAD:
#			stimulate = False
#			leftVideoRenderingBoard.visible(False)
#			rightVideoRenderingBoard.visible(False)
			videoRenderingBoard.visible(False)
			setBackgroundVisibility(True)
			
#			if videoToPlay is not None:
#				if (videoToPlay.getState() == viz.MEDIA_RUNNING): videoToPlay.stop()

	elif e.object is theControllerNOTtoUse:
		print "\nPlease use the other controller.\n"

viz.callback(viz.SENSOR_UP_EVENT,onSensorUp)

lowerTimeThresholdForStimCycleCompletion = 0.8

def printMessageAtTheStartOfCycle():
	global videoLoopsRemaining, videoListIndex, sparseVideoPlaceholder, sparseVideoPaths

	print "\nStimulation cycles remaining: " + str(videoLoopsRemaining[videoListIndex]) + "; each of duration:" + str((sparseVideoPlaceholder[videoListIndex]).getDuration())
	print "Press the trackpad to play the stimulation video: " + sparseVideoPaths[videoListIndex]

def printMessageAtTheEndOfCycle():
	print "Visual stimulation is complete for this round. Please check other canvases.\n"

def getCompletion_ONLY_FromVisualStimFunction():
	global maxNumberOfVideoLoops, vidLoopsRemaining, videoListIndex
	return (maxNumberOfVideoLoops - vidLoopsRemaining)*100.0/maxNumberOfVideoLoops

lowerCompletionThresholdForDenserStim = 30
upperCompletionThresholdForDenserStim = 70
def visualStim(controller):
	global theControllerToUse, trackpadState, stimulate, videoListIndex, paintingIndex, sparseVideoPlaceholder, denseVideoPlaceholder, videoLoopsRemaining
	global leftVideoRenderingBoard, rightVideoRenderingBoard, videoRenderingBoard, vidLoopsRemaining, videoToPlay, lowerTimeThresholdForStimCycleCompletion

	completion = getCompletion_ONLY_FromVisualStimFunction()
	print "Stimulation completed at this portal: " + str(getCompletion_ONLY_FromVisualStimFunction()) + "%"

	if (completion <= lowerCompletionThresholdForDenserStim) or (completion >= upperCompletionThresholdForDenserStim):
		print "Initiating a stimulation cycle with a sparse stimulation video"
		videoToPlay = sparseVideoPlaceholder[videoListIndex]
	else:
		print "Initiating a stimulation cycle with a dense stimulation video"
		videoToPlay = denseVideoPlaceholder[videoListIndex]

	videoRenderingBoard.texture(videoToPlay)
	
	videoToPlay.play()
	yield viztask.waitAny([viztask.waitMediaEnd(videoToPlay), viztask.waitSensorUp(controller, steamvr.BUTTON_TRACKPAD)])
	
	paintings[paintingIndex].texblend((maxNumberOfVideoLoops - vidLoopsRemaining)/maxNumberOfVideoLoops, '', 1)
	print "Completion: " + str(getCompletion_ONLY_FromVisualStimFunction()) + "%"
	print "Loops remaining: " + str(vidLoopsRemaining)

	if (videoToPlay.getState() == viz.MEDIA_RUNNING):
		durationPlayed = videoToPlay.getTime()
		print "Trackpad released. durationPlayed = " + str(durationPlayed)
		totalDuration = videoToPlay.getDuration()
		print "durationPlayed = " + str(durationPlayed) + "; totalDuration = " + str(totalDuration)
		if (float(durationPlayed/totalDuration) > lowerTimeThresholdForStimCycleCompletion):
			vidLoopsRemaining -= 1
			videoLoopsRemaining[videoListIndex] = vidLoopsRemaining
		else:
			print "Stimulation completed in this cycle: " + str(float((durationPlayed*100.0)/totalDuration)) + "% only. So this cycle will be repeated."
		videoToPlay.stop()
		if vidLoopsRemaining > 0: printMessageAtTheStartOfCycle()
	else:
		vidLoopsRemaining -= 1
		videoLoopsRemaining[videoListIndex] = vidLoopsRemaining
		if vidLoopsRemaining > 0:
			viztask.schedule(visualStim(controller))
		else:
			printMessageAtTheEndOfCycle()

def onSensorDown(e):
#	print "e.button1 = " + str(e.button)
	global theControllerToUse, theControllerNOTtoUse, trackpadState, stimulate, videoListIndex, paintingIndex, videoLoopsRemaining
	global leftVideoRenderingBoard, rightVideoRenderingBoard, videoRenderingBoard, vidLoopsRemaining, videoToPlay

	if e.object is theControllerToUse:
		if (e.button == steamvr.BUTTON_TRACKPAD) and (stimulate):
			#stimulation code below:
			
			vidLoopsRemaining = videoLoopsRemaining[videoListIndex]
			
			if vidLoopsRemaining > 0:
#				leftVideoRenderingBoard.visible(True)
#				rightVideoRenderingBoard.visible(True)
				videoRenderingBoard.visible(True)
				setBackgroundVisibility(False)

#				leftVideoRenderingBoard.texture(videoToPlay)
#				rightVideoRenderingBoard.texture(videoToPlay)
				
				viztask.schedule(visualStim(theControllerToUse))
			else:
				printMessageAtTheEndOfCycle()
	
	elif e.object is theControllerNOTtoUse:
		print "\nPlease use the other controller.\n"
			

viz.callback(viz.SENSOR_DOWN_EVENT,onSensorDown)

# Add directions to canvasForInitMsg
canvasForInitMsg = viz.addGUICanvas(pos=[0, 3.0, 6.0])
canvasForInitMsg.setMouseStyle(0)
canvasForInitMsg.alignment(viz.ALIGN_CENTER)
canvasForInitMsg.setRenderWorld([400,400], [5.0,5.0])

instructions ="""1. 10 out of the 11 frames pack unique visual stimulation.
2. Find each frame with an active stimulation.
3. Complete each session to view (and appreciate!) the painting.

TODO: Use the trigger to select and jump to a painting. GO GET THEM!!"""
panel = vizinfo.InfoPanel(instructions, title='NON-INVASIVE STIMULATION FOR VISION RESTORATION', key=None, icon=False, align=viz.ALIGN_CENTER, parent=canvasForInitMsg)

#hiding all text canvases
canvasForInitMsg.visible(False)

# Add directions to canvasForStim
canvasForStim = viz.addGUICanvas(pos=[0, 3.0, 6.0])
canvasForStim.setMouseStyle(0)
canvasForStim.alignment(viz.ALIGN_CENTER)
canvasForStim.setRenderWorld([400,400], [2.0,2.0])
canvasForStim.visible(False)

instructions ="""1. Pull the trigger to START the stimulation
2. Keep the trigger pressed to CONTINUE
3. Release the trigger to STOP it
4. Complete the stimulation to see the art!!
"""
panelForStimInstructions = vizinfo.InfoPanel(instructions, title='VISUAL STIMULATION IN STORE FOR YOU!', key=None, icon=False, align=viz.ALIGN_CENTER, parent=canvasForStim)

#hiding all text canvases
canvasForStim.visible(False)

# Add directions to canvasWithoutStim
canvasWithoutStim = viz.addGUICanvas(pos=[0, 3.0, 6.0])
canvasWithoutStim.setMouseStyle(0)
canvasWithoutStim.alignment(viz.ALIGN_CENTER)
canvasWithoutStim.setRenderWorld([400,400], [2.0,2.0])
canvasWithoutStim.visible(False)

instructions ="""This canvas either has no stimulation,
OR you got it already!

Appreciate the art, and explore a different one.
"""
panelForCanvasWithoutStim = vizinfo.InfoPanel(instructions, title='ENJOY THE ART, AND MOVE ON!', key=None, icon=False, align=viz.ALIGN_CENTER, parent=canvasWithoutStim)

#hiding all text canvases
canvasWithoutStim.visible(False)

#videos to be played
numberOfVideos = 10
sparseVideoPaths = [None] * numberOfVideos
denseVideoPaths = [None] * numberOfVideos
sparseVideoPlaceholder = [None] * numberOfVideos
denseVideoPlaceholder = [None] * numberOfVideos
videoLoopsRemaining = [None] * numberOfVideos	#this stores the number of loops for each video remaining to be played, which is totalLengthOfEachStimulationSessionInSeconds/video.getDuration()

if 'experimental condition' == choices[conditionChosen]:
	if 'dense' == stimuliChoices[stimChosen]:
		sparseVideoPaths[0] = 'media/onParasol1_dense.avi'
		sparseVideoPaths[1] = 'media/offParasol1_dense.avi'
		sparseVideoPaths[2] = 'media/onMidget1_dense.avi'
		sparseVideoPaths[3] = 'media/offMidget1_dense.avi'
		sparseVideoPaths[4] = 'media/sbc1_dense.avi'
		sparseVideoPaths[5] = 'media/onParasol2_dense.avi'
		sparseVideoPaths[6] = 'media/offParasol2_dense.avi'
		sparseVideoPaths[7] = 'media/onMidget2_dense.avi'
		sparseVideoPaths[8] = 'media/offMidget2_dense.avi'
		sparseVideoPaths[9] = 'media/sbc2_dense.avi'

		denseVideoPaths[0] = 'media/onParasol1_densest.avi'
		denseVideoPaths[1] = 'media/offParasol1_densest.avi'
		denseVideoPaths[2] = 'media/onMidget1_densest.avi'
		denseVideoPaths[3] = 'media/offMidget1_densest.avi'
		denseVideoPaths[4] = 'media/sbc1_densest.avi'
		denseVideoPaths[5] = 'media/onParasol2_densest.avi'
		denseVideoPaths[6] = 'media/offParasol2_densest.avi'
		denseVideoPaths[7] = 'media/onMidget2_densest.avi'
		denseVideoPaths[8] = 'media/offMidget2_densest.avi'
		denseVideoPaths[9] = 'media/sbc2_densest.avi'
	else:
		sparseVideoPaths[0] = 'media/onParasol1_sparse.avi'
		sparseVideoPaths[1] = 'media/offParasol1_sparse.avi'
		sparseVideoPaths[2] = 'media/onMidget1_sparse.avi'
		sparseVideoPaths[3] = 'media/offMidget1_sparse.avi'
		sparseVideoPaths[4] = 'media/sbc1_sparse.avi'
		sparseVideoPaths[5] = 'media/onParasol2_sparse.avi'
		sparseVideoPaths[6] = 'media/offParasol2_sparse.avi'
		sparseVideoPaths[7] = 'media/onMidget2_sparse.avi'
		sparseVideoPaths[8] = 'media/offMidget2_sparse.avi'
		sparseVideoPaths[9] = 'media/sbc2_sparse.avi'

		denseVideoPaths[0] = 'media/onParasol1_dense.avi'
		denseVideoPaths[1] = 'media/offParasol1_dense.avi'
		denseVideoPaths[2] = 'media/onMidget1_dense.avi'
		denseVideoPaths[3] = 'media/offMidget1_dense.avi'
		denseVideoPaths[4] = 'media/sbc1_dense.avi'
		denseVideoPaths[5] = 'media/onParasol2_dense.avi'
		denseVideoPaths[6] = 'media/offParasol2_dense.avi'
		denseVideoPaths[7] = 'media/onMidget2_dense.avi'
		denseVideoPaths[8] = 'media/offMidget2_dense.avi'
		denseVideoPaths[9] = 'media/sbc2_dense.avi'
else:
	sparseVideoPaths[0] = 'media/whiteNoise.avi'
	sparseVideoPaths[1] = 'media/whiteNoise.avi'
	sparseVideoPaths[2] = 'media/whiteNoise.avi'
	sparseVideoPaths[3] = 'media/whiteNoise.avi'
	sparseVideoPaths[4] = 'media/whiteNoise.avi'
	sparseVideoPaths[5] = 'media/whiteNoise.avi'
	sparseVideoPaths[6] = 'media/whiteNoise.avi'
	sparseVideoPaths[7] = 'media/whiteNoise.avi'
	sparseVideoPaths[8] = 'media/whiteNoise.avi'
	sparseVideoPaths[9] = 'media/whiteNoise.avi'

	denseVideoPaths[0] = 'media/whiteNoise.avi'
	denseVideoPaths[1] = 'media/whiteNoise.avi'
	denseVideoPaths[2] = 'media/whiteNoise.avi'
	denseVideoPaths[3] = 'media/whiteNoise.avi'
	denseVideoPaths[4] = 'media/whiteNoise.avi'
	denseVideoPaths[5] = 'media/whiteNoise.avi'
	denseVideoPaths[6] = 'media/whiteNoise.avi'
	denseVideoPaths[7] = 'media/whiteNoise.avi'
	denseVideoPaths[8] = 'media/whiteNoise.avi'
	denseVideoPaths[9] = 'media/whiteNoise.avi'

for i in range(10):
	sparseVideoPlaceholder[i] = viz.addVideo(sparseVideoPaths[i])
	denseVideoPlaceholder[i] = viz.addVideo(denseVideoPaths[i])
	print "totalLengthOfEachStimulationSessionInSeconds = " + str(totalLengthOfEachStimulationSessionInSeconds)
	print "sparseVideoPlaceholder[" + str(i) + "].getDuration() = " + str(sparseVideoPlaceholder[i].getDuration())
	print "denseVideoPlaceholder[" + str(i) + "].getDuration() = " + str(denseVideoPlaceholder[i].getDuration())
	videoLoopsRemaining[i] = totalLengthOfEachStimulationSessionInSeconds/sparseVideoPlaceholder[i].getDuration()

maxNumberOfVideoLoops = videoLoopsRemaining[0]

#sparseVideoPlaceholder[0] = viz.addVideo('media/onParasol1.avi')
#
#sparseVideoPaths[1] = 'media/onParasol2.avi'
#sparseVideoPlaceholder[1] = viz.addVideo('media/onParasol2.avi')
#
#sparseVideoPaths[2] = 'media/offParasol1.avi'
#sparseVideoPlaceholder[2] = viz.addVideo('media/offParasol1.avi')
#
#sparseVideoPaths[3] = 'media/offParasol2.avi'
#sparseVideoPlaceholder[3] = viz.addVideo('media/offParasol2.avi')
#
#sparseVideoPaths[4] = 'media/onMidget1.avi'
#sparseVideoPlaceholder[4] = viz.addVideo('media/onMidget1.avi')
#sparseVideoPlaceholder[5] = viz.addVideo('media/onMidget2.avi')
#sparseVideoPlaceholder[6] = viz.addVideo('media/offMidget1.avi')
#sparseVideoPlaceholder[7] = viz.addVideo('media/offMidget2.avi')
#sparseVideoPlaceholder[8] = viz.addVideo('media/sbc1.avi')
#sparseVideoPlaceholder[9] = viz.addVideo('media/sbc2.avi')

#videoList = []
#videoPlaceholderIndex = 0
#for i in range(11):
#	if i == itemIndexWithNoStimulation:
#		videoList.append(None)
#	else:
#		videoList.append(sparseVideoPlaceholder[videoPlaceholderIndex])
#		videoPlaceholderIndex += 1


def togglePaintingsVisibility():
	painting_birth_of_venus.visible(viz.TOGGLE)
	painting_dali_memory.visible(viz.TOGGLE)
	painting_harring_bestbuddies.visible(viz.TOGGLE)
	painting_magritte.visible(viz.TOGGLE)
	painting_monalisa.visible(viz.TOGGLE)
	painting_monet_venice.visible(viz.TOGGLE)
	painting_picasso.visible(viz.TOGGLE)
	painting_scream.visible(viz.TOGGLE)
	painting_starry_night.visible(viz.TOGGLE)
	painting_van_gogh.visible(viz.TOGGLE)
	painting_warhol_soup.visible(viz.TOGGLE)

	painting_birth_of_venus_black.visible(viz.TOGGLE)
	painting_dali_memory_black.visible(viz.TOGGLE)
	painting_harring_bestbuddies_black.visible(viz.TOGGLE)
	painting_magritte_black.visible(viz.TOGGLE)
	painting_monalisa_black.visible(viz.TOGGLE)
	painting_monet_venice_black.visible(viz.TOGGLE)
	painting_picasso_black.visible(viz.TOGGLE)
	painting_scream_black.visible(viz.TOGGLE)
	painting_starry_night_black.visible(viz.TOGGLE)
	painting_van_gogh_black.visible(viz.TOGGLE)
	painting_warhol_soup_black.visible(viz.TOGGLE)

vizact.onkeydown('v', togglePaintingsVisibility)


alphaOfPic = 0.0
alphaOfBlack = 1.0
change = 0.1
paintingName = 'painting_starry-night'
#paintingsDictionary[paintingName].visible(True)
#paintingsDictionary[paintingName + '_black'].visible(True)
#
#paintingsDictionary[paintingName].enable(viz.BLEND)
#paintingsDictionary[paintingName + '_black'].enable(viz.BLEND)
#paintingsDictionary[paintingName].drawOrder(10,bin=viz.BIN_TRANSPARENT)
#paintingsDictionary[paintingName + '_black'].drawOrder(10,bin=viz.BIN_TRANSPARENT)

def alterTheFirstPaintingsAlpha(direction = "plus"):
	global alphaOfPic, alphaOfBlack, change, paintingsDictionary, paintingName
	
	print "\nalphaOfPic = " + str(alphaOfPic)
	print "alphaOfBlack = " + str(alphaOfBlack)
	
	if (direction == "plus") and (alphaOfPic < 0.9):
		print "incrementing alpha"
		alphaOfPic += change
		print "alphaOfPic = " + str(alphaOfPic)
	if (direction == "minus") and (alphaOfPic > 0.1):
		print "decrementing alpha"
		alphaOfPic -= change
		print "alphaOfPic = " + str(alphaOfPic)

	paintingsDictionary[paintingName].alpha(alphaOfPic)
	paintingsDictionary[paintingName + '_black'].alpha(alphaOfBlack)

#vizact.onkeydown('y', alterTheFirstPaintingsAlpha, "plus")
#vizact.onkeydown('t', alterTheFirstPaintingsAlpha, "minus")

#using a video
video = sparseVideoPlaceholder[0]
#naturalSceneVideo = viz.addVideo("media/naturalScene.avi")

#video.setBorderRect([0.0, 0.0, 0.75, 1.0])

#Adding a quad to show a movie
leftVideoRenderingBoard = viz.addTexQuad(parent = viz.WORLD)
rightVideoRenderingBoard = viz.addTexQuad(parent = viz.WORLD)
videoRenderingBoard = viz.addTexQuad(parent = viz.WORLD)
#leftVideoRenderingBoard.texture(video)
#rightVideoRenderingBoard.texture(video)
#videoRenderingBoard.texture(video)
#videoRenderingBoard.texture(naturalSceneVideo)
#rightVideoRenderingBoard.setPosition([0.0, 0.0, 0.0], mode = viz.REL_PARENT)
#video.loop()
#video.play()
#naturalSceneVideo.loop()
#naturalSceneVideo.play()

#rightVideoRenderingBoard.setTexQuadDisplayMode(viz.TEXQUAD_CORNER_FIXED)
#rightVideoRenderingBoard.setSize([1.0830, 1.2040])
#rightVideoRenderingBoard.setSize([1.0, 1.0])

sideLength = 0.05

xShift = 0.031 	#meters
zShift = 0.005 	#meters

leftVideoRenderingBoard.setSize([sideLength, sideLength])
leftVideoRenderingBoard.setPosition([-xShift, 0.0, zShift])
rightVideoRenderingBoard.setSize([sideLength, sideLength])
rightVideoRenderingBoard.setPosition([xShift, 0.0, zShift])

videoRenderingBoard.setSize([width*scale, height*scale])
videoRenderingBoard.setPosition([0.0, 0.0, gapFromViveScreens])

videoRenderingBoard.visible(False)

#attaching the video rendering board to the head/eye
leftVideoRenderingBoard.setReferenceFrame(viz.RF_VIEW)
rightVideoRenderingBoard.setReferenceFrame(viz.RF_VIEW)
videoRenderingBoard.setReferenceFrame(viz.RF_VIEW)

#keeping them invisible to begin with
leftVideoRenderingBoard.visible(False)
rightVideoRenderingBoard.visible(False)

#print "rightVideoRenderingBoard.getTexQuadDisplayMode() = " + str(rightVideoRenderingBoard.getTexQuadDisplayMode())
#print "rightVideoRenderingBoard.getSize() = " + str(rightVideoRenderingBoard.getSize())
#print "video.getFrameCount() = " + str(video.getFrameCount())
#print "video.getDuration() = " + str(video.getDuration())
print "Visual stimulation will be running at: " + str(video.getFrameCount()/video.getDuration()) + " FPS\n"


# a canvas for the visual stimulation
#canvasForVisStim = viz.addGUICanvas()
#canvasForVisStim.setMouseStyle(0)
#canvasForVisStim.alignment(viz.ALIGN_CENTER)
##canvasForVisStim.setRenderWorld([400,400], [5.0,5.0])
#canvasForVisStim.setRenderWorldOverlay([800,800],50,3)
#
#viz.MainWindow.setDefaultGUICanvas(canvasForVisStim)
#
#leftVideoRenderingBoard.setParent(canvasForVisStim)
#canvasForVisStim.setPosition([0,0,0])

#canvasForVisStim.setRenderScreenOrtho()
#canvasForVisStim.setPosition([0,0,0])

def reposition(direction="forward"):
	global videoRenderingBoard, gapFromViveScreens
	
	if direction == "forward": gapFromViveScreens += 0.01
	else: gapFromViveScreens -= 0.01
	
	print "gapFromViveScreens = " + str(gapFromViveScreens)
	
	videoRenderingBoard.setPosition([0.0, 0.0, gapFromViveScreens])

vizact.onkeydown('m', reposition, "forward")
vizact.onkeydown('n', reposition, "backward")

def resize(direction="scaleUp"):
	global videoRenderingBoard, width, height, scale
	
	if direction == "scaleUp": scale += 0.01
	else: scale -= 0.01
	
	print "scale = " + str(scale)
	
	videoRenderingBoard.setSize([width*scale, height*scale])
	
vizact.onkeydown('j', resize, "scaleUp")
vizact.onkeydown('k', resize, "scaleDown")

def changeBackgroundColor(direction="scaleUp"):
	global colorSaturationValue
	if (direction == "scaleUp") and (colorSaturationValue < 0.9): colorSaturationValue += 0.01
	elif (direction == "scaleDown") and (colorSaturationValue > 0.1): colorSaturationValue -= 0.01
	
	print "colorSaturationValue = " + str(colorSaturationValue)

	viz.clearcolor(colorSaturationValue, colorSaturationValue, colorSaturationValue)


vizact.onkeydown('g', changeBackgroundColor, "scaleUp")
vizact.onkeydown('h', changeBackgroundColor, "scaleDown")

#scale = 3.81
#gapFromViveScreens = 0.2

#def initializeDataRecording():
#	
