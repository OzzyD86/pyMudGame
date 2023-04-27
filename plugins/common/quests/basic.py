import core.quest

class basicQuest(core.quest.quest):
	def _begin(self):
		self.out = "Will you accept my quest?"
	
MANIFEST = [basicQuest]