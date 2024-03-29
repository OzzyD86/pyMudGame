print("Loading dependencies...")

config = {
	"loaders" : [ "cmds.opts", "cmds.make", "cmds.engine", "cmds.npcHail"],
	"core": {
		"npcpt" : 80,
		"fow_size" : 12
	}
}
import mud, core.mapper, core.phraseReplace
import core.tickableObject, tickers.doNPCtick
import sys, random
import json
import core.gEngine
import importlib
import core.quest

from core.gEngine import array_merge

import plugins
#from quests.basic import basicQuest

print(plugins.INS)

print("Done.")

muds = plugins.INS['cmds']['muds']
cmds = plugins.INS['cmds']['cmds']
events = plugins.INS['events']

class Hello(core.tickableObject.tickableObject):
	def runTick(self):
		self.out += "This is a tickable object. "
	
def countTiles(gEngine):
	return "There are " + str(len(gEngine.mapp.tiles)) + " tiles on this map. "

print("Loading MORE dependencies...")
	
for i in config['loaders']:
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
	if hasattr(x, "events"):
		#print("Cmds")
		events = array_merge(events, x.events)

print("Done.")

def doTime(time = 0):
	out = ""
	d = time // 1440
	out += str(d + 1) + "d, "

	#if (time >= 60):
	h = (time // 60) % 24
	out += str(h) + "h, "

	m = time % 60
	out += str(m) + "m"
	return out
	
#e = mud.mud()
print("Setting up gEngine...")
ge = core.gEngine.gEngine()
ge.config = config
ge.partLoad("mapp", core.mapper.mapper())
ge.mapp.passTownNames(plugins.INS['narration'])
ge.partLoad("mud", mud.mud())
ge.new()
#ge.load("test.json")
ge.tickOps.append(Hello)
ge.tickOps.append(tickers.doNPCtick.doNPCTick)
ge.narration = plugins.INS['narration']
ge.cmds = cmds
ge.quests = plugins.INS['quests']
ge.muds = muds # Is this line superfluous? # Update: Nope
ge.cmdExec("INITIALISE")
ge.events = events

#ge.cmdExec('ENGINE GAME LOAD "test"')
print("Done.")

#random.seed(1)
transcript = ""

ge.coreRun()
