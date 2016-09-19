
from .. compiler.tokenizer import Token
from .. ops import OPERATORS
from .. constants import *
from .. common import find_op_by_symbol, find_endblock_token_index
from .. error_format import error_format


def _print(interpreter, num_args, args):
	L = []
	for x in args:
		L.insert(0,str(interpreter.get_as_value(x)))
	interpreter.print_buffer.append(string.join(L, ", "))


def _del(interpreter, num_args, args):
	if num_args < 1:
		error_format(interpreter.current_token, "\"del\" expects at least one argument.")  # TODO:
	for arg in args:
		if arg.type == TYPE_TERM:
			if arg.value in interpreter.variables:
				interpreter.variables.pop(arg.value)
		else:
			# TODO:
			error_format(interpreter.current_token, "\"del\" received an argument that wasn't a term (expects variable names).")

def _while(interpreter, num_args, args):
	return args[0]

def _if(interpreter, num_args, args):
	return args[0]

class Interpreter(object):
	def __init__(self, compiled_script):
		if len(compiled_script.tokens) > TOKEN_MAX:
			raise Exception("Derp, token limit exceeded.")

		self.script = compiled_script
		self.stack = []
		self.variables = {}
		self.functions = {
			"if": _if,
			"while": _while,
			"print": _print,
			"del": _del
		}
		self.cursor = 0
		self.next_cursor = None

		self.current_token = None
		self.print_buffer = []
		self.eof = False

	def get_as_value(self,token):
		if type(token) is Token:
			if token.type == TYPE_NUMBER:
				return float(token.value)
			elif token.type == TYPE_STRING:
				return token.value
			elif token.type == TYPE_TERM:
				if token.value not in self.variables:
					error_format(token, "\"{term}\" is not an existing variable.".format(term=token.value))
				else:
					return self.variables[token.value]
		return token

	def assign(self, operand1, operand2):
		if type(operand1) is Token and operand1.type == TYPE_TERM:
			if operand1.value in self.functions:
				error_format(self.current_token, "{v} is the name of a function; it is a reserved keyword.".format(v=operand1.value))
			if operand1.value in MISC_KEYWORDS:
				error_format(self.current_token, "{v} is a reserved keyword.".format(v=operand1.value))
			if len(self.variables) >= VAR_MAX:
				error_format(self.current_token, "OUT OF MEMORY")
			self.variables[operand1.value] = self.get_as_value(operand2)
		else:
			error_format(self.current_token, "Unexpected assignment failure.")

	def runtime_error(self, error):
		raise error #error_format(self.current_token, str(error))

	def process_one(self):
		self.print_buffer = []

		if self.next_cursor is not None:
			self.cursor = self.next_cursor
		if self.cursor >= len(self.script.tokens):
			self.eof = True
			return

		self.current_token = self.script.tokens[self.cursor]

		t = self.current_token.type
		v = self.current_token.value

		output = None

		if t == TYPE_CALL:
			num_args = v[0]
			token2 = v[1]
			t2 = token2.type
			v2 = token2.value

			if t2 == TYPE_OPERATOR:
				args = []
				for i in xrange(num_args):
					args.append(self.pop_stack())
				args.reverse()
				the_op = None
				for op in OPERATORS:
					if op.SYMBOL == v2 and op.NUM_OPERANDS == num_args:
						the_op = op
						break
				if the_op is not None:
					if len(args) == 1: args.append(None)
					output = the_op.perform_op(args[0],args[1],self)
				else:
					error_format(self.current_token, "No operator \"{v}\" expects {x} operands.".format(v=v2,x=len(args)))
				self.next_cursor = self.cursor + 1

			elif t2 == TYPE_FUNCTION:
				if v2 in self.functions:
					args = []
					for i in xrange(num_args):
						args.append(self.pop_stack())
					output = self.functions[v2](self, num_args, args)

					# We check if there's a body after this function.
					# In the event that there is and the output evaluates to false,
					# we skip that body.
					if self.cursor + 1 < len(self.script.tokens) and \
						self.script.tokens[self.cursor + 1].type == TYPE_BLOCK_START and \
						self.script.tokens[self.cursor + 1].value == BLOCK_START_CHAR:
						if output:
							self.next_cursor = self.cursor + 1
						else:
							end_index = find_endblock_token_index(self.script.tokens, self.cursor + 2)
							self.next_cursor = end_index + 1
						output = None
					else:
						self.next_cursor = self.cursor + 1
				else:
					error_format(self.current_token, "Function \"{v}\" does not exist.".format(v=v2))

		elif t == TYPE_GOTO:
			self.next_cursor = v

		elif t == TYPE_BLOCK_START or t == TYPE_BLOCK_END:
			self.next_cursor = self.cursor + 1

		elif t in (TYPE_NUMBER, TYPE_STRING):
			self.push_stack(self.get_as_value(self.current_token))
			self.next_cursor = self.cursor + 1

		else:
			if v not in MISC_KEYWORDS:
				self.push_stack(self.current_token)
			self.next_cursor = self.cursor + 1

		if output is not None:
			if type(output) in (tuple,list):
				for x in output:
					self.push_stack(x)
			else:
				self.push_stack(output)

	def push_stack(self, x):
		if len(self.stack) >= STACK_MAX:
			raise Exception("STACK OVERFLOW!")
		self.stack.append(x)

	def pop_stack(self, error_on_failure=True):
		if len(self.stack) == 0:
			if error_on_failure:
				raise Exception("Doop, no more stuff in the stack.")
				#TODO: Raise a proper error here.
			return None
		return self.stack.pop()