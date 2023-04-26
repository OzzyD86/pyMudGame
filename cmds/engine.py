import random, sys

class engine():
	def __init__(self, gEngine, opts):
		self.out = ""
		p = opts#.split(" ")
		if (p[1] == "EXIT"):
			import sys
			gEngine.save("test.json")
			print(gEngine.transcript)
			ff = open("transcript.txt", "w")
			ff.write(gEngine.transcript)
			ff.close()

			sys.exit(1)
		elif (p[1] == "GAME"):
			if (p[2] == "SAVE"):
				self.out += "You save the game"
				
				
				if (len(p) > 3 and p[3] == "AS"):
					sav = p[4].strip("\"")
				else:
					sav = gEngine.config['save_name']
				self.out += " as " + sav + "."
				gEngine.save(sav)
			elif (p[2] in [ "LOAD","OPEN" ]):
#				try:
					gEngine.load(p[3])
#				except:
#					print("No. That didn't work")
#					self.out = ""
			elif (p[2] == "NEW"):
				import sys
				seed = random.randrange(sys.maxsize)
#				print(len(p))
				if (len(p) > 3):
					print(p[3], p[4])
					if (p[3] == "WITH" and p[4] == "SEED"):
						seed = int(p[5])
				#print(seed)
				gEngine.new(seed)
		#elif (p[1] == "TRANSCRIPT"):
		#	if (p[2] == "SAVE"):
		#		pass
		#	elif (p[2] == "SHOW"):
		#		print(
		pass
		
	def pushTime(self):
		return 0.001
		
	def describe(self):
		return self.out
		
muds = {
	"START" : [ "ENGINE [ENGINE_ACTION]" ],
	"ENGINE_ACTION" : [ "EXIT", "GAME SAVE", "GAME SAVE AS [%STRING%]", "GAME LOAD [%STRING%]", "GAME NEW", "GAME NEW WITH SEED [%NUMBER%]" ],
}

cmds = {
	"ENGINE" : [ "cmds.engine", "engine" ],
}
