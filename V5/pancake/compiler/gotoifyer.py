"""
The purpose of the gotoifyer is to place TYPE_GOTO tokens into the script where they're needed. TYPE_GOTO tokens are
necessary for if-else chains, while loops, and breaks to work.
"""

from tokenizer import Token
from constants import *
from common import find_endblock_token_index, find_startblock_token_index, increment_gotos_pointing_after_here, decrement_gotos_pointing_after_here
from error_format import error_format


class Gotoifyer(object):
	@staticmethod
	def process(tokenlist):
		#first we go though and remove every pseudo-function's argument-count literal.
		pseudo_functions = (
			"while",
			"if"
		)

		i = 0
		while i < len(tokenlist.tokens):
			token = tokenlist.tokens[i]
			t = token.type
			if t == TYPE_FUNCTION:
				v = token.value
				if v in pseudo_functions:
					tokenlist.tokens.pop(i-1)
					i -= 1
			i += 1

		# then we go through and add all needed goto's.
		i = 0
		while i < len(tokenlist.tokens):
			token = tokenlist.tokens[i]
			t = token.type

			if t == TYPE_FUNCTION:
				v = token.value
				if v == "if":
					# first we must determine that there is in fact a body following this function.
					if i+1 < len(tokenlist.tokens) and tokenlist.tokens[i+1].type == TYPE_BLOCK_START and \
						tokenlist.tokens[i + 1].value == BLOCK_START_CHAR:
						pass
					else:
						error_format(token,"\"if\" should be followed by a block.")

					# only if the body following this if-function has an "else" will this goto be added.
					index = find_endblock_token_index(tokenlist.tokens, i + 2)
					if index + 1 < len(tokenlist.tokens):
						token2 = tokenlist.tokens[index + 1]
						t2 = token2.type
						v2 = token2.value
						if t2 == TYPE_TERM and v2 == "else":
							end_of_chain = find_endblock_token_index(tokenlist.tokens,i)
							if end_of_chain is None:
								end_of_chain = len(tokenlist.tokens)
							tokenlist.tokens.insert(index, Token(TYPE_GOTO,end_of_chain,None,None,0))
							increment_gotos_pointing_after_here(tokenlist,index)

				elif v == "while":
					# first we must determine that there is in fact a body following this function.
					if i + 1 < len(tokenlist.tokens) and tokenlist.tokens[i + 1].type == TYPE_BLOCK_START and \
									tokenlist.tokens[i + 1].value == BLOCK_START_CHAR:
						pass
					else:
						error_format(token, "\"while\" should be followed by a body.")

					# Next we place a goto at the end of that body to point back at this while-function's args.
					index = find_endblock_token_index(tokenlist.tokens, i+1)
					goto = find_startblock_token_index(tokenlist.tokens, i-3)
					tokenlist.tokens.insert(index-1, Token(TYPE_GOTO, goto, None, None,0))
					increment_gotos_pointing_after_here(tokenlist, index)
			i += 1

		# next we go through and remove all of the else tokens that aren't followed by a block.
		# Those that are will be removed also, but that block's start and end will be removed as well.
		i = 0
		while i < len(tokenlist.tokens):
			token = tokenlist.tokens[i]
			t = token.type
			if t == TYPE_TERM:
				v = token.value
				if v == "else":
					tokenlist.tokens.pop(i)
					decrement_gotos_pointing_after_here(tokenlist, i)
					i -= 1
					if i + 1 < len(tokenlist.tokens) and tokenlist.tokens[i+1].type == TYPE_BLOCK_START and tokenlist.tokens[i+1].value == BLOCK_START_CHAR:
						tokenlist.tokens.pop(i+1)
						decrement_gotos_pointing_after_here(tokenlist, i+1)
						i -= 1
						end_index = find_endblock_token_index(tokenlist.tokens, i + 2)
						tokenlist.tokens.pop(end_index)
						decrement_gotos_pointing_after_here(tokenlist, end_index)
						i -= 1
			i += 1

		# lastly we go through and remove all of the pseudo-functions.
		i = 0
		while i < len(tokenlist.tokens):
			token = tokenlist.tokens[i]
			t = token.type
			if t == TYPE_FUNCTION:
				v = token.value
				if v in pseudo_functions:
					tokenlist.tokens.pop(i)
					decrement_gotos_pointing_after_here(tokenlist, i)
					i -= 1
			i += 1




def process(tokenlist):
	Gotoifyer.process(tokenlist)