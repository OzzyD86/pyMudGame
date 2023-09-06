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
			
			#print(gEngine.player)
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
			
			if (select_npc is None and len(npcs) > 1):
				self.out += response
			elif (len(npcs) == 0):
				self.out += "There is no-one around\n"
			elif(select_npc is not None and ((select_npc < 0) or ((select_npc) > len(npcs)))):
				self.out += "There is no such option on this list\n"
			else:
				self.out += "Switch to " + sw + " for NPC " + str(select_npc) + ". Action!"
				## Okay. If we're here, things need to get done
#				self.out += "\n" + str(npcs[select_npc - 1]) + "\n" # I need not write this line any more. Keeping it for debug and completeness and what not
				if (select_npc is None):
					self.out += "\nPlease select an NPC."
				else:
					pp = npcs[select_npc - 1]
					if (not "quest" in pp):
						pp['quest'] = None
						print("Adding quest to NPC. Let's see what happens")
				
					if (not "uid" in pp):
						pp['uid'] = gEngine.genUniqueNum()
						print(pp['uid'])

					if pp['quest'] is None:
						#print(gEngine.quests)
						x = random.choice(gEngine.quests)(gEngine, ['', '', sw.upper(), pp['uid']])
						pp['quest'] = x
						print("Give NPC a quest here!")
					else:
						print("This NPC has a quest!")
						x = pp['quest'].state(['', '', sw.upper(), pp['uid']])	# Now then ... can I do this?

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