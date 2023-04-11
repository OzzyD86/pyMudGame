ORTHS = [(0,1), (1,0), (0,-1), (-1, 0)]

import random, json, math as maths
import noise2
#import noise

#random.seed(1) # We won't need this in the future!

class mapper():
	def __init__(self):
		self.tiles = {}
		self.edge_tiles = [(0,0)]
		self.nm = noise2.noiseMachine()
		self.nm.buildNoiseBase(128)
		self.nm.buildNoiseBase(64)
		# Sorted?
		pass
	
	def reset(self):
		self.tiles = {}
		self.edge_tiles = [(0,0)]
	
	def get_tile(self, x = 0, y = 0):
		if ((x,y) in self.tiles):
			return self.tiles[x,y]
		else:
			self.set_tile(x, y)
			return self.tiles[x,y]
			
#			return False
			
	def set_tile(self, x = 0, y = 0, force_edging = True):
		z = False
		if (not (x,y) in self.tiles):
			np = self.nm.locBuild((x, y))[0,0]
			print(np)
			mappo = maths.floor(np / 255 * 4)
			#mappo = 
			print(mappo)
			self.tiles[x,y] = {"type" : int(mappo), "storage" : random.choice([True, False])}
			if (self.tiles[x,y]['type'] == 0):
				q = random.randrange(0, 3)
				print(q)
				if (q == 2):
					self.tiles[x,y]['house'] = True
					print("Spawned a house!")
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
		
		return json.dumps({ "tiles" : x, "edges" : self.edge_tiles })
	
	def raw_load(self, data):
		#print(data)
		
		#data = json.load(f)
		dic = json.loads(data)
		self.edge_tiles = dic['edges']
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

	def aStarSearch(self, start, finish, iterations = 100, partial_object = []):
		tried_squares = []
		its = 0
		if not (partial_object == []):
			pass
		else:
			search = { abs(start[0] - finish[0]) + abs(start[1] - finish[1]) : [{ "current" : start, "history" : [] }] }
			
		
		while (True):
			p = list(search.keys())
			p.sort()
			
			t = search[p[0]]
			del search[p[0]]
			
			for i in t:
				for j in ORTHS:
					tr = (i['current'][0] + j[0], i['current'][1] + j[1])
					if not (tr in tried_squares):
						if (tr in self.tiles):
							rtdt = abs(tr[0] - finish[0]) + abs(tr[1] - finish[1])
							if (rtdt == 0):
								#print(start)
								print({ "current" : tr, "history" : i['history'] + [i['current'], finish] })
								print("Found it")
								return { "current" : tr, "history" : i['history'] + [i['current'], finish] }
								#sys.exit(1)
							if (not rtdt in search):
								search[rtdt] = [{ "current" : tr, "history" : i['history'] + [i['current']] }]
							else:
								search[rtdt].append({ "current" : tr, "history" : i['history'] + [i['current']] })
						tried_squares.append(tr)
				its += 1
			
			
			if (its > iterations):
				print("Iterations exceeded")
				return search
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
