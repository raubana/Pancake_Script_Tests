from PC_Class import PC_Class
from PC_Exception import PC_Exception
from PC_Boolean import PC_Boolean


class PC_Number(PC_Class):
	TYPE = "NUMBER"

	def calculate_memory_size(self):
		self.memory_size = 4

	def __add__(self, other):
		try: return PC_Number(self.value + other.value)
		except: return PC_Exception("ADD_FAILED")

	def __sub__(self, other):
		try: return PC_Number(self.value - other.value)
		except: return PC_Exception("SUB_FAILED")

	def __mul__(self, other):
		try: return PC_Number(self.value * other.value)
		except: return PC_Exception("MUL_FAILED")

	def __div__(self, other):
		try: return PC_Number(self.value / other.value)
		except: return PC_Exception("DIV_FAILED")

	def __mod__(self, other):
		try: return PC_Number(self.value % other.value)
		except: return PC_Exception("MOD_FAILED")

	def __pow__(self, other):
		try: return PC_Number(self.value ** other.value)
		except: return PC_Exception("POW_FAILED")

	def __neg__(self):
		try: return PC_Number(-self.value)
		except: return PC_Exception("NEG_FAILED")

	def __nonzero__(self):
		return self.value != 0

	def __lt__(self, other):
		try: return PC_Boolean(self.value < other.value)
		except: return PC_Exception("LT_FAILED")

	def __le__(self, other):
		try: return PC_Boolean(self.value <= other.value)
		except: return PC_Exception("LE_FAILED")

	def __eq__(self, other):
		try: return PC_Boolean(self.value == other.value)
		except: return PC_Exception("EQ_FAILED")

	def __ne__(self, other):
		try: return PC_Boolean(self.value != other.value)
		except: return PC_Exception("NE_FAILED")

	def __gt__(self, other):
		try: return PC_Boolean(self.value > other.value)
		except: return PC_Exception("GT_FAILED")

	def __ge__(self, other):
		try: return PC_Boolean(self.value >= other.value)
		except: return PC_Exception("GE_FAILED")