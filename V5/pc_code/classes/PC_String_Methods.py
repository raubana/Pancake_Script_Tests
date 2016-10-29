from PC_String import *
from ..interpreter import Interpreter


def STRING_upper(interpreter, args):
	if len(args) != 1: raise Exception("NUM_ARGS")
	return [PC_String(args[0].value.upper())]
Interpreter.functions["STRING.upper"] = STRING_upper

def STRING_lower(interpreter, args):
	if len(args) != 1: raise Exception("NUM_ARGS")
	return [PC_String(args[0].value.lower())]
Interpreter.functions["STRING.lower"] = STRING_lower

def STRING_substring(interpreter, args):
	if len(args) != 3: raise Exception("NUM_ARGS")
	print(args)
	return [PC_String(args[0].value[ int(args[1].value) : int(args[2].value) ])]
Interpreter.functions["STRING.sub"] = STRING_substring