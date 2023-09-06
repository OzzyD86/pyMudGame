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
				print(p[3:])
				p = p[3:]
				while (len(p) > 0):
					print(p)
					if (p[0] == "WITH" and p[1] == "SEED"):
						seed = int(p[2])
						p = p[3:]
					elif (p[0] == "AS"):
						nm = str(p[1])
						gEngine.config['save_name'] = nm
						p = p[2:]
					else:
						p = p[1:]
				#print(seed)
				
				gEngine.new(seed)
				gEngine.save(nm)
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
	"ENGINE_ACTION" : [ "EXIT", "GAME SAVE", "GAME SAVE AS [%STRING%]", "GAME LOAD [%STRING%]", "GAME NEW AS [%STRING%]", "GAME NEW [GLIST]" ],
	"GLIST" : [ "[NEW_GAME_OPTS]", "[NEW_GAME_OPTS] AND [NEW_GAME_OPTS]", "[NEW_GAME_OPTS], [GLIST]" ],
	"NEW_GAME_OPTS": [ "WITH SEED [%NUMBER%]", "AS [%STRING%]"], 
}

cmds = {
	"ENGINE" : [ "cmds.engine", "engine" ],
}
