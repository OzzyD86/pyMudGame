class tickableObject(): 
	def __init__(self, gEngine): 
		self.gEngine = gEngine
		self.out = ""
		
	def runTick(self): pass

	def describe(self): 
		return self.out
