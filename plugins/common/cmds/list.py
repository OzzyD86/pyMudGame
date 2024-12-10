import core.autolat
	
class list():
	def __init__(self, gEngine, opts):
		self.tPlus = 0
		self.out = ""
	
		#print(opts)
		
		if (len(opts) > 1):
			pre = opts[:1]
			post = opts[1:]

			a = gEngine.handlePartial("list", post[0], post, pre)
			self.out += a.describe()
			self.tPlus += a.pushTime() # if any!
			
		else:
			print("This is the list function")
			d = []
			pl = gEngine.player[gEngine.data['piq']]
			if ("score_breakdown" in pl):
				for i in pl['score_breakdown'].values():
					print(i)
					d.append([i['nature']+ ":", "{:,.2f}".format(float(i['score']))])
				
			if ("score" in pl):
				d.append(["Current balance:", "{:,.2f}".format(float(pl['score']))])
		
			if (len(d) > 0):
				print(core.autolat.autolatCradle(d).go())
	def pushTime(self):
		return self.tPlus
		
	def describe(self):
		return self.out

print("Is this loaded?")

MANIFEST = {
	"muds": {
		"START" : [ "LIST" ]
	},
	"cmds" : {
		"LIST" : list,
	}
}
