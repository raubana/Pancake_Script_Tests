from .. constants import *

class Op(object):
	SYMBOL = None
	PRECEDENCE = 0
	ASSOCIATIVITY = LEFT_TO_RIGHT
	NUM_OPERANDS = 2

	@staticmethod
	def perform_op(operand1, operand2, interpreter):
		pass