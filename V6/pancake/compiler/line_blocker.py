"""
The purpose of the line blocker is to block off sections of code that are their own line. This prevents the shunter
from reordering sections of code that must remain in a particular order.
"""

from tokenizer import Token
from constants import *


class LineBlocker(object):
	@staticmethod
	def process(tokenlist):
		#STAGE 1 takes care of blocks and seperators.
		start_index_stack = [0]
		level_has_content = [False]
		x = 0
		while x < len(tokenlist.tokens):
			token = tokenlist.tokens[x]
			t = token.type

			if t == TYPE_BLOCK_START:
				start_index_stack.append(x+1)
				level_has_content.append(False)
			elif t == TYPE_BLOCK_END:
				if level_has_content[-1]:
					tokenlist.tokens.insert(start_index_stack[-1], Token(TYPE_BLOCK_START,None,None,None))
					x += 1
					tokenlist.tokens.insert(x, Token(TYPE_BLOCK_END, None, None, None))
					x += 1
				start_index_stack.pop()
				level_has_content.pop()
			elif t == TYPE_SEPARATOR:
				tokenlist.tokens.insert(start_index_stack[-1], Token(TYPE_BLOCK_START, None, None, None))
				x += 1
				tokenlist.tokens.insert(x, Token(TYPE_BLOCK_END, None, None, None))
				x += 1
				start_index_stack[-1] = x + 1
			else:
				level_has_content[-1] = True
			x += 1

		# STAGE 2 takes care of actual lines.
		start_index_stack = [0]
		x = 0
		while x < len(tokenlist.tokens):
			token = tokenlist.tokens[x]
			t = token.type

			if t == TYPE_BLOCK_START:
				start_index_stack.append(x + 1)
			elif t == TYPE_BLOCK_END:
				start_index_stack.pop()
			elif t == TYPE_EOL:
				tokenlist.tokens.insert(start_index_stack[-1], Token(TYPE_BLOCK_START, None, None, None))
				x += 1
				tokenlist.tokens[x] = Token(TYPE_BLOCK_END, None, None, None)
				start_index_stack[-1] = x + 1
			x += 1

		#STAGE 3 removes redundant, empty BLOCK START followed by BLOCK END tokens
		x = 0
		while x < len(tokenlist.tokens):
			token = tokenlist.tokens[x]
			t = token.type
			v = token.value

			if t == TYPE_BLOCK_START and v is None:
				if x + 1 < len(tokenlist.tokens):
					token2 = tokenlist.tokens[x+1]
					t2 = token2.type
					v2 = token2.value
					if t2 == TYPE_BLOCK_END and v2 is None:
						tokenlist.tokens.pop(x)
						tokenlist.tokens.pop(x)
			x += 1


def process(tokenlist):
	LineBlocker.process(tokenlist)