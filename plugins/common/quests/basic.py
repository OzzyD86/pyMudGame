import core.quest

class basicQuest(core.quest.quest):
	def _begin(self):
		if (self.internal_state == "ACCEPTED"):
			self.out = "You have accepted my quest already"
			return False
		elif (self.internal_state in ["DECLINED", "COMPLETED"]):
			self.out = "It's no longer important."
			return False
		else:
			self.out = "Will you accept my quest?"
			return True
			
MANIFEST = [basicQuest]
