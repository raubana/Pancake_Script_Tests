from op import *


class Op_Assign(Op):
	SYMBOL = "="
	PRECEDENCE = 10
	@staticmethod
	def perform_op(operand1, operand2, interpreter):
		interpreter.assign(operand1, interpreter.get_as_value(operand2))