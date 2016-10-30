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

def STRING_sub(interpreter, args):
	if len(args) != 3: raise Exception("NUM_ARGS")
	return [PC_String(args[0].value[ int(args[1].value) : int(args[2].value) ])]
Interpreter.functions["STRING.sub"] = STRING_sub

def STRING_toUpper(interpreter, args):
	if len(args) != 1: raise Exception("NUM_ARGS")
	args[0].value = args[0].value.upper()
Interpreter.functions["STRING.toUpper"] = STRING_toUpper

def STRING_toLower(interpreter, args):
	if len(args) != 1: raise Exception("NUM_ARGS")
	args[0].value = args[0].value.lower()
Interpreter.functions["STRING.toLower"] = STRING_toLower

def STRING_toSub(interpreter, args):
	if len(args) != 3: raise Exception("NUM_ARGS")
	args[0].value = args[0].value[ int(args[1].value) : int(args[2].value) ]
	args[0].calculate_memory_size()
Interpreter.functions["STRING.toSub"] = STRING_toSub