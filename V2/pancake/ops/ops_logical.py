from op import *


class Op_And(Op):
	SYMBOL = "&"
	PRECEDENCE = 8
	@staticmethod
	def perform_op(operand1, operand2, interpreter):
		try:return interpreter.get_as_value(operand1) and interpreter.get_as_value(operand2)
		except Exception as e: interpreter.runtime_error(e)


class Op_Or(Op):
	SYMBOL = "|"
	PRECEDENCE = 9
	@staticmethod
	def perform_op(operand1, operand2, interpreter):
		try:return interpreter.get_as_value(operand1) or interpreter.get_as_value(operand2)
		except Exception as e: interpreter.runtime_error(e)


class Op_Not(Op):
	SYMBOL = "!"
	PRECEDENCE = 2
	ASSOCIATIVITY = RIGHT_TO_LEFT
	NUM_OPERANDS = 1
	@staticmethod
	def perform_op(operand1, operand2, interpreter):
		try:return not interpreter.get_as_value(operand1)
		except Exception as e: interpreter.runtime_error(e)