def dist(p1, p2):
	return (abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]))
	
import random 

class npcHail():
	def __init__(self, gEngine, opts):
		self.out = ""
		self.timeshift = 0.05
		pl = gEngine.player[gEngine.data['piq']]
		if (opts[1] in ["HAIL"]):
			self.out = "You hail people around you. "
			print(pl)
			hails = 0
			
			for i in gEngine.player:
				if i == pl:
					print("i is player")
				else:
					#print("i is not player")
					d = dist((pl['position']['x'], pl['position']['y']), (i['position']['x'], i['position']['y']))
					if (d <= 15):
						hails += 1
						print("An NPC within hailing distance")
			if (hails == 0):
				self.out += "No-one hears you. "
			else:
				self.out += str(hails) + " people hear you. "
		elif (opts[1] in ["QUEST"]):
			npcs = []
			for i in gEngine.player:
					if i != pl:
						d = dist((pl['position']['x'], pl['position']['y']), (i['position']['x'], i['position']['y']))
						if (d <= 15):
							#print(d)
							npcs.append(i)
							
			print("QUEST!!")
			#print(opts, len(opts))
			add = 0
			opts = opts[2:]
			#print(opts)

			nx = 0
			#if (len(npcs) == 0):
			#	self.out += "There are no people in range:\n"
			#elif (len(npcs) == 1):
			#	self.out += str(i) + "\n"
			#else:
			response = "There are multiple people in range:\n"
			for i in npcs:
				nx += 1
				if not ("uid" in i):
					i['uid'] = gEngine.genUniqueNum()
				response += str(nx) + ": " + str(i) + "\n"
			select_npc = None
			sw = "default"
			while (len(opts) > 0):
				#print(opts)
				if (opts[0] in ['OPTION']):
					select_npc = int(opts[1].strip("\""))
					#if (select_npc > 0) and (select_npc <= len(npcs)):
						#self.out += str(select_npc) + ":" + str(npcs[select_npc - 1]) + "\n"
					#else:
					# Set up quest here for chosen NPC
					opts = opts[2:]
					pass
				
				elif (opts[0] in ['ACCEPT']):
					# Do accept
					sw = "accept"
					opts = opts[1:]
				elif (opts[0] in ['DECLINE']):
					# Do decline
					sw = "decline"
					opts = opts[1:]
				elif (opts[0] in ['COMPLETE']):
					# Do complete
					sw = "complete"
					opts = opts[1:]
				else:
					opts = opts[1:]
			
			if (select_npc is None and len(npcs) > 0):
				self.out += response
			elif (len(npcs) == 0):
				self.out += "There is no-one around\n"
			elif (select_npc is not None and ((select_npc < 0) or ((select_npc) > len(npcs)))):
				self.out += "There is no such option on this list\n"
			elif (select_npc is None):
				self.out= "Does this get run here? And why? What is the reason?"
			else:
				self.out += "Switch to " + sw + " for NPC " + str(select_npc) + ". Action!"
				## Okay. If we're here, things need to get done
#				self.out += "\n" + str(npcs[select_npc - 1]) + "\n" # I need not write this line any more. Keeping it for debug and completeness and what not
				pp = npcs[select_npc - 1]
				if (not "quest" in pp):
					pp['quest'] = None
					print("Adding quest to NPC. Let's see what happens")
				
				if pp['quest'] is None:
					#print(gEngine.quests)
					for i in [1,2,3,4,5]:
						p = random.choice(gEngine.quests)
						if (p(gEngine, [])._isAssignable()):
							break
							
					x = p(gEngine, ['', '', sw.upper()])
					pp['quest'] = x
					print("Give NPC a quest here!")
				else:
					print("This NPC has a quest!")
					x = pp['quest'].state(['', '', sw.upper()])	# Now then ... can I do this?
					
				if (sw.upper() in ['ACCEPT'] and x.last_state):
					gEngine.registerEvent(gEngine.data['piq'], pp['uid'], pp['quest'])
				elif (sw.upper() in ['DECLINE', 'COMPLETE'] and x.last_state):
					gEngine.deregisterEvent(gEngine.data['piq'], pp['uid'], pp['quest'])

				self.out += "\n" + x.describe()
				self.timeshift += x.pushTime()

	def pushTime(self):
		return self.timeshift
		
	def describe(self):
		return self.out
		
cmds = { "NPC": ["cmds.npcHail", "npcHail"] }

muds = {
	"START": ["NPC HAIL", "NPC QUEST", "NPC QUEST [CHOOSE_NPC]", "NPC QUEST [QUEST_OPTS]", "NPC QUEST [QUEST_OPTS] [CHOOSE_NPC]"],
	"CHOOSE_NPC" : [ "OPTION [%NUMBER%]" ],
	"QUEST_OPTS" : ["ACCEPT", "DECLINE", "COMPLETE"],
}