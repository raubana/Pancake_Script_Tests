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

create_op(".",".",1,LEFT_TO_RIGHT,2)

create_op("+","+",5,LEFT_TO_RIGHT,2)
create_op("-","-",5,LEFT_TO_RIGHT,2)
create_op("*","*",4,LEFT_TO_RIGHT,2)
create_op("/","/",4,LEFT_TO_RIGHT,2)
create_op("%","%",4,LEFT_TO_RIGHT,2)
create_op("-","neg",2,RIGHT_TO_LEFT,1)
create_op("^","^",2,LEFT_TO_RIGHT,2)

create_op("=","=",10,RIGHT_TO_LEFT,2)

create_op("==","==",7,LEFT_TO_RIGHT,2)
create_op("!=","!=",7,LEFT_TO_RIGHT,2)

create_op("&","&",8,LEFT_TO_RIGHT,2)
create_op("|","|",9,LEFT_TO_RIGHT,2)
create_op("!","!",2,RIGHT_TO_LEFT,1)

create_op(">",">",6,LEFT_TO_RIGHT,2)
create_op(">=",">=",6,LEFT_TO_RIGHT,2)
create_op("<","<",6,LEFT_TO_RIGHT,2)
create_op("<=","<=",6,LEFT_TO_RIGHT,2)