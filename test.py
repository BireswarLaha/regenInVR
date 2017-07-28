import viz
viz.go()

myTexQuad = viz.addTexQuad(pos=[0,1.8,2])
myTexQuad.name = "texQuadCustomName"

info = viz.intersect([0,1.8,0],[0,1.8,4])
if info.valid:
	if info.object == myTexQuad:
		print myTexQuad.name
		
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

myTexQuad.apply(highlightEffect, node=myTexQuad.name)
