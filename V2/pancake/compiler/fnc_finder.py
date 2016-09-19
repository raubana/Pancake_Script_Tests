"""
The purpose of the FncFinder is to search for terms that are immediately followed by a tuple. This is an indication that
that term token is being called, so it will have it's type changed to TYPE_FUNCTION.
"""

from .. constants import *

class FncFinder(object):
	@staticmethod
	def process(tokenlist):
		x = 0
		while x < len(tokenlist.tokens) - 1:
			token1 = tokenlist.tokens[x]
			token2 = tokenlist.tokens[x+1]
			if token1.type == TYPE_TERM and token2.type == TYPE_BLOCK_START and token2.value == TUPLE_START_CHAR:
				token1.type = TYPE_FUNCTION
			x += 1


def process(tokenlist):
	FncFinder.process(tokenlist)