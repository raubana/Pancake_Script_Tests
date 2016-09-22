from constants import *
from error_format import *


class Token(object):
	def __init__(self, type, value, line_number, char_number):
		self.type = type
		self.value = value
		self.line_number = line_number
		self.char_number = char_number

	def __str__(self):
		return "T({type}, {value}, {line}, {char})".format(
			type=TYPE_NAMES[self.type],
			value=repr(self.value),
			line=self.line_number,
			char=self.char_number
		)

	def __repr__(self):
		return self.__str__()


class TokenList(object):
	def __init__(self):
		self.tokens = []

	def push(self, token):
		self.tokens.append(token)
		
	def __str__(self):
		output = ""
		indent = 0
		for token in self.tokens:
			if token.type == TYPE_BLOCK_END:
				indent = max(indent-1,0)
			output += "\t"*indent
			output += str(token)+"\n"
			if token.type == TYPE_BLOCK_START:
				indent += 1
		if len(output) > 0:
			output = output[:-1]
		return output
		
	def __repr__(self):
		return self.__str__()


class Tokenizer(object):
	@staticmethod
	def tokenize(text, ignore_errors = False):
		tokens = TokenList()
		line_number = 1
		char_number = 1
		index = 0

		current_token = None
		while index < len(text):
			ch = text[index]

			#START OF NEW TOKEN
			if current_token is None:
				current_token = Token(TYPE_NULL, str(ch), line_number, char_number)
				if ch == COMMENT_CHAR: #comments
					current_token.type = TYPE_COMMENT
				elif ch in VARIABLE_NAME_START_CHARACTERS: #term
					current_token.type = TYPE_TERM
				elif ch in NUMBER_START_CHARACTERS: #number
					current_token.type = TYPE_NUMBER
				elif ch == STRING_CHAR: #string
					current_token.type = TYPE_STRING
					current_token.value = ""
				elif ch == EOL_CHAR: # End Of Line
					current_token.type = TYPE_EOL
					tokens.push(current_token)
					current_token = None
				elif ch == SEPARATOR_CHAR: # separator
					current_token.type = TYPE_SEPARATOR
					tokens.push(current_token)
					current_token = None
				elif ch in WHITESPACE:
					current_token.type = TYPE_WHITESPACE
				elif ch in ENCLOSING_CHARACTERS:
					current_token.type = TYPE_ENCLOSED
					tokens.push(current_token)
					current_token = None
				else:
					current_token.type = TYPE_OTHER

			#CONTINUATION/ENDING OF A TOKEN
			else:
				finish_token = False
				push_token = True
				decrement = True

				t = current_token.type
				if t == TYPE_COMMENT:
					if ch == NEWLINE_CHAR:
						finish_token = True
						decrement = False
					else:
						current_token.value += ch
				elif current_token.type == TYPE_TERM:
					if ch in VARIABLE_NAME_CHARACTERS:
						current_token.value += ch
					else:
						finish_token = True
						if current_token.value in ["true","false"]:
							current_token.type = TYPE_BOOLEAN
							current_token.value = current_token.value == "true"
				elif current_token.type == TYPE_NUMBER:
					if ch in NUMBER_CHARACTERS:
						current_token.value += ch
					else:
						finish_token = True
				elif current_token.type == TYPE_WHITESPACE:
					if ch in WHITESPACE:
						current_token.value += ch
					else:
						finish_token = True
						push_token = False
				elif current_token.type == TYPE_STRING:
					if ch == STRING_CHAR:
						finish_token = True
						decrement = False
					else:
						current_token.value += ch
				elif current_token.type == TYPE_OTHER:
					if current_token.value == "-" and ch in NUMBER_CHARACTERS:
						current_token.type = TYPE_NUMBER
						current_token.value += ch
					else:
						if ch in WHITESPACE or ch in NUMBER_CHARACTERS or ch in VARIABLE_NAME_CHARACTERS or \
							ch in ENCLOSING_CHARACTERS or ch == EOL_CHAR or ch == STRING_CHAR:
							finish_token = True
						else:
							current_token.value += ch
				if finish_token:
					if push_token:
						tokens.push(current_token)
					current_token = None
					if decrement:
						index -= 1
						char_number -= 1

			if ch == NEWLINE_CHAR:
				line_number += 1
				char_number = 0

			char_number += 1
			index += 1

		if current_token is not None:
			if current_token.type not in [TYPE_WHITESPACE]:
				tokens.push(current_token)
			if current_token.type == TYPE_STRING:
				if not ignore_errors:
					error_format(current_token, "String doesn't have an ending {ch} .".format(ch=STRING_CHAR))
				else:
					current_token.type = TYPE_NULL

		return tokens


def tokenize(script, ignore_errors = False):
	return Tokenizer.tokenize(script, ignore_errors)