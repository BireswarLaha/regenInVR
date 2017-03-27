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
gallery = vizfx.addChild('gallery.osgb')
gallery.hint(viz.OPTIMIZE_INTERSECT_HINT)
gallery.disable(viz.SHADOW_CASTING)

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
		if mode:
			gallery.apply(highlightEffect, node=name)
		else:
			gallery.unapply(highlightEffect, node=name)

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

			# Hide instruction canvas after first jump
			canvas.visible(False)

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

# Add directions to canvas
canvas = viz.addGUICanvas(pos=[0, 3.0, 6.0])
canvas.setMouseStyle(0)
canvas.alignment(viz.ALIGN_CENTER)
canvas.setRenderWorld([400,400], [5.0,5.0])

instructions ="""INSTRUCTIONS:
1. 10 out of the 11 paintings pack unique visual stimulation.
2. Find each painting with an active stimulation.
3. Complete all sessions to your satisfaction.

TODO: Use the trigger to select and jump to a painting. GO GET THEM!!"""
panel = vizinfo.InfoPanel(instructions, title='NON-INVASIVE STIMULATION FOR VISION RESTORATION', key=None, icon=False, align=viz.ALIGN_CENTER, parent=canvas)

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
