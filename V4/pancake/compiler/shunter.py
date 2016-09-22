"""
The purpose of the shunter is to perform the shunting-yard algorithm on the list of tokens. This will rearrange
processes so that infix notation becomes reveres polish notation, which is easier to process by an interpreter.
"""

from constants import *
from common import find_endblock_token_index


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
			v = token.value
			if t in LITERAL_TYPES or t == TYPE_TERM:
				output.append(token)
			elif token.type == TYPE_FUNCTION:
				stack.append(token)
			elif t == TYPE_SEPARATOR:
				while len(stack) > 0 and stack[-1].type != TYPE_SEPARATOR:
					output.append(stack.pop())
			elif token.type == TYPE_OPERATOR:
				while True:
					if len(stack) > 0:
						token2 = stack[-1]
						t2 = token2.type
						v2 = token2.value
						if t2 == TYPE_OPERATOR:
							ass = v.associativity
							pres = v2.precedence - v.precedence
							if ((ass == LEFT_TO_RIGHT and pres <= 0) or (ass == RIGHT_TO_LEFT and pres > 0)):
								output.append(stack.pop())
							else:
								break
						else:
							break
					else:
						break

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