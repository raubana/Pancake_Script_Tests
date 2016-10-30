from PC_Class import *


class PC_Array(PC_Class):
	TYPE = "ARRAY"

	def __init__(self, value=None):
		if value is None:
			super(PC_Array, self).__init__(list())
		else:
			super(PC_Array, self).__init__(value)

	def calculate_memory_size(self):
		self.memory_size = 1 + 4 + 1 * len(self.value)
		for val in self.value:
			self.memory_size += val.get_memory_size()

	def __str__(self):
		output = "["
		for i in xrange(len(self.value)):
			output += str(self.value[i])
			if i < len(self.value) - 1:
				output += ", "
		output += "]"
		return output

	def __repr__(self):
		output = ""
		i = 0
		for val in self.value:
			lines = repr(val).split("\n")
			first = True
			for line in lines:
				if first:
					first = False
					output += "\t" + str(i) + ": " + line + "\n"
				else:
					output += "\t" + (" "*len(str(i)+": ")) + line + "\n"
			i += 1
		if output:
			output = output[:-1]
		return "{type}: {size}B:\n{value}".format(
			type=self.TYPE,
			value=output,
			size=self.memory_size,
		)