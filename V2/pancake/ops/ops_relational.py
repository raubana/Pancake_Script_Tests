from op import *


class Op_Relational(Op):
	PRECEDENCE = 6


class Op_GreaterThan(Op_Relational):
	SYMBOL = ">"
	@staticmethod
	def perform_op(operand1, operand2, interpreter):
		try:return interpreter.get_as_value(operand1) > interpreter.get_as_value(operand2)
		except Exception as e: interpreter.runtime_error(e)


class Op_GreaterThanEqualTo(Op_Relational):
	SYMBOL = ">="
	@staticmethod
	def perform_op(operand1, operand2, interpreter):
		try:return interpreter.get_as_value(operand1) >= interpreter.get_as_value(operand2)
		except Exception as e: interpreter.runtime_error(e)


class Op_LessThan(Op_Relational):
	SYMBOL = "<"
	@staticmethod
	def perform_op(operand1, operand2, interpreter):
		try:return interpreter.get_as_value(operand1) < interpreter.get_as_value(operand2)
		except Exception as e: interpreter.runtime_error(e)


class Op_LessThanEqualTo(Op_Relational):
	SYMBOL = "<="
	@staticmethod
	def perform_op(operand1, operand2, interpreter):
		try:return interpreter.get_as_value(operand1) <= interpreter.get_as_value(operand2)
		except Exception as e: interpreter.runtime_error(e)