from PIL import Image, ImageDraw
import math as maths

class make():
	def __init__(self, gEngine, opts):
		self.out = ""
		p = opts.split(" ")
		if (p[1] == "MAP"):
			print("Let's make a map")
			img = Image.new("RGB", (1960, 1080))
			min_x = 0
			min_y = 0
			max_x = 0
			max_y = 0
			for i in gEngine.mapp.tiles.keys():
				if (i[0] < min_x):
					min_x = i[0]
				elif (i[0] > max_x):
					max_x = i[0]

				if (i[1] < min_y):
					min_y = i[1]
				elif (i[1] > max_y):
					max_y = i[1]
					
				#print(i)
			cols = [(255,255,255),(0,255,0), (127,127,127), (0, 127, 0), (0, 64, 0)]
			print(min_x, max_x, min_y, max_y)
			min_scale_x = 1960 / (max_x - min_x + 1)
			min_scale_y = 1080 / (max_y - min_y + 1)
			#print(min_scale_x, min_scale_y)
			scale = maths.floor(min(min_scale_x, min_scale_y))
			#print("Scale is:", scale)
			drw = ImageDraw.Draw(img)
			#print(gEngine.mapp.tiles.keys())
			for i in range(min_x, max_x+2):
				for j in range(min_y, max_y+2):
					if ((i,j) in gEngine.mapp.tiles.keys()):
						#print("Yes - ", (i,j))
						drw.rectangle(((i - min_x) * scale, (j - min_y) * scale, (i - min_x + 1) * scale, (j - min_y + 1) * scale), fill=cols[gEngine.mapp.tiles[i,j]['type'] % len(cols)])
						
						if (gEngine.mapp.tiles[i,j]['type'] == 0) and ("house" in gEngine.mapp.tiles[i,j]) and (gEngine.mapp.tiles[i,j]['house'] == True):
							drw.ellipse(((i - min_x + 0.2) * scale, (j - min_y + 0.2) * scale, (i - min_x + 0.8) * scale, (j - min_y + 0.8) * scale), fill=(255,0,0)) 
							drw.ellipse(((i - min_x + 0.3) * scale, (j - min_y + 0.3) * scale, (i - min_x + 0.7) * scale, (j - min_y + 0.7) * scale), fill=(127,127,0)) 
					else:
						#print("No - ", (i,j))
						pass
						
 #			drw.circle((gEngine.player[0]
		#	drw.ellipse(((gEngine.position['x'] - min_x + 0.4) * scale, (gEngine.position['y'] - min_y + 0.4) * scale, (gEngine.position['x'] - min_x + 0.6) * scale, (gEngine.position['y'] - min_y + 0.6) * scale), fill=(255,0,0)) 
			for i in gEngine.player:
				if (i['human'] == False):
					print(i)
					if ("route" in i and len(i['route']) > 0):
						end = i['route'][-1]
						drw.line(((i['position']['x'] - min_x + 0.5) * scale, (i['position']['y'] - min_y+0.5) * scale, (end[0] - min_x+0.5) * scale, (end[1] - min_y+0.5) * scale), fill=(0,0,255), width=5)
					co = (0,0,255)
				else:
					co = (255,0,0)
					
				drw.ellipse(((i['position']['x'] - min_x + 0.4) * scale, (i['position']['y'] - min_y + 0.4) * scale, (i['position']['x'] - min_x + 0.6) * scale, (i['position']['y'] - min_y + 0.6) * scale), fill=co) 

			self.out += "Map saved at map.png. "
			img.save("map.png")
			pass
			
		else:
			print(opts)
	
	def pushTime(self):
		return 0
	
	def describe(self):
		return ""
		
muds = {
	"START" : [ "MAKE [MAKE_OPTIONS]" ],
	"MAKE_OPTIONS" : [ "MAP" ],
}

cmds = {
	"MAKE" : [ "cmds.make", "make" ],
}
