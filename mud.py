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
				#print(c,p)
				if not (p in self.checker):
					if (p in ["%STRING%", "%NUMBER%"]):
						tx = string[string.find("\"", c.find("["))+1:]
						tx = tx[:tx.find("\"")]
						#print(p, tx)
						if (p == "%NUMBER%"):
							#print(p, tx)
							try:
								tx = int(tx)
							except:
								return []	# Can we PLEASE make this nicer somehow?
								
						outs.append(c[:c.find("[")] + "'" + str(tx) + "'" + c[c.find("]") + 1:])
						#print(string)
					else:
						return []
				else:
					for i in self.checker[p]:
						#print("DEBUG: ", c, ", ", i) 
						#print(c, i, string)
#						print("DEBUG: ", i[:i.find("[")], len(i[:i.find("[")]))
						cd = c.find("[")
						
						#print(cd)
						if (i.find("[") < 0):
							if (string[:cd] + i + c[c.find("]") + 1:] == string):
								#print(string[:c.find("[")] + i + c[c.find("]") + 1:] + " is identical")
								outs.append(string[:c.find("[")] + i + c[c.find("]") + 1:])
						elif (string[:cd] + i[:i.find("[")] == string[:cd] + string[:i.find("[")]):
	#						print("Match")
							outs.append(string[:cd] + i + c[c.find("]") + 1:])
							#print("Match between '" + string[:cd] + i[:i.find("[")] + "' and '" + string[:cd] + string[:i.find("[")] + "'")
						#else:
						#	print("No match between '" + string[:cd] + i[:i.find("[")] + "' and '" + string[:cd] + string[:i.find("[")] + "'")
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
