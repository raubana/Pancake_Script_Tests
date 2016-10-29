from PC_Class import *


class PC_Boolean(PC_Class):
	TYPE = "BOOLEAN"

	def __nonzero__(self):
		return self.value