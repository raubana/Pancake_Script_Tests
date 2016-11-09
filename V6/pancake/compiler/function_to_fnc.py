"""
The purpose of the Function2Fnc is to add argument-count literals before each function.
"""

from tokenizer import Token
from constants import *
from common import find_endblock_token_index, find_startblock_token_index, increment_gotos_pointing_after_here
from error_format import error_format


def _count_args(L, start_index, end_index):
	arg_count = 0
	layer = 0
	found_arg = False
	for x in xrange(start_index+1, end_index):
		token = L[x]
		t = token.type
		if t == TYPE_BLOCK_END:
			layer -= 1
			if found_arg and layer == 0:
				found_arg = False
				arg_count += 1
		elif t == TYPE_BLOCK_START:
			layer += 1
		else:
			found_arg = True
	return arg_count


class Function2Fnc(object):
	@staticmethod
	def process(tokenlist):
		i = 0
		while i < len(tokenlist.tokens):
			token = tokenlist.tokens[i]
			t = token.type
			v = token.value

			if t == TYPE_FUNCTION:
				start_location = find_startblock_token_index(tokenlist.tokens, i-1)
				arg_count = _count_args(tokenlist.tokens, start_location, i)
				#print i, start_location, end_location, arg_count
				tokenlist.tokens.insert(i, Token(TYPE_NUMBER, str(arg_count), None, None))

				i += 1
				if v == "elseif":
					tokenlist.tokens.insert(start_location, Token(TYPE_TERM, "else", None, None))
					i += 1
					token.value = "if"
			i += 1


def process(tokenlist):
	Function2Fnc.process(tokenlist)