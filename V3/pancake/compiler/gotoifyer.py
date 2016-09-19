"""
The purpose of the gotoifyer is to place TYPE_GOTO tokens into the script where they're needed. TYPE_GOTO tokens are
necessary for if-else chains, while loops, and for breaks to work.
"""

from tokenizer import Token
from .. constants import *
from .. common import find_endblock_token_index, find_startblock_token_index, increment_gotos_pointing_after_here
from .. error_format import error_format


class Gotoifyer(object):
	@staticmethod
	def process(tokenlist):
		i = 0
		while i < len(tokenlist.tokens):
			token = tokenlist.tokens[i]
			t = token.type

			if t == TYPE_CALL:
				token2 = token.value[1]
				t2 = token2.type
				if t2 == TYPE_FUNCTION:
					v2 = token2.value
					if v2 == "if":
						#first we must determine that there is in fact a body following this function.
						if i+1 < len(tokenlist.tokens) and tokenlist.tokens[i+1].type == TYPE_BLOCK_START and \
							tokenlist.tokens[i + 1].value == BLOCK_START_CHAR:
							pass
						else:
							error_format(token,"\"if\" should be followed by a block.")

						#only if the body following this if-function has an "else" will this goto be added.
						index = find_endblock_token_index(tokenlist.tokens, i + 2)
						if index + 1 < len(tokenlist.tokens) and tokenlist.tokens[index + 1].type == TYPE_TERM and \
							tokenlist.tokens[index + 1].value == "else":
							end_of_chain = find_endblock_token_index(tokenlist.tokens,i)
							tokenlist.tokens.insert(index, Token(TYPE_GOTO,end_of_chain,None,None))
							increment_gotos_pointing_after_here(tokenlist,index)
					elif v2 == "while":
						# first we must determine that there is in fact a body following this function.
						if i + 1 < len(tokenlist.tokens) and tokenlist.tokens[i + 1].type == TYPE_BLOCK_START and \
										tokenlist.tokens[i + 1].value == BLOCK_START_CHAR:
							pass
						else:
							error_format(token, "\"while\" should be followed by a body.")

						#Next we place a goto at the end of that body to point back at this while-function's args.
						index = find_endblock_token_index(tokenlist.tokens, i+1)
						goto = find_startblock_token_index(tokenlist.tokens, i-3)
						tokenlist.tokens.insert(index-1, Token(TYPE_GOTO, goto, None, None))
						increment_gotos_pointing_after_here(tokenlist, index)
			i += 1




def process(tokenlist):
	Gotoifyer.process(tokenlist)