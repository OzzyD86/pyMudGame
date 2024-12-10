ORTHS = [(0,1,0), (1,0,0), (0,-1,0), (-1, 0,0)]

import core.phraseReplace

#import plugins.common.narration.test as t

#prd = t.MANIFEST

from random import Random
import json, math as maths
import noise2
import pathlib, os
#import noise

#random.seed(1) # We won't need this in the future!

def find_loc(x, y):
	return (x // 100, y // 100, x % 100, y % 100)
	
def unfind_loc(x1, y1, x2, y2):
	return ((x1 * 100) + x2, (y1 * 100) + y2) 
	
class aStarComplete():
	def __init__(self, current, history):
		self.current = current
		self.history = history
		#self.finish = finish
	
	def getHistory(self):
		pass

class aStarPartial():
	def __init__(self, search, finish, ts = []):
		self.tried_squares = ts
		self.search = search
		self.finish = finish
		
	def getContents(self):
		return self.search

class mapper():
	town_tiles = [0, 1, 7]
	forbid_move = [6, 8]
	tile_types = {
		"land" : [0, 1, 2, 3],
		"ocean" : [6, 7],
		"underground": [8, 9],
	}
	
	def passTownNames(self, townNames):
		self.town_names = townNames
		
	def setNoise(self, seed = 1024, version = 3):
		self.random.seed(seed)
		print("Noise is " + str(seed))
		self.nm = noise2.noiseMachine()
		self.nm.passRandomObj(self.random)
		self.nm.buildNoiseBase(128)
		self.nm.buildNoiseBase(64)

		self.houses = noise2.noiseMachine()
		self.houses.passRandomObj(self.random)
		self.houses.buildNoiseBase(16)

		self.sea = noise2.noiseMachine()
		self.sea.passRandomObj(self.random)
		self.sea.buildNoiseBase(32)

		if (True):
			self.sea.buildNoiseBase(64)
			self.sea.buildNoiseBase(92)
			self.sea.addScope([2, 119, 2]).addScope([1, 11, 2]).addScope([0, 19, 1])

		if (version == 0):	# Original
			self.nm.addScope([0, 3, 1]).addScope([0, 5, 0]).addScope([1, 19, 2]).addScope([1, 29, 0])
			self.nm.addScope([0, 61, 2])
		elif (version == 1):
			self.nm.addScope([0, 47, 1]).addScope([0, 11, 0]).addScope([1, 23, 2]).addScope([1, 5, 0])
		elif (version == 2):
			self.nm.addScope([0, 19, 1]).addScope([0, 11, 0]).addScope([1, 23, 2]).addScope([1, 5, 0])
		elif (version == 3):
			self.nm.addScope([0, 17, 1]).addScope([0, 11, 0]).addScope([1, 5, 2]).addScope([1, 2, 0])
			
		else:
		
			raise Exception("Version not known")
			
		self.houses.addScope([0, 4, 1])

		self.sea.addScope([0, 17, 0])
	
	def __init__(self, seed = 1024):
		self.seed = seed
		self.random = Random(seed)
		print("Set seed " + str(seed))
		self.tiles = {}
		self.edge_tiles = [(0,0,0)]
		self.towns = []
		self.setNoise(seed)
		#print(self.houses.noise)
		# Sorted?
		pass
	
	def reset(self, seed = None):
		self.tiles = {}
		self.edge_tiles = [(0,0,0)]
		self.towns = []
		del self.nm
		del self.houses
		print("Reset seed " + str(seed))
		self.setNoise(seed)
	
	def get_tile(self, x = 0, y = 0, z = 0, in_town_mode = False, force_make = True):
		if ((x,y,z) in self.tiles):
			return self.tiles[x,y,z]
		else:
			if (force_make):
				self.set_tile(x, y, z, in_town_mode = in_town_mode)
				return self.tiles[x,y,0]
			else:
				return None
			
#			return False
			
	def set_tile(self, x = 0, y = 0, z = 0, force_edging = True, in_town_mode = False):
		zx = False
		if (not (x,y,z) in self.tiles):
		
			if (z > 0):
				self.tiles[x,y,z] = {"type" : 8, "storage" : self.random.choice([True, False, False]), "visible" : False }
				return 
				
			np = self.nm.locBuild((x, y))[0,0]
			sea = self.sea.locBuild((x, y))[0,0]
			#print(np)
			# This will make towns smaller with bigger city areas...
			if (np < 35): # 51?
				mappo = 0
			elif (np < 60): # 102?
				mappo = 1
			else:
				mappo = maths.floor(np / 255 * 5)
			#mappo = 
			#print(mappo)
			self.tiles[x,y,z] = {"type" : int(mappo), "storage" : self.random.choice([True, False, False]), "visible" : False }
			this_tile = self.tiles[x,y,z]
			#print(sea)
			if (sea < 64 + 24 - (np / 255 * 16)):
				self.tiles[x,y,z]['storage'] = False
				self.tiles[x,y,z]['type'] = 6
				print("Make sea tile")
				if (int(mappo) in [0, 1]):
					self.tiles[x,y,z]['type'] = 7
			
			if (self.tiles[x,y,z]['type'] in self.town_tiles): # I DO NOT want this code to run ... yet!
				if (not "processed" in this_tile and in_town_mode != True):
					ttypes = {}
					gen_houses = 0
					print("Look for a town!")
					# Set up for town search
					bounds = [[x, y,0], [x, y,0]]
					searched = [(x,y,0)]
					to_search = []
					for w in ORTHS:
						v = self.get_tile(x+w[0], y+w[1], z, in_town_mode = True)
						print(v)
						if (v['type'] in self.town_tiles and ("processed" not in v or v['processed'] != True)):
							to_search.append((x+w[0], y+w[1], 0))
					self.tiles[x,y,z]["processed"] = True
					if ("house" in this_tile and this_tile['house']):
						gen_houses += 1
					
					#print("TOWN:", to_search)
					if (True):
					#try:
						while (len(to_search) > 0):
							#print(len(to_search))
							v = to_search.pop(0)
							t = self.get_tile(v[0], v[1], v[2], in_town_mode = True)
							if (v not in searched):
								if (v[0] < bounds[0][0]):
									bounds[0][0] = v[0]
								elif (v[0] > bounds[1][0]):
									bounds[1][0] = v[0]

								if (v[1] < bounds[0][1]):
									bounds[0][1] = v[1]
								elif (v[1] > bounds[1][1]):
									bounds[1][1] = v[1]

								self.tiles[v]['processed'] = True
									

								if ("house" in self.tiles[v] and self.tiles[v]['house']):
									gen_houses += 1
								searched.append(v)
								for w in ORTHS:
									u = self.get_tile(v[0]+w[0], v[1]+w[1], z, in_town_mode = True)
									#print(u)
									if ((v[0]+w[0], v[1]+w[1], z) not in searched):
										if not u['type'] in ttypes:
											ttypes[u['type']] = 1
										else:
											ttypes[u['type']] += 1
										#print(ttypes)

										if (u['type'] in self.town_tiles and ("processed" not in u or u['processed'] != True)):
											if (u['type'] != t['type'] or True):
											#print("Add", (v[0]+w[0], v[1]+w[1]))
												to_search.append((v[0]+w[0], v[1]+w[1], z))
					#except:
					#	print("Whoops")
					ran = self.random.getstate()
					print(bounds)
					if (gen_houses > 0):
						p = ((gen_houses * (bounds[0][0] * bounds[0][1])) + (bounds[1][0] * bounds[1][1])) * len(searched)
						print(p)
						op = { "town" : { "ocean": 0, "land" : 0 }, "surround" : { "ocean" : 0, "land" : 0 }}
						for ab, bc in ttypes.items():
							if (ab in self.town_tiles):
								if (ab in self.tile_types['land']):
									op['town']['land'] += bc
								else:
									op['town']['ocean'] += bc
							else:
								if (ab in self.tile_types['land']):
									op['surround']['land'] += bc
								else:
									op['surround']['ocean'] += bc
								
							#print(ab, bc)
						print(op)
						water = op['town']['ocean'] + op['surround']['ocean']
						land = op['town']['land'] + op['surround']['land']
						wateriness = water / (land + water)
						print("WATERINESS:", wateriness)
						
						if (wateriness > 0.5):
							tp = "oceanic"
						elif (wateriness > 0.2):
							tp = "seaside"
						else:
							tp = "landlocked"
						self.random.seed(p)
						#global prd
						town_name, self.town_names = core.phraseReplace.phraseReplace_v2("<%olds.towns." + tp + "%>", self.town_names)
						print(town_name, "with", gen_houses, "house(s)")
						self.towns.append([town_name, bounds, p])
						print("===")
						print(ttypes)
						self.random.setstate(ran)
					else:
						print("Sorry. Number of houses not met for city creation :(")
					#print(bounds)
					
				house = self.houses.locBuild((x, y))[0,0]
				q = maths.floor(house / 255 * (10)) # not 12 at the moment
				an = self.tiles[x,y,z]['type'] 
				#q = random.randrange(0, 3)
				print(q)
#				if (q in [9, 10, 11]):
#					if (q in [10, 11]):
#						self.tiles[x,y]['type']  = 2
#					elif (q == 9):
#						if (an == 0):
#							self.tiles[x,y]['type']  = 1
#						else:
#							self.tiles[x,y]['type']  = 2
							
				if ((an == 0 and q in [2, 7]) or (an in [1, 7] and q in [2])):
					self.tiles[x,y,z]['house'] = True
					self.tiles[x,y,z]['storage'] = True
					print("Spawned a house!")
				elif (q == 3 and an == 0):
					self.tiles[x,y,z]['shop'] = True
					print("Spawned a shop!")
				elif (q == 8 and an == 0):
					self.tiles[x,y,z]['station'] = True
					print("Spawned a station!")
				else:
					self.tiles[x,y,z]['house'] = False
					
			if (self.tiles[x,y,z]['storage'] == True):
				self.tiles[x,y,z]['contents'] = []
				
			if ((x,y,z) in self.edge_tiles):
				self.edge_tiles.remove((x,y,z))
				zx = True

			if (zx or force_edging):			
				for i in ORTHS:
					#print(i)
					if (not (x+i[0], y+i[1], z) in self.tiles):
						if (not (x+i[0], y+i[1], z) in self.edge_tiles):
							self.edge_tiles.append((x+i[0], y+i[1], z))
			#print(self.edge_tiles)
		else:
			return False
	
	def list_tiles(self):
		out = []
		for i,j in self.tiles.items():
			#print(i,j)
			out.append({"pos" : i, "data" : j})
		return out
	
	def load(self, file):	# Not supported yet
		try:
			y = os.scandir("saves/" + file + "/maps/0")
			for i in y:
				if (".map" in str(i.name)):
					x = open("saves/" + file + "/maps/0/" + str(i.name))
					z = json.loads(x.read())
					x.close()
					p = str(i.name).split(".")
					x1 = int(p[0])
					y1 = int(p[1])
					for x2, j in z.items():
						for y2, k in j.items():
							#print(unfind_loc(x1, y1, int(x2), int(y2)), k)
							self.tiles[tuple([*unfind_loc(x1, y1, int(x2), int(y2)), 0])] = k
					#print(x1, y1)
					#print(i)
		except Exception as e:
			print(e)
		#finally:
			pass
		#print("NOT SUPPORTED")
		return "NOT SUPPORTED";

	def raw_save(self):
		
		#k = self.tiles.keys() 
		#v = self.tiles.values() 
		#k1 = [str(i) for i in k]
		#x = json.dumps(dict(zip(*[k1,v]))) 
		
		return json.dumps({ "edges" : self.edge_tiles, "towns" : self.towns })
	
	def raw_load(self, data):
		#print(data)
		
		#data = json.load(f)
		dic = json.loads(data)
		self.edge_tiles = dic['edges']
		if ("towns" in dic):
			self.towns = dic['towns']
		
		if ("tiles" in dic): 	# Which will become increasingly less likely!
			dic = json.loads(dic['tiles'])

			k = dic.keys() 
			v = dic.values() 
			k1 = [eval(i) for i in k]
			o = dict(zip(*[k1,v])) 
			self.tiles = o
		
	def save(self, locPass):	# Not supported yet
		diggle = {}
		
		pathlib.Path(locPass + "/maps/0/").mkdir(exist_ok=True, parents=True)
		for i, j in self.tiles.items():
			scope = i[2]
			
			if not (scope in diggle):
				diggle[scope] = {}
			nn = find_loc(i[0], i[1])
			if (not nn[0] in diggle[scope]):
				diggle[scope][nn[0]] = {}
				
			if (not nn[1] in diggle[scope][nn[0]]):
				diggle[scope][nn[0]][nn[1]] = {}
				
			if (not nn[2] in diggle[scope][nn[0]][nn[1]]):
				diggle[scope][nn[0]][nn[1]][nn[2]] = {}
				
			diggle[scope][nn[0]][nn[1]][nn[2]][nn[3]] = j

		for sc, i in diggle.items():
			for a, b in i.items():
				for c, d in b.items():
					g = open(locPass + "/maps/" + str(sc) + "/" + str(a) + "." + str(c) + ".map", "w")
					g.write(json.dumps(d))
					g.close()
		#print("NOT SUPPORTED")
		return "NOT SUPPORTED";

	def aStarSearch(self, start, finish, iterations = 500, partial_object = []):
		tried_squares = []
		its = 0

		#print(partial_object)
		
		if not (partial_object == []):
			# Start is not required ... I don't think
			if (isinstance(partial_object, aStarPartial)):
				if (hasattr(partial_object, "tried_squares")):
					tried_squares = partial_object.tried_squares
				
				search = partial_object.getContents()
				finish = partial_object.finish
			else:
				search = partial_object
		else:
			search = { abs(start[0] - finish[0]) + abs(start[1] - finish[1] + abs(start[2] - finish[2])) : [{ "current" : start, "history" : [] }] }
			
		while (True):
			p = list(search.keys())
			p.sort()
			if (len(search) < 1):
				return False
				
			t = search[p[0]]
			del search[p[0]]
			
			for i in t:
				for j in ORTHS:
					tr = (i['current'][0] + j[0], i['current'][1] + j[1], i['current'][2] + j[2])
					if not (tr in tried_squares):
						if (tr in self.tiles and self.tiles[tr]['type'] not in self.forbid_move):
							rtdt = abs(tr[0] - finish[0]) + abs(tr[1] - finish[1]) + abs(tr[2] - finish[2])
							if (rtdt == 0):
								#print(start)
								print({ "current" : tr, "history" : i['history'] + [i['current'], finish] })
								print("Found it")
								return aStarComplete(tr, i['history'] + [i['current'], finish])
								#return { "current" : tr, "history" : i['history'] + [i['current'], finish] }
								#sys.exit(1)
							if (not rtdt in search):
								search[rtdt] = [{ "current" : tr, "history" : i['history'] + [i['current']] }]
							else:
								search[rtdt].append({ "current" : tr, "history" : i['history'] + [i['current']] })
						tried_squares.append(tr)
				its += 1
			
			
			if (its > iterations):
				print("Iterations exceeded")
				return aStarPartial(search, finish, tried_squares)
		print (p)
		p.sort()
		x = p[0]
		print(x)
	
		

if (False):
	#y = 
	x = mapper()
	x.set_tile()
	p = x.get_tile()
	x.set_tile(0, 1)
	x.set_tile(1, 1)
	print(p)
	print(x.edge_tiles)
	for i in x.list_tiles():
		print(i)
