class mud():
	def __init__(self):
		self.checker = {}
		
		pass
	def load(self, data):
		self.checker = data
		
	def check(self, string = "", cond = "[START]"):
		outs = [cond]
		#print(cond.find("["))
		c = outs.pop()
		if (c.find("]") >= 0):
			if (c.find("[") >= 0):
				p = c[c.find("[")+1:c.find("]")]
				if not (p in self.checker):
					return []
				for i in self.checker[p]:
#					print(i[:i.find("[")]):
					if (i.find("[") < 0):
						if (string[:c.find("[")] + i + c[c.find("]") + 1:] == string):
							outs.append(string[:c.find("[")] + i + c[c.find("]") + 1:])
					elif (string[:c.find("[")] + i[:i.find("[")] == string[:i.find("[")]):
#						print("Match")
						outs.append(string[:c.find("[")] + i + c[c.find("]") + 1:])

				#print(c[c.find("[")+1:c.find("]")])
		return outs
		
	def xref(self, prompt):
		trai = prompt
		t = ["[START]"]
		found = False
		while (found == False):
			if (len(t) == 0):
				#print("Nothing matched")
				return False
			f = self.check(trai, t.pop(0))
			#print(f)
			for i in f:
				t.append(i)
				if (i.find("[") == -1):
					#print(i)
					found = True
					return True
