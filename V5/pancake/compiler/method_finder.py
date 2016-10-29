"""
The purpose of the MethodFinder is to find method calls (".") and to setup tokens to work with methods.
"""

from tokenizer import Token
from constants import *
from common import find_endblock_token_index, find_startblock_token_index, increment_gotos_pointing_after_here
from error_format import error_format


class MethodFinder(object):
	@staticmethod
	def process(tokenlist):
		i = 0
		while i < len(tokenlist.tokens):
			token = tokenlist.tokens[i]
			if token.type == TYPE_OPERATOR:
				if token.value.function == ".":
					#There should be a method following this.
					func_token = None
					if i+1 < len(tokenlist.tokens):
						func_token = tokenlist.tokens[i+1]
					if func_token is not None and func_token.type == TYPE_FUNCTION:
						tokenlist.tokens.pop(i)
						i -= 1
						func_token.value = "."+func_token.value
					else:
						error_format(token, "Expected a method name to follow the '.' symbol.")

			i += 1




def process(tokenlist):
	MethodFinder.process(tokenlist)