from constants import *
from ops import OPERATORS

def find_endblock_token_index(L, start_index):
	layer = 0
	for x in xrange(start_index, len(L)):
		token = L[x]
		t = token.type
		if t == TYPE_BLOCK_END:
			if layer == 0:
				return x
			else:
				layer -= 1
		elif t == TYPE_BLOCK_START:
			layer += 1
	return None  # ???

def find_startblock_token_index(L, start_index):
	layer = 0
	for x in xrange(start_index, 0, -1):
		token = L[x]
		t = token.type
		if t == TYPE_BLOCK_START:
			if layer == 0:
				return x
			else:
				layer -= 1
		elif t == TYPE_BLOCK_END:
			layer += 1
	return None  # ???


def find_op_by_symbol(symbol, num_args=2):
	for op in OPERATORS:
		if op.SYMBOL == symbol and op.NUM_OPERANDS == num_args:
			return op


def increment_gotos_pointing_after_here(tokenlist, index):
	for token in tokenlist.tokens:
		if token.type == TYPE_GOTO and token.value > index:
			token.value += 1


def decrement_gotos_pointing_after_here(tokenlist, index):
	for token in tokenlist.tokens:
		if token.type == TYPE_GOTO and token.value > index:
			token.value -= 1