import core.tickableObject
import random

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
				ra = (abs(i['position']['x'] - pl['position']['x'])) + abs((i['position']['y'] - pl['position']['y']))
				#print(ra)
				if (ra <= 7):
					self.out += "An NPC is within detectable range of the player. "

						#self.out += "They start to follow. "
						#a = self.gEngine.mapp.aStarSearch((i['position']['x'], i['position']['y']), (pl['position']['x'], pl['position']['y']))['history'][1:]
						#i['route'] = a
						#print("Path obj: ", a)
				
				via = []
				if (("route" in i) and (len(i['route']) > 0)):
					x = i['route'].pop(0)
					nx = (abs(i['position']['x'] - x[0]) + abs(i['position']['y'] - x[1])) 
					if (nx <= 1):
						i['position'] = { "x" : x[0], "y" : x[1] }
						print("Update NPC's position based on a route... ")
					else:
						print(nx)
						print("Cannot move NPC at " + str(pl['position']) + " to " + str(x))
						print("Was there an issue?")
				else:
					# Just frollick
					for j in [(0,1), (1, 0), (0,-1), (-1, 0)]:
						if ((i['position']['x'] + j[0], i['position']['y'] + j[1]) in self.gEngine.mapp.tiles):
							via.append((i['position']['x'] + j[0], i['position']['y'] + j[1]))
					
					if (len(via) > 0):
						ch = random.choice(via)
						self.out += "Update NPC position from " + str(i['position']) + " to " + str(ch) + ".\n"
						i['position'] = { "x" : ch[0], "y" : ch[1] }
				print(i)
				i['time'] += 1.4
			else:
				print("NPC waiting...")
		ti = len(self.gEngine.mapp.tiles)
		print(str(ti) + " tile(s) should spawn " + str(ti // 50) + " NPCs, and there are " + str(c))
		spw = (ti // 50) - c 
		print("Spawn " + str(spw) + " more!")
		
		for i in range(spw):
			print("Spawning NPC " + str(i + 1) + "...")
			x = random.choice(self.gEngine.mapp.edge_tiles)
			print("try", x, "?")
			via = []
			for j in [(0,1), (1, 0), (-1, 0), (0, -1)]:
				v = (x[0] + j[0], x[1] + j[1])
				if (v in self.gEngine.mapp.tiles):
					via.append(v)
					print(v, "is viable.")
			
			if (len(via) > 0):
				w = random.choice(via)
				print("Spawn at " + str(w) + "?")
				self.gEngine.player.append({ "position" : { "x" : w[0], "y": w[1] }, "time" : self.gEngine.time, "human" : False }) 