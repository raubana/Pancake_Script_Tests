from PC_Array import *
from ..interpreter import Interpreter


def ARRAY_new(interpreter, args):
	return [PC_Array()]
Interpreter.functions["Array"] = ARRAY_new

def ARRAY_push(interpreter, args):
	if len(args) != 2: raise Exception("NUM_ARGS")
	if args[1].TYPE == "ARRAY": raise Exception("ARRAY_IN_ARRAY")
	args[0].value.append(args[1])
	args[0].calculate_memory_size()
Interpreter.functions["ARRAY.push"] = ARRAY_push

def ARRAY_pushAt(interpreter, args):
	if len(args) != 3: raise Exception("NUM_ARGS")
	if args[1].TYPE == "ARRAY": raise Exception("ARRAY_IN_ARRAY")
	args[0].value.insert(args[2].value, args[1])
	args[0].calculate_memory_size()
Interpreter.functions["ARRAY.pushAt"] = ARRAY_pushAt

def ARRAY_pop(interpreter, args):
	if len(args) != 1: raise Exception("NUM_ARGS")
	val = args[0].value.pop()
	args[0].calculate_memory_size()
	return val
Interpreter.functions["ARRAY.pop"] = ARRAY_pop

def ARRAY_popAt(interpreter, args):
	if len(args) != 2: raise Exception("NUM_ARGS")
	val = args[0].value.pop(args[1].value)
	args[0].calculate_memory_size()
	return val
Interpreter.functions["ARRAY.popAt"] = ARRAY_popAt

def ARRAY_slice(interpreter, args):
	if len(args) != 3: raise Exception("NUM_ARGS")
	return PC_Array(args[0].value[ int(args[1].value) : int(args[2].value) ])
Interpreter.functions["ARRAY.slice"] = ARRAY_slice

def ARRAY_get(interpreter, args):
	if len(args) != 2: raise Exception("NUM_ARGS")
	return args[0].value[ int(args[1].value) ]
Interpreter.functions["ARRAY.get"] = ARRAY_get

def ARRAY_set(interpreter, args):
	if len(args) != 3: raise Exception("NUM_ARGS")
	args[0].value[ int(args[1].value) ] = args[2]
	args[0].calculate_memory_size()
Interpreter.functions["ARRAY.set"] = ARRAY_set