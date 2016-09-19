from op import *


class Op_Equality(Op):
	PRECEDENCE = 7


class Op_EqualTo(Op_Equality):
	SYMBOL = "=="
	@staticmethod
	def perform_op(operand1, operand2, interpreter):
		try: return interpreter.get_as_value(operand1) == interpreter.get_as_value(operand2)
		except Exception as e: interpreter.runtime_error(e)


class Op_NotEqualTo(Op_Equality):
	SYMBOL = "!="
	@staticmethod
	def perform_op(operand1, operand2, interpreter):
		try:return interpreter.get_as_value(operand1) != interpreter.get_as_value(operand2)
		except Exception as e: interpreter.runtime_error(e)