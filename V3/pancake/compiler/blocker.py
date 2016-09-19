"""
The purpose of the blocker is to substitute TYPE_ENCLOSED tokens with their appropriate
TYPE_BLOCK_START/TYPE_BLOCK_END pairs. It also checks that every block token is properly paired.
"""

from .. constants import *
from .. error_format import error_format

class Blocker(object):
	@staticmethod
	def process(tokenlist):
		index = 0
		while index < len(tokenlist.tokens):
			token = tokenlist.tokens[index]
			if token.type == TYPE_ENCLOSED:
				i = ENCLOSING_CHARACTERS.index(token.value)
				if i % 2 == 0: # start
					token.type = TYPE_BLOCK_START
				else: # end
					token.type = TYPE_BLOCK_END
			index += 1

		#we need to check that everything is properly paired.
		stack = []
		for token in tokenlist.tokens:
			if token.type == TYPE_BLOCK_START:
				stack.append(token)
			elif token.type == TYPE_BLOCK_END:
				if len(stack) > 0:
					start = stack.pop()
					i = ENCLOSING_CHARACTERS.index(start.value)
					expected_char = ENCLOSING_CHARACTERS[i+1]
					if expected_char != token.value:
						token.type = TYPE_NULL
						error_format(token, "{val} is missing a starting pair.".format(val=token.value))
				else:
					token.type = TYPE_NULL
					error_format(token, "{val} is missing a starting pair.".format(val=token.value))
		if len(stack) > 0:
			stack[0].type = TYPE_NULL
			error_format(stack[0], "{val} is missing an ending pair.".format(val=stack[0].value))


def process(tokenlist):
	return Blocker.process(tokenlist)