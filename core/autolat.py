LALIGN = 0
RALIGN = 1
x = [
["Bonus", 400, "Aaa?"],
["Test", 950],
["Carried Forward", 120, "NER NER NER"],
["Total", (400+120+950)]

]

class autolatCradle():
	def __init__(self, x, p = [LALIGN, RALIGN]): #, y = [None] * 2):
		y = [None] * len(x[0])
		self.superout = []
		for i in x:
			for j in range(len(i)):
				if (y[j] is None or y[j] < len(str(i[j]))):
					y[j] = len(str(i[j]))
					#print(j)
				
			pass
			
		for i in x:
			out = ""
			for j in range(len(i)):
				#print(y[j] +len(str(i[j])))
				if (p[j]== LALIGN):
					out += str(i[j]) + (" " * (y[j] - len(str(i[j])) + 1))
				elif (p[j] == RALIGN):
					out += (" " * (y[j] - len(str(i[j])) + 1)) + str(i[j]) + " "
				#print(out)
			self.superout.append(out)
			
	def go(self):
		return "\n".join(self.superout)