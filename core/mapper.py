ORTHS = [(0,1), (1,0), (0,-1), (-1, 0)]

import random, json
#import noise

#random.seed(1) # We won't need this in the future!

class mapper():
	def __init__(self):
		self.tiles = {}
		self.edge_tiles = [(0,0)]
		pass
	
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
			self.tiles[x,y] = {"type" : random.randrange(0,5), "storage" : random.choice([True, False])}
			
			if (self.tiles[x,y]['storage'] == True):
				self.tiles[x,y]['contents'] = []
				
			if ((x,y) in self.edge_tiles):
				self.edge_tiles.remove((x,y))
				z = True

			if (z or force_edging):			
				for i in ORTHS:
					print(i)
					if (not (x+i[0], y+i[1]) in self.tiles):
						if (not (x+i[0], y+i[1]) in self.edge_tiles):
							self.edge_tiles.append((x+i[0], y+i[1]))
			print(self.edge_tiles)
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