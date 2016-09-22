import tokenizer
import blocker
import fnc_finder
import op_finder
import line_blocker

import shunter
import function_to_fnc
import op_to_fnc
import gotoifyer
import unblocker

import tokenlist_to_pccode


def compile(script):
	# TOKENIZE PHASE
	tokenlist = tokenizer.tokenize(script)
	blocker.process(tokenlist)
	fnc_finder.process(tokenlist)
	op_finder.process(tokenlist)
	line_blocker.process(tokenlist)

	# TOKENS TO PC CODE PHASE
	shunter.process(tokenlist)
	function_to_fnc.process(tokenlist)
	op_to_fnc.process(tokenlist)
	gotoifyer.process(tokenlist)
	unblocker.process(tokenlist)

	return tokenlist


def generate(tokenlist):
	return tokenlist_to_pccode.generate(tokenlist)