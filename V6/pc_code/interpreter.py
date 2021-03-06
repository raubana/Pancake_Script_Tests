import string
from constants import *
from classes import *


NUM_CHARS = "1234567890."


class Term(PC_String):
	TYPE = "TERM"

class SubFlag(PC_Number):
	TYPE = "SUB_FLAG"




def _print(interpreter, args):
	L = []
	for x in args:
		L.append(str(x))
	interpreter.print_buffer.append(string.join(L, " "))


def _del(interpreter, args):
	for x in args:
		if x.value in interpreter.ram:
			del interpreter.ram[x.value]



class Interpreter(object):
	functions = {"print" : _print,
				 "del": _del}

	def __init__(self, script):
		self.script = string.split(script,"\n")

		self.functions = dict(Interpreter.functions)
		self.stack = []
		self.ram = {}
		self.memory = 0

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

		output = None
		if t1 == "TRM":
			output = self.Op_TRM(t2)
		elif t1 == "LIT":
			output = self.Op_LIT(t2)
		elif t1 == "ASN":
			output = self.Op_ASN()
		elif t1 == "DEL":
			output = self.Op_DEL(t2)
		elif t1 == "GO2":
			output = self.Op_GO2(t2)
		elif t1 == "CAL":
			output = self.Op_CAL(t2)
		elif t1 == "RTN":
			output = self.Op_RTN()
		elif t1 == "FNC":
			output = self.Op_FNC(t2)
		elif t1 == "{":
			output = self.Op_RUNBLOCK()
		elif t1 == "}":
			pass
		else:
			output = PC_Exception("UNKNOWN_OPCODE")

		if output:
			output.pc_line = self.current_line_index
			return output

		if self.next_line_index is None:
			self.next_line_index = self.current_line_index + 1

	def Op_TRM(self,t2):
		if not t2: return PC_Exception("NO_ARGUMENT")
		self.push_stack(Term(t2))

	def Op_LIT(self,t2):
		if not t2: return PC_Exception("NO_ARGUMENT")
		value = self.parse_literal(t2)
		if value.TYPE == "EXCEPTION": return value
		result = self.push_stack(value)
		return result

	def Op_ASN(self):
		value = self.pop_stack()
		var_name = self.pop_stack()

		if type(var_name) != Term:
			return PC_Exception("WRONG_TYPE")

		if type(value) == Term:
			value = self.read_ram(value.value)
		else:
			value = value

		if value.TYPE == "EXCEPTION": return value

		result = self.write_ram(var_name.value, value)
		return result

	def Op_DEL(self,t2):
		if not t2: return PC_Exception("NO_ARGUMENT")
		if t2 in self.ram:
			del self.ram[t2]
			self.recalculate_memory()

	def Op_GO2(self,t2):
		if not t2: return PC_Exception("NO_ARGUMENT")
		line_num = 0
		try:
			line_num = int(t2)
		except:
			return PC_Exception("PARSE_ERROR")
		self.next_line_index = line_num

	def Op_CAL(self,t2):
		if not t2: return PC_Exception("NO_ARGUMENT")
		line_num = 0
		try:
			line_num = int(t2)
		except:
			return PC_Exception("PARSE_ERROR")
		self.next_line_index = line_num
		self.push_stack(SubFlag(self.current_line_index+1))

	def Op_RTN(self):
		while True:
			token = self.pop_stack()
			if token.TYPE == "SUB_FLAG":
				self.next_line_index = token.value
				break

	def Op_FNC(self,t2):
		num_args = self.pop_stack()
		if type(num_args) != PC_Number:
			return PC_Exception("WRONG_TYPE")

		num_args = int(num_args.value)
		arguments = []
		for x in xrange(num_args):
			val = self.pop_stack()
			if type(val) == Term:
				val = self.read_ram(val.value)
				if val.TYPE == "EXCEPTION": return val
			arguments.append(val)
		arguments.reverse()

		# here we check if the function is actually a method call.
		if t2.startswith("."):
			instance = self.pop_stack()
			if instance.TYPE == "TERM":
				instance = self.read_ram(instance.value)
				if instance.TYPE == "EXCEPTION": return instance
			t2 = instance.TYPE + t2
			arguments.insert(0,instance)
			num_args += 1

		if t2 not in self.functions: return PC_Exception("NOT_A_FUNCTION")

		returned = self.functions[t2](self,arguments)
		self.recalculate_memory()

		if returned is not None:
			if type(returned) == list:
				for val in returned:
					if val.TYPE == "EXCEPTION": return val
					output = self.push_stack(val)
					if output is not None and output.TYPE == "EXCEPTION": return output
			else:
				if returned is not None and returned.TYPE == "EXCEPTION": return returned
				return self.push_stack(returned)


	def Op_RUNBLOCK(self):
		value = self.pop_stack()
		while True:
			if type(value) == Term:
				value = self.read_ram(value.term)
			else:
				break

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
					return PC_Exception("UNEXPECTED_EOF")
				self.next_line_index += 1

	def read_ram(self, location):
		if location not in self.ram:
			return PC_Exception("NULL_POINTER")
		return self.ram[location]

	def write_ram(self, location, value):
		if location != self.ram and len(self.ram) >= RAM_SIZE:
			return PC_Exception("OUT_OF_VARS")
		self.ram[location] = value
		return self.recalculate_memory()

	def push_stack(self, value):
		if len(self.stack) >= STACK_SIZE: return PC_Exception("STACK_OVERFLOW")
		self.stack.append(value)
		return self.recalculate_memory()

	def pop_stack(self):
		if len(self.stack) <= 0: return PC_Exception("STACK_UNDERFLOW")
		to_return = self.stack.pop()
		output = self.recalculate_memory()
		if output: return output
		return to_return

	def recalculate_memory(self):
		self.memory = 0
		for value in self.stack:
			self.memory += value.get_memory_size()
		for key in self.ram:
			self.memory += self.ram[key].get_memory_size()
		if self.memory > MEMORY_SIZE:
			return PC_Exception("OUT_OF_MEMORY")

	@staticmethod
	def parse_literal(s):
		# boolean
		if s == "true" or s == "false":
			return PC_Boolean(s == "true")
		# string
		if s.startswith("\"") and s.endswith("\""):
			return PC_String(s[1:-1])
		# number
		could_be_number = True
		for ch in s:
			if not (ch in NUM_CHARS or ch  == "." or ch  == "-"):
				could_be_number = False
				break
		if "-" in s and s.rfind("-") != 0:
			could_be_number = False
		if could_be_number:
			return PC_Number(float(s))
		return PC_Exception("PARSE_ERROR")


import functions
import classes.PC_Class_Methods