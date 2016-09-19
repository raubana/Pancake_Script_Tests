from op import *


class Op_Addition(Op):
	SYMBOL = "+"
	PRECEDENCE = 5
	@staticmethod
	def perform_op(operand1, operand2, interpreter):
		try:return interpreter.get_as_value(operand1) + interpreter.get_as_value(operand2)
		except Exception as e: interpreter.runtime_error(e)


class Op_Subtraction(Op):
	SYMBOL = "-"
	PRECEDENCE = 5
	@staticmethod
	def perform_op(operand1, operand2, interpreter):
		try:return interpreter.get_as_value(operand1) - interpreter.get_as_value(operand2)
		except Exception as e: interpreter.runtime_error(e)


class Op_Multiplication(Op):
	SYMBOL = "*"
	PRECEDENCE = 4
	@staticmethod
	def perform_op(operand1, operand2, interpreter):
		try:return interpreter.get_as_value(operand1) * interpreter.get_as_value(operand2)
		except Exception as e: interpreter.runtime_error(e)


class Op_Division(Op):
	SYMBOL = "/"
	PRECEDENCE = 4
	@staticmethod
	def perform_op(operand1, operand2, interpreter):
		try:return interpreter.get_as_value(operand1) / interpreter.get_as_value(operand2)
		except Exception as e: interpreter.runtime_error(e)


class Op_Modulus(Op):
	SYMBOL = "%"
	PRECEDENCE = 4
	@staticmethod
	def perform_op(operand1, operand2, interpreter):
		try:return interpreter.get_as_value(operand1) % interpreter.get_as_value(operand2)
		except Exception as e: interpreter.runtime_error(e)


class Op_Power(Op):
	SYMBOL = "^"
	PRECEDENCE = 3
	@staticmethod
	def perform_op(operand1, operand2, interpreter):
		try:return interpreter.get_as_value(operand1) ** interpreter.get_as_value(operand2)
		except Exception as e: interpreter.runtime_error(e)


class Op_Negate(Op):
	SYMBOL = "-"
	PRECEDENCE = 2
	ASSOCIATIVITY = RIGHT_TO_LEFT
	NUM_OPERANDS = 1
	@staticmethod
	def perform_op(operand1, operand2, interpreter):
		try:return -interpreter.get_as_value(operand1)
		except Exception as e: interpreter.runtime_error(e)