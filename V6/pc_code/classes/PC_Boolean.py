from PC_Class import PC_Class


class PC_Boolean(PC_Class):
	TYPE = "BOOLEAN"

	def __nonzero__(self):
		return self.value