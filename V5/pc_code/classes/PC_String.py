from PC_Class import *
from PC_Boolean import *


class PC_String(PC_Class):
	TYPE = "STRING"

	def calculate_memory_size(self):
		self.memory_size = 1 + 4 + 1*len(self.value)

	def __add__(self, other):
		return PC_String(self.value+str(other))

	def __nonzero__(self):
		return PC_Boolean(len(self.value) > 0)
