class quest():
	def __init__(self, gEngine, opts):
		# This will be called at the beginning ... I mean ... obviously!
		self.internal_state = None
		self.engine = gEngine
		self.opts = opts
		# Glad we got that out of the way!
		
		# Depending on how the command is set up with depend on whether this changes. For now, expect the following:
		# NPC QUEST [%NUMBER%] [ACTION], or NPC QUEST [ACTION] when one NPC within hailable distance
		# Number refers to which NPC of a list is being referred to
		
		# I'm not imagining that this will need to be altered when complete?
		
		self.state(opts)
		
	def state(self, opts):
		self.last_state = False
		# Basically, once the system has started, this will be the way we interact with the class from the top, but for now
		print(opts)
		if (len(opts) > 3 and opts[3] in ["ACCEPT", "DECLINE", "COMPLETE"]):
			action = opts[3]
		elif (len(opts) > 2 and opts[2] in ["ACCEPT", "DECLINE", "COMPLETE"]):
			action = opts[2]
		else:
			action = "INIT"
		
		if (self.internal_state == "FAILED"):
			return self
			
		if (action == "ACCEPT"):
			if (self._accept()):
				self.internal_state = "ACCEPTED"
				self.last_state = True
				#self.engine.registerEvent(self.engine.data['piq'], None, self)
		elif (action == "DECLINE"):
			if (self._decline()):
				self.internal_state = "DECLINED"
				self.last_state = True
				#self.engine.deregisterEvent(self.engine.data['piq'], None, self)
		elif (action == "COMPLETE"):
			if (self._complete()):
				self.internal_state = "COMPLETED"
				self.last_state = True
				#self.engine.deregisterEvent(self.engine.data['piq'], None, self)
		else:
			if (self._begin()):
				self.last_state = True
				self.internal_state = "INITIALISED"

		return self
		
	def _criteria_met(self):
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
		
	def explain(self):
		return "Please put a 'def explain() in your quest, returning a brief explanation"
	
	def _isAssignable(self):
		return True
		
	def _accept(self):
		if (self.internal_state in ["COMPLETED", "DECLINED"]):
			self.out = "It's no longer important."
			return False
			
		if (self.internal_state == "INITIALISED"):
			self.out = "That's wonderful"
			return True
		else:
			self.out = "Yes yes. I heard you say you're going to do it"
			return False
			
	def _decline(self):
			if (self.internal_state == "DECLINED"):
				self.out = "Begone!"
				return False
				
			self.out = "Oh :("
			return True
		
	def _complete(self):
		# Work out if the criteria for the task have been met
		if (self.internal_state is None):
			self.out = "Hold on! You don't know what I'm asking yet!!"
			return False
			
		if (self.internal_state == "DECLINED"):
			self.out = "No, no. You've had your chance!"
			return False
			
		if (self._criteria_met()):
			self.out = "Wonderful! Here's your reward"
			return True
			# Issue reward, clear quest, clean up
		else:
			self.out = "Hold up! Finish the quest first, please!"
			return False
	
	def _fail(self):
		self.internal_state == "FAILED"
		return True
	
	def describe(self):
		return self.out
	
	def detail(self):
		ret = "No details are defined for this quest.\n\n"
		ret += "To add some, add a 'def detail(self): ... ' function to your quest\n\n"
		ret += "Also, if you haven't done so already, add a 'describe' definition to add a brief description of your quest.\n\nThanks." 
		return ret
		
	def pushTime(self):
		return 0.01