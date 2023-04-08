class head():
	def __init__(self, gEngine, opts):
		self.out = ""
		self.ge = gEngine
		p = opts.split(" ")
		pl = gEngine.player[gEngine.data['piq']]

		if (p[1] == "NORTH"):
			pl['position']['y'] -= 1
		elif(p[1] == "SOUTH"):
			pl['position']['y'] += 1
		elif (p[1] == "EAST"):
			pl['position']['x'] += 1
		elif(p[1] == "WEST"):
			pl['position']['x'] -= 1
		
		self.out += "You head " + p[1].lower() + "."

		q = gEngine.mapp.get_tile(pl['position']['x'], pl['position']['y'])
		self.out += " You are in square " + str(pl['position']) + ". This square is of type " + str(q['type']) + "."
		if (q['storage']):
			self.out += " There is storage on this tile."

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
				
muds = {
	"START" : [ "HEAD [DIRECTION]" ]
}

cmds = {
	"HEAD" : [ "cmds.opts", "head" ],
}
