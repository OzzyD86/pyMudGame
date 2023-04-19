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
					sav = "test"
				gEngine.save(sav)
			elif (p[2] in [ "LOAD","OPEN" ]):
#				try:
					gEngine.load(p[3])
#				except:
#					print("No. That didn't work")
#					self.out = ""
			elif (p[2] == "NEW"):
				gEngine.new()
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
	"ENGINE_ACTION" : [ "EXIT", "GAME SAVE", "GAME SAVE AS [%STRING%]", "GAME LOAD [%STRING%]" ],
}

cmds = {
	"ENGINE" : [ "cmds.engine", "engine" ],
}
