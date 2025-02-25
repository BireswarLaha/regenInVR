﻿#Developed on Vizard sample code, titled 'steamvrExample.py'
#Bireswar Laha, Huberman Lab, Department of Neurobiology, Stanford University
#Dated: March-July, 2017

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

totalLengthOfEachStimulationSessionInSeconds = 180 #the length of each stimulation session in seconds
width = 0.11	#http://doc-ok.org/?p=1414 - Vive has approximately 100 degrees HFOV at 10 mm screen separation from the eyes
height = 0.11	#http://doc-ok.org/?p=1414 - Vive has approximately 110 degrees VFOV at 10 mm screen separation from the eyes
scale = 5.25
gapFromViveScreens = 0.43

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

viz.window.setSize([1980, 1080])

stimTime = [0] * 10
#stim1time = stim2time = stim3time = stim4time = stim5time = stim6time = stim7time = stim8time = stim9time = stim10time = 0

#open a CSV file at the beginning
dataFilePresent = os.path.isfile(dataDir + dataFile)

if not dataFilePresent:
	print "creating data file and writing the header"
	with open(dataDir + dataFile, 'wb') as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()
		print "adding the first data line to the data file"
		writer.writerow({'ID': ID, 'stim1time': stimTime[0], 'stim2time': stimTime[1], 'stim3time': stimTime[2], 'stim4time': stimTime[3], 'stim5time': stimTime[4], 'stim6time': stimTime[5], 'stim7time': stimTime[6], 'stim8time': stimTime[7], 'stim9time': stimTime[8], 'stim10time': stimTime[9]})
else:
	print "data file is present in the data folder already"
	with open(dataDir + dataFile, 'ab') as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		print "appending another data line to the data file"
		writer.writerow({'ID': ID, 'stim1time': stimTime[0], 'stim2time': stimTime[1], 'stim3time': stimTime[2], 'stim4time': stimTime[3], 'stim5time': stimTime[4], 'stim6time': stimTime[5], 'stim7time': stimTime[6], 'stim8time': stimTime[7], 'stim9time': stimTime[8], 'stim10time': stimTime[9]})

#write out data to the file at the start and end of stimulation, and flush the cache!
def writeData(lastStimTime = 0):
	global ID, dataDir, dataFile, videoListIndex, stimTimeCalc
	print "Updating datafile now ..."
	#open data file for reading
	f = open(dataDir + dataFile, 'rb')
	
	#use a reader to read the lines from the file
	r = csv.reader(f)

	#putting the lines of the file in a list for parsing
	lines = [l for l in r]

	#update the time for the specific stimulation
	for line in lines:
#		items = line.split(',')
#		print str(line)
#		print "line[0] = " + str(line[0])
		if (len(line) > 0) and (line[0] == str(ID)):
			itemIndexToUpdate = videoListIndex + 1
			print "line to update: " + str(line)
			print "updating the " + str(itemIndexToUpdate) + "th counter for ID: " + str(ID)
			currentItem = int(line[itemIndexToUpdate])
			updatedItem = currentItem + lastStimTime
			line[itemIndexToUpdate] = str(updatedItem)
			print "updated line: " + str(line)
			
	#replace the line in the data file
	
	#open data file for writing
	f = open(dataDir + dataFile, 'wb')

	#write the lines back into the file
	writer = csv.writer(f)
	writer.writerows(lines)
	f.flush()

	print "datafile updated."

startTimeForStim = 0
stimTimerRunning = False
def startStimTimer():
	global elapsedTime, stimTimerRunning, startTimeForStim, stimTimeCalc
	stimTimeCalc = 0
	print "stim timer start"
	startTimeForStim = int(time.time())
	print "startTimeForStim = " + str(startTimeForStim)
	stimTimerRunning = True
	setCompletionBoardVisibility(False)
	videoRenderingBoard.visible(True)
	setBackgroundVisibility(False)

def endStimTimer():
	global startTimeForStim, stimTimerRunning, stimTime, stimTimeCalc, selectedPaintingIndex, videoRenderingBoard
	if stimTimerRunning:
		print "ending stim timer and updating data file"
#		print "startTimeForStim inside endStimTimer = " + str(startTimeForStim)
		currentTime = int(time.time())
		stimTime = currentTime - startTimeForStim
		print "currentTime = " + str(currentTime)
		print "time spent between the trackpad press and release " + str(stimTime) + " secs"
		print "***stimTimeCalc " + str(stimTimeCalc) + " secs"
#		writeData(stimTime)
		writeData(stimTimeCalc)
		updateCompletionDisplay(selectedPaintingIndex)
		stimTime = 0
		stimTimeCalc = 0
		stimTimerRunning = False
		setCompletionBoardVisibility(True)
		videoRenderingBoard.visible(False)
		setBackgroundVisibility(True)

# Initialize window
viz.setMultiSample(8)
viz.go()

colorSaturationValue = 0.5
viz.clearcolor(colorSaturationValue, colorSaturationValue, colorSaturationValue)

choices = ['experimental condition', 'control condition']
stimuliChoices = ['dense', 'sparse']
experimentalConditionChosen = viz.choose('Choose the condition for this run: ', choices)
print 'Group chosen:',choices[experimentalConditionChosen]

if 'experimental condition' == choices[experimentalConditionChosen]:
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
listOfPaintings = []
positionOfTex = [None] * numberOfPaintings
eulerOfTex = [None] * numberOfPaintings
sizeOfTex = [None] * numberOfPaintings

#0-(numberOfPaintings-1) paintingsInTheBackground are the texquads for the paintings
#numberOfPaintings-(2*numberOfPaintings-1) paintingsInTheBackground are the black osgbs, hiding the main paintings
paintingsInTheBackground = [None] * (numberOfPaintings * 2)

prefixForTextures = "textures/painting_"
postfixForTextures = ".png"
textureNameForPainting = [None] * numberOfPaintings
#textureNameForPainting[0] = 'textures/painting_picasso.png'
#textureNameForPainting[1] = 'textures/painting_dali-memory.png'
#textureNameForPainting[2] = 'textures/painting_van-gogh.png'
#textureNameForPainting[3] = 'textures/painting_monet-venice.png'
#textureNameForPainting[4] = 'textures/painting_scream.png'
#textureNameForPainting[5] = 'textures/painting_starry-night.png'
#textureNameForPainting[6] = 'textures/painting_harring-bestbuddies.png'
#textureNameForPainting[7] = 'textures/painting_monalisa.png'
#textureNameForPainting[8] = 'textures/painting_warhol_soup.png'
#textureNameForPainting[9] = 'textures/painting_birth-of-venus.png'
#textureNameForPainting[10] = 'textures/painting_magritte.png'
textureNameForPainting[0] = 'picasso'
textureNameForPainting[1] = 'dali-memory'
textureNameForPainting[2] = 'van-gogh'
textureNameForPainting[3] = 'monet-venice'
textureNameForPainting[4] = 'scream'
textureNameForPainting[5] = 'starry-night'
textureNameForPainting[6] = 'harring-bestbuddies'
textureNameForPainting[7] = 'monalisa'
textureNameForPainting[8] = 'warhol_soup'
textureNameForPainting[9] = 'birth-of-venus'
textureNameForPainting[10] = 'magritte'

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

# Create shader effect that blends textures and applies to diffuse color
#code borrowed from tutorial_multiTexture.py of worldviz, and modified
code = """
Effect "Texture Blend" {

	Float BlendAmount { value 0 }
	Texture2D Texture1 { unit 0 }
	Texture2D Texture2 { unit 1 }

	Shader {

		BEGIN Material
		m.diffuse = mix( texture2D( Texture1, uvTexture1).rgb, texture2D( Texture2, uvTexture2).rgb, BlendAmount);
		END

	}

}
"""
texBlendEffect = viz.addEffect(code)

#backgroundBlackTex = viz.addTexture('textures/blackSquare.png')
#backgroundBlackTex = viz.addTexture('textures/skyBlue.png')
backgroundBlackTex = viz.addTexture('textures/blackSquare.png')
for i in range(numberOfPaintings):
#	painting = viz.addTexQuad(size=sizeOfTex[i])
#	painting.name("test
	paintings[i] = viz.addTexQuad(size=sizeOfTex[i])
	paintings[i].name = textureNameForPainting[i]
	tex = viz.addTexture(prefixForTextures + textureNameForPainting[i] + postfixForTextures)
	paintings[i].texture(backgroundBlackTex)
	paintings[i].texture(tex,'',1)
	paintings[i].texblend(0.0, '', 1)
	paintings[i].setPosition(positionOfTex[i])
	paintings[i].setEuler(eulerOfTex[i])
	paintingsInTheBackground[i] = paintings[i]
	listOfPaintings.append(paintings[i])
	paintings[i].visible(False)
#	print "name of this tex quad node = " + str(paintingsInTheBackground[i].getNodeNames())

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
painting_birth_of_venus_blend = vizfx.addChild('models/painting_birth-of-venus_blend.osgb')
painting_birth_of_venus_blend.apply(texBlendEffect)
painting_birth_of_venus_blend.setUniformFloat('BlendAmount', 1.0)
#painting_birth_of_venus_black = vizfx.addChild('models/painting_birth-of-venus_black.osgb')
#painting_birth_of_venus_black = vizfx.addChild('models/painting_birth-of-venus.osgb')
#painting_birth_of_venus_blend.visible(False)
paintingsDictionary['painting_birth-of-venus_blend'] = painting_birth_of_venus_blend
#paintingsDictionary['painting_birth-of-venus_black'] = painting_birth_of_venus_black
#paintingsDictionary['painting_birth-of-venus_black'] = paintings[0]
#paintingsDictionary[textureNameForPainting[0]] = paintings[0]
#paintingsDictionary['painting_birth-of-venus_black'].visible(False)
paintingsInTheBackground[0 + numberOfPaintings] = painting_birth_of_venus_blend
#paintingsInTheBackground[0 + numberOfPaintings] = painting_birth_of_venus_black

painting_dali_memory_blend = vizfx.addChild('models/painting_dali-memory_blend.osgb')
painting_dali_memory_blend.apply(texBlendEffect)
painting_dali_memory_blend.setUniformFloat('BlendAmount', 1.0)
#painting_dali_memory_black = vizfx.addChild('models/painting_dali-memory_black.osgb')
#painting_dali_memory_black = vizfx.addChild('models/painting_dali-memory.osgb')
#painting_dali_memory_blend.visible(False)
paintingsDictionary['painting_dali-memory_blend'] = painting_dali_memory_blend
#paintingsDictionary['painting_dali-memory_black'] = painting_dali_memory_black
#paintingsDictionary['painting_dali-memory_black'] = paintings[1]
#paintingsDictionary[textureNameForPainting[1]] = paintings[1]
#paintingsDictionary['painting_dali-memory_black'].visible(False)
paintingsInTheBackground[1 + numberOfPaintings] = painting_dali_memory_blend
#paintingsInTheBackground[1 + numberOfPaintings] = painting_dali_memory_black

painting_harring_bestbuddies_blend = vizfx.addChild('models/painting_harring-bestbuddies_blend.osgb')
painting_harring_bestbuddies_blend.apply(texBlendEffect)
painting_harring_bestbuddies_blend.setUniformFloat('BlendAmount', 1.0)
#painting_harring_bestbuddies_black = vizfx.addChild('models/painting_harring-bestbuddies_black.osgb')
#painting_harring_bestbuddies_black = vizfx.addChild('models/painting_harring-bestbuddies.osgb')
#painting_harring_bestbuddies_blend.visible(False)
paintingsDictionary['painting_harring-bestbuddies_blend'] = painting_harring_bestbuddies_blend
#paintingsDictionary['painting_harring-bestbuddies_black'] = painting_harring_bestbuddies_black
#paintingsDictionary['painting_harring-bestbuddies_black'] = paintings[2]
#paintingsDictionary[textureNameForPainting[2]] = paintings[2]
#paintingsDictionary['painting_harring-bestbuddies_black'].visible(False)
paintingsInTheBackground[2 + numberOfPaintings] = painting_harring_bestbuddies_blend
#paintingsInTheBackground[2 + numberOfPaintings] = painting_harring_bestbuddies_black

painting_magritte_blend = vizfx.addChild('models/painting_magritte_blend.osgb')
painting_magritte_blend.apply(texBlendEffect)
painting_magritte_blend.setUniformFloat('BlendAmount', 1.0)
#painting_magritte_black = vizfx.addChild('models/painting_magritte_black.osgb')
#painting_magritte_black = vizfx.addChild('models/painting_magritte.osgb')
#painting_magritte_blend.visible(False)
paintingsDictionary['painting_magritte_blend'] = painting_magritte_blend
#paintingsDictionary['painting_magritte_black'] = painting_magritte_black
#paintingsDictionary['painting_magritte_black'] = paintings[3]
#paintingsDictionary[textureNameForPainting[3]] = paintings[3]
#paintingsDictionary['painting_magritte_black'].visible(False)
paintingsInTheBackground[3 + numberOfPaintings] = painting_magritte_blend
#paintingsInTheBackground[3 + numberOfPaintings] = painting_magritte_black

painting_monalisa_blend = vizfx.addChild('models/painting_monalisa_blend.osgb')
painting_monalisa_blend.apply(texBlendEffect)
painting_monalisa_blend.setUniformFloat('BlendAmount', 1.0)
#painting_monalisa_black = vizfx.addChild('models/painting_monalisa_black.osgb')
#painting_monalisa_black = vizfx.addChild('models/painting_monalisa.osgb')
#painting_monalisa_blend.visible(False)
paintingsDictionary['painting_monalisa_blend'] = painting_monalisa_blend
#paintingsDictionary['painting_monalisa_black'] = painting_monalisa_black
#paintingsDictionary[textureNameForPainting[4]] = paintings[4]
#paintingsDictionary['painting_monalisa_black'].visible(False)
paintingsInTheBackground[4 + numberOfPaintings] = painting_monalisa_blend
#paintingsInTheBackground[4 + numberOfPaintings] = painting_monalisa_black

painting_monet_venice_blend = vizfx.addChild('models/painting_monet-venice_blend.osgb')
painting_monet_venice_blend.apply(texBlendEffect)
painting_monet_venice_blend.setUniformFloat('BlendAmount', 1.0)
#painting_monet_venice_black = vizfx.addChild('models/painting_monet-venice_black.osgb')
#painting_monet_venice_black = vizfx.addChild('models/painting_monet-venice.osgb')
#painting_monet_venice_blend.visible(False)
paintingsDictionary['painting_monet-venice_blend'] = painting_monet_venice_blend
#paintingsDictionary['painting_monet-venice_black'] = painting_monet_venice_black
#paintingsDictionary['painting_monet-venice_black'] = paintings[5]
#paintingsDictionary[textureNameForPainting[5]] = paintings[5]
#paintingsDictionary['painting_monet-venice_black'].visible(False)
paintingsInTheBackground[5 + numberOfPaintings] = painting_monet_venice_blend
#paintingsInTheBackground[5 + numberOfPaintings] = painting_monet_venice_black

painting_picasso_blend = vizfx.addChild('models/painting_picasso_blend.osgb')
painting_picasso_blend.apply(texBlendEffect)
painting_picasso_blend.setUniformFloat('BlendAmount', 1.0)
#painting_picasso_black = vizfx.addChild('models/painting_picasso_black.osgb')
#painting_picasso_black = vizfx.addChild('models/painting_picasso.osgb')
#painting_picasso_blend.visible(False)
paintingsDictionary['painting_picasso_blend'] = painting_picasso_blend
#paintingsDictionary['painting_picasso_black'] = painting_picasso_black
#paintingsDictionary['painting_picasso_black'] = paintings[6]
#paintingsDictionary[textureNameForPainting[6]] = paintings[6]
#paintingsDictionary['painting_picasso_black'].visible(False)
paintingsInTheBackground[6 + numberOfPaintings] = painting_picasso_blend
#paintingsInTheBackground[6 + numberOfPaintings] = painting_picasso_black

painting_scream_blend = vizfx.addChild('models/painting_scream_blend.osgb')
painting_scream_blend.apply(texBlendEffect)
painting_scream_blend.setUniformFloat('BlendAmount', 1.0)
#painting_scream_black = vizfx.addChild('models/painting_scream_black.osgb')
#painting_scream_black = vizfx.addChild('models/painting_scream.osgb')
#painting_scream_blend.visible(False)
paintingsDictionary['painting_scream_blend'] = painting_scream_blend
#paintingsDictionary['painting_scream_black'] = painting_scream_black
#paintingsDictionary['painting_scream_black'] = paintings[7]
#paintingsDictionary[textureNameForPainting[7]] = paintings[7]
#paintingsDictionary['painting_scream_black'].visible(False)
paintingsInTheBackground[7 + numberOfPaintings] = painting_scream_blend
#paintingsInTheBackground[7 + numberOfPaintings] = painting_scream_black

painting_starry_night_blend = vizfx.addChild('models/painting_starry-night_blend.osgb')
painting_starry_night_blend.apply(texBlendEffect)
painting_starry_night_blend.setUniformFloat('BlendAmount', 1.0)
#painting_starry_night_black = vizfx.addChild('models/painting_starry-night_black.osgb')
#painting_starry_night_black = vizfx.addChild('models/painting_starry-night.osgb')
#painting_starry_night_blend.visible(False)
paintingsDictionary['painting_starry-night_blend'] = painting_starry_night_blend
#paintingsDictionary['painting_starry-night_black'] = painting_starry_night_black
#paintingsDictionary['painting_starry-night_black'] = paintings[8]
#paintingsDictionary[textureNameForPainting[8]] = paintings[8]
#paintingsDictionary['painting_starry-night_black'].visible(False)
paintingsInTheBackground[8 + numberOfPaintings] = painting_starry_night_blend
#paintingsInTheBackground[8 + numberOfPaintings] = painting_starry_night_black

painting_van_gogh_blend = vizfx.addChild('models/painting_van-gogh_blend.osgb')
painting_van_gogh_blend.apply(texBlendEffect)
painting_van_gogh_blend.setUniformFloat('BlendAmount', 1.0)
#painting_van_gogh_black = vizfx.addChild('models/painting_van-gogh_black.osgb')
#painting_van_gogh_black = vizfx.addChild('models/painting_van-gogh.osgb')
#painting_van_gogh_blend.visible(False)
paintingsDictionary['painting_van-gogh_blend'] = painting_van_gogh_blend
#paintingsDictionary['painting_van-gogh_black'] = painting_van_gogh_black
#paintingsDictionary['painting_van-gogh_black'] = paintings[9]
#paintingsDictionary[textureNameForPainting[9]] = paintings[9]
#paintingsDictionary['painting_van-gogh_black'].visible(False)
paintingsInTheBackground[9 + numberOfPaintings] = painting_van_gogh_blend
#paintingsInTheBackground[9 + numberOfPaintings] = painting_van_gogh_black

painting_warhol_soup_blend = vizfx.addChild('models/painting_warhol_soup_blend.osgb')
painting_warhol_soup_blend.apply(texBlendEffect)
painting_warhol_soup_blend.setUniformFloat('BlendAmount', 1.0)
#painting_warhol_soup_black = vizfx.addChild('models/painting_warhol_soup_black.osgb')
#painting_warhol_soup_black = vizfx.addChild('models/painting_warhol_soup.osgb')
#painting_warhol_soup_blend.visible(False)
paintingsDictionary['painting_warhol_soup_blend'] = painting_warhol_soup_blend
#paintingsDictionary['painting_warhol_soup_black'] = painting_warhol_soup_black
#paintingsDictionary['painting_warhol_soup_black'] = paintings[10]
#paintingsDictionary[textureNameForPainting[10]] = paintings[10]
#paintingsDictionary['painting_warhol_soup_black'].visible(False)
paintingsInTheBackground[10 + numberOfPaintings] = painting_warhol_soup_blend
#paintingsInTheBackground[10 + numberOfPaintings] = painting_warhol_soup_black

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
#JUMP_LOCATIONS = {   textureNameForPainting[0]: [-3.4, -0.00000, 0.42632]
#					,textureNameForPainting[1]: [-3.4, 0.00000, 2.61695]
#					,textureNameForPainting[2]: [-3.4, -0.00000, 4.85902]
#					,textureNameForPainting[3]: [-3.4, -0.00000, 6.79640]
#					,textureNameForPainting[4]: [-2.00545, 0.00000, 7.09077]
#					,textureNameForPainting[5]: [0.0, 0.00000, 8.0]
#					,textureNameForPainting[6]: [2.35362, -0.00000, 7.05530]
#					,textureNameForPainting[7]: [3.4, 0.00000, 6.89882]
#					,textureNameForPainting[8]: [3.4, 0.00000, 4.62012]
#					,textureNameForPainting[9]: [3.4, -0.00000, 2.19906]
#					,textureNameForPainting[10]: [3.4, 0.00000, 0.07459]
#}
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
		
		nameNew = name
#		nameNew = name + "_black"
		nameNew = name + "_blend"
		splitNames = nameNew.split("-")
		
#		print "name = " + name
		
		global paintingsDictionary

#		if paintingsDictionary[nameNew].getVisible() == False:
#			nameNew = nameNew + "_black"

		if mode:
#			gallery.apply(highlightEffect, node=name)
#			paintingsDictionary[nameNew].apply(highlightEffect, node=paintingsDictionary[nameNew])
			paintingsDictionary[nameNew].apply(highlightEffect, node=name)
		else:
#			gallery.unapply(highlightEffect, node=name)
#			paintingsDictionary[nameNew].unapply(highlightEffect, node=paintingsDictionary[nameNew])
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
				
			node_name = ''
#			print "info.object = " + str(info.object)
#			if info.object in listOfPaintings:
#				print "intersected with " + str(info.object.name)
			
			# Check if name is a jump location painting
			node_name = info.name if info.name in JUMP_LOCATIONS else ''
#				node_name = info.object.name if info.object.name in JUMP_LOCATIONS else ''
#				print "node_name = " + str(node_name)

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
selectedPaintingIndex = -1
selectedKeyForPaintingsDictionary = ''

def JumpTask(controller):
	"""Task that users trigger button press/release to jump to painting locations"""
	while True:

		# Wait for trigger to press
		yield viztask.waitSensorDown(controller, steamvr.BUTTON_TRACKPAD)

		# Start highlighting task
		highlightTask = viztask.schedule(HighlightTask(controller))

		# Wait for trigger to release
		yield viztask.waitSensorUp(controller, steamvr.BUTTON_TRACKPAD)

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
			global paintings, stimulate, videoListIndex, selectedPaintingIndex, previousPaintingName, previousVidListIndex
			global selectedKeyForPaintingsDictionary

			# Hide instruction canvasForInitMsg after first jump
			canvasForInitMsg.visible(False)

			separationOnHorizontalPlane = 0.8
			verticalPosOfCanvas = 0.6
			normalizedDirectionToShiftTheCanvas = vector3.Vec3ToVizardFloatList(vector3.vizardFloatListToVec3([-info.normal[0], 0.0, -info.normal[2]]).normalize())

			videoListIndex = dictionaryMappingPaintingNamesToVideoListIndex[info.name]
			selectedPaintingIndex = dictionaryMappingPaintingNamesToVideoListIndex[info.name]
			selectedKeyForPaintingsDictionary = info.name + "_blend"
			if videoListIndex > itemIndexWithNoStimulation: videoListIndex -= 1	#this is under the assumption that the indices of the videos associated to the canvases go up from 0 to 10, ignoring the index for the item to be ignored
#			paintingsDictionary[info.name + "_black"].visible(False)

			if (info.name != paintingNames[itemIndexWithNoStimulation]):
				#visual stimulation ready to be taken
				stimulate = True
				print "\n==========================\nPainting: " + info.name + ". Video: " + sparseVideoPaths[videoListIndex] + ". Index# " + str(videoListIndex)
				printMessageAtTheStartOfCycle()
			else:
				#visual stimulation unavailable or already taken
				print "\n=========================\nPainting: " + info.name + ". The visual stimulation here is either unavailable, or is complete for this round. Please check other canvases."
				######Use paintingsDictionary to retrieve the painting in focus, instead of paintings list in line below
#				paintings[selectedPaintingIndex].texblend(1.0, '', 1)
#				print "paintingsDictionary[selectedKeyForPaintingsDictionary] = " + str(paintingsDictionary[selectedKeyForPaintingsDictionary])
				paintingsDictionary[selectedKeyForPaintingsDictionary].setUniformFloat('BlendAmount', 0.0)
				stimulate = False

			#show the previous empty canvas if the stimulation is incomplete there
#			if (previousPaintingName is not None) and (previousVidListIndex != -1) and (previousPaintingName != paintingNames[itemIndexWithNoStimulation]) and (videoLoopsRemaining[previousVidListIndex] > 0):	#stimulation is not complete at the previous canvas
#				paintingsDictionary[previousPaintingName + "_black"].visible(True)
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
	
#	if visibility == False:
#		#save the current visibility in a global array, and hide all paintingsInTheBackground
#		for i in range(numberOfPaintings * 2):
#			visibilityArray[i] = paintingsInTheBackground[i].getVisible()
#			paintingsInTheBackground[i].visible(False)
#	else:
#		for i in range(numberOfPaintings * 2):
##			print "i = " + str(i)
#			if visibilityArray[i] is not None: paintingsInTheBackground[i].visible(visibilityArray[i])

	painting_birth_of_venus_blend.visible(visibility)

	painting_dali_memory_blend.visible(visibility)

	painting_harring_bestbuddies_blend.visible(visibility)

	painting_magritte_blend.visible(visibility)

	painting_monalisa_blend.visible(visibility)

	painting_monet_venice_blend.visible(visibility)

	painting_picasso_blend.visible(visibility)

	painting_scream_blend.visible(visibility)

	painting_starry_night_blend.visible(visibility)

	painting_van_gogh_blend.visible(visibility)

	painting_warhol_soup_blend.visible(visibility)

def setCompletionBoardVisibility(state = False):
	global totalCanvases, completionCanvas
	
	for i in range(totalCanvases):
		completionCanvas[i].visible(state)

videoToPlay = None
def onSensorUp(e):
	global theControllerToUse, theControllerNOTtoUse, trackpadState, stimulate
	global leftVideoRenderingBoard, rightVideoRenderingBoard, videoRenderingBoard, videoLoopsRemaining, vidLoopsRemaining, videoToPlay

#	print "e.button = " + str(e.button)
	if e.object is theControllerToUse:
		if e.button == steamvr.BUTTON_TRIGGER:
#			stimulate = False
#			leftVideoRenderingBoard.visible(False)
#			rightVideoRenderingBoard.visible(False)
			videoRenderingBoard.visible(False)
			setBackgroundVisibility(True)
			
#			if videoToPlay is not None:
#				if (videoToPlay.getState() == viz.MEDIA_RUNNING): videoToPlay.stop()

	elif e.object is theControllerNOTtoUse:
#	if e.object is theControllerNOTtoUse:
		print "\nPlease use the other controller.\n"

viz.callback(viz.SENSOR_UP_EVENT,onSensorUp)

lowerTimeThresholdForStimCycleCompletion = 0.8

def printMessageAtTheStartOfCycle():
	global videoLoopsRemaining, videoListIndex, lengthOfEachStimVideo

	print "\nStimulation cycles remaining: " + str(int(videoLoopsRemaining[videoListIndex])) + ", each of duration " + str(lengthOfEachStimVideo)
	print "Press the trackpad to play the stimulation video now ..."# + sparseVideoPaths[videoListIndex]

def printMessageAtTheEndOfCycle():
	print "Visual stimulation is complete for this round. Please check other canvases.\n"

def getCompletion_ONLY_FromVisualStimFunction():
	global maxNumberOfVideoLoops, vidLoopsRemaining, videoListIndex
	global totalLengthOfEachStimulationSessionInSeconds, videoLoopsRemaining, lengthOfEachStimVideo, timeToStartPlayingTheVideoFrom
#	return (maxNumberOfVideoLoops - vidLoopsRemaining)*100.0/maxNumberOfVideoLoops
	return int(((totalLengthOfEachStimulationSessionInSeconds - (videoLoopsRemaining[videoListIndex] * lengthOfEachStimVideo - timeToStartPlayingTheVideoFrom[videoListIndex]))/totalLengthOfEachStimulationSessionInSeconds) * 100.0)

lowerCompletionThresholdForDenserStim = 30
upperCompletionThresholdForDenserStim = 70
def visualStim(controller):
	global theControllerToUse, trackpadState, stimulate, videoListIndex, selectedPaintingIndex, sparseVideoPlaceholder, denseVideoPlaceholder, videoLoopsRemaining, stimTimeCalc, maxNumberOfVideoLoops
	global leftVideoRenderingBoard, rightVideoRenderingBoard, videoRenderingBoard, vidLoopsRemaining, videoToPlay, lowerTimeThresholdForStimCycleCompletion, timeToStartPlayingTheVideoFrom
	global totalLengthOfEachStimulationSessionInSeconds, lengthOfEachStimVideo, selectedKeyForPaintingsDictionary

	completion = getCompletion_ONLY_FromVisualStimFunction()
	print "Completion: " + str(completion) + "%"

	if (completion <= lowerCompletionThresholdForDenserStim) or (completion >= upperCompletionThresholdForDenserStim):
		print "Initiating a sparse stim"
		videoToPlay = sparseVideoPlaceholder[videoListIndex]
	else:
		print "Initiating a dense stim"
		videoToPlay = denseVideoPlaceholder[videoListIndex]

	videoRenderingBoard.texture(videoToPlay)
	
	print "Loops remaining: " + str(int(vidLoopsRemaining))
	print "Playing the stim video from: " + str(timeToStartPlayingTheVideoFrom[videoListIndex]) + " secs"
	#setting the time of the video to the number of seconds at which the last cycle ended
	videoToPlay.setTime(timeToStartPlayingTheVideoFrom[videoListIndex])
	videoToPlay.play()
	yield viztask.waitAny([viztask.waitMediaEnd(videoToPlay), viztask.waitSensorUp(controller, steamvr.BUTTON_TRIGGER)])
	
	if (videoToPlay.getState() == viz.MEDIA_RUNNING):
		#the stop of the stimulation is triggered here from the release of the controller trackpad ... need to call the stim end timer
		durationPlayed = int(videoToPlay.getTime())
		totalDuration = videoToPlay.getDuration()
		print "Trackpad released. durationPlayed for this round = " + str(durationPlayed) + " secs; totalDuration = " + str(totalDuration) + " secs"
#		if (float(durationPlayed/totalDuration) > lowerTimeThresholdForStimCycleCompletion):
#			vidLoopsRemaining -= 1
#			videoLoopsRemaining[videoListIndex] = vidLoopsRemaining
#		else:
#			print "Stimulation completed in this cycle: " + str(float((durationPlayed*100.0)/totalDuration)) + "% only. So this cycle will be repeated."
		videoToPlay.stop()
		print "Stimulation completed for this round of stim video: " + str(float((durationPlayed*100.0)/totalDuration)) + "%"
		
		stimTimeCalc += int(durationPlayed - timeToStartPlayingTheVideoFrom[videoListIndex])
		timeToStartPlayingTheVideoFrom[videoListIndex] = durationPlayed
		
		endStimTimer()
		if vidLoopsRemaining > 0: printMessageAtTheStartOfCycle()
	else:
		#the stop of the stimulation is triggered here from the end of the stimulation video
		vidLoopsRemaining -= 1
		videoLoopsRemaining[videoListIndex] = vidLoopsRemaining

		stimTimeCalc += int(videoToPlay.getDuration() - timeToStartPlayingTheVideoFrom[videoListIndex])
		timeToStartPlayingTheVideoFrom[videoListIndex] = 0

		if vidLoopsRemaining > 0:
			#there is at least another round of stimulation remaining from the same stimulation video; initializing the next round now ...
			viztask.schedule(visualStim(controller))
		else:
			#there are no more cycles of stimulation remaining from the same stimulation video; this is the end of this stimulation cycle ... need to call the stim end timer
			printMessageAtTheEndOfCycle()
			endStimTimer()

#	paintings[selectedPaintingIndex].texblend((maxNumberOfVideoLoops - vidLoopsRemaining)/maxNumberOfVideoLoops, '', 1)
	print "Visibility/completion of this image is at " + str(getCompletion_ONLY_FromVisualStimFunction()) + "%\n---------------------"
	######Use paintingsDictionary to retrieve the painting in focus, instead of paintings list in line below
#	paintings[selectedPaintingIndex].texblend(completion/100.0, '', 1)
#	print "paintingsDictionary[selectedKeyForPaintingsDictionary] = " + str(paintingsDictionary[selectedKeyForPaintingsDictionary])
#	print "completion/100.0 = " + str(completion/100.0)
	paintingsDictionary[selectedKeyForPaintingsDictionary].setUniformFloat('BlendAmount', 1.0 - float(completion/100.0))

def onSensorDown(e):
#	print "e.button1 = " + str(e.button)
	global theControllerToUse, theControllerNOTtoUse, trackpadState, stimulate, videoListIndex, selectedPaintingIndex, videoLoopsRemaining
	global leftVideoRenderingBoard, rightVideoRenderingBoard, videoRenderingBoard, vidLoopsRemaining, videoToPlay

	if e.object is theControllerToUse:
		if (e.button == steamvr.BUTTON_TRIGGER) and (stimulate):
			#stimulation code below:
			
			vidLoopsRemaining = videoLoopsRemaining[videoListIndex]
			
			if vidLoopsRemaining > 0:
#				leftVideoRenderingBoard.visible(True)
#				rightVideoRenderingBoard.visible(True)
#				videoRenderingBoard.visible(True)
#				setBackgroundVisibility(False)

#				leftVideoRenderingBoard.texture(videoToPlay)
#				rightVideoRenderingBoard.texture(videoToPlay)

				startStimTimer()
				
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
timeToStartPlayingTheVideoFrom = [None] * numberOfVideos		#this stores the number of seconds into the video from where it should start playing in the next cycle

if 'experimental condition' == choices[experimentalConditionChosen]:
	if 'dense' == stimuliChoices[stimChosen]:
		#In the "dense" experimental condition, during the first 30% and the last 30% of time, the _dense vids are shown, 
		#and the _densest videos are shown during the middle 40% of time.
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
		#In the "sparse" experimental condition, during the first 30% and the last 30% of time, the _sparsest vids are shown, 
		#and the _sparse videos are shown during the middle 40% of time.
		sparseVideoPaths[0] = 'media/onParasol1_sparsest.avi'
		sparseVideoPaths[1] = 'media/offParasol1_sparsest.avi'
		sparseVideoPaths[2] = 'media/onMidget1_sparsest.avi'
		sparseVideoPaths[3] = 'media/offMidget1_sparsest.avi'
		sparseVideoPaths[4] = 'media/sbc1_sparsest.avi'
		sparseVideoPaths[5] = 'media/onParasol2_sparsest.avi'
		sparseVideoPaths[6] = 'media/offParasol2_sparsest.avi'
		sparseVideoPaths[7] = 'media/onMidget2_sparsest.avi'
		sparseVideoPaths[8] = 'media/offMidget2_sparsest.avi'
		sparseVideoPaths[9] = 'media/sbc2_sparsest.avi'

		denseVideoPaths[0] = 'media/onParasol1_sparse.avi'
		denseVideoPaths[1] = 'media/offParasol1_sparse.avi'
		denseVideoPaths[2] = 'media/onMidget1_sparse.avi'
		denseVideoPaths[3] = 'media/offMidget1_sparse.avi'
		denseVideoPaths[4] = 'media/sbc1_sparse.avi'
		denseVideoPaths[5] = 'media/onParasol2_sparse.avi'
		denseVideoPaths[6] = 'media/offParasol2_sparse.avi'
		denseVideoPaths[7] = 'media/onMidget2_sparse.avi'
		denseVideoPaths[8] = 'media/offMidget2_sparse.avi'
		denseVideoPaths[9] = 'media/sbc2_sparse.avi'
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
	timeToStartPlayingTheVideoFrom[i] = 0

lengthOfEachStimVideo = 0
if 'experimental condition' == choices[experimentalConditionChosen]:
	lengthOfEachStimVideo = denseVideoPlaceholder[0].getDuration()
else:
	lengthOfEachStimVideo = sparseVideoPlaceholder[0].getDuration()

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

#timer and completion
totalCanvases = 11
# Add canvases for completion and timer displays
completionCanvas = [0] * totalCanvases
completionCanvasPos = [0] * totalCanvases
completionCanvasEuler = [0] * totalCanvases
completionPanel = [0] * totalCanvases

#timeredCanvas = [0] * totalCanvases
#timeredCanvasPos = [0] * totalCanvases
#timeredCanvasEuler = [0] * totalCanvases
#timeredPanel = [0] * totalCanvases

#timerCompletionLink = [0] * totalCanvases

completionInstructions ="""00:00
"""
#timeredInstructions ="""0% complete.
#"""

canvasSize = 1.5

completionCanvasPos[0] = [-4.85, 0.85, 0.3]
completionCanvasPos[1] = [-4.85, 0.8, 2.5]
completionCanvasPos[2] = [-4.85, 0.95, 4.8]
completionCanvasPos[3] = [-4.85, 1.15, 6.7]
completionCanvasPos[4] = [-3.3, 1.05, 9.0]
completionCanvasPos[5] = [0.0, 1.1, 9.83]
completionCanvasPos[6] = [3.0, 1.3, 9.2]
completionCanvasPos[7] = [4.75, 1.4, 6.7]
completionCanvasPos[8] = [4.75, 1.2, 4.6]
completionCanvasPos[9] = [4.75, 1.6, 2.5]
completionCanvasPos[10] = [4.75, 1.55, 0.3]

completionCanvasEuler[0] = [-90.0, 0.0, 0.0]
completionCanvasEuler[1] = [-90.0, 0.0, 0.0]
completionCanvasEuler[2] = [-90.0, 0.0, 0.0]
completionCanvasEuler[3] = [-90.0, 0.0, 0.0]
completionCanvasEuler[4] = [-35.0, 0.0, 0.0]
completionCanvasEuler[5] = [0.0, 0.0, 0.0]
completionCanvasEuler[6] = [35.0, 0.0, 0.0]
completionCanvasEuler[7] = [90.0, 0.0, 0.0]
completionCanvasEuler[8] = [90.0, 0.0, 0.0]
completionCanvasEuler[9] = [90.0, 0.0, 0.0]
completionCanvasEuler[10] = [90.0, 0.0, 0.0]

#timerCompletionSeparation = 0.48

#for i in range(totalCanvases):
#	if i <= int(totalCanvases/3.0):
#		timeredCanvasPos[i] = [completionCanvasPos[i][0], completionCanvasPos[i][1], completionCanvasPos[i][2] - timerCompletionSeparation]
#	elif i == 4:
#		timeredCanvasPos[i] = [completionCanvasPos[i][0] - timerCompletionSeparation/2.0, completionCanvasPos[i][1], completionCanvasPos[i][2] - timerCompletionSeparation/2.0]
#	elif i == 5:
#		timeredCanvasPos[i] = [completionCanvasPos[i][0] - timerCompletionSeparation, completionCanvasPos[i][1], completionCanvasPos[i][2]]
#	elif i == 6:
#		timeredCanvasPos[i] = [completionCanvasPos[i][0] - timerCompletionSeparation/2.0, completionCanvasPos[i][1], completionCanvasPos[i][2] - timerCompletionSeparation/2.0]
#	elif i >= int(2 * totalCanvases/3.0):
#		timeredCanvasPos[i] = [completionCanvasPos[i][0], completionCanvasPos[i][1], completionCanvasPos[i][2] + timerCompletionSeparation]

#timeredCanvasPos[1] = [-4.75, 0.85, 2.7 - timerCompletionSeparation]
#timeredCanvasPos[2] = [-4.75, 0.85, 4.0 - timerCompletionSeparation]
#timeredCanvasPos[3] = [-4.75, 0.85, 5.5 - timerCompletionSeparation]
#timeredCanvasPos[4] = [-1.0, 0.85, 7.0]
#timeredCanvasPos[5] = [0.0, 0.85, 7.0]
#timeredCanvasPos[6] = [1.0, 0.85, 7.0]
#timeredCanvasPos[7] = [4.75, 0.85, 3.5 + timerCompletionSeparation]
#timeredCanvasPos[8] = [4.75, 0.85, 2.5 + timerCompletionSeparation]
#timeredCanvasPos[9] = [4.75, 0.85, 1.5 + timerCompletionSeparation]
#timeredCanvasPos[10] = [4.75, 0.85, 0.5 + timerCompletionSeparation]

#	timeredCanvasEuler[i] = [completionCanvasEuler[i][0], completionCanvasEuler[i][1], completionCanvasEuler[i][2]]
#timeredCanvasEuler[0] = [-90.0, 0.0, 0.0]
#timeredCanvasEuler[1] = [-90.0, 0.0, 0.0]
#timeredCanvasEuler[2] = [-90.0, 0.0, 0.0]
#timeredCanvasEuler[3] = [-90.0, 0.0, 0.0]
#timeredCanvasEuler[4] = [-45.0, 0.0, 0.0]
#timeredCanvasEuler[5] = [0.0, 0.0, 0.0]
#timeredCanvasEuler[6] = [45.0, 0.0, 0.0]
#timeredCanvasEuler[7] = [90.0, 0.0, 0.0]
#timeredCanvasEuler[8] = [90.0, 0.0, 0.0]
#timeredCanvasEuler[9] = [90.0, 0.0, 0.0]
#timeredCanvasEuler[10] = [90.0, 0.0, 0.0]

#maxNumberOfVideoLoops
#videoLoopsRemaining[
#itemIndexWithNoStimulation

def updateCompletionDisplay(canvasIndex = selectedPaintingIndex):
	global maxNumberOfVideoLoops, videoLoopsRemaining, totalLengthOfEachStimulationSessionInSeconds, lengthOfEachStimVideo, completionPanel, timeToStartPlayingTheVideoFrom

	if canvasIndex == -1: return
	
	videoListInd = canvasIndex
	completion = 100.0

	if videoListInd > itemIndexWithNoStimulation: videoListInd -= 1
	
	totalTime = totalLengthOfEachStimulationSessionInSeconds
	
	if canvasIndex != itemIndexWithNoStimulation:
		timeElapsed = totalTime - (videoLoopsRemaining[videoListInd] * lengthOfEachStimVideo - timeToStartPlayingTheVideoFrom[videoListInd])	#this is the stim-time that is remaining at this specific stimulation portal
		completion = (timeElapsed/totalTime) * 100.0
	else:
		timeElapsed = totalTime
#		completion = (maxNumberOfVideoLoops - videoLoopsRemaining[videoListInd])*100.0/maxNumberOfVideoLoops
	

#	timeredPanelText = str('%0*d' % (3, int(completion))) + "%"
	if int(completion) == 100:
		completionPanelText = str('%0*d' % (3, int(completion))) + "%"
	else:
		completionPanelText = str('%0*d' % (3, int(completion))) + "%: " + str('%0*d' % (3, int(timeElapsed))) + " of " + str(totalTime) + " seconds"

#	print "for canvasIndex " + str(canvasIndex) + ", completion: " + timeredPanelText
	print "for canvasIndex " + str(canvasIndex) + ", completion: " + completionPanelText
	
#	timeredPanel[canvasIndex].setText(timeredPanelText)
	completionPanel[canvasIndex].setText(completionPanelText)

for i in range(totalCanvases):

#	test = viz.addGUICanvas(pos=completionCanvasPos[i])
#	test
#	completionCanvas[i] = viz.addGUICanvas(pos=completionCanvasPos[i])
	completionCanvas[i] = viz.addGUICanvas()
	completionCanvas[i].setMouseStyle(0)
	completionCanvas[i].alignment(viz.ALIGN_CENTER)
	completionCanvas[i].setRenderWorld([400,400], [canvasSize,canvasSize])

	completionPanel[i] = vizinfo.InfoPanel(completionInstructions, title='Completion', key=None, icon=False, align=viz.ALIGN_CENTER, parent=completionCanvas[i])

#	timeredCanvas[i] = viz.addGUICanvas(pos=timeredCanvasPos[i])
#	timeredCanvas[i].setEuler(timeredCanvasEuler[i])
#	timeredCanvas[i] = viz.addGUICanvas()
#	link = viz.link(completionCanvas[i], timeredCanvas[i])
#	link.
#	timerCompletionLink[i] = viz.link(completionCanvas[i], timeredCanvas[i])
#	timerCompletionLink[i].preTrans([-timerCompletionSeparation, 0.0, 0.0])
#	timeredCanvas[i].setParent(completionCanvas[i])
#	timeredCanvas[i].setPosition([-timerCompletionSeparation, 0.0, 0.0])
#	timeredCanvas[i].setMouseStyle(0)
#	timeredCanvas[i].alignment(viz.ALIGN_CENTER)
#	timeredCanvas[i].setRenderWorld([400,400], [canvasSize,canvasSize])

#	timeredPanel[i] = vizinfo.InfoPanel(timeredInstructions, title='Completion', key=None, icon=False, align=viz.ALIGN_CENTER, parent=timeredCanvas[i])
	
	#positioning and orienting the timer and completion display canvases
	completionCanvas[i].setPosition(completionCanvasPos[i])
	completionCanvas[i].setEuler(completionCanvasEuler[i])
	
	updateCompletionDisplay(i)


#testing for transparency below
#gallery.visible(False)
#starry_night_black = vizfx.addChild('models/painting_starry-night_black.osgb')
#starry_night = vizfx.addChild('models/painting_starry-night.osgb')
#
#starry_night_black.drawOrder(0)
#starry_night.drawOrder(1)
#
#starry_night.enable(viz.BLEND)
#starry_night.blendFunc(viz.GL_SRC_ALPHA, viz.GL_ONE_MINUS_SRC_ALPHA)

#viz.enable(viz.ALPHA_TEST)
#starry_night.alphaFunc(viz.GL_LESS)
#starry_night.alpha(0.1)

#birth_of_venus = vizfx.addChild('models/painting_birth-of-venus_blend.osgb')
#dali_memory = vizfx.addChild('models/painting_dali-memory_blend.osgb')
#harring_bestbuddies = vizfx.addChild('models/painting_harring-bestbuddies_blend.osgb')
#magritte = vizfx.addChild('models/painting_magritte_blend.osgb')
#monalisa = vizfx.addChild('models/painting_monalisa_blend.osgb')
#monet_venice = vizfx.addChild('models/painting_monet-venice_blend.osgb')
#picasso = vizfx.addChild('models/painting_picasso_blend.osgb')
#scream = vizfx.addChild('models/painting_scream_blend.osgb')
#starry_night = vizfx.addChild('models/painting_starry-night_blend.osgb')
#van_gogh = vizfx.addChild('models/painting_van-gogh_blend.osgb')
#warhol_soup = vizfx.addChild('models/painting_warhol_soup_blend.osgb')

#starry_night.visible(False)
#logo = viz.addChild('logo.ive')
#logo.visible(False)
#logo.setPosition(starry_night.getPosition())
#tex1 = viz.addTexture('brick.jpg', wrap=viz.REPEAT)
#tex2 = viz.addTexture('gb_noise.jpg', wrap=viz.REPEAT)

# Apply the effect to the models
#birth_of_venus.apply(texBlendEffect)
#dali_memory.apply(texBlendEffect)
#harring_bestbuddies.apply(texBlendEffect)
#magritte.apply(texBlendEffect)
#monalisa.apply(texBlendEffect)
#monet_venice.apply(texBlendEffect)
#picasso.apply(texBlendEffect)
#scream.apply(texBlendEffect)
#starry_night.apply(texBlendEffect)
#van_gogh.apply(texBlendEffect)
#warhol_soup.apply(texBlendEffect)

#def SetBlendAmount(pos, model):
#	#Set the value of the blend amount property
#	model.setUniformFloat('BlendAmount', pos)
#	print "pos = " + str(pos)

# Create sliders to control the blend amount for each object
#slider1 = viz.addSlider(pos=[0.75,0.1,0])
#
#vizact.onslider(slider1, SetBlendAmount, birth_of_venus)
#vizact.onslider(slider1, SetBlendAmount, dali_memory)
#vizact.onslider(slider1, SetBlendAmount, harring_bestbuddies)
#vizact.onslider(slider1, SetBlendAmount, magritte)
#vizact.onslider(slider1, SetBlendAmount, monalisa)
#vizact.onslider(slider1, SetBlendAmount, monet_venice)
#vizact.onslider(slider1, SetBlendAmount, picasso)
#vizact.onslider(slider1, SetBlendAmount, scream)
#vizact.onslider(slider1, SetBlendAmount, starry_night)
#vizact.onslider(slider1, SetBlendAmount, van_gogh)
#vizact.onslider(slider1, SetBlendAmount, warhol_soup)

#starry_night.texture(tex1)
#starry_night.texture(tex2,'',1)
#blend = viz.addFragmentProgram('multitexblend.fp')
#starry_night.apply(blend)
#
#blend.param(0,0.0)
#
#slider = viz.addSlider()
#slider.setPosition(0.5,0.1)
#
#def blendTextures(pos):
#	blend.param(0,pos)
#
#vizact.onslider(slider, blendTextures)
