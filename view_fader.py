"""Fades the view on each display to a solid color"""

import viz
import vizconnect
import vizact
import vizshape
import viztask


class Fader(viz.VizNode):
	"""Screenspace quad of solid color for fade in/out effect"""
	def __init__(self, color=viz.BLACK, fadeTime=0.5):
		# Init the base class from a group node parented to ortho
		node = viz.addGroup()
		viz.VizNode.__init__(self, node.id)
		
		# Initialize a GUI canvas to serve as the fade parent
		self.canvas = viz.addGUICanvas()
		
		# Define the dimensions of the canvas
		canvasDimensions = [800, 600]  # width, height in (virtual) pixels
		
		# Canvas field of view will be huge, just shy of maximum
		canvasFOV = 179.9
		
		# Depth of 1m
		canvasDepth = 1  # distance out in front (meters)
		
		# Set up the canvas render parameters to be face-locked
		self.canvas.setRenderWorldOverlay(canvasDimensions, canvasFOV, canvasDepth)
		
		# Add quad parented to the canvas, placing it at the origin in
		# canvas-space, which is the lower-left corner of the canvas.
		# When setting the size, the units are pixels, not meters
		self._fadeQuad = vizshape.addQuad(color=color, parent=self.canvas, size=canvasDimensions, disable=viz.LIGHTING)
		
		# Center the quad in canvas space
		self._fadeQuad.setPosition(canvasDimensions[0] / 2, canvasDimensions[1] / 2, 0)
		
		# Preserve the fade time attribute
		self._fadeTime = fadeTime
		
		# Define action object attributes for fades in and out
		self._fadeInAction = vizact.fadeTo(0, time=self._fadeTime)
		self._fadeOutAction = vizact.fadeTo(1, time=self._fadeTime)
	
	def fadeIn(self):
		"""Fades in to the scene, quad becomes transparent"""
		self._fadeQuad.runAction(self._fadeInAction)
	
	def fadeInTask(self):
		"""Yieldable task for fading in"""
		self.fadeIn()
		yield viztask.waitActionEnd(self._fadeQuad, self._fadeInAction)
	
	def fadeOut(self):
		"""Fades to black, quad becomes opaque"""
		self._fadeQuad.runAction(self._fadeOutAction)
	
	def fadeOutTask(self):
		"""Yieldable task for fading out"""
		self.fadeOut()
		yield viztask.waitActionEnd(self._fadeQuad, self._fadeOutAction)


def addFader(color=viz.BLACK, fadeTime=1):
	"""Convenience function to add and return a new fader"""
	return Fader(color=color, fadeTime=fadeTime)


if __name__ == '__main__':
	viz.go()
	
	piazza = viz.add('piazza.osgb')
	
	fader = addFader()
	
	def fadeDemoTask():
		"""Task demonstrating use of fade tasks"""
		while True:
			yield fader.fadeOutTask()
			yield viztask.waitTime(1)
			yield fader.fadeInTask()
			yield viztask.waitTime(1)
	
#viztask.schedule(fadeDemoTask)