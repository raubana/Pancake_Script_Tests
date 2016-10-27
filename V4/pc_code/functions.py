from interpreter import Term, Literal, Interpreter

import random, math


# Arithmetic

def negate(interpreter, args):
	if len(args) != 1: raise Exception("NUM_ARGS")
	return [Literal(-args[0].value)]
Interpreter.functions["neg"] = negate

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


# Relational

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


# Comparative

def equalto(interpreter, args):
	if len(args) != 2: raise Exception("NUM_ARGS")
	return [Literal(args[0].value == args[1].value)]
Interpreter.functions["=="] = equalto

def notequalto(interpreter, args):
	if len(args) != 2: raise Exception("NUM_ARGS")
	return [Literal(args[0].value != args[1].value)]
Interpreter.functions["!="] = notequalto


# Logical

def _and(interpreter, args):
	if len(args) != 2: raise Exception("NUM_ARGS")
	return [Literal(args[0].value and args[1].value)]
Interpreter.functions["&"] = _and

def _or(interpreter, args):
	if len(args) != 2: raise Exception("NUM_ARGS")
	return [Literal(args[0].value or args[1].value)]
Interpreter.functions["|"] = _or

def _not(interpreter, args):
	if len(args) != 1: raise Exception("NUM_ARGS")
	return [Literal(not args[0].value)]
Interpreter.functions["!"] = _not


# Misc

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