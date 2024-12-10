#print("Do I run and what of it?")
import importlib, os
#print(__file__)

from core.gEngine import array_merge

x = __file__.split("\\")
imp = ".".join(x[-3:-1])
print("Shall we import achievements?")
#try:
z = importlib.import_module(imp + ".achievements")
#except:
#print("Could not")
#print(imp)
INS = { "quests" : [],  }
INS['achievements'] = z.MANIFEST

local = "/".join(__file__.split("\\")[:-1])

for y in ["quests", "cmds", "narration", "partials"]:
	if (y in ["cmds", "narration", "partials"]):
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
					if (hasattr(z, "MANIFEST")):
						if (y not in ["cmds", "narration", "partials"]):
							INS[y] += z.MANIFEST
						else:
							INS[y] = array_merge(INS[y], z.MANIFEST)	#	 Was +=
					#print(z.MANIFEST)
					
					#print(INS[y])
				
			#y = importlib.import_module(imp + "." + y)
	#else:
		#print("No " + y + " directory found for " + x[-2])

#print(INS['partials'])
#exit(1)