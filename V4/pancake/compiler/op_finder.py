"""
The purpose of the op finder is to go through each token and find tokens of type TYPE_OTHER and attempt to
find a matching operator. If one of that symbol doesn't exist, an error is raised.
"""

import ops
from tokenizer import Token
from constants import *
from error_format import error_format


OPERATORS = ops.OPERATORS

class Op_Finder(object):
	@staticmethod
	def find_matching_op(symbol):
		for op in OPERATORS:
			if op.symbol == symbol:
				return op

	@staticmethod
	def process(tokenlist, skip_unmatched):
		i = 0
		while i < len(tokenlist.tokens):
			token = tokenlist.tokens[i]
			if token.type == TYPE_OTHER:
				match = None
				if len(token.value) > 2:
					pass # We assume that groups of 2 or more op-like characters are too complex to decipher.
				else:
					match = Op_Finder.find_matching_op(token.value)
				if not match and len(token.value) == 2:
					#There's a chance the token is actually two ops without a character between them.
					match = Op_Finder.find_matching_op(token.value[0])
					tokenlist.tokens.insert( i+1, Token(TYPE_OTHER, token.value[1], token.line_number, token.char_number+1) )
					token.value = token.value[0]
				if match:
					token.type = TYPE_OPERATOR
					token.value = match
				else:
					if not skip_unmatched:
						token.type = TYPE_NULL
						error_format(token,"{op} is not a recognized operator.".format(op=token.value))
			i += 1



def process(tokenlist, skip_unmatched = False):
	Op_Finder.process(tokenlist, skip_unmatched)

