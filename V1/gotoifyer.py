"""
The purpose of the gotoifyer is to place "goto" tokens into the compiled script pointing towards parts of the compiled
script that the cursor should go to when that token is reached.
"""


from firsttokenizer import Token
from error_format import error_format

import time


class GoToIfyer(object):
	def __init__(self, block):
		self.input_block = block

		self._current_index = [-1]
		self._goto_list = []

		self._gotoify()

	def _get_token_at(self, location):
		current_token = self.input_block
		for i in location:
			if i < 0 or i >= len(current_token.tokens):
				return None
			current_token = current_token.tokens[i]
		return current_token

	def _get_next_token(self):
		if len(self._current_index) == 0: return None
		self._current_index[-1] = self._current_index[-1] + 1
		token = self._get_token_at(self._current_index)
		if token is None:
			self._current_index.pop()
			token = self._get_next_token()
		elif token.type == "block":
			self._current_index.append(-1)
			token = self._get_next_token()
		return token

	def _gotoify(self):
		while True:
			current_token = self._get_next_token()
			#print "CUR:",self._current_index
			#print "TOK:",current_token
			if current_token is None:
				break
			if current_token.type == "function":
				#we need to get this functions args
				args = self._get_token_at(self._current_index[:-1]+[self._current_index[-1]-1])
				if args is None or args.type != "block" or args.enclosed_type[0] != "(":
					error_format(current_token,"Functions are expected to be followed by a tuple of arguments.")
					# This should never happen because of how functions are recognized by the fact that they're
					# a term-type token followed by a block enclosed in parentheses.

				if current_token.value in ("if","while"):
					#we need to first check that the correct number of args exist.
					if len(args.tokens) != 1:
						error_format(current_token,"\"{fnc}\" should have 1 argument; instead has {num}.".format(fnc=current_token.value,num=len(args.tokens)))
					#we need to find the body that should immediately follow this if function.
					body = self._get_token_at(self._current_index[:-1]+[self._current_index[-1]+1])
					if body is None or body.type != "block" or body.enclosed_type[0] != "{":
						error_format(current_token,"\"{fnc}\" is expected to be followed by a body enclosed in braces (\"{\").".format(fnc=current_token.value,num=len(args.tokens)))
					# By default, the interpreter should just continue to the next line should this function's
					# condition evaluate to true, and will skip the body that follows the function should the
					# condition evaluate to false.

					if current_token.value == "if":
						# We need to also add a "goto" token into the end of this if-function's body telling the interpreter
						# to skip to the end of this if-chain, since an if-chain would be contained within a block of it's own.
						body.append(Token( "goto", self._current_index[:-2]+[self._current_index[-2]+1], None, None))
					elif current_token.value == "while":
						# We need to also add a "goto" token into the end of this while-function's body telling the
						# interpreter go back to the while-function once the body has finished executing.
						body.append(Token( "goto", self._current_index[:-1]+[self._current_index[-1]-1], None, None))