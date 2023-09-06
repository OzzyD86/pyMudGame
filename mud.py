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
		#print("Initial: ", string, cond)
		#print(cond.find("["))
		c = outs.pop()
		#print("c:", c)
		#print(string, c)
		if (c.find("]") >= 0):
			if (c.find("[") >= 0):
				p = c[c.find("[")+1:c.find("]")]
				#print("p:", p)
				if (len(c[:c.find("[")]) > 0):
					print("Pre p: '", c[:c.find("[")], "'")
					print("Pre s: '", string[:c.find("[")], "'")
					if (c[:c.find("[")] == string[:c.find("[")]):
						#print("Matched")
						#print(string[c.find("["):])
						string = string[c.find("["):]
						c = c[c.find("["):]	#	 I mean ... obviously!
						print("Identical")
					else:
						print("Non-identical")
						return []
						
				if not (p in self.checker):
					#print("3 No")
					#print("3:", string, c)
					if (p in ["%STRING%", "%NUMBER%"]):
						tx = string[string.find("\"", c.find("["))+1:]
						tx = tx[:tx.find("\"")]
						#print("OUTS:", outs)
						#print(p, tx)
						#if (p == "%NUMBER%"):
						#	#print("O:", p, tx)
						#	try:
						#		tx = int(tx)
						#	except:
						#		print("A number included text")
						#		print(tx)
						#		return []	# Can we PLEASE make this nicer somehow?
						#print("TX:", tx)
#						print(, c)
						xxx = c[:c.find("[")] + "\"" + str(tx) + "\"" + c[c.find("]") + 1:]
						#op = [string[string.find("\"", 1)+1:], c[c.find("[", 2):]]
						if (string[0] in ["\"", "'"]):
							ls = string[0]
							# [1:] is missing first letter
							x = string[1:]
							y = x[x.find(ls):]
							op = [x[x.find(ls)+1:], c[c.find("]")+1:]]
							#print("OP is set")
						else:
							ls = " "
							#pn = c.find(ls)
							pa = c.find(ls)
							pb = c.find("]")
							#print(string)
							#print(c)
							#print("JUST PLEASE ... STOP!")
							#print("'" + c + "'", pa)
							#print(pa, pb, pb-pa)
							
							if (pa == -1):
								c += ls
								string += ls
								pa = c.find(ls)
								pb = c.find("]")
								
							pc = string[:string.find(ls)]
							pd = c[:c.find(ls)]
							#print("So ... match '" + pd + "' against '" + pc + "'?")
							pe = pd[pd.find("]")+1:]
							
							#print(c, string)
							#print(len(pe))
							
							pf = c[c.find(pe)+len(pe):]
							pg = string[string.find(pe)+len(pe):]
							#print(pd)
							pi = string[:string.find(pe)]
							if (p == "%NUMBER%"):
								try:
									if (len(pe) == 0):	# makes pi a search for an empty string... fun but impractical
										print(pi)
										pi = string[:string.find(" ")] # Ah much better!
										pi = int(pi)
										print(pi)
										
									else:
										print("So ... NOW match '" + pi + "'?")
										pi = int(pi)

									#op = [pg, pf]	# Replaced this
									op = [pg[pg.find(" "):], pf[pf.find(" "):]]	# With this
									
								except Exception as e:
									print(e)
									print("Numberwang?")
									op = None
							else:
								# pd is c, pc is string
								# pf is c, pd is string 
								#print(pe)
								ph = c[len(pd):]
								pj = string[len(pc):]
								
								op = [pj,ph]
#								sys.exit(1)
#							print("So ... match '" + c[c.find(ls):] + "' against '" + string[string.find(ls):] + "'?")
							#pc = c[:c.find(ls)][pb-pa+1:]
							#pd = string[:string.find(ls)][pb-pa+1:]
							
							#print("'" + pc + "'", "'" + pd + "'")
							#if (pc == pd):
							#	print("YES")
							#	pe = c[c.find(ls)+(pb-pa+1)+1:] 
							#	pf = string[string.find(ls)+(pb-pa+1)+1:]
							#	op = [pf, pe]
							#else:
							#	print("NO")
							#	op = None
							
							#x = string#[0:]	# I need this ... oh that's no fun(!)
							#print(x)
							#print("P2", 
							#print("P2", c[pn+1:c.find(" ")], string[po-1], string.find(" "))
							#y = string[:string.find(ls)]
							#z = c[:c.find(ls)]
							#pn = c.find("]")
							
							#print("pn", pn- len(z) + 1)
							#print(y, z, pn, "'" + string[pn-len(z)+1:] + "'", "'" + c[pn-len(z)+1:] + "'")
#							if (z[pn-len(z)+1:] == y[pn-len(z)+1:]):
							#if (string[pn-len(z)+1:] == c[pn-len(z)+1:]):
							#	print("YES!")
								#op = [x[x.find(ls)+1:], c[c.find("]")+1:]]
							#	op = [ string[string.find(ls):], c[c.find(ls):] ]
							#	print("OP is set")
							#else:
							#	print("NO!")
							#	print("OP is set")
#							else:
								# There's northing left
#								op = ['', '']
							#print(y)
						
						print("OP:",op)
						print("^^^")
						if (op is not None):
							outs.append(op)

					else:
						print("Self checker returned a blank")
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
							#print("WHAT? [1]:",op)
							outs.append(op)	# This bit seems to work fine
						elif (i.find("[") < 0):
							#print("=== DOES THIS EVER EXECUTE? (1) ===") # Yes it executes.
							#print("found [")
							if (string[:cd] + i + c[c.find("]") + 1:] == string):
								#print(string[:c.find("[")] + i + c[c.find("]") + 1:] + " is identical")
								xxx = [string[:cd] + i + c[c.find("]") + 1:], string]
								#rro = [string[qq:], i[qq:]] # WHY?!
#								print("xxx2:",xxx)
#								raise Exception("I'm causing issues again!")
								#print("WHAT? [2]:",xxx)
								outs.append(xxx)
								#print("If 1 pass")
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
								#outs.append(string[:cd] + i + c[c.find("]") + 1:])	# Do I homestly need this?
								qq = i.find("[")
								#print("* Should match '" + string[qq:] + "' against '" + i[qq:] + "'")

								if (qq == -1):
									outs.append(['',''])
									
								rro = [string[qq:], i[qq:]] # WHY?!
								#print("rro:",rro)
								#print("WHAT? [3]:",rro)

								outs.append(rro) # WHY?!
#								print("Match between '" + a + "' and '" + b + "'")
							#else:
								#print("If 2 fail")
								#print("No match between '" + a + "' and '" + b + "'")
				#print(outs)
		return outs
		
	def xref(self, prompt, base = "[START]"):
		t = [[prompt, base]]
		found = False
		while (found == False):
			#print(len(t))
			if (len(t) == 0):
				#print("Nothing matched")
				return False
			st = t.pop(0)
			#print(st)
			f = self.check(st[0], st[1])
			#print("=" * 8)
			#print("Self-check: ")
			for i in f:
				#print(i)
				t.append(i)
				#print("xref i:",i)
				if (i[1].find("[") == -1):	# This line once errored with a string index out of bounds which I missed/neglected at the time
					if (i[0] == i[1]):
						#print("MUD COMPLETE?",i)
						#print(i)

						found = True
						return True
