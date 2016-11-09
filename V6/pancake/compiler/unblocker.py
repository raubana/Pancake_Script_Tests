"""
The purpose of the unblocker is to remove all block types so that the compiled code is as short at possible.
"""

from constants import *
from common import decrement_gotos_pointing_after_here

class UnBlocker(object):
	@staticmethod
	def process(tokenlist):
		i = len(tokenlist.tokens)-1
		while i >= 0:
			token = tokenlist.tokens[i]
			t = token.type
			v = token.value
			if t in (TYPE_BLOCK_START,TYPE_BLOCK_END) and v not in (BLOCK_START_CHAR, BLOCK_END_CHAR):
				tokenlist.tokens.pop(i)
				decrement_gotos_pointing_after_here(tokenlist,i)
			i -= 1


def process(tokenlist):
	UnBlocker.process(tokenlist)