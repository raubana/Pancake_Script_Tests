from constants import *
import ops


def find_endblock_token_index(L, start_index, offset=0):
	layer = offset
	for x in xrange(start_index, len(L)):
		token = L[x]
		t = token.type
		if t == TYPE_BLOCK_END:
			layer -= 1
			if layer == 0:
				return x
		elif t == TYPE_BLOCK_START:
			layer += 1
	return None  # ???


def find_startblock_token_index(L, start_index, offset=0):
	layer = offset
	x = start_index
	while x >= 0:
		token = L[x]
		t = token.type
		if t == TYPE_BLOCK_START:
			layer -= 1
			if layer == 0:
				return x
		elif t == TYPE_BLOCK_END:
			layer += 1
		x -= 1
	return None  # ???


def increment_gotos_pointing_after_here(tokenlist, index):
	for token in tokenlist.tokens:
		if token.type in (TYPE_GOTO,TYPE_GOSUB) and type(token.value) is int and token.value > index:
			token.value += 1


def decrement_gotos_pointing_after_here(tokenlist, index):
	for token in tokenlist.tokens:
		if token.type in (TYPE_GOTO,TYPE_GOSUB) and type(token.value) is int and token.value > index:
			token.value -= 1