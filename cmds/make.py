from PIL import Image, ImageDraw, ImageFont
import math as maths

def marker(img, loc = (0,0)):
	return img

class make():
	def __init__(self, gEngine, opts):
	
		m_offset = [0,0]
		self.out = ""
		heatmap = False
		forced_bounds = [None, None, None, None]
		fog = True
		viz = False
		houses = True
		p = opts#.split(" ")
		if (p[1] == "MAP"):
			print("Let's make a map")
			nx = p[2:]
			if (len(nx) > 0):
				if (nx[0] == "WITH"):
					nx.pop(0)
					while (len(nx) > 0):
						print(nx)
						if (len(nx) > 2 and nx[0] == "LOWER" and nx[1] == "X"):
							#print(nx)
							set_min_x = int(nx[2].strip(",\""))
							nx = nx[3:]
							forced_bounds[0] = set_min_x
						elif (len(nx) > 2 and nx[0] == "LOWER" and nx[1] == "Y"):
							#print(nx)
							set_min_y = int(nx[2].strip(",\""))
							nx = nx[3:]
							forced_bounds[2] = set_min_y
						elif (len(nx) > 2 and nx[0] == "UPPER" and nx[1] == "X"):
							#print(nx)
							set_min_x = int(nx[2].strip(",\""))
							nx = nx[3:]
							forced_bounds[1] = set_min_x
						elif (len(nx) > 2 and nx[0] == "UPPER" and nx[1] == "Y"):
							#print(nx)
							set_min_y = int(nx[2].strip(",\""))
							nx = nx[3:]
							forced_bounds[3] = set_min_y
							
						elif (nx[0] == "HEAT" and nx[1] in ["ZONES", "ZONES,"]):
							nx = nx[2:]
							heatmap = True
						elif(nx[0] == "NO" and nx[1] in ["HOUSES", "HOUSES,"]):
							nx = nx[2:]
							houses = False
						elif(nx[0] == "NO" and nx[1] == "FOG" and nx[2] == "OF" and nx[3] in ["WAR", "WAR,"]):
							nx = nx[4:]
							fog = False
						elif(nx[0] == "ALL" and nx[1] in ["SQUARES", "TILES"] and nx[2] in ["VISIBLE", "VISIBLE,"]):
							nx = nx[3:]
							viz = True
						else:
							nx = nx[1:]
						
			img = Image.new("RGB", (1960, 1080))
			img_overlay = Image.new("RGBA", (1960, 1080), (0,0,0,0))
			fow = Image.new("RGBA", (1960, 1080), (0,0,0,0))
			min_x = None
			min_y = None
			max_x = None
			max_y = None
			for i in gEngine.mapp.tiles.keys():
				if ("visible" in gEngine.mapp.tiles[i] and gEngine.mapp.tiles[i]['visible'] == True) or (viz == True):
					if (min_x is None or i[0] < min_x):
						min_x = i[0]
					elif (max_x is None or  i[0] > max_x):
						max_x = i[0]

					if (min_y is None or i[1] < min_y):
						min_y = i[1]
					elif (max_y is None or i[1] > max_y):
						max_y = i[1]
				elif ("visible" not in gEngine.mapp.tiles[i]):
					gEngine.mapp.tiles[i]['visible'] = False

			if (forced_bounds[0] is not None):
				min_x = forced_bounds[0]
			if (forced_bounds[1] is not None):
				max_x = forced_bounds[1]
			if (forced_bounds[2] is not None):
				min_y = forced_bounds[2]
			if (forced_bounds[3] is not None):
				max_y = forced_bounds[3]
				
				#print(i)
			cols = [(255,255,255),(192, 255, 192), (0,255,0), (0, 127, 0), (0, 64, 0), (127, 127, 127), (64,64,255), (255, 127, 0)]
			#print(min_x, max_x, min_y, max_y)
			min_scale_x = 1960 / (max_x - min_x + 1)
			min_scale_y = 1080 / (max_y - min_y + 1)
			scale = maths.floor(min(min_scale_x, min_scale_y))
			
			if (True):
				# So if I was to force the scale to be 16 around player 0?
				scale = 16
				pos = gEngine.player[gEngine.data['piq']]['position']
				min_x = pos['x'] - maths.ceil((1960/2) / 16)
				max_x = pos['x'] + maths.ceil((1960/2) / 16)
				min_y = pos['y'] - maths.ceil((1080/2) / 16)
				max_y = pos['y'] + maths.ceil((1080/2) / 16)
				
			drw = ImageDraw.Draw(img)
			ol = ImageDraw.Draw(img_overlay)
			max_sight = 0

			for i in range(min_x, max_x+2):
				for j in range(min_y, max_y+2):
					if ((i,j) in gEngine.mapp.tiles.keys()):
						if ("sightings" in gEngine.mapp.tiles[i,j]):
							if (gEngine.mapp.tiles[i,j]['sightings'] > max_sight):
								max_sight = gEngine.mapp.tiles[i,j]['sightings']

			# No tile drawing done before this point
			
			fowdrw = ImageDraw.Draw(fow)
			for i in range(min_x, max_x+2):
				for j in range(min_y, max_y+2):
					#p = gEngine.mapp.get_tile(i, j)
					if ((i,j) in gEngine.mapp.tiles.keys() and (gEngine.mapp.tiles[(i,j)]['visible'] == True or viz == True)):
						xo = abs(gEngine.player[gEngine.data['piq']]['position']['x'] - i) + abs(gEngine.player[gEngine.data['piq']]['position']['y'] - j)
						if (xo > gEngine.config['core']['fow_size']):
							fowdrw.rectangle((m_offset[0] + ((i - min_x) * scale), m_offset[1] + ((j - min_y) * scale), m_offset[0] + ((i - min_x + 1) * scale), m_offset[1] + ((j - min_y + 1) * scale)), fill=(0,0,0,255))

						drw.rectangle((m_offset[0] + ((i - min_x) * scale), m_offset[1] + ((j - min_y) * scale), m_offset[0] + ((i - min_x + 1) * scale), m_offset[1] + ((j - min_y + 1) * scale)), fill=cols[gEngine.mapp.tiles[i,j]['type'] % len(cols)])

			# Calculations redone to here
			# Xs with brockets to here
			# Ys with brockets to here
			
						if ("sightings" in gEngine.mapp.tiles[i,j]):
							ol.rectangle((m_offset[0] + (i - min_x) * scale, m_offset[1] + (j - min_y) * scale, (i - min_x + 1) * scale, m_offset[1] + (j - min_y + 1) * scale), fill=(255,0,0,int(gEngine.mapp.tiles[i,j]['sightings'] / max_sight * 255)))
							
						if (houses and gEngine.mapp.tiles[i,j]['type'] in [0, 1, 7]) and ("house" in gEngine.mapp.tiles[i,j]) and (gEngine.mapp.tiles[i,j]['house'] == True):
							drw.ellipse((m_offset[0] + (i - min_x + 0.2) * scale, m_offset[1] + (j - min_y + 0.2) * scale, m_offset[0] + (i - min_x + 0.8) * scale, m_offset[1] + (j - min_y + 0.8) * scale), fill=(255,0,0)) 
							drw.ellipse((m_offset[0] + (i - min_x + 0.3) * scale, m_offset[1] + (j - min_y + 0.3) * scale, m_offset[0] + (i - min_x + 0.7) * scale, m_offset[1] + (j - min_y + 0.7) * scale), fill=(127,127,0))

						if (houses and gEngine.mapp.tiles[i,j]['type'] in [0, 1, 7]) and ("station" in gEngine.mapp.tiles[i,j]) and (gEngine.mapp.tiles[i,j]['station'] == True):
							drw.ellipse((m_offset[0] + (i - min_x + 0.3) * scale, m_offset[1] + (j - min_y + 0.3) * scale, m_offset[0] + (i - min_x + 0.7) * scale, m_offset[1] + (j - min_y + 0.7) * scale), fill=(127,127,255)) 
							drw.ellipse((m_offset[0] + (i - min_x + 0.4) * scale, m_offset[1] + (j - min_y + 0.4) * scale, m_offset[0] + (i - min_x + 0.6) * scale, m_offset[1] + (j - min_y + 0.6) * scale), fill=(0,0,127))

						if (houses and gEngine.mapp.tiles[i,j]['type'] in [0, 1, 7]) and ("shop" in gEngine.mapp.tiles[i,j]) and (gEngine.mapp.tiles[i,j]['shop'] == True):
							drw.ellipse((m_offset[0] + (i - min_x + 0.3) * scale, m_offset[1] + (j - min_y + 0.3) * scale, m_offset[0] + (i - min_x + 0.7) * scale, m_offset[1] + (j - min_y + 0.7) * scale), fill=(127,255,127)) 
							drw.ellipse((m_offset[0] + (i - min_x + 0.4) * scale, m_offset[1] + (j - min_y + 0.4) * scale, m_offset[0] + (i - min_x + 0.6) * scale, m_offset[1] + (j - min_y + 0.6) * scale), fill=(0,127,0))

						#elif ("storage" in gEngine.mapp.tiles[i,j] and gEngine.mapp.tiles[i,j]["storage"]):
						#	drw.rectangle(((i - min_x + 0.3) * scale, (j - min_y + 0.3) * scale, (i - min_x +  0.7) * scale, (j - min_y + 0.7) * scale), outline=(63,127,0))
							
					else:
						#drw.rectangle(((i - min_x) * scale, (j - min_y) * scale, (i - min_x + 1) * scale - 1, (j - min_y + 1) * scale - 1), fill=(0,0,0))
						fowdrw.rectangle((m_offset[0] + (i - min_x) * scale, m_offset[1] + (j - min_y) * scale, m_offset[0] + (i - min_x + 1) * scale, m_offset[1] + (j - min_y + 1) * scale), fill=(0,0,0,255))
						
 #			drw.circle((gEngine.player[0]
		#	drw.ellipse(((gEngine.position['x'] - min_x + 0.4) * scale, (gEngine.position['y'] - min_y + 0.4) * scale, (gEngine.position['x'] - min_x + 0.6) * scale, (gEngine.position['y'] - min_y + 0.6) * scale), fill=(255,0,0)) 
			if (heatmap):
				img.paste(img_overlay, (0,0), img_overlay)

			fog_img = img.copy()
			ft = ImageFont.truetype("core/arial.ttf", 14)			
			
			for i in gEngine.mapp.towns:
				drw.text((m_offset[0] + (i[1][0][0] - min_x) * scale + 3, m_offset[1] + (i[1][0][1] - min_y) * scale + 3), i[0], (0, 0, 0), font=ft)
				drw.text((m_offset[0] + (i[1][0][0] - min_x) * scale + 2, m_offset[1] + (i[1][0][1] - min_y) * scale + 2), i[0], (255, 255, 255), font=ft)
				drw.rectangle((m_offset[0] + (i[1][0][0] - min_x) * scale, m_offset[1] + (i[1][0][1] - min_y) * scale, m_offset[0] + (i[1][1][0] + 1 - min_x) * scale, m_offset[1] + (i[1][1][1] + 1 - min_y) * scale), outline=(255,0,0))
				#print(i)
						
			for i in gEngine.player:
				if (i['human'] == False):
					#print(i)
					if ("route" in i):
						if (isinstance(i['route'], list) and len(i['route']) > 0):
							end = i['route'][-1]
							#print(i['route'], i['route'][1:])
							drw.line((m_offset[0] + (i['position']['x'] - min_x + 0.5) * scale, m_offset[1] + (i['position']['y'] - min_y+0.5) * scale, m_offset[0] + (i['route'][0][0] - min_x+0.5) * scale, m_offset[1] + (i['route'][0][1] - min_y+0.5) * scale), fill=(0,0,255), width=3)
							
							for j in range(1,len(i['route'])):
								drw.line((m_offset[0] + (i['route'][j-1][0] - min_x + 0.5) * scale, m_offset[1] + (i['route'][j-1][1] - min_y+0.5) * scale, m_offset[0] + (i['route'][j][0] - min_x+0.5) * scale, m_offset[1] + (i['route'][j][1] - min_y+0.5) * scale), fill=(0,0,255), width=3)
#							drw.line(((i['position']['x'] - min_x + 0.5) * scale, (i['position']['y'] - min_y+0.5) * scale, (end[0] - min_x+0.5) * scale, (end[1] - min_y+0.5) * scale), fill=(0,0,255), width=5)
					co = (0,0,255)
				else:
					co = (255,0,0)
					
				drw.ellipse((m_offset[0] + (i['position']['x'] - min_x + 0.3) * scale, m_offset[1] + (i['position']['y'] - min_y + 0.3) * scale, m_offset[0] + (i['position']['x'] - min_x + 0.7) * scale, m_offset[1] + (i['position']['y'] - min_y + 0.7) * scale), fill=co) 

			self.out += "Map saved at map.png. "

			if (fog):
				img.paste(fog_img.convert("L"), (0,0), fow)

			if ("players" in  gEngine.map_data and gEngine.data['piq'] in gEngine.map_data["players"]):
				if ("map_points" in gEngine.map_data["players"][gEngine.data['piq']]):
					for j in gEngine.map_data["players"][gEngine.data['piq']]['map_points']:
						#print(j)
						
						drw.text((m_offset[0] + (j['location'][0] - min_x + 0.8) * scale, m_offset[1] + ((j['location'][1] - min_y + 0.5) * scale) -7), j['label'],(255,255,255),font=ft)
						drw.ellipse((m_offset[0] + (j['location'][0] - min_x + 0.3) * scale, m_offset[1] + (j['location'][1] - min_y + 0.3) * scale, m_offset[0] + (j['location'][0] - min_x + 0.7) * scale, m_offset[1] + (j['location'][1] - min_y + 0.7) * scale), fill=(255,0,255))

			img.save("map.png")
			pass
			# Xs with no brackets to here
			# Ys with no brackets to here
			
		else:
			print(opts)
	
	def pushTime(self):
		return 0
	
	def describe(self):
		return self.out
		
muds = {
	"START" : [ "MAKE [MAKE_OPTIONS]" ],
	"MAKE_OPTIONS" : [ "MAP", "MAP WITH [MAP_WITH_OPTIONS]" ],
	"MAP_WITH_OPTIONS" : [ "[MAP_OPT]", "[MAP_OPT] AND [MAP_OPT]", "[MAP_OPT], [MAP_WITH_OPTIONS]" ],
	"MAP_OPT" : ["HEAT ZONES", "NO HOUSES", "NO FOG OF WAR", "ALL [NAMES_FOR_TILES] VISIBLE", "[UPPY_DOWNY] [SPAC] [%NUMBER%]"],
	"NAMES_FOR_TILES" : [ "SQUARES", "TILES" ],
	"SPAC" : ["X", "Y"],
	"UPPY_DOWNY" : ["UPPER", "LOWER"]
}

cmds = {
	"MAKE" : [ "cmds.make", "make" ],
}
