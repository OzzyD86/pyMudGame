class head():
	def __init__(self, gEngine, opts):
		self.out = ""
		self.ge = gEngine
		p = opts#.split(" ")
		pl = gEngine.player[gEngine.data['piq']]

		if (p[1] in ["NORTH", "UP"]):
			pl['position']['y'] -= 1
		elif(p[1] in ["SOUTH", "DOWN"]):
			pl['position']['y'] += 1
		elif (p[1] in ["EAST", "RIGHT"]):
			pl['position']['x'] += 1
		elif(p[1] in ["WEST", "LEFT"]):
			pl['position']['x'] -= 1
		
		self.out += "You head " + p[1].lower() + "."

		q = gEngine.mapp.get_tile(pl['position']['x'], pl['position']['y'])
		self.out += " You are in square " + str(pl['position']) + ". This square is of type " + str(q['type']) + "."
		if (q['storage']):
			self.out += " There is storage on this tile."

		for j, i in {"east" : (1,0), "south" : (0,1), "north" : (0, -1), "west" : (-1, 0)}.items():
			#print(i, j)
			x = gEngine.mapp.get_tile(pl['position']['x']+i[0], pl['position']['y']+i[1])
			
		if ("onMove" in gEngine.events):
			for i in gEngine.events['onMove']:
				self.out += i(gEngine)

		#print(gEngine.mapp.get_tile(gEngine.position['x'], gEngine.position['y']))
		#print(p[1])
		#print("Your current position is ", gEngine.position)
		#print("Hello!")
		#self.gEngine = gEngine
		pass
		
	def pushTime(self):
		return 1
		
	def describe(self):
		#out = ""
		return self.out

def evtMove(gEngine):
	return ""
	
muds = {
	"START" : [ "HEAD [DIRECTION]" ]
}

cmds = {
	"HEAD" : [ "cmds.opts", "head" ],
}

events = {
	"onMove" : [ evtMove ]
}
