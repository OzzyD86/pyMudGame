#print("Do I run and what of it?")

import os, importlib
from core.gEngine import array_merge
INS = {}

for i in os.listdir("./plugins"):
	if (os.path.isdir("./plugins/" + i)):
		if (i != "__pycache__"):
			j = importlib.import_module("plugins." + i)
			#print(i,j)
			INS = array_merge(INS, j.INS)
			#print(j.INS)
			
