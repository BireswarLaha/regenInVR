import vizfx
import vizcam

viz.setMultiSample(8)
viz.go()

tracker = vizcam.addKeyboard6DOF()
tracker.setPosition([0,1.8,0])
viz.link(tracker, viz.MainView)

painting = vizfx.addChild('models/painting_starry-night.osgb')
background = vizfx.addChild('models/painting_starry-night_black.osgb')

painting.visible(True)
background.visible(True)

painting.enable(viz.BLEND)
background.enable(viz.BLEND)
painting.drawOrder(10,bin=viz.BIN_TRANSPARENT)
background.drawOrder(10,bin=viz.BIN_TRANSPARENT)

alphaOfPic = 0.0
alphaOfBlack = 1.0
change = 0.1

def alterTheFirstPaintingsAlpha(direction = "plus"):
	global alphaOfPic, alphaOfBlack, change
	
	print "\nalphaOfPic = " + str(alphaOfPic)
	print "alphaOfBlack = " + str(alphaOfBlack)
	
	if (direction == "plus") and (alphaOfPic < 0.9):
		print "incrementing alpha"
		alphaOfPic += change
		print "alphaOfPic = " + str(alphaOfPic)
	if (direction == "minus") and (alphaOfPic > 0.1): alphaOfPic -= change

	painting.alpha(alphaOfPic)
	background.alpha(alphaOfBlack)

vizact.onkeydown('i', alterTheFirstPaintingsAlpha, "plus")
vizact.onkeydown('u', alterTheFirstPaintingsAlpha, "minus")
