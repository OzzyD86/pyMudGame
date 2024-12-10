import time

def num(nm, nm2):
	return (nm > nm2)

class value:
	def __init__(self, thing):
		self.inn = thing
	
	def __call__(self):
		return 

class conf:
	gun = 0
	def __init__(self):
		self.gun = 0
#gun = 0
bb = conf()

class achievement_stack:
	def __init__(self):
		
		self.vars = {
			"steps": 0,
		}
		self.stack = {
			"complete": [],
			"incomplete": []
		}
	
	def check_var(self, name, val):
		if (self.vars[name] >= val):
			return True
		return False
		
	def add(self, achievement):
		if (achievement.check()):
			self.stack["complete"].append(achievement)
		else:
			self.stack["incomplete"].append(achievement)

	def autoGrant(self, ls):
		c = self.stack["incomplete"]
		self.stack["incomplete"] = []
		st = time.time()
		ret = []
		for i in c:
			if (i.iname in ls):
				self.stack["complete"].append(i)
				#ret.append(i)
				#print("Complete")
			else:
				self.stack["incomplete"].append(i)

	def checkAll(self):
		c = self.stack["incomplete"]
		self.stack["incomplete"] = []
		st = time.time()
		ret = []
		for i in c:
			if (i.check()):
				self.stack["complete"].append(i)
				ret.append(i)
				#print("Complete")
			else:
				self.stack["incomplete"].append(i)
		fi = time.time()
		print("Check took",(fi-st),"seconds.")
		return ret
	
	def reset(self):
		while (len(self.stack['complete']) > 0):
			a = self.stack['complete'].pop()
			self.stack['incomplete'].append(a)
			
	def get_completed(self):
		out = []
		for i in self.stack['complete']:
			out.append(i.iname)
		return out
		
class achievement:
	def __init__(self, title, desc = "", iname = None):
		self.checks = []
		self.title = title
		self.iname = iname
		self.desc = desc
		
	def add(self, fn, *vars):
		self.checks.append([fn, *vars])
		pass
		
	def check(self):
		for i in self.checks:
			#print (i[1:])
			if (not i[0](*i[1:])):
				return False
		return True
		
'''ach = achievement_stack()
a = achievement("Five hundred miles", iname = "500mi")
#a.add(num, 152, 151)
a.add(ach.check_var, "steps", 804672)

ach.add(a)

a = achievement("Streaker!")
a.add(ach.check_var, "nude_steps", 1)
ach.add(a)

a = achievement("Skin Runner", iname="skr")
a.add(ach.check_var, "nude_steps", 100)
ach.add(a)

a = achievement("Casual half hour", iname = "cah")
a.add(ach.check_var, "nude_time", 30)
ach.add(a)

a = achievement("A day in the pink", iname = "dip")
a.add(ach.check_var, "nude_time", 1440)
ach.add(a)

a = achievement("Adventure time", iname = "adt")
a.add(ach.check_var, "quests", 1)
ach.add(a)

a = achievement("Adventure lover", iname = "adlov")
a.add(ach.check_var, "quests", 10)
ach.add(a)

a = achievement("Adventure legend", iname = "adleg")
a.add(ach.check_var, "quests", 25)
ach.add(a)

ach.autoGrant(["dip"])
ach.vars["nude_steps"] = 300

p = ach.checkAll()
#print(ach.stack)
#print(p)

for i in p:
	print(i.title,":",i.desc)

print(len(ach.stack["complete"]) / (len(ach.stack["complete"]) + len(ach.stack["incomplete"]) )*100, "%")
''''''print("===")
for i in ach.stack["complete"]:
	print(i.title,":",i.desc)'''