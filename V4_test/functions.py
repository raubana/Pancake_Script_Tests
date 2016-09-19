from interpreter import Term, Literal, Interpreter

def negate(interpreter, args):
	if len(args) != 1: raise Exception("NUM_ARGS")
	return [Literal(-args[0].value)]
Interpreter.functions["negate"] = negate

def addition(interpreter, args):
	if len(args) != 2: raise Exception("NUM_ARGS")
	return [Literal(args[0].value + args[1].value)]
Interpreter.functions["addition"] = addition

def subtract(interpreter, args):
	if len(args) != 2: raise Exception("NUM_ARGS")
	return [Literal(args[0].value - args[1].value)]
Interpreter.functions["subtract"] = subtract

def greaterthan(interpreter, args):
	if len(args) != 2: raise Exception("NUM_ARGS")
	return [Literal(args[0].value > args[1].value)]
Interpreter.functions["greaterthan"] = greaterthan

def lessthan(interpreter, args):
	if len(args) != 2: raise Exception("NUM_ARGS")
	return [Literal(args[0].value < args[1].value)]
Interpreter.functions["lessthan"] = lessthan

def equalto(interpreter, args):
	if len(args) != 2: raise Exception("NUM_ARGS")
	return [Literal(args[0].value == args[1].value)]
Interpreter.functions["equalto"] = equalto