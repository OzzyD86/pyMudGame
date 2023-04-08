print("Loading dependencies...")

import importlib, sys, random


import mud, core.mapper
import core.tickableObject
import tickers.doNPCtick
import json
import core.gEngine

from core.gEngine import array_merge

print("Done.")

muds = {}
cmds = {}

class Hello(core.tickableObject.tickableObject):
	def runTick(self):
		self.out += "This is a tickable object. "
	
def countTiles(gEngine):
	return "There are " + str(len(gEngine.mapp.tiles)) + " tiles on this map. "

print("Loading MORE dependencies...")
	
for i in ["cmds.opts", "cmds.make"]:
	x = importlib.import_module(i)
	#y = i.split(".")
	#x = __import__(i)
	#if (len(y) > 1):
	
	#print("Loading " + str(i))
	if hasattr(x, "muds"):
		#print("Muds")
		muds = array_merge(muds, x.muds)
	if hasattr(x, "cmds"):
		#print("Cmds")
		cmds = array_merge(cmds, x.cmds)

print("Done.")

def doTime(time = 0):
	out = ""
	if (time >= 60):
		h = time // 60
		out += str(h) + "h, "

	m = time % 60
	out += str(m) + "m"
	return out
	
#e = mud.mud()
print("Setting up gEngine...")
ge = core.gEngine.gEngine()
ge.partLoad("mapp", core.mapper.mapper())
ge.partLoad("mud", mud.mud())
#ge.load("test.json")
ge.tickOps.append(Hello)
#ge.tickOps.append(tickers.doNPCtick.doNPCTick)
ge.cmds = cmds
ge.muds = muds
print("Done.")

#ge.partLoad("mud", e)

random.seed(1)
transcript = ""

ge.coreRun()