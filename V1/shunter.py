"""
The purpose of the shunter is to take the tokens from the second tokenizer and rearrange them
so that they're in reverse polish notation. This will help speed up the code during runtime.
"""


from error_format import error_format
from blocker import Block
from operators import *





def _sign(x):
	if x > 0: return 1
	if x < 0: return -1
	return 0


def _get_op_precedence(op):
	for x in xrange(len(OPERATOR_PRECEDENCE)):
		op_list = OPERATOR_PRECEDENCE[x]
		if op in op_list:
			return x
	return None #this shouldn't happen.


def _compare_precedence(op1, op2):
	op1_pres = _get_op_precedence(op1)
	op2_pres = _get_op_precedence(op2)
	return _sign(op1_pres-op2_pres)


class Shunter(object):
	def __init__(self, block):
		self.output_block = self._reorganize(block)

	def _reorganize(self, input_block):
		our_tokens = Block()
		our_tokens.enclosed_type = input_block.enclosed_type
		# we need to dump the tokens from the input block into our block.
		for token in input_block.tokens:
			if token.type == "block":
				our_tokens.append(self._reorganize(token))
			else:
				our_tokens.append(token)
		self._do_shunting_yard_algorithm(our_tokens)
		return our_tokens

	def _do_shunting_yard_algorithm(self, block):
		input_tokens = list(block.tokens)
		stack = []
		output = []

		#print "START"
		while len(input_tokens) > 0:
			token = input_tokens.pop(0)
			#print token

			if token.type in ("number","string","term"):
				output.append(token)
			elif token.type == "function":
				stack.append(token)
			elif token.type == "separator":
				while len(stack) > 0 and stack[-1].type != "separator":
					output.append(stack.pop())
			elif token.type == "operator":
				while len(stack) > 0:
					pres = _compare_precedence(token.value,stack[-1].value)
					if not (((token.value not in R_TO_L_ASSOCIATIVE_OPS) and pres <= 0) or
							((token.value in R_TO_L_ASSOCIATIVE_OPS) and pres < 0)):
						break
					output.append(stack.pop())
				stack.append(token)
			#elif token.type == "enclosed": THIS WILL NOT HAPPEN BECAUSE OF BLOCKS.
			elif token.type == "block":# and token.enclosed_type is not None and token.enclosed_type[0] == "(":
				#I don't know what to do here, soooo...
				if token.enclosed_type is not None and token.enclosed_type[0] == "(":
					output.append(token)
					if len(stack) > 0 and stack[-1].type == "function":
						output.append(stack.pop())
				else:
					output.append(token)
			else:
				print "uh oh...", token
				#output.append(token)

			#print stack
			#print output
			#print

		while len(stack) > 0:
			output.append(stack.pop())
		#print "DONE:"
		#print stack
		#print output
		#print
		block.tokens = output


