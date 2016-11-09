from PC_Class import PC_Class
from PC_Boolean import PC_Boolean


class PC_String(PC_Class):
	TYPE = "STRING"

	def calculate_memory_size(self):
		self.memory_size = 1 + 4 + 1*len(self.value)

	def __add__(self, other):
		return PC_String(self.value+str(other))

	def __nonzero__(self):
		return len(self.value) > 0
