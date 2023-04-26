warn_level = 1#3
warn = []

import random
import sys
sys.path.append("../")

dirpos = "."

class replacer:
	def __init__(self, d):
		self.d = d
		self.warn = []

	def doImports(self, includes = []):
		for i in includes:
			j = __import__(i, globals(), locals(), ['d', 'warn', 'nature', 'version'])
			if (hasattr(j, 'version')):
				if (j.version == 2):
					for k, l in j.d.items():
						self.d = dictReplace(self.d, l, tx = k)
						#print(k,l)
				elif (j.version == 1):
					self.d = dictReplace(self.d, j.d, tx = 1)
			else:
				self.d = dictReplace(self.d, j.d, tx = 1)
			if (j.warn):
				self.warn.append({ "nature" : j.nature['nature'], "root" : i })

	def syntaxualise(self, p = None, seps =("(%", '%)')):
		if (p is None):
			p = self.d
		#print(p)
		if (type(p) == list):
			new_p = []
			for i in p:
			#print(i)
				if (type(i) == dict):
					o =[]
				#print(i)
					if (i['text'].find(seps[0]) >= 0):
						raise Exception("I still need to do this")
						#print(i)
					o.append(i)
				
					new_p += [i]
				#print(new_p)
				else:
					o = []
					q = [i]
					while (len(q) > 0):
						i = q.pop()
						#print(i)
						if (i.find(seps[0]) >= 0):
							#print(i)
							a = i.find(seps[1])
							c = i[:a]
							e = c.rfind(seps[0])+len(seps[0]) # the +2 is the length of the search string to add.
							f = c[e:]
							h = self.d
							for g in f.split('.'):
								#print(h)
								h = h[g]
						
							for j in h:
								k = i[:e-len(seps[0])] + j + i[a+len(seps[1]):]
								q.append(k)
								#print(k)
						else:
							o.append(i)
							#print(i)
					new_p += o
			return new_p
		elif (type(p) == dict):
			new_p = {}
			for i,j in p.items():
				out = self.syntaxualise(j, seps)
				if (len(out) > 0):
					new_p[i] = out
			return new_p
		#print("False")
		return False
	
def decr(*kwargs):
	if (int(d['vars']['val'][0]) > 0):
		d['vars']['val'][0] = str(int(d['vars']['val'][0]) - 1)
	if (int(d['vars']['val'][0]) == 0):
		d["vars"]["gameOver"] = ["yes"]
		d["lex"]["nouns"]["wild"] = ["tame", "naked"]
		global b
		b = "<%tamed%>"
	return kwargs

def incr(*kwargs):
	#if (int(d['vars']['val'][0]) > 0):
		d['vars']['lev'][0] = str(int(d['vars']['lev'][0]) + 1)
		if ((int(d['vars']['lev'][0]) % 2) == 0):
			if (len(farp) > 0):
				d['start'].append(farp.pop(0))
		return kwargs

def oo(*kwargs):
	kwargs = (kwargs[0], kwargs[1][::-1].replace("that"[::-1], "those"[::-1], 1)[::-1])
	
	return kwargs

def dictReplace(a, b, recurse = True, tx = 1):
	#print(tx)
	tb = b
	#print('Test ' + str(a) + ' against ' + str(b))
	#print('')
	out ={}
	for tc,td in a.items():
		#print(tc)
		if (tc in b):
			#print(type(tc))
			if (type(td) == dict and type(b[tc]) == dict):
				out[tc] = dictReplace(td, b[tc], tx = tx)
			elif (type(td) == list and type(b[tc]) == list):
				#print("Here?", tx == 1)
				#raise Exception("Where?")
				if (tx == 2):
					out[tc] = td.union(b[tc])
					#out[tc] = td.symmetric_difference(b[tc])
				elif (tx == 1):
					out[tc] = td + b[tc]
				else:
					out[tc] = b[tc]
			#	print('lists')
			else:# not (type(d) == dict )
				
				out[tc] = b[tc]
			#b.pop(tc)
		else:
			#print(type(td))
			out[tc] = td
		#print(str(c) + ' ' + str(d))
	
	for tc,td in b.items():
		if not (tc in out): # NOT THAT IT SHOULD!!
			out[tc] = td
	b = tb
	return out

def listCombine(a, b):
	out = {}
	for n,i in a.items():
		if (i in b):
			pass
		else:
			out[n] = i
	return out
#print(main)

def displayWarning(warnings: list = [], level: int = 2) -> str:
	out = ""
	if (level > 1):
		if (len(warnings) > 0):
			j = "This file has generated warnings of "
			pp = []
			for i in warnings:
				pp.append(i['nature'] + " from " + i['root'])
			if (len(pp) > 1):
				x = pp.pop()
				j += ", ".join(pp) + ", and " + x
				pp.append(x)
			else:
				j += pp[0]
			j += ". "

	if (level == 3):
		out += "".join(["Although we don't actively encourage or discourage the use of offensive or potentially illegal language " 
			"in our software, we do insist that all such material is reserved for modules that are to be included at the user's " 
			"disgression. \n\nTo this end, several included modules have been flagged in this file as potentially harmful or " 
			"offensive. These modules, and their reasons, are as follows: \n\n-> " + "\n-> ".join(pp) + "\n\n"
			"Please disable any modules that may cause any offense now by searching the phraseReplace.py file for 'includes' "
			"and removing the mentioned quoted item from the list.\n\nAlternatively, if this error is too annoying for you, "
			"please alter the number after 'warn_level = ' downwards until a satisfactory outcome is achieved.\n\nThank you "
			"for your understanding!\n\n"])
	elif (level == 2):
		out += j + "\n\n"
	elif (level == 1):
		if (len(warnings) > 0):
			out += "Offensive module listing supressed.\n\n" 
			
	return out

#import time
#dxr = replacer(d)


b='<%start%>'
def pushUpper(a, uStr = '%UNL%'):
	o = ''
	while (a.find(uStr) >= 0):
		x = a.find(uStr)
		q = a[x+len(uStr):x+len(uStr)+1]
		o += a[:x] + q.upper()
#		print(a[x+5:x+6])
		a = a[x+len(uStr)+1:]
	o += a
	return o

def structureTest(d):
	if (type(d) == list):
		return d
	elif (type(d) == dict):
		new_d = {}
		for i,j in d.items():
			out = structureTest(j)
			if (len(out) > 0):
				new_d[i] = out
		return new_d
	return False
	
def phraseReplace(fr, d, seps = ('<%', '%>')):
	while (fr.find(seps[1]) >= 0):
			a = fr.find(seps[1])
			c = fr[:a]
			e = c.rfind(seps[0])+len(seps[0]) # the +2 is the length of the search string to add.
			f = c[e:]
			h = d
			for g in f.split('.'):
				h = h[g]
	
			i = random.choice(h)
			j = fr[:e-len(seps[0])] + i + fr[a+len(seps[1]):]
			fr = j
	return fr

def phraseReplace_v2(fr, d, seps = ('<%', '%>')):
	while (fr.find(seps[1]) >= 0):
		a = fr.find(seps[1])
		c = fr[:a]
		e = c.rfind(seps[0])+len(seps[0]) # the +2 is the length of the search string to add.
		f = c[e:]
		h = d
		for g in f.split('.'):
			if not g in h:
				raise Exception("no '" + g + "' in '" + f + "'")
			h = h[g]
	
		#print(h)
		i = random.choice(h)
		if (type(i) == dict):
#			print(i)
#			print(i['follow_up'])
			j = fr[:e-len(seps[0])] + i['text'] + fr[a+len(seps[1]):]
			#print((i['follow_up']))
			if ('exec' in i['follow_up'] and callable(i['follow_up']['exec'][0])):
				#print(type(i['follow_up']['exec'][0]) == func)
				(i,j) = i['follow_up']['exec'][0](i,j)
			else:
				d = dictReplace(d, i['follow_up'], tx = 0)
		else:
			j = fr[:e-len(seps[0])] + i + fr[a+len(seps[1]):]
		fr = j
	return (fr, d)

#print(structureTest(com.pr.callmehorse.d))
#out = ''
#for i in range(0, 150):
'''
	o, d = phraseReplace_v2(b, d)
	out += o
out = pushUpper(out)'''

def permuteAll(p, d, seps = ("<%", "%>")):
	o = []
	q = [p]
	while (len(q) > 0):
		i = q.pop()
		if (i.find(seps[0]) >= 0):
			a = i.find(seps[1])
			c = i[:a]
			e = c.rfind(seps[0])+len(seps[0]) # the +2 is the length of the search string to add.
			f = c[e:]
			h = d
			for g in f.split('.'):
				h = h[g]
						
			for j in h:
				#print(j)
				if (type(j) == dict):
					k = i[:e-len(seps[0])] + j['text'] + i[a+len(seps[1]):]
				else:
					k = i[:e-len(seps[0])] + j + i[a+len(seps[1]):]
				o.append(k)
				#print(k)
		#else:
			#o.append(i)
	return o

def highlightIn(x, y):
	f = True
	t = ''
	for a in y:
		p = x.lower().find(a.lower())
		if (p < 0):
			raise Exception('Ran out of milk')
		if (p > 0 and not f):
			t += ']'
		t += x[:p]
		if (p > 0 or f):
			t += '['
		t += a
		f = False
		x = x[p+1:]
	t += ']' + x
	return t

def arrayMake(num, arr, min_length = 1):
	o = []
	if (num == 0):
		return [arr[0]]
	while (num > 0) or (len(o) < min_length):	
		o.append(arr[num % len(arr)])
		arr.pop(num % len(arr))
		num = (num // len(arr))
		print(arr)
	o.reverse()
	return o

