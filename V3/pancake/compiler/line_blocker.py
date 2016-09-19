"""
The purpose of the line blocker is to block off sections of code that are their own line. This prevents the shunter
from reordering sections of code that must remain in a particular order.
"""

from tokenizer import Token
from .. constants import *


class LineBlocker(object):
	@staticmethod
	def process(tokenlist):
		start_index_stack = [0]
		x = 0
		while x < len(tokenlist.tokens):
			token = tokenlist.tokens[x]
			t = token.type
			if t == TYPE_EOL or t == TYPE_SEPARATOR:
				tokenlist.tokens.insert(start_index_stack[-1], Token(TYPE_BLOCK_START,None,None,None))
				x += 1
				if t == TYPE_EOL:
					tokenlist.tokens[x] = Token(TYPE_BLOCK_END, None, None, None)
				else:
					tokenlist.tokens.insert(x, Token(TYPE_BLOCK_END, None, None, None))
					x += 1
				start_index_stack[-1] = x + 1
			elif t == TYPE_BLOCK_END:
				start_index_stack.pop()
			elif t == TYPE_BLOCK_START:
				start_index_stack.append( x + 1 )
			x += 1


def process(tokenlist):
	LineBlocker.process(tokenlist)