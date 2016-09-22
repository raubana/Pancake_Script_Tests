"""
The purpose of the Op2Fnc is to turn operators into a PC code friendly version.
"""

from tokenizer import Token
from constants import *
from common import find_endblock_token_index, find_startblock_token_index, increment_gotos_pointing_after_here
from error_format import error_format


class Op2Fnc(object):
	@staticmethod
	def process(tokenlist):
		i = 0
		while i < len(tokenlist.tokens):
			token = tokenlist.tokens[i]
			t = token.type

			if t == TYPE_OPERATOR:
				num_operands = token.value.num_operands
				function = token.value.function
				if function == "assign":
					token.type = TYPE_ASSIGN
					token.value = "="
				else:
					tokenlist.tokens.insert(i, Token(TYPE_NUMBER, num_operands, None, None))
					i += 1

					token.type = TYPE_FUNCTION
					token.value = token.value.symbol

			i += 1




def process(tokenlist):
	Op2Fnc.process(tokenlist)