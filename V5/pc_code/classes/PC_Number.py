from PC_Class import *
from PC_Boolean import *


class PC_Number(PC_Class):
	TYPE = "NUMBER"

	def calculate_memory_size(self):
		self.memory_size = 4

	def __add__(self, other):
		return PC_Number(self.value + other.value)

	def __sub__(self, other):
		return PC_Number(self.value - other.value)

	def __mul__(self, other):
		return PC_Number(self.value * other.value)

	def __div__(self, other):
		return PC_Number(self.value / other.value)

	def __mod__(self, other):
		return PC_Number(self.value % other.value)

	def __neg__(self):
		return PC_Number(-self.value)

	def __nonzero__(self):
		return PC_Boolean(self.value > 0)

	def __lt__(self, other):
		return PC_Boolean(self.value < other.value)

	def __le__(self, other):
		return PC_Boolean(self.value <= other.value)

	def __eq__(self, other):
		return PC_Boolean(self.value == other.value)

	def __ne__(self, other):
		return PC_Boolean(self.value != other.value)

	def __gt__(self, other):
		return PC_Boolean(self.value > other.value)

	def __ge__(self, other):
		return PC_Boolean(self.value != other.value)