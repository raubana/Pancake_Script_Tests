"""
The purpose of the op finder is to take the tokens of code from the blocker and find which tokens are meant to be
operators.
"""

from error_format import error_format
from operators import *


class OpFinder(object):
	def __init__(self, tokens):
		self._refine(tokens)

	def _refine(self, tokens):
		# We look for operators
		for token in tokens:
			if token.type == "block":
				self._refine(token.tokens)
			else:
				if token.type == "other":
					if token.value in OPERATORS:
						token.type = "operator"
					else:
						error_format(token, "{value} is not a recognized keyword or operator.".format(value=token.value))

