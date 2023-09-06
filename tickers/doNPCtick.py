import core.tickableObject
import random
import core.autolat
class doNPCTick(core.tickableObject.tickableObject):
	def runTick(self):
		c = 0
		players = []
		npcs = []
		for i in self.gEngine.player:
			if (i['human']):
				players.append(i)
			else:
				npcs.append(i)
				
		for i in npcs:
			c += 1
			if (i['time'] < self.gEngine.time):
				pl = self.gEngine.player[self.gEngine.data['piq']]
				#if (not "z" in pl['position']):
				#	pl['position']['z'] = 0
				if (not "z" in i['position']):
					i['position']['z'] = 0
					
				ra = (abs(i['position']['x'] - pl['position']['x']) + abs((i['position']['y'] - pl['position']['y'])) + abs((i['position']['z'] - pl['position']['z']) * 4))
				#print(ra)
				if (ra <= 7):
					self.out += self.gEngine.say("<%NPC.sighted%>") #"An NPC is within detectable range of the player. "
					if (True):
						if not ("z" in i['position']):
							i['position']['z'] = 0
						pt = self.gEngine.mapp.tiles[i['position']['x'], i['position']['y'], i['position']['z']]
						if ("sightings" in pt):
							pt['sightings'] += 1
						else:
							pt['sightings'] = 1
							
						#print("ALERT: ", self.gEngine.mapp.tiles[i['position']['x'], i['position']['y']])
						if (i['nature'] == "chaser"):
							self.out += "They start to follow. "
							a = self.gEngine.mapp.aStarSearch((i['position']['x'], i['position']['y'], i['position']['z']), (pl['position']['x'], pl['position']['y'], pl['position']['z']))
							if (isinstance(a, core.mapper.aStarComplete)):
								#print(a.history)
								i['route'] = a.history.copy()[1:]
								i['mode'] = "chase"
								i['data'] = { "location" : pl['position'] }
							elif (isinstance(a, core.mapper.aStarPartial)):
								i['route'] = a
							#print("Path obj: ", a)
						elif (i['nature'] == "shouter"):
							self.out += "They shout. "
							p = 0
							for j in npcs:
								if not (i == j):
									
									ra = (abs(i['position']['x'] - j['position']['x']) + abs((i['position']['y'] - j['position']['y'])) + abs((i['position']['z'] - j['position']['z'])))
									if (ra <= 15 and j['mode'] != "chase"):
										#print(j)
										p += 1
										print(i['position'], j['position'])
										if not ("z" in j['position']):
											j['position']['z'] = 0
										a = self.gEngine.mapp.aStarSearch((j['position']['x'], j['position']['y'], j['position']['z']), (i['position']['x'], i['position']['y'], i['position']['z']))
										if (isinstance(a, core.mapper.aStarComplete)):
											j['route'] = a.history.copy()[1:]
											print("a:", a.history)
											j['data'] = { "location" : i['position'] }
											j['mode'] = "alert"
										elif (isinstance(a, core.mapper.aStarPartial)):
											j['route'] = a
#										j['route'] = a.copy()
										#print(j)
									#sys.exit(1)
							if (p > 0):
								self.out += str(p) + " more people are alerted! "
				
				via = []
				if ("route" in i):
					if (isinstance(i['route'], core.mapper.aStarPartial)):
						#print("Route IS a partial")
						a = self.gEngine.mapp.aStarSearch(None, i['route'].finish, partial_object = i['route'])
						if (isinstance(a, core.mapper.aStarComplete)):
							print(a.history)
							i['route'] = a.history.copy()[1:]
						elif (isinstance(a, core.mapper.aStarPartial)):
							i['route'] = a
						else:
							print("Well I don't know what's going on here!")
					elif (len(i['route']) > 0):
						x = i['route'].pop(0)
						nx = (abs(i['position']['x'] - x[0]) + abs(i['position']['y'] - x[1]) + abs(i['position']['z'] - x[2])) 
						if (nx <= 1):
							i['position'] = { "x" : x[0], "y" : x[1], "z": x[2] }
							#print("Update NPC's position based on a route... ")
						else:
							print(x, nx, i['route'])
							#print(nx)
							print("Cannot move NPC at " + str(i['position']) + " to " + str(x))
							print("Was there an issue?")
					else:
						print(i['route'])
						del i['route']						
						print("I think we're done with routing?")
				else:
					i['mode'] = "frolick"
					# Just frollick
					if not ("z" in i['position']):
						i['position']['z'] = 0
					for j in [(0,1,0), (1, 0,0), (0,-1,0), (-1, 0,0)]:
						if ((i['position']['x'] + j[0], i['position']['y'] + j[1], i['position']['z'] + j[2]) in self.gEngine.mapp.tiles and self.gEngine.mapp.tiles[(i['position']['x'] + j[0], i['position']['y'] + j[1], i['position']['z'] + j[2])]['type'] not in self.gEngine.mapp.forbid_move):
							via.append((i['position']['x'] + j[0], i['position']['y'] + j[1], i['position']['z'] + j[2]))
					
					if (len(via) > 0):
						ch = random.choice(via)
						#self.out += "Update NPC position from " + str(i['position']) + " to " + str(ch) + ".\n"
						i['position'] = { "x" : ch[0], "y" : ch[1], "z": ch[2] }
				#print(i)
				i['time'] += 1.4
				
				if (i['position'] == pl['position']):
					self.gEngine.cueEvts("playerCaught")

					print("'You have been caught, and for you, the chase is over' - Bradley Walsh")
					print(core.autolat.autolatCradle([["You have lost", self.gEngine.data['quests']['cashPot']]]).go())
					pl['naked'] = False
					self.gEngine.data['quests']['cashPot'] = 0
			#else:
			#	print("NPC waiting...")
		ti = len(self.gEngine.mapp.tiles)
		#print(self.gEngine.mapp.tiles)
		#print(str(ti) + " tile(s) should spawn " + str(ti // self.gEngine.config['core']['npcpt']) + " NPCs, and there are " + str(c))
		spw = (ti // self.gEngine.config['core']['npcpt']) - c
#		print(ti)
		if (spw < 0): spw = 0
		#print("Spawn " + str(spw) + " more!")
		
		for i in range(spw):
			#print("Spawning NPC " + str(i + 1) + "...")
			x = random.choice(self.gEngine.mapp.edge_tiles)
#			print("try", x, "?")
			via = []
			for j in [(0,1,0), (1, 0,0), (-1, 0,0), (0, -1,0)]:
				v = (x[0] + j[0], x[1] + j[1], x[2] + j[2])
				if (v in self.gEngine.mapp.tiles and self.gEngine.mapp.tiles[v]['type'] not in self.gEngine.mapp.forbid_move):
					via.append(v)
					#print(v, "is viable.")
			
			if (len(via) > 0):
				spw = True
#				print(via)
				w = random.choice(via)
#				print("Spawn at " + str(w) + "?")
				for i in players:
					if ((abs(w[0] - i['position']['x']) + abs(w[1] - i['position']['y']) + 0) < 10):
						print("Tried to spawn NPC too close to player")
						spw = False
						break
					else:
						print("Spawn")

				if (spw):
					self.gEngine.player.append({ "position" : { "x" : w[0], "y": w[1], "z" : 0 }, "time" : self.gEngine.time, "human" : False, "nature" : random.choice(["chaser", "chaser", "shouter"]), "mode" : "frolick", "data": {} })
