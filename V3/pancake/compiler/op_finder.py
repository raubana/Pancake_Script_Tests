"""
The purpose of the op finder is to go through each token and find tokens of type TYPE_OTHER and attempt to
find a matching operator. If one of that symbol doesn't exist, an error is raised.
"""


from .. ops import OPERATORS
from .. constants import *
from .. error_format import error_format

class Op_Finder(object):
	@staticmethod
	def process(tokenlist, skip_unmatched):
		for token in tokenlist.tokens:
			if token.type == TYPE_OTHER:
				matched = False
				for op in OPERATORS:
					if op.SYMBOL == token.value:
						matched = True
						break
				if matched:
					token.type = TYPE_OPERATOR
				else:
					if not skip_unmatched:
						token.type = TYPE_NULL
						error_format(token,"{op} is not a recognized operator.".format(op=token.value))



def process(tokenlist, skip_unmatched = False):
	Op_Finder.process(tokenlist, skip_unmatched)

