"""
The purpose of the Tokenlist2PCCode is to turn operators into a PC code friendly version.
"""

from tokenizer import Token
from constants import *
from common import find_endblock_token_index, find_startblock_token_index, increment_gotos_pointing_after_here
from error_format import error_format


class Tokenlist2PCCode(object):
	@staticmethod
	def generate(tokenlist):
		final_output = ""
		i = 0
		while i < len(tokenlist.tokens):
			token = tokenlist.tokens[i]

			t = token.type
			v = token.value
			output = ""
			if t == TYPE_TERM:
				output = "TRM " + v
			elif t in LITERAL_TYPES:
				if t == TYPE_NUMBER:
					output = "LIT " + str(v)
				elif t == TYPE_STRING:
					output = "LIT \"" + v +"\""
				elif t == TYPE_BOOLEAN:
					output = "LIT "
					if v:
						output += "true"
					else:
						output += "false"
			elif t == TYPE_FUNCTION:
				output = "FNC " + v
			elif t == TYPE_BLOCK_START or t == TYPE_BLOCK_END:
				output = v
			elif t == TYPE_GOTO:
				output = "GO2 " + str(v)
			elif t == TYPE_ASSIGN:
				output = "ASN"
			i += 1

			if i < len(tokenlist.tokens):
				output += "\n"
			final_output += output

		return final_output


def generate(tokenlist):
	return Tokenlist2PCCode.generate(tokenlist)