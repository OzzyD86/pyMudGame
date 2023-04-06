import json
import sys
sys.path.append("../")
import mapper

class gEngine():
	def __init__(self):
		self.out = ""
		self.tickOps = []
		self.time = 0
		self.position = {"x" : 0,"y" : 0 }
		self.mapp = mapper.mapper()

	def load(self, name):
		d = open(name, "r")
		op = json.loads(d.read())
		d.close()
		self.time = op['time']
		self.position = op['self']
		self.mapp.raw_load(op['map'])
		
	def tick(self, quantity = 1):
		for i in range(quantity):
			self.time += 1
			#self.out = " Time is pushed on by 1. (" + doTime(self.time) + ")\n" # doTime is still in main.py - needs moving to work
			for j in self.tickOps:
				#print(j, type(j), str(type(j)))
				if (str(type(j)).find("function") > 0):	# Ooh this looks messy!
					#print("Function!")
					d = j(self)
					self.out += d
				elif (str(type(j)).find("type") > 0):	# Ooh this looks messy!
					 d = j(self)
					 d.runTick()
					 self.out += d.describe()
				else:
					print(j, type(j), str(type(j)))
				
				# Loop through all the tick operations
				#p = j()
				#p.runTick(self)
				pass
	
	def passiveTranscript(self):
		x = self.out
		self.out = ""
		return x
		
	def save(self, name):
		d = open(name, "w")
		op = json.dumps({ "self" : self.position, "map" : self.mapp.raw_save(), "time" : self.time })
		d.write(op)
		d.close()
