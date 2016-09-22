from interpreter import Term, Literal, Interpreter

import random, math

def negate(interpreter, args):
	if len(args) != 1: raise Exception("NUM_ARGS")
	return [Literal(-args[0].value)]
Interpreter.functions["negate"] = negate

def add(interpreter, args):
	if len(args) != 2: raise Exception("NUM_ARGS")
	return [Literal(args[0].value + args[1].value)]
Interpreter.functions["+"] = add

def subtract(interpreter, args):
	if len(args) != 2: raise Exception("NUM_ARGS")
	return [Literal(args[0].value - args[1].value)]
Interpreter.functions["-"] = subtract

def multiply(interpreter, args):
	if len(args) != 2: raise Exception("NUM_ARGS")
	return [Literal(args[0].value * args[1].value)]
Interpreter.functions["*"] = multiply

def divide(interpreter, args):
	if len(args) != 2: raise Exception("NUM_ARGS")
	return [Literal(args[0].value / args[1].value)]
Interpreter.functions["/"] = divide

def modulus(interpreter, args):
	if len(args) != 2: raise Exception("NUM_ARGS")
	return [Literal(args[0].value % args[1].value)]
Interpreter.functions["%"] = modulus

def greaterthanequalto(interpreter, args):
	if len(args) != 2: raise Exception("NUM_ARGS")
	return [Literal(args[0].value >= args[1].value)]
Interpreter.functions[">="] = greaterthanequalto

def lessthanequalto(interpreter, args):
	if len(args) != 2: raise Exception("NUM_ARGS")
	return [Literal(args[0].value <= args[1].value)]
Interpreter.functions["<="] = lessthanequalto

def greaterthan(interpreter, args):
	if len(args) != 2: raise Exception("NUM_ARGS")
	return [Literal(args[0].value > args[1].value)]
Interpreter.functions[">"] = greaterthan

def lessthan(interpreter, args):
	if len(args) != 2: raise Exception("NUM_ARGS")
	return [Literal(args[0].value < args[1].value)]
Interpreter.functions["<"] = lessthan

def equalto(interpreter, args):
	if len(args) != 2: raise Exception("NUM_ARGS")
	return [Literal(args[0].value == args[1].value)]
Interpreter.functions["=="] = equalto

def _random(interpreter, args):
	return Literal(random.random())
Interpreter.functions["random"] = _random

def floor(interpreter, args):
	if len(args) != 1: raise Exception("NUM_ARGS")
	return Literal(math.floor(args[0].value))
Interpreter.functions["floor"] = floor

def ceil(interpreter, args):
	if len(args) != 1: raise Exception("NUM_ARGS")
	return Literal(math.ceil(args[0].value))
Interpreter.functions["ceil"] = ceil