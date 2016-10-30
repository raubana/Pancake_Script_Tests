"""
The purpose of the gotoifyer is to place TYPE_GOTO tokens into the script where they're needed. TYPE_GOTO tokens are
necessary for if-else chains, while loops, and breaks to work.
"""

from tokenizer import Token
from constants import *
from common import find_endblock_token_index, find_startblock_token_index, increment_gotos_pointing_after_here, decrement_gotos_pointing_after_here
from error_format import error_format


class SubroutineFinder(object):
	@staticmethod
	def process(tokenlist):
		# First we find all instances of the "sub" term and replace them and their name with a TYPE_SUBROUTINE.
		# We also do something similar to the "call" term.
		i = 0
		while i < len(tokenlist.tokens):
			token = tokenlist.tokens[i]
			t = token.type
			v = token.value

			if t == TYPE_TERM :
				if v == "sub":
					# we look for a term following this.
					subname_token = None
					if i+1 < len(tokenlist.tokens):
						subname_token = tokenlist.tokens[i+1]
					if subname_token is None or subname_token.type != TYPE_TERM:
						error_format(token, "Sub is expected to be followed by the name of the subroutine.")

					# We remove the sub token.
					tokenlist.tokens.pop(i)
					decrement_gotos_pointing_after_here(tokenlist, i)
					i -= 1

					# We then change the type of the second token to TYPE_SUBROUTINE.
					subname_token.type = TYPE_SUBROUTINE

				elif v == "call":
					# we look for a term following this.
					subname_token = None
					if i + 1 < len(tokenlist.tokens):
						subname_token = tokenlist.tokens[i + 1]
					if subname_token is None or subname_token.type != TYPE_TERM:
						error_format(token, "Call is expected to be followed by the name of the subroutine.")

					# We remove the call token.
					tokenlist.tokens.pop(i)
					decrement_gotos_pointing_after_here(tokenlist, i)
					i -= 1

					# We then change the type of the second token to TYPE_GOSUB.
					subname_token.type = TYPE_GOSUB
			i += 1

		# Next we generate a dictionary of locations for the subroutines.
		subroutine_locations = {}
		i = 0
		while i < len(tokenlist.tokens):
			token = tokenlist.tokens[i]
			t = token.type
			v = token.value

			if t == TYPE_SUBROUTINE:
				subroutine_locations[v] = i+2
			i += 1

		# Finally we go through and change all of the TYPE_GOSUB values to their appropriate locations.
		i = 0
		while i < len(tokenlist.tokens):
			token = tokenlist.tokens[i]

			if token.type == TYPE_GOSUB:
				if token.value in subroutine_locations:
					token.value = subroutine_locations[token.value]
				else:
					error_format(token, "Call points to a nonexistant subroutine.")
			i += 1






def process(tokenlist):
	SubroutineFinder.process(tokenlist)