class mud():
	def __init__(self):
		self.checker = { "START" : [ "INITIALISE" ] }
		pass
		
	def reset(self):
		pass
		
	def load(self, data):
		self.checker = data
	
#	def expand(self, input, vs):
#		p = input
#		q = p.find("[")
#		print(p,q)
#		r = p[q:]
#		print(r)
	
	def check(self, string = "", cond = "[START]"):
		outs = [cond]
		#print(cond.find("["))
		c = outs.pop()
		#print("c:", c)
		
		if (c.find("]") >= 0):
			#print("1 Yes")
			if (c.find("[") >= 0):
				#print("2 Yes")
				p = c[c.find("[")+1:c.find("]")]
				#print("p:", p)
				if not (p in self.checker):
					#print("3 No")
					if (p in ["%STRING%", "%NUMBER%"]):
						tx = string[string.find("\"", c.find("["))+1:]
						tx = tx[:tx.find("\"")]
						#print(p, tx)
						if (p == "%NUMBER%"):
							#print(p, tx)
							try:
								tx = int(tx)
							except:
								#print("A number included text")
								return []	# Can we PLEASE make this nicer somehow?
								
						outs.append(c[:c.find("[")] + "'" + str(tx) + "'" + c[c.find("]") + 1:])
						#print(string)
					else:
						#print("Self checker returned a blank")
						return []
				else:
					#print("3 Yes")
					for i in self.checker[p]:
						#print(i)
						#print("DEBUG: ", c, ", ", i) 
						#print(c, i, string)
#						print("DEBUG: ", i[:i.find("[")], len(i[:i.find("[")]))
						cd = c.find("[")
						
						chk = i + c[c.find("]")+1:]
						pos = chk.find("[")
						
						#print(pos, string[:pos], ",", chk[:pos])
						if (pos != -1 and chk[:pos] == string[:pos]):
							op = [string[pos:], chk[pos:]]
							#print("WHAT?",op)
							outs.append(op)
						elif (i.find("[") < 0):
							#print("=== DOES THIS EVER EXECUTE? (1) ===") # Yes it executes.
							#print("found [")
							if (string[:cd] + i + c[c.find("]") + 1:] == string):
								#print(string[:c.find("[")] + i + c[c.find("]") + 1:] + " is identical")
								outs.append(string[:cd] + i + c[c.find("]") + 1:])
								print("If 1 pass")
							#else:
								#print("If 1 fail")
						else:
							#print("=== DOES THIS EVER EXECUTE? (2) ===") # Yes it executes
							a = string[:cd] + i[:i.find("[")]
							b = string[:cd] + string[cd:i.find("[")+cd]
							#print("check '" + a + "' against '" + b + "'")
							if (a == b):
		#						print("Match")
								#print("If 2 pass")
								outs.append(string[:cd] + i + c[c.find("]") + 1:])
								qq = i.find("[")
								#print("* Should match '" + string[qq:] + "' against '" + i[qq:] + "'")
								outs.append([string[qq:], i[qq:]])
#								print("Match between '" + a + "' and '" + b + "'")
							#else:
								#print("If 2 fail")
								#print("No match between '" + a + "' and '" + b + "'")
				#print(outs)
		return outs
		
	def xref(self, prompt):
		t = [[prompt, "[START]"]]
		found = False
		while (found == False):
			#print(len(t))
			if (len(t) == 0):
				#print("Nothing matched")
				return False
			st = t.pop(0)
			#print(st)
			f = self.check(st[0], st[1])
			for i in f:
				t.append(i)
				#print("xref i:",i)
				if (i[1].find("[") == -1):	# This line once errored with a string index out of bounds which I missed/neglected at the time
					#print(i)
					found = True
					return True
