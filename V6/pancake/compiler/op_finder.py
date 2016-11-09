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
	def find_matching_op(symbol, num_operands=None):
		for op in OPERATORS:
			if op.symbol == symbol and (num_operands == None or op.num_operands == num_operands):
				return op

	@staticmethod
	def process(tokenlist, skip_unmatched):
		#First thing we do is break up grouped ops.
		i = 0
		while i < len(tokenlist.tokens):
			token = tokenlist.tokens[i]
			if token.type == TYPE_OTHER:
				match = Op_Finder.find_matching_op(token.value)
				if not match and len(token.value) >= 2:
					tokenlist.tokens.insert(i + 1, Token(TYPE_OTHER, token.value[1:], token.line_number, token.char_number + 1, token.length-1))
					token.value = token.value[0]
					token.length = 1
			i += 1

		# Then we parse all of the ops.
		i = 0
		while i < len(tokenlist.tokens):
			token = tokenlist.tokens[i]
			if token.type == TYPE_OTHER:
				to_left = None
				to_right = None

				if i-1 >= 0:
					to_left = tokenlist.tokens[i-1]
				if i+1 < len(tokenlist.tokens):
					to_right = tokenlist.tokens[i+1]

				num_operands = 0

				if to_left and to_left.type in LITERAL_TYPES+(TYPE_TERM, TYPE_BLOCK_END):
					num_operands += 1

				if to_right and to_right.type in LITERAL_TYPES+(TYPE_TERM, TYPE_BLOCK_START, TYPE_FUNCTION):
					num_operands += 1

				match = Op_Finder.find_matching_op(token.value, num_operands)

				if not match:
					match = Op_Finder.find_matching_op(token.value)

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

