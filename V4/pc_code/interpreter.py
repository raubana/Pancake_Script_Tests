import string
from constants import *


NUM_CHARS = "1234567890."


class Term(object):
	def __init__(self, term):
		self.term = term

	def __str__(self):
		return str(self.term)

	def __repr__(self):
		return str(self.term)


class Literal(object):
	def __init__(self, value):
		self.value = value

	def __str__(self):
		return str(self.value)

	def __repr__(self):
		return str(self.value)




def _print(interpreter, args):
	L = []
	for x in args:
		L.append(str(x))
	interpreter.print_buffer.append(string.join(L, " "))




class Interpreter(object):
	functions = {"print" : _print}

	def __init__(self, script):
		self.script = string.split(script,"\n")

		self.functions = dict(Interpreter.functions)
		self.stack = []
		self.memory = {}

		self.print_buffer = []

		self.next_line_index = 0
		self.current_line_index = None

		self.running = True

	def go_to_next_line(self):
		self.print_buffer = []
		if self.next_line_index is None or self.next_line_index >= len(self.script):
			self.running = False
			return
		if self.next_line_index < 0:
			self.next_line_index = 0
		self.current_line_index = self.next_line_index
		self.next_line_index = None

	def process_current_line(self):
		line = self.script[self.current_line_index]
		tokens = string.split(line)

		t1 = None
		t2 = None

		if len(tokens) > 0:
			t1 = tokens[0]
		if len(tokens) > 1:
			t2 = string.join(tokens[1:])

		if t1 == "TRM":
			self.Op_TRM(t2)
		elif t1 == "LIT":
			self.Op_LIT(t2)
		elif t1 == "ASN":
			self.Op_ASN()
		elif t1 == "DEL":
			self.Op_DEL(t2)
		elif t1 == "GO2":
			self.Op_GO2(t2)
		elif t1 == "FNC":
			self.Op_FNC(t2)
		elif t1 == "{":
			self.Op_RUNBLOCK()
		elif t1 == "}":
			pass
		else:
			raise Exception("UNKNOWN_OPCODE")

		if self.next_line_index is None:
			self.next_line_index = self.current_line_index + 1

	def Op_TRM(self,t2):
		if not t2: raise ("NO_ARGUMENT")
		self.push_stack(Term(t2))

	def Op_LIT(self,t2):
		if not t2: raise ("NO_ARGUMENT")
		self.push_stack(self.parse_literal(t2))

	def Op_ASN(self):
		value = self.pop_stack()
		var_name = self.pop_stack()

		if type(var_name) != Term:
			raise Exception("WRONG_TYPE")

		if type(value) == Literal:
			pass
		elif type(value) == Term:
			value = self.read_memory(value.term)
		else:
			raise Exception("WRONG_TYPE")

		self.write_memory(var_name.term, value)

	def Op_DEL(self,t2):
		if not t2: raise ("NO_ARGUMENT")
		if t2 in self.memory:
			del self.memory[t2]

	def Op_GO2(self,t2):
		if not t2: raise ("NO_ARGUMENT")
		line_num = 0
		try:
			line_num = int(t2)
		except:
			raise Exception("PARSE_ERROR")
		self.next_line_index = line_num

	def Op_FNC(self,t2):
		if t2 not in self.functions:
			raise Exception("NOT_A_FUNCTION")
		num_args = self.pop_stack()
		if type(num_args) != Literal or type(num_args.value) != float:
			raise Exception("WRONG_TYPE")
		num_args = int(num_args.value)
		arguments = []
		for x in xrange(num_args):
			val = self.pop_stack()
			if type(val) == Term:
				val = self.read_memory(val.term)
			arguments.append(val)
		arguments.reverse()
		returned = self.functions[t2](self,arguments)
		if returned:
			if type(returned) == Literal:
				self.push_stack(returned)
			else:
				for val in returned:
					self.push_stack(val)

	def Op_RUNBLOCK(self):
		value = self.pop_stack()
		while True:
			if type(value) == Literal:
				value = value.value
				break
			elif type(value) == Term:
				value = self.read_memory(value.term)
			else:
				raise Exception("WRONG_TYPE")

		skip_block = not bool(value)

		if skip_block:
			#we iterate forward until we find the end of this block.
			level = 0
			self.next_line_index = self.current_line_index + 1
			while True:
				if self.next_line_index < len(self.script):
					line = self.script[self.next_line_index]
					if line == "{":
						level += 1
					elif line == "}":
						if level == 0:
							self.next_line_index += 1
							break
						level -= 1
				else:
					raise Exception("UNEXPECTED_EOF")
				self.next_line_index += 1

	def read_memory(self, location):
		if location not in self.memory:
			raise Exception("NULL_POINTER")
		return self.memory[location]

	def write_memory(self, location, value):
		if location != self.memory and len(self.memory) >= MEMORY_SIZE:
			raise Exception("OUT_OF_MEMORY")
		self.memory[location] = value

	def push_stack(self, value):
		if len(self.stack) >= STACK_SIZE: raise Exception("STACK_OVERFLOW")
		self.stack.append(value)

	def pop_stack(self):
		if len(self.stack) <= 0: raise Exception("STACK_UNDERFLOW")
		return self.stack.pop()

	@staticmethod
	def parse_literal(s):
		# boolean
		if s == "true" or s == "false":
			return Literal(s == "true")
		# string
		if s.startswith("\"") and s.endswith("\""):
			return Literal(s[1:-1])
		# number
		could_be_number = True
		for ch in s:
			if not (ch in NUM_CHARS or ch  == "." or ch  == "-"):
				could_be_number = False
				break
		if "-" in s and s.rfind("-") != 0:
			could_be_number = False
		if could_be_number:
			return Literal(float(s))
		raise Exception("PARSE_ERROR")


import functions