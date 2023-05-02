#print("Do I run and what of it?")
import importlib, os
#print(__file__)

from core.gEngine import array_merge

x = __file__.split("\\")
imp = ".".join(x[-3:-1])
INS = { "quests" : [] }
local = "/".join(__file__.split("\\")[:-1])

for y in ["quests", "cmds", "narration", "events"]:
	if (y in ["cmds", "narration", "events"]):
		INS[y] = {}
	else:
		INS[y] = []
	
	if (os.path.isdir(local + "/" + y)):
		#print("Running " + y + " directory for " + x[-2])
		if (os.path.isdir(local + "/" + y)):
			for i in os.listdir(local + "/" + y):
				#print(y + "...")
				if (i != "__pycache__"):
					z = importlib.import_module(imp + "." + y + "." + i.split(".")[0])
					if (y not in ["cmds", "narration", "events"]):
						INS[y] += z.MANIFEST
					else:
						INS[y] = array_merge(INS[y], z.MANIFEST)	#	 Was +=
				
			#y = importlib.import_module(imp + "." + y)
	#else:
		#print("No " + y + " directory found for " + x[-2])
