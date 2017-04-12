viz.go()

#Add some textures 
tex1 = viz.addTexture('textures/blackSquare.png')
tex2 = viz.addTexture('textures/starryNight.png')

#Add a texture quad
quad = viz.addTexQuad()

#Apply the textures to the quad
quad.texture(tex1)
quad.texture(tex2,'',1)

#Blend 60% of tex2 with 40% of tex1
quad.texblend(0.6,'',1)
