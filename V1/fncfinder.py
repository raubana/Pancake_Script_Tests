"""
The purpose of the second tokenizer is to take the blocks of code from the blocker and find which tokens are meant to be
functions and operators.
"""

from error_format import error_format
from operators import *


class FncFinder(object):
	def __init__(self, tokens):
		self._refine(tokens)

	def _refine(self, tokens):
		#We look for functions (or more accurately, for terms being "called").
		for token in tokens:
			if token.type == "block":
				self._refine(token.tokens)
		for x in xrange(len(tokens)-1):
			token1 = tokens[x]
			token2 = tokens[x+1]
			if token1.type == "term" and token2.type == "block":
				if token2.enclosed_type is not None and token2.enclosed_type[0] == "(":
					token1.type = "function"

