import time
from error_format import error_format
from firsttokenizer import Token


STACK_MAX = 8
VAR_MAX = 16


class Interpreter(object):
	def __init__(self, compiled_script):
		self.script = compiled_script
		self.stack = []
		self.variables = {}
		self.current_index = [-1]
		self.current_token = None

		self.subroutine_level = 0

		self.print_buffer = []
		self.eof = False

	def _get_token_at(self, location):
		current_token = self.script
		for i in location:
			if i < 0 or i >= len(current_token.tokens):
				return None
			current_token = current_token.tokens[i]
		return current_token

	def _get_next_token(self):
		if len(self.current_index) == 0: return None
		self.current_index[-1] = self.current_index[-1] + 1
		token = self._get_token_at(self.current_index)
		if token is None:
			self.current_index.pop()
			token = self._get_next_token()
		elif token.type == "block":
			self.current_index.append(-1)
			token = self._get_next_token()
		return token

	def _get_as_value(self,token):
		if type(token) is Token:
			if token.type == "number":
				return float(token.value)
			elif token.type == "string":
				return token.value
			elif token.type == "term":
				return self.variables[token.value]
		return token

	def _args_as_values(self,args):
		return (self._get_as_value(args[0]), self._get_as_value(args[1]))

	def process_one(self):
		self.print_buffer = []
		#we find our current token in the script
		current_token = self._get_next_token()
		self.current_token = current_token

		if current_token is None:
			#We have reached the end of the program. We terminate.
			#error_format(None,"EOF")
			self.eof = True
			return
		
		#if the type of that token is an operator, we process it immediately.
		if current_token.type == "operator":
			op = current_token.value
			args = [self.stack.pop(), self.stack.pop()]
			args.reverse()
			output = None
			if op == "+":
				args = self._args_as_values(args)
				output = args[0] + args[1]
			elif op == "-":
				args = self._args_as_values(args)
				output = args[0] - args[1]
			elif op == "*":
				args = self._args_as_values(args)
				output = args[0] * args[1]
			elif op == "/":
				args = self._args_as_values(args)
				output = args[0] / args[1]
			elif op == "%":
				args = self._args_as_values(args)
				output = args[0] % args[1]
			elif op == "=":
				if type(args[0]) is Token and args[0].type == "term":
					if len(self.variables) == VAR_MAX:
						error_format(current_token,"OUT OF MEMORY")
					self.variables[args[0].value] = self._get_as_value( args[1] )
			elif op == "==":
				args = self._args_as_values(args)
				output =  args[0] == args[1]
			elif op == ">":
				args = self._args_as_values(args)
				output =  args[0] >  args[1]
			elif op == ">=":
				args = self._args_as_values(args)
				output =  args[0] >= args[1]
			elif op == "<":
				args = self._args_as_values(args)
				output =  args[0] < args[1]
			elif op == "<=":
				args = self._args_as_values(args)
				output =  args[0] <= args[1]
			elif op == "&":
				args = self._args_as_values(args)
				output = args[0] and args[1]
			elif op == "|":
				args = self._args_as_values(args)
				output = args[0] or args[1]
			else:
				error_format(current_token,"\"{op}\" isn't a recognized operator.".format(op=op))
			self._push_to_stack(output)
		elif current_token.type == "function":
			fnc = current_token.value
			args = []
			while len(self.stack) > 0:
				args.append(self.stack.pop())
			if fnc == "print":
				args.reverse()
				output = ""
				i = 0
				while True:
					output += str(self._get_as_value(args[i]))
					i += 1
					if i < len(args):
						output += ", "
					else:
						break
				self.print_buffer.append(output)
			elif fnc == "pause":
				time.sleep(1.0)
			elif fnc == "del":
				if len(args) < 1:
					error_format(current_token,"\"del\" expects at least one argument.")
				for arg in args:
					if arg.type == "term":
						if arg.value in self.variables:
							self.variables.pop(arg.value)
					else:
						error_format(current_token,"\"del\" received an argument that wasn't a term (expects variable names).")
			elif fnc in ("if","while"):
				# We must check if the function's one argument evaluates to true or false.
				if self._get_as_value(args[0]):
					# It evaluated to true, so we continue.
					pass
				else:
					# It evaluated to false, so we skip the next line.
					self.current_index[-1] = self.current_index[-1] + 1
			else:
				error_format(current_token,"\"{fnc}\" isn't a recognized function.".format(fnc=fnc))
		elif current_token.type == "goto":
			self.current_index = current_token.value
			# Because we call "get_next_token", we have to subtract one index value from the end of this list.
			self.current_index = current_token.value[:-1] + [current_token.value[-1]-1]
		elif current_token.type == "term":
			val = current_token.value
			if val == "else":
				pass
			else:
				self._push_to_stack(current_token)
		else:
			if current_token.type != "block":
				self._push_to_stack(current_token)

	def _push_to_stack(self, value):
		if len(self.variables) == STACK_MAX:
			error_format(value,"STACK OVERFLOW")
		if value is None:
			return
		self.stack.append(value)