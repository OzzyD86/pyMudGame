class head():
	def __init__(self, gEngine, opts):
		self.out = ""
		self.tm = 1
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

		q = gEngine.mapp.get_tile(pl['position']['x'], pl['position']['y'])
		if (q['type'] not in gEngine.mapp.forbid_move):
			self.out += "You head " + p[1].lower() + "."
			if (q['visible'] == False):
				q['visible'] = True
			self.out += " You are in square " + str(pl['position']) + ". This square is of type " + str(q['type']) + "."
			if (q['storage']):
				self.out += " There is storage on this tile."

			for j, i in {"east" : (1,0), "south" : (0,1), "north" : (0, -1), "west" : (-1, 0)}.items():
				#print(i, j)
				x = gEngine.mapp.get_tile(pl['position']['x']+i[0], pl['position']['y']+i[1])
				x['visible'] = True
				
			tt = gEngine.cueEvts("onMove")
			self.out += tt['transcript']
			#if ("onMove" in gEngine.events):
			#	for i in gEngine.events['onMove']:
			#		self.out += i(gEngine)
		else:
			self.out += "You cannot head " + p[1].lower() + "."
			if (p[1] in ["NORTH", "UP"]):	# Is there a better way than doing this?
				pl['position']['y'] += 1
			elif(p[1] in ["SOUTH", "DOWN"]):
				pl['position']['y'] -= 1
			elif (p[1] in ["EAST", "RIGHT"]):
				pl['position']['x'] -= 1
			elif(p[1] in ["WEST", "LEFT"]):
				pl['position']['x'] += 1	
			self.tm = 0

		#print(gEngine.mapp.get_tile(gEngine.position['x'], gEngine.position['y']))
		#print(p[1])
		#print("Your current position is ", gEngine.position)
		#print("Hello!")
		#self.gEngine = gEngine
		pass
		
	def pushTime(self):
		return self.tm
		
	def describe(self):
		#out = ""
		return self.out

#def evtMove(gEngine):
#	return ""
	
muds = {
	"WAYS_I_SPELL_HEAD" : [ "HEAD", "HAED", "EHAD" ],
	"START" : [ "[WAYS_I_SPELL_HEAD] [DIRECTION_CLASSIC]"]
}

cmds = {
	"HEAD" :  head,
	"EHAD" :  head,
	"HAED" :  head, # For those like me who  type too fast and get annoyed by it!
}

def tick(gEngine, **kwargs):
	print (gEngine.time % 1440)
	if ((gEngine.time % 1440) == 0):
		print("DO SOME CLEANUP")
		for i in gEngine.player:
			if ("quest" in i and i["quest"] is not None):
				print(i["quest"].internal_state)
				if (i['quest'].internal_state in ["COMPLETED", "DECLINED", "FAILED"]):
					print("None quest")
					i["quest"] = None
				
	return "I have ticked. "

events = {
	"onTick": [ tick ]
}
