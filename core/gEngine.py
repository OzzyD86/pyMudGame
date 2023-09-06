import json, pickle, pathlib
import sys, importlib
import random, os
import core.phraseReplace

#sys.path.append("../")
#import mapper

def array_merge(a, b, path = None):
	if path is None: path = []
	
	for key in b:
		if (key in a):
			if isinstance(a[key], dict) and isinstance(b[key], dict):
				a[key] = array_merge(a[key], b[key])
			elif isinstance(a[key], list) and isinstance(b[key], list):
				a[key] += b[key]
			elif a[key] == b[key]:
				# Do nothing
				pass
			else:
				a[key] = b[key]
		else:
			if (type(a) == list):
				a = dict(a)
				#print(type(b), type(a), key)
			a[key] = b[key]
		#print(key)
	return a

def split_special(string = "", around = " "):
	sp_string = "%%"
	exp = []
	
	while (string.find("\"") >= 0):
		st = string.find("\"")
		en = string.find("\"", st+1)
		if (en < st):
			break
		#print(en, st)
		#print(string[st+1:en])
		exp.append(string[st+1:en])
		string = string[:st] + sp_string + string[en+1:]
		#print(string)
	
	expl_in = string.split(around)
	expl_out = []
	for i in expl_in:
		if (i == "%%"):
			expl_out.append(exp.pop(0))
		elif (i[:2] == "%%"):
			expl_out.append(exp.pop(0) + i[2:])
		elif (i.find("%%") > -1):
			expl_out.append(i[:i.find("%%")] + exp.pop(0) + i[i.find("%%")+2:])	# Or something like that
		else:
			expl_out.append(i)
	
	return expl_out

class gEngine():
	def __init__(self):
		self.map_data = {}
		self.cmds = {}
		self.config = {  }
		self.events = { "onMove" : [] }	# For example
		self.tickOps = []
		self.loaders = []
		self.data = {}
		#self.new()
		#self.position = {"x" : 0,"y" : 0 }

	def say(self, text = ""):
		#print(self.narration)
		x, self.narration = core.phraseReplace.phraseReplace_v2(text, self.narration)
		return x
		
	def new(self, seed = None):
		self.map_data = {}
		self.out = ""
		self.transcript = ""
		self.time = 0
		self.player = [{ "time" : 0, "human" : True, "position": { "x": 0, "y" : 0, "z" : 0 }}]
		
		for i in self.loaders:
			getattr(self, i).reset()
		if (seed is None):
			self.config['seed'] = random.randrange(sys.maxsize)
		else:
			self.config['seed'] = seed
		random.seed(self.config['seed'])
		self.mapp.reset(self.config['seed'])

		while (self.mapp.get_tile(self.player[0]['position']['x'], self.player[0]['position']['y'])['type'] in self.mapp.forbid_move):
			p = random.choice(self.mapp.edge_tiles)
			print("Try" + str(p))
			self.player[0]['position'] = { "x" : p[0], "y" : p[1], "z" : p[2] }
			print(".", end='')
		
		print(self.player[0]['position'])
		
	def load(self, name):
		dir = "./saves/" + name
		if (not os.path.isdir(dir)):
			return False
			
		d = open(dir + "/main.pkl", "rb")
		#d = open(name, "rb")
		op = pickle.loads(d.read())
		d.close()
		self.time = op['time']
		d = open(dir + "/defaults.pkl", "rb")
		defs = pickle.loads(d.read())
		d.close()
		
		if (os.path.isfile(dir + "/map_data.pkl")):
			d = open(dir + "/map_data.pkl", "rb")
			self.map_data = pickle.loads(d.read())
			d.close()
		else:
			self.map_data = {}
		
		self.config['save_name'] = name
		self.config['seed'] = defs['seed']
		print("Seed is " + str(self.config['seed']))
		self.mapp.reset(self.config['seed'])
		#self.position = op['self']
		self.player = op['player']
		for i in self.player:
			if not ("z" in i['position']):
				i['position']['z'] = 0
		self.data = op['data']
		if (op['map'] != {}):
			self.mapp.raw_load(op['map'])
		
		self.mapp.load(name)
		
	def partLoad(self, part, obj):
		self.loaders.append(part)
		setattr(self, part, obj)
		
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
		dir = "./saves/" + name 
		pathlib.Path(dir).mkdir(exist_ok=True)
		
		d = open(dir + "/main.pkl", "wb")
		self.mapp.save(dir)
		
		op = pickle.dumps({ "map" : self.mapp.raw_save(), "time" : self.time, "player" : self.player, "data" : self.data })
		d.write(op)
		d.close()
		d = open(dir + "/defaults.pkl", "wb")
		self.config['save_name'] = name
		d.write(pickle.dumps({ "seed" : self.config['seed'] }))
		
		d = open(dir + "/map_data.pkl", "wb")
		d.write(pickle.dumps(self.map_data))
		
		d.close()
	
	def genUniqueNum(self):
		if ("uidc" not in self.data):
			self.data['uidc'] = 0
			
		self.data['uidc'] += 1
		return self.data['uidc']
		
	def cmdExec(self, cmd = ""):
		o = self.mud.xref(cmd)
		if (o):
			if (cmd == "INITIALISE"):
				self.mud.load(array_merge(self.muds, {
					"START" : [ "EXIT" ],
					"DIRECTION_TRADITIONAL" : [ "UP", "DOWN", "LEFT", "RIGHT" ],
					"DIRECTION_CLASSIC" : ["NORTH", "EAST", "SOUTH", "WEST" ],
					"DIRECTION" : [
						"[DIRECTION_TRADITIONAL]",
						"[DIRECTION_CLASSIC]",
					]
				}))
			else:			
				p = split_special(cmd, " ")
				foo = importlib.import_module(self.cmds[p[0]][0])
				r = getattr(foo, self.cmds[p[0]][1])
				a = r(self, p)
				return a
		else:
			print(cmd + " is invalid")	
			
	def coreRun(self):
		self.transcript = ""
		
		self.data['piq'] = 0 # Spurious hack. Look into this?

#		x = sorted(self.player, key=lambda x: x['time'])
#		print(x)
		
		while True:
						
			x = input("Choose your action: ").upper()
			print()
			if ("map_state" not in self.map_data['players'][self.data['piq']]):
				self.map_data['players'][self.data['piq']]['map_state'] = 0
			
			ms = self.map_data['players'][self.data['piq']]['map_state']
			if (ms == 0):
				state = "[START]"
			elif(ms == 1):
				state = "[SHOP_INSIDE]"
			o = self.mud.xref(x, state)
			#print(o)
			if (o):
				if (x == "EXIT"):
					#for i in self.mapp.list_tiles():
					#	print(i)
					print("Saving as " + self.config['save_name'] + "...")
					self.save(self.config['save_name'])
					#print(self.transcript)
					#ff = open("transcript.txt", "w")
					#ff.write(self.transcript)
					#ff.close()
					sys.exit(1)
				else:
					#print("Okay MUD Complete!")
					#print(x)
					p = split_special(x, " ")
					#print(p)
					#print(p)
					#p = x.split(" ")
					#print(self.cmds[p[0]])
					if (isinstance(self.cmds[p[0]], list)):
						#print("Yes")
						foo = importlib.import_module(self.cmds[p[0]][0])
						r = getattr(foo, self.cmds[p[0]][1])
					else:
						r = self.cmds[p[0]]
						#print(self.cmds[p[0]])
						#print("no")
						
					a = r(self, p)
					#print(a)
					self.player[self.data['piq']]['time'] += a.pushTime()
					while (self.player[0]['time'] > self.time):
						self.tick()
					t = self.passiveTranscript()
					self.transcript += "> " + x + "\n" + a.describe() + " " + t + "\n\n"
					print(a.describe() + t)
		#			print(t)
				pass
			else:
				print(x + " is invalid")
				
	def registerEvent(self, pid, npcid, quest):
		if not ("questList" in self.data):
			self.data['questList'] = []
		
		self.data['questList'].append([pid, npcid, quest])
		print("Registered")
		return None

	def deregisterEvent(self, pid, npcid):
		q = []
		for i in self.data['questList']:
			if not (i[0] == pid and i[1] == npcid):
				q.append(i)
				
		self.data['questList'] = q
		return None
		
	def cueEvts(self, event = ""):
		out = ""
		if (event in self.events):
			for i in self.events[event]:
				out += i(self)
		
		if ("questList" in self.data):
			print(self.data['questList'])
			for i in self.data['questList']:
				if (event in i[2].events):
					for j in i[2].events[event]:
						out += j(self)
					
		return { "transcript" : out }
