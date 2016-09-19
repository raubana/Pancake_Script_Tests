"""
The purpose of the callifyer is to replace operator and function tokens with TYPE_CALL tokens, and to determine how
many parameters each should be expecting to receive.
"""

from tokenizer import Token
from .. constants import *
from .. common import find_endblock_token_index, find_op_by_symbol
from .. error_format import error_format


class Callifyer(object):
	@staticmethod
	def process(tokenlist):
		i = 0
		while i < len(tokenlist.tokens):
			token = tokenlist.tokens[i]
			t = token.type
			v = token.value

			if t == TYPE_FUNCTION:
				# This one is easy - we just count the number of separators in the tuple of arguments that are on the
				# same level as the first argument.
				end_index = find_endblock_token_index(tokenlist.tokens, i+2)
				total_seps = 0
				level = 0
				for j in xrange(i+2,end_index):
					token2 = tokenlist.tokens[j]
					t2 = token2.type
					v2 = token2.value
					if t2 == TYPE_BLOCK_START and v2 == TUPLE_START_CHAR:
						level += 1
					elif t2 == TYPE_BLOCK_END and v2 == TUPLE_END_CHAR:
						level -= 1
					elif t2 == TYPE_SEPARATOR:
						if level == 0:
							total_seps += 1

				new_token = Token(TYPE_CALL, (total_seps+1, token), None, None)
				tokenlist.tokens[i] = new_token

			elif t == TYPE_OPERATOR:
				# This one is a little trickier. Some operators only require one operand, while most require two.
				# TODO: Finish this part so it worksproper.
				left = None
				right = None
				if i-1 >= 0:
					left = tokenlist.tokens[i-1]
				if i+1 < len(tokenlist.tokens):
					right = tokenlist.tokens[i+1]

				print left, right, token

				if right is None:
					error_format(token, "Operator \"{op}\"has no operand to its right.".format(op=v))

				total_operands = 0
				if left is None:
					pass
				elif Callifyer.is_valid_operand_type(left):
					total_operands += 1

				if right is None:
					pass
				elif Callifyer.is_valid_operand_type(right):
					total_operands += 1

				if total_operands == 0:
					error_format(token, "Operators should have at least one operand.")

				op = find_op_by_symbol(v, total_operands)
				if op is not None:
					total_operands = min(total_operands, op.NUM_OPERANDS)
				else:
					error_format(token, "Operator \"{op}\" doesn't exists.".format(op=v))

				new_token = Token(TYPE_CALL, (total_operands, token), None, None)
				tokenlist.tokens[i] = new_token

			i += 1

	@staticmethod
	def is_valid_operand_type(token):
		return token.type in (TYPE_BLOCK_START,TYPE_BLOCK_END,TYPE_TERM,TYPE_NUMBER,TYPE_STRING,TYPE_FUNCTION,TYPE_CALL,TYPE_OPERATOR)



def process(tokenlist):
	Callifyer.process(tokenlist)