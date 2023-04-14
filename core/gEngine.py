import json
import sys, importlib
#sys.path.append("../")
#import mapper

def array_merge(a, b, path = None):
	if path is None: path = []
	
	for key in b:
		if (key in a):
			pass
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
		else:
			expl_out.append(i)
	
	return expl_out

class gEngine():
	def __init__(self):
		self.cmds = {}
		self.events = { "onMove" : [] }	# For example
		self.tickOps = []
		self.loaders = []
		self.new()
		#self.position = {"x" : 0,"y" : 0 }

	def new(self):
		self.out = ""
		self.transcript = ""
		self.time = 0
		self.player = [{ "time" : 0, "human" : True, "position": { "x": 0, "y" : 0 }}]
		for i in self.loaders:
			getattr(self, i).reset()
		self.mapp.reset()
		
	def load(self, name):
		d = open(name, "r")
		op = json.loads(d.read())
		d.close()
		self.time = op['time']
		#self.position = op['self']
		self.player = op['player']
		self.data = op['data']
		self.mapp.raw_load(op['map'])
	
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
		d = open(name, "w")
		op = json.dumps({ "map" : self.mapp.raw_save(), "time" : self.time, "player" : self.player, "data" : self.data })
		d.write(op)
		d.close()

	def coreRun(self):
		self.transcript = ""
		
		self.mud.load(array_merge(self.muds, {
			"START" : [  
				"EXIT", 
			],
			"DIRECTION_TRADITIONAL" : [ "UP", "DOWN", "LEFT", "RIGHT" ],
			"DIRECTION_CLASSIC" : ["NORTH", "EAST", "SOUTH", "WEST" ],
			"DIRECTION" : [
				#"[DIRECTION_TRADITIONAL]",
				"[DIRECTION_CLASSIC]",
			]
		}))

		self.data['piq'] = 0 # Spurious hack. Look into this?

		while True:
			
			x = input("Choose your action: ").upper()
			o = self.mud.xref(x)
			#print(o)
			if (o):
				if (x == "EXIT"):
					#for i in self.mapp.list_tiles():
					#	print(i)
					self.save("test.json")
					print(self.transcript)
					ff = open("transcript.txt", "w")
					ff.write(self.transcript)
					ff.close()
					sys.exit(1)
				else:
					p = split_special(x, " ")
					#print(p)
					#p = x.split(" ")
					foo = importlib.import_module(self.cmds[p[0]][0])
					#foo = __import__(self.cmds[p[0]][0])
					r = getattr(foo, self.cmds[p[0]][1])
					a = r(self, p)
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
