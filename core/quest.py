class quest():
	def __init__(self, gEngine, opts):
		# This will be called at the beginning ... I mean ... obviously!
		self.engine = gEnigne
		self.opts = opts
		# Glad we got that out of the way!
		
		# Depending on how the command is set up with depend on whether this changes. For now, expect the following:
		# NPC QUEST [%NUMBER%] [ACTION], or NPC QUEST [ACTION] when one NPC within hailable distance
		# Number refers to which NPC of a list is being referred to
		
		# I'm not imagining that this will need to be altered when complete?
		
		if (len(opts) > 3):
			if (opts[3] in ["ACCEPT", "DECLINE", "COMPLETE"]):
				action = opts[3]
		elif (len(opts) > 2):
			if (opts[2] in ["ACCEPT", "DECLINE", "COMPLETE"]):
				action = opts[2]
		else:
			action = "INIT"
		
		if (action == "ACCEPT"):
			self._accept()
		elif (action == "DECLINE"):
			self._decline()
		elif (action == "COMPLETE"):
			self._complete()
		else:
			self._begin()
		
	def _citeria_met(self):
		return False
		
	def _begin(self):
		# Check if the NPC has a quest. This may include finding one
		quest = False
		active = False
		if (quest):
			if (active):
				self.out = "How's the quest going?"
				if (self._criterial_met()):
					self.out += " Are you any further forward?"
			else:
				self.out = "Ah. Just the person I wanted to see. Can you do something for me?"
		else:
			self.out = "Sorry. I have no errands for you at the moment"
		pass
		
	def questTick(self):
		# This quest tick does nothing
		return ""
		
	def _accept(self):
		active = False
		if (active == False):
			self.out = "That's wonderful"
			active = True
		else:
			self.out = "Yes yes. I heard you say you're going to do it"
	
	def _decline(self):
		pass
		
	def _complete(self):
		# Work out if the criteria for the task have been met
		if (self._criteria_met()):
			self.out = "Wonderful! Here's your reward"
			# Issue reward, clear quest, clean up
		else:
			self.out = "Hold up! Finish the quest first, please!"
	
	def describe(self):
		return self.out
	
	def pushTime(self):
		return 0.01