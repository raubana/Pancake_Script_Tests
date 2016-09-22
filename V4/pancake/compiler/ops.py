from constants import *

OPERATORS = []

class Op(object):
	def __init__(self, symbol, function, precedence, associativity, num_operands):
		self.symbol = symbol
		self.function = function
		self.precedence = precedence
		self.associativity = associativity
		self.num_operands = num_operands

	def __str__(self):
		return str((self.symbol, self.function))

	def __repr__(self):
		return self.__str__()


def create_op(symbol,function,precedence,associativity,num_operands):
	OPERATORS.append(Op(symbol,function,precedence,associativity,num_operands))


create_op("+","add",5,LEFT_TO_RIGHT,2)
create_op("-","subtract",5,LEFT_TO_RIGHT,2)
create_op("*","multiply",4,LEFT_TO_RIGHT,2)
create_op("/","divide",4,LEFT_TO_RIGHT,2)
create_op("%","modulus",4,LEFT_TO_RIGHT,2)
create_op("-","negate",2,RIGHT_TO_LEFT,1)

create_op("=","assign",10,RIGHT_TO_LEFT,2)

create_op("==","equalto",7,LEFT_TO_RIGHT,2)
create_op("!=","notequalto",7,LEFT_TO_RIGHT,2)

create_op("&","and",8,LEFT_TO_RIGHT,2)
create_op("|","or",9,LEFT_TO_RIGHT,2)
create_op("!","not",2,RIGHT_TO_LEFT,1)

create_op(">","greaterthan",6,LEFT_TO_RIGHT,2)
create_op(">=","greaterthanequalto",6,LEFT_TO_RIGHT,2)
create_op("<","lessthan",6,LEFT_TO_RIGHT,2)
create_op("<=","lessthanequalto",6,LEFT_TO_RIGHT,2)