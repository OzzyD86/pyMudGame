class mapCmd():
	def __init__(self, gEngine, opts):
		self.out = ""
		if not "players" in gEngine.map_data:
			gEngine.map_data['players'] = {}
		
		if not gEngine.data['piq'] in gEngine.map_data['players']:
			gEngine.map_data['players'][gEngine.data['piq']] = {}
			gEngine.map_data['players'][gEngine.data['piq']]['map_points'] = []
			
		
		#print("Done something!")
		print(opts)
		if (opts[2] in  ["LIST", "DELETE", "DEL"]):
			if (opts[1] == "WAYPOINT"):
				if (opts[3] == "HERE"):
					p = 0
					c = 0
					dl = None
					dd = tuple(gEngine.player[gEngine.data['piq']]['position'].values())
					print(dd)
					for i in gEngine.map_data['players'][gEngine.data['piq']]['map_points']:
#						print(i)
						#print(i['location'], dd)
						if (i['location'] == dd):
							#print("yeah")
							#print(opts[4])
							if (opts[2] in ["DELETE"] and p == int(opts[4])):
								dl = c
								print("C:",c)
							self.out += str(p) + ": " + i['label'] + "\n"
							p += 1
						c += 1
					
					if (opts[2] in ["DELETE"] and dl is not None):
						#for i in (gEngine.map_data['players'][gEngine.data['piq']]['map_points']):
						#	print(i)
						#print("==")
						#for i in (gEngine.map_data['players'][gEngine.data['piq']]['map_points'][:dl] + gEngine.map_data['players'][gEngine.data['piq']]['map_points'][dl+1:]):
						#	print(i)
						gEngine.map_data['players'][gEngine.data['piq']]['map_points'] = gEngine.map_data['players'][gEngine.data['piq']]['map_points'][:dl] + gEngine.map_data['players'][gEngine.data['piq']]['map_points'][dl+1:]
		if (opts[2] == "ADD"):
			print("Add...")
			if (opts[1] == "WAYPOINT"):
				print("Waypoint")
				w_name = opts[3]
				print("Waypoint name: ", w_name)
				
				loc = (int(opts[6].strip(",(")), int(opts[7].strip(")")))
				print("Location:", loc)
				
				gEngine.map_data['players'][gEngine.data['piq']]['map_points'].append({ "location" : loc, "label" : w_name})
				
	def pushTime(self):
		return 0.001
	
	def describe(self):
		return self.out
		
muds = {
	"START" : [ "MAP [MAP_OPTIONS]" ],
	"MAP_OPTIONS" : [ "WAYPOINT ADD [%STRING%] [MAP_LOCS]", "WAYPOINT LIST HERE", "WAYPOINT DELETE HERE [%NUMBER%]"],
	"MAP_LOCS" : [ "AT LOCATION ([%NUMBER%], [%NUMBER%])", "HERE"]
#	"MAP_WITH_OPTIONS" : [ "[MAP_OPT]", "[MAP_OPT] AND [MAP_OPT]", "[MAP_OPT], [MAP_WITH_OPTIONS]" ],
#	"MAP_OPT" : ["HEAT ZONES", "NO HOUSES", "NO FOG OF WAR", "ALL SQUARES VISIBLE"]
}

cmds = {
	"MAP" : [ "cmds.map", "mapCmd" ],
}
