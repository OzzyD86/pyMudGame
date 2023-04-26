ORTHS = [(0,1), (1,0), (0,-1), (-1, 0)]

import core.phraseReplace

prd = {
	"start" : [
		"<%town.pre%><%town.core%><%town.post%><%posts%>",
		"<%town2.exec%>",
	],
	"space": [ "", "-", " " ],
	"town2" : {
		"begin" : [ "", "Upper ", "Lower ", "Inner ", "Outer " ],
		"core1" : [ "Ren", "Ten", "Twin", "Twig", "Hex", "Fox", "Pas"],
		"core2" : [ "fell", "all", "gle", "gen", "gon", "fall", "nell", "nal", "try"],
		"exec": [ "<%town2.begin%><%town2.core1%><%town2.core2%>" ]
	},
	"town" : {
		"pre": [
			"High ", "Low ", "<%positionals%>", ""
		],
		"core" : [
			"fart", "wang", "Slon", "Covid", "Butt", "dive", "fenn", "mole", "fingley", "Ten", "Net", "Fet"
		],
		"posts": [
			"<%town.post%><%posts%>", "<%town.post%>",
			
		],
		"post" : [
			"ville", "ton", "hole", "wood", "borough"
		]
	},
	"posts" : [
		"-on-sea", " by <%town2.exec%>", " <%more_positionals.based%> <%town2.exec%>"
	],
	"more_positionals" : {
		"based" : [
			"over", "under", "juxta", "tween"
		]
	},
	"positionals" : [
		"Upper", "Lower"
	]
}

import random, json, math as maths
import noise2
#import noise

#random.seed(1) # We won't need this in the future!

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
	forbid_move = [6]
	
	def setNoise(self, seed = 1024):
		random.seed(seed)
		self.nm = noise2.noiseMachine()
		self.nm.buildNoiseBase(128)
		self.nm.buildNoiseBase(64)
		self.nm.addScope([0, 3, 1]).addScope([0, 5, 0]).addScope([1, 19, 2]).addScope([1, 29, 0])
		self.houses = noise2.noiseMachine()
		self.houses.buildNoiseBase(16)
		self.houses.addScope([0, 4, 1])
		self.sea = noise2.noiseMachine()
		self.sea.buildNoiseBase(32)
		self.sea.addScope([0, 17, 0])
	
	def __init__(self, seed = 1024):
		self.seed = seed
		print("Set seed " + str(seed))
		self.tiles = {}
		self.edge_tiles = [(0,0)]
		self.towns = []
		self.setNoise(seed)
		#print(self.houses.noise)
		# Sorted?
		pass
	
	def reset(self, seed = None):
		self.tiles = {}
		self.edge_tiles = [(0,0)]
		self.towns = []
		del self.nm
		del self.houses
		print("Reset seed " + str(seed))
		self.setNoise(seed)
	
	def get_tile(self, x = 0, y = 0, in_town_mode = False):
		if ((x,y) in self.tiles):
			return self.tiles[x,y]
		else:
			self.set_tile(x, y, in_town_mode = in_town_mode)
			return self.tiles[x,y]
			
#			return False
			
	def set_tile(self, x = 0, y = 0, force_edging = True, in_town_mode = False):
		z = False
		if (not (x,y) in self.tiles):
			np = self.nm.locBuild((x, y))[0,0]
			sea = self.sea.locBuild((x, y))[0,0]
			#print(np)
			mappo = maths.floor(np / 255 * 5)
			#mappo = 
			#print(mappo)
			self.tiles[x,y] = {"type" : int(mappo), "storage" : random.choice([True, False, False]), "visible" : False }
			this_tile = self.tiles[x,y]
			print(sea)
			if (sea < 64):
				self.tiles[x,y]['storage'] = False
				self.tiles[x,y]['type'] = 6
				print("Make sea tile")
				if (int(mappo) in [0, 1]):
					self.tiles[x,y]['type'] = 7
			
			if (self.tiles[x,y]['type'] in self.town_tiles): # I DO NOT want this code to run ... yet!
				if (not "processed" in this_tile and in_town_mode != True):
					ttypes = {}
					gen_houses = 0
					print("Look for a town!")
					# Set up for town search
					bounds = [[x, y], [x, y]]
					searched = [(x,y)]
					to_search = []
					for w in ORTHS:
						v = self.get_tile(x+w[0], y+w[1], in_town_mode = True)
						print(v)
						if (v['type'] in self.town_tiles and ("processed" not in v or v['processed'] != True)):
							to_search.append((x+w[0], y+w[1]))
					self.tiles[x,y]["processed"] = True
					if ("house" in this_tile and this_tile['house']):
						gen_houses += 1
					
					#print("TOWN:", to_search)
					if (True):
					#try:
						while (len(to_search) > 0):
							#print(len(to_search))
							v = to_search.pop(0)
							t = self.get_tile(v[0], v[1], in_town_mode = True)
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
									u = self.get_tile(v[0]+w[0], v[1]+w[1], in_town_mode = True)
									#print(u)
									if ((v[0]+w[0], v[1]+w[1]) not in searched):
										if not u['type'] in ttypes:
											ttypes[u['type']] = 1
										else:
											ttypes[u['type']] += 1
										#print(ttypes)

										if (u['type'] in self.town_tiles and ("processed" not in u or u['processed'] != True)):
											if (u['type'] != t['type'] or True):
											#print("Add", (v[0]+w[0], v[1]+w[1]))
												to_search.append((v[0]+w[0], v[1]+w[1]))
					#except:
					#	print("Whoops")
					ran = random.getstate()
					print(bounds)
					if (gen_houses > 0):
						p = ((gen_houses * (bounds[0][0] * bounds[0][1])) + (bounds[1][0] * bounds[1][1])) * len(searched)
						print(p)
						random.seed(p)
						global prd
						town_name, prd = core.phraseReplace.phraseReplace_v2("<%start%>", prd)
						print(town_name, "with", gen_houses, "house(s)")
						self.towns.append([town_name, bounds, p])
						print("===")
						print(ttypes)
						random.setstate(ran)
					else:
						print("Sorry. Number of houses not met for city creation :(")
					#print(bounds)
					
				house = self.houses.locBuild((x, y))[0,0]
				q = maths.floor(house / 255 * (10)) # not 12 at the moment
				an = self.tiles[x,y]['type'] 
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
					self.tiles[x,y]['house'] = True
					self.tiles[x,y]['storage'] = True
					print("Spawned a house!")
				elif (q == 3 and an == 0):
					self.tiles[x,y]['shop'] = True
					print("Spawned a shop!")
				elif (q == 8 and an == 0):
					self.tiles[x,y]['station'] = True
					print("Spawned a station!")
				else:
					self.tiles[x,y]['house'] = False
					
			if (self.tiles[x,y]['storage'] == True):
				self.tiles[x,y]['contents'] = []
				
			if ((x,y) in self.edge_tiles):
				self.edge_tiles.remove((x,y))
				z = True

			if (z or force_edging):			
				for i in ORTHS:
					#print(i)
					if (not (x+i[0], y+i[1]) in self.tiles):
						if (not (x+i[0], y+i[1]) in self.edge_tiles):
							self.edge_tiles.append((x+i[0], y+i[1]))
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
		print("NOT SUPPORTED")
		return "NOT SUPPORTED";

	def raw_save(self):
		#with open("file", "w") as f:
		k = self.tiles.keys() 
		v = self.tiles.values() 
		k1 = [str(i) for i in k]
		x = json.dumps(dict(zip(*[k1,v]))) 
		
		return json.dumps({ "tiles" : x, "edges" : self.edge_tiles, "towns" : self.towns })
	
	def raw_load(self, data):
		#print(data)
		
		#data = json.load(f)
		dic = json.loads(data)
		self.edge_tiles = dic['edges']
		if ("towns" in dic):
			self.towns = dic['towns']
		
		dic = json.loads(dic['tiles'])

#		print(dic)
		
		k = dic.keys() 
		v = dic.values() 
#		print(k)
		k1 = [eval(i) for i in k]
		o = dict(zip(*[k1,v])) 
#		print(o)
		self.tiles = o
#		sys.exit(1)
		
	def save(self, file):	# Not supported yet
		print("NOT SUPPORTED")
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
			search = { abs(start[0] - finish[0]) + abs(start[1] - finish[1]) : [{ "current" : start, "history" : [] }] }
			
		while (True):
			p = list(search.keys())
			p.sort()
			if (len(search) < 1):
				return False
				
			t = search[p[0]]
			del search[p[0]]
			
			for i in t:
				for j in ORTHS:
					tr = (i['current'][0] + j[0], i['current'][1] + j[1])
					if not (tr in tried_squares):
						if (tr in self.tiles and self.tiles[tr]['type'] not in self.forbid_move):
							rtdt = abs(tr[0] - finish[0]) + abs(tr[1] - finish[1])
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
