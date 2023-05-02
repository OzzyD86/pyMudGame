class npcQuest():
	def __init__(self, gEngine, opts):
		self.tPlus = 0
		self.out = ""
		print("Hello!")
	
	def pushTime(self):
		return self.tPlus
		
	def describe(self):
		return self.out

MANIFEST = {
	"muds": {
		"START" : [ "NPC QUEST [QUEST_ACTION]" ]
	},
	"cmds" : {
		"NPC" : npcQuest,
	}
}
