from interpreter import Interpreter
from classes import *

import random, math


# Arithmetic

def negate(interpreter, args):
	if len(args) != 1: return PC_Exception("NUM_ARGS")
	return [-args[0]]
Interpreter.functions["neg"] = negate

def add(interpreter, args):
	if len(args) != 2: return PC_Exception("NUM_ARGS")
	return [args[0] + args[1]]
Interpreter.functions["+"] = add

def subtract(interpreter, args):
	if len(args) != 2: return PC_Exception("NUM_ARGS")
	return [args[0] - args[1]]
Interpreter.functions["-"] = subtract

def multiply(interpreter, args):
	if len(args) != 2: return PC_Exception("NUM_ARGS")
	return [args[0] * args[1]]
Interpreter.functions["*"] = multiply

def divide(interpreter, args):
	if len(args) != 2: return PC_Exception("NUM_ARGS")
	return [args[0] / args[1]]
Interpreter.functions["/"] = divide

def modulus(interpreter, args):
	if len(args) != 2: return PC_Exception("NUM_ARGS")
	return [args[0] % args[1]]
Interpreter.functions["%"] = modulus

def power(interpreter, args):
	if len(args) != 2: return PC_Exception("NUM_ARGS")
	return [args[0] ** args[1]]
Interpreter.functions["^"] = power


# Relational

def greaterthanequalto(interpreter, args):
	if len(args) != 2: return PC_Exception("NUM_ARGS")
	return [args[0] >= args[1]]
Interpreter.functions[">="] = greaterthanequalto

def lessthanequalto(interpreter, args):
	if len(args) != 2: return PC_Exception("NUM_ARGS")
	return [args[0] <= args[1]]
Interpreter.functions["<="] = lessthanequalto

def greaterthan(interpreter, args):
	if len(args) != 2: return PC_Exception("NUM_ARGS")
	return [args[0] > args[1]]
Interpreter.functions[">"] = greaterthan

def lessthan(interpreter, args):
	if len(args) != 2: return PC_Exception("NUM_ARGS")
	return [args[0] < args[1]]
Interpreter.functions["<"] = lessthan


# Comparative

def equalto(interpreter, args):
	if len(args) != 2: return PC_Exception("NUM_ARGS")
	return [args[0] == args[1]]
Interpreter.functions["=="] = equalto

def notequalto(interpreter, args):
	if len(args) != 2: return PC_Exception("NUM_ARGS")
	return [args[0] != args[1]]
Interpreter.functions["!="] = notequalto


# Logical

def _and(interpreter, args):
	if len(args) != 2: return PC_Exception("NUM_ARGS")
	return [args[0] and args[1]]
Interpreter.functions["&"] = _and

def _or(interpreter, args):
	if len(args) != 2: return PC_Exception("NUM_ARGS")
	return [args[0] or args[1]]
Interpreter.functions["|"] = _or

def _not(interpreter, args):
	if len(args) != 1: return PC_Exception("NUM_ARGS")
	return [not args[0]]
Interpreter.functions["!"] = _not


# Misc

def _random(interpreter, args):
	return PC_Number(random.random())
Interpreter.functions["random"] = _random

def floor(interpreter, args):
	if len(args) != 1: return PC_Exception("NUM_ARGS")
	if args[0].TYPE != "NUMBER": return PC_Exception("WRONG_TYPE")
	return PC_Number(math.floor(args[0].value))
Interpreter.functions["floor"] = floor

def ceil(interpreter, args):
	if len(args) != 1: return PC_Exception("NUM_ARGS")
	if args[0].TYPE != "NUMBER": return PC_Exception("WRONG_TYPE")
	return PC_Number(math.ceil(args[0].value))
Interpreter.functions["ceil"] = ceil