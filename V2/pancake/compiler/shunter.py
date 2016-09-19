"""
The purpose of the shunter is to perform the shunting-yard algorithm on the list of tokens. This will rearrange
processes so that infix notation becomes reveres polish notation, which is easier to process by an interpreter.
"""

from .. constants import *
from .. common import find_endblock_token_index, find_op_by_symbol


class Shunter(object):
	@staticmethod
	def process(tokenlist):
		tokenlist.tokens = Shunter._process(tokenlist.tokens)

	@staticmethod
	def _process(L):
		stack = []
		output = []

		i = 0
		while i < len(L):
			token = L[i]
			t = token.type
			if t in (TYPE_NUMBER,TYPE_TERM,TYPE_STRING):
				output.append(token)
			elif t == TYPE_FUNCTION:
				stack.append(token)
			elif t == TYPE_SEPARATOR:
				while len(stack) > 0 and stack[-1].type != TYPE_SEPARATOR:
					output.append(stack.pop())
			elif t == TYPE_OPERATOR:
				op1 = find_op_by_symbol(token.value)
				while len(stack) > 0 and stack[-1].type == TYPE_OPERATOR:
					op2 = find_op_by_symbol(stack[-1].value)
					pres = op2.PRECEDENCE - op1.PRECEDENCE
					if not ((pres <= 0 and op1.ASSOCIATIVITY == LEFT_TO_RIGHT) or
							(pres > 0 and op1.ASSOCIATIVITY == RIGHT_TO_LEFT)):
						break
					output.append(stack.pop())
				stack.append(token)
			elif t == TYPE_BLOCK_START:
				#we need to get the index of the end of this block
				end_index = find_endblock_token_index(L,i+1)
				result = Shunter._process(L[i+1:end_index])
				output.append(token)
				output += result
				output.append(L[end_index])
				i = end_index
				if token.value == TUPLE_START_CHAR and len(stack) > 0 and stack[-1].type == TYPE_FUNCTION:
					output.append(stack.pop())
			else:
				print 'uh oh...', token
			i += 1

		while len(stack) > 0:
			output.append(stack.pop())

		return output


def process(tokenlist):
	Shunter.process(tokenlist)