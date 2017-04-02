#Developed on Vizard sample code, titled 'steamvrExample.py'
#Bireswar Laha, Huberman Lab, Department of Neurobiology, Stanford University
#Dated: March, 2017

import sys
import viz
import vizfx
import vizact
import vizinfo
import viztask
import steamvr
import vector3

# Initialize window
viz.setMultiSample(8)
viz.go()

# Setup SteamVR HMD
hmd = steamvr.HMD()
if not hmd.getSensor():
	sys.exit('SteamVR HMD not detected')

# Setup navigation node and link to main view
navigationNode = viz.addGroup()
viewLink = viz.link(navigationNode, viz.MainView)
viewLink.preMultLinkable(hmd.getSensor())

# Load environment
gallery = vizfx.addChild('models/galleryWithoutPaintings.osgb')
gallery.hint(viz.OPTIMIZE_INTERSECT_HINT)
gallery.disable(viz.SHADOW_CASTING)

paintingsDictionary = {}
#load paintings
painting_birth_of_venus = vizfx.addChild('models/painting_birth-of-venus.osgb')
paintingsDictionary['painting_birth-of-venus'] = painting_birth_of_venus
painting_dali_memory = vizfx.addChild('models/painting_dali-memory.osgb')
paintingsDictionary['painting_dali-memory'] = painting_dali_memory
painting_harring_bestbuddies = vizfx.addChild('models/painting_harring-bestbuddies.osgb')
paintingsDictionary['painting_harring-bestbuddies'] = painting_harring_bestbuddies
painting_magritte = vizfx.addChild('models/painting_magritte.osgb')
paintingsDictionary['painting_magritte'] = painting_magritte
painting_monalisa = vizfx.addChild('models/painting_monalisa.osgb')
paintingsDictionary['painting_monalisa'] = painting_monalisa
painting_monet_venice = vizfx.addChild('models/painting_monet-venice.osgb')
paintingsDictionary['painting_monet-venice'] = painting_monet_venice
painting_picasso = vizfx.addChild('models/painting_picasso.osgb')
paintingsDictionary['painting_picasso'] = painting_picasso
painting_scream = vizfx.addChild('models/painting_scream.osgb')
paintingsDictionary['painting_scream'] = painting_scream
painting_starry_night = vizfx.addChild('models/painting_starry-night.osgb')
paintingsDictionary['painting_starry-night'] = painting_starry_night
painting_van_gogh = vizfx.addChild('models/painting_van-gogh.osgb')
paintingsDictionary['painting_van-gogh'] = painting_van_gogh
painting_warhol_soup = vizfx.addChild('models/painting_warhol_soup.osgb')
paintingsDictionary['painting_warhol_soup'] = painting_warhol_soup

painting_birth_of_venus.visible(False)
painting_dali_memory.visible(False)
painting_harring_bestbuddies.visible(False)
painting_magritte.visible(False)
painting_monalisa.visible(False)
painting_monet_venice.visible(False)
painting_picasso.visible(False)
painting_scream.visible(False)
painting_starry_night.visible(False)
painting_van_gogh.visible(False)
painting_warhol_soup.visible(False)

painting_birth_of_venus_black = vizfx.addChild('models/painting_birth-of-venus_black.osgb')
paintingsDictionary['painting_birth-of-venus_black'] = painting_birth_of_venus_black
painting_dali_memory_black = vizfx.addChild('models/painting_dali-memory_black.osgb')
paintingsDictionary['painting_dali-memory_black'] = painting_dali_memory_black
painting_harring_bestbuddies_black = vizfx.addChild('models/painting_harring-bestbuddies_black.osgb')
paintingsDictionary['painting_harring-bestbuddies_black'] = painting_harring_bestbuddies_black
painting_magritte_black = vizfx.addChild('models/painting_magritte_black.osgb')
paintingsDictionary['painting_magritte_black'] = painting_magritte_black
painting_monalisa_black = vizfx.addChild('models/painting_monalisa_black.osgb')
paintingsDictionary['painting_monalisa_black'] = painting_monalisa_black
painting_monet_venice_black = vizfx.addChild('models/painting_monet-venice_black.osgb')
paintingsDictionary['painting_monet-venice_black'] = painting_monet_venice_black
painting_picasso_black = vizfx.addChild('models/painting_picasso_black.osgb')
paintingsDictionary['painting_picasso_black'] = painting_picasso_black
painting_scream_black = vizfx.addChild('models/painting_scream_black.osgb')
paintingsDictionary['painting_scream_black'] = painting_scream_black
painting_starry_night_black = vizfx.addChild('models/painting_starry-night_black.osgb')
paintingsDictionary['painting_starry-night_black'] = painting_starry_night_black
painting_van_gogh_black = vizfx.addChild('models/painting_van-gogh_black.osgb')
paintingsDictionary['painting_van-gogh_black'] = painting_van_gogh_black
painting_warhol_soup_black = vizfx.addChild('models/painting_warhol_soup_black.osgb')
paintingsDictionary['painting_warhol_soup_black'] = painting_warhol_soup_black

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
paintingNames.append('painting_picasso')
paintingNames.append('painting_dali-memory')
paintingNames.append('painting_van-gogh')
paintingNames.append('painting_monet-venice')
paintingNames.append('painting_scream')
paintingNames.append('painting_starry-night')
paintingNames.append('painting_harring-bestbuddies')
paintingNames.append('painting_monalisa')
paintingNames.append('painting_warhol_soup')
paintingNames.append('painting_birth-of-venus')
paintingNames.append('painting_magritte')

from random import randint
itemIndexWithNoStimulation = randint(0,10)
print "itemIndexWithNoStimulation = " + str(itemIndexWithNoStimulation)
print "painting without stimulation for this round is " + str(paintingNames[itemIndexWithNoStimulation])

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
		splitNames = nameNew.split("-")
		global paintingsDictionary

		if paintingsDictionary[nameNew].getVisible() == False:
			nameNew = nameNew + "_black"
		
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

			global itemIndexWithNoStimulation, paintingNames, canvasForStim, canvasWithoutStim, canvasForInitMsg, paintingsDictionary

			# Hide instruction canvasForInitMsg after first jump
			canvasForInitMsg.visible(False)
			
			separationOnHorizontalPlane = 0.8
			verticalPosOfCanvas = 0.6
			normalizedDirectionToShiftTheCanvas = vector3.Vec3ToVizardFloatList(vector3.vizardFloatListToVec3([-info.normal[0], 0.0, -info.normal[2]]).normalize())
			
			if (info.name != paintingNames[itemIndexWithNoStimulation]) and (paintingsDictionary[info.name].getVisible() == False) :
				canvasWithoutStim.visible(False)
				canvasForStim.visible(True)
				canvasForStim.billboard(viz.BILLBOARD_VIEW_POS)
				canvasForStim.setPosition(
					jumpPos[0] + (normalizedDirectionToShiftTheCanvas[0] * separationOnHorizontalPlane),
					verticalPosOfCanvas,
					jumpPos[2] + (normalizedDirectionToShiftTheCanvas[2] * separationOnHorizontalPlane))
					
			else:
				print "info.name = " + str(info.name)
				paintingsDictionary[info.name + '_black'].visible(False)
				paintingsDictionary[info.name].visible(True)
				canvasForStim.visible(False)
				canvasWithoutStim.visible(True)
				canvasWithoutStim.billboard(viz.BILLBOARD_VIEW_POS)
				canvasWithoutStim.setPosition(
					jumpPos[0] + (normalizedDirectionToShiftTheCanvas[0] * separationOnHorizontalPlane),
					verticalPosOfCanvas,
					jumpPos[2] + (normalizedDirectionToShiftTheCanvas[2] * separationOnHorizontalPlane))

# Add controllers
for controller in steamvr.getControllerList():

	# Create model for controller
	controller.model = controller.addModel(parent=navigationNode)
	controller.model.disable(viz.INTERSECTION)
	viz.link(controller, controller.model)

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

#videos to be played
videoPlaceholder1 = viz.addVideo('media/maxFireStim1_OffParasol.avi')
#videoPlaceholder2 = viz.addVideo('media/onParasol2.avi')
#videoPlaceholder3 = viz.addVideo('media/offParasol1.avi')
#videoPlaceholder4 = viz.addVideo('media/offParasol2.avi')
#videoPlaceholder5 = viz.addVideo('media/onMidget1.avi')
#videoPlaceholder6 = viz.addVideo('media/onMidget2.avi')
#videoPlaceholder7 = viz.addVideo('media/offMidget1.avi')
#videoPlaceholder8 = viz.addVideo('media/offMidget2.avi')
#videoPlaceholder9 = viz.addVideo('media/SBS1.avi')
#videoPlaceholder10 = viz.addVideo('media/SBS1.avi')

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
