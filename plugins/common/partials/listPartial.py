import core.autolat

class listy():
	def __init__(self, columns = 1):
		self.data = []
		self.fLengths = [0] * columns
		self.columns = columns
		
	def add_data(self, data):
		#print(self.fLengths)
		for i in range(min(self.columns, len(data))):
			#if (i in self.fLengths):
				self.fLengths[i] = max(len(str(data[i])) + 1, self.fLengths[i])
				#print(i)
		self.data.append(data)
	
	def draw(self):
		out = ""
		#print("Draw")
		#print(self.fLengths)
		for i in self.data:
			for j in range(min(len(i), self.columns)):
				#print(i, j)
				out += str(i[j]) + (" " * (self.fLengths[j] - len(str(i[j]))))
				#out += str(i[j]) + " " * (self.fLengths[j] - len(str(i[j])))
			out += "\n"
		return out
		
class questPartial():
	def __init__(self, gEngine, preOpts, postOpts):
		self.tPlus = 0
		self.out = ""
		#print("This should list quests")
		
		ls = []
		l = listy(6)
		for i in gEngine.player:
			if (i['human'] == False and "quest" in i):
				c = i['quest'].internal_state
				if (c == "ACCEPTED" and i['quest']._criteria_met() == True):
					c = "RETURNABLE"
				ls.append([i['uid'], i['position'], i['quest'].internal_state, c, i['quest']._criteria_met(), i['quest'].explain(), i])
				l.add_data([i['uid'], i['position'], i['quest'].internal_state, c, i['quest']._criteria_met(), i['quest'].explain()])
				
		#print(l.draw())
				#print(i)
		
		if (len(postOpts) > 1):
			#print(postOpts[1])
			if (postOpts[1] == "DETAIL"):
				p = int(postOpts[2])
				#print(len(ls), p)
				if (len(ls) < p):
					self.out += "Invalid"
				elif (p < 1):
					self.out += "Invalid"
				else:
					self.out += str(ls[p-1][:-1]) + "\n"
					self.out += "\n" + ls[p-1][-1]['quest'].detail()
		else:
			self.out += l.draw()
#			for i in ls:

				#print(i[:-1])
			
		#d = []
		#pl = gEngine.player[gEngine.data['piq']]
		#if ("score_breakdown" in pl):
		#	for i in pl['score_breakdown'].values():
		#		print(i)
		#		d.append([i['nature'], i['score']])
		#	
		#if ("score" in pl):
		#	d.append(["Current balance:", pl['score']])
		#
		#if (len(d) > 0):
		#	print(core.autolat.autolatCradle(d).go())

	def pushTime(self):
		return self.tPlus
		
	def describe(self):
		return self.out

print("Partial Loading")

MANIFEST = {
	"cmds" : {
		"list" : {
			"quests" : questPartial
		}
	},
	
	"muds": {
		"START" : [ "LIST QUESTS", "LIST QUESTS DETAIL [%NUMBER%]"]
	},
}
