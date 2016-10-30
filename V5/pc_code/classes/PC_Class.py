class PC_Class(object):
	TYPE = "???"

	def __init__(self, value):
		self.value = value
		self.calculate_memory_size()

	def calculate_memory_size(self):
		self.memory_size = 1

	def get_memory_size(self):
		return self.memory_size

	def __str__(self):
		return str(self.value)

	def __repr__(self):
		return "{type}: {size}B: {value}".format(
			type=self.TYPE,
			value=repr(self.value),
			size=self.memory_size,
		)