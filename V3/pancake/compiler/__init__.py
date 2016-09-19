import tokenizer
import op_finder
import blocker
import fnc_finder
import line_blocker
import callifyer
import shunter
import gotoifyer
import unblocker

def compile(script):
	tokenlist = tokenizer.tokenize(script)
	op_finder.process(tokenlist)
	blocker.process(tokenlist)
	fnc_finder.process(tokenlist)
	line_blocker.process(tokenlist)
	callifyer.process(tokenlist)
	shunter.process(tokenlist)
	gotoifyer.process(tokenlist)
	unblocker.process(tokenlist)
	return tokenlist