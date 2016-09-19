"""
The purpose of the blocker is to take the tokens from the first tokenizer and move tokens that are contained between
enclosing tokens (such as parentheses, brackets, and braces) into their own block.
"""

from error_format import error_format


ENCLOSED_TYPES = (
	("(",")","parenthesis"),
	("[","]","bracket"),
	("{","}","brace")
)


def _get_enclosed_type(token):
	if token is None: return None
	for	enclosed_type in ENCLOSED_TYPES:
		if token.value == enclosed_type[0] or token.value == enclosed_type[1]:
			return enclosed_type
	return None


class Block(object):
	def __init__(self, tokens=None):
		self.tokens = tokens or []
		self.type = "block"
		self.enclosed_type = None

	def append(self, token):
		self.tokens.append(token)

	def simplify(self):
		if self.enclosed_type is not None:
			self.tokens.pop()
			self.tokens.pop(0)
		for token in self.tokens:
			if token.type == "block":
				token.simplify()

	def __str__(self):
		import string

		start = ""
		end = ""
		if self.enclosed_type is not None:
			start = self.enclosed_type[0]
			end = self.enclosed_type[1]

		output = "B"+start+"\n"
		for token in self.tokens:
			lines = string.split(str(token),"\n")
			for x in xrange(len(lines)):
				lines[x] = "\t" + lines[x]

			if token.type == "block":
				for x in xrange(len(lines)):
					lines[x] = lines[x] + "\n"
					output += lines[x]
			else:
				output += lines[x] + "\n"
				if token.type == "EOL":
					output += "\t ----- \n"
		output += end+"B"
		return output

	def __repr__(self):
		return self.__str__()


class Blocker(object):
	def __init__(self, first_tokens):
		self._input_tokens = first_tokens
		self.block = None
		self._pos = 0

		self._generate_blocks()

	def _generate_blocks(self, start_token=None):
		current_block = Block()

		start_token_enclosed_type = _get_enclosed_type(start_token)

		if start_token_enclosed_type is not None:
			current_block.enclosed_type = start_token_enclosed_type

		if start_token is not None:
			current_block.append(start_token)

		while self._pos < len(self._input_tokens):
			token = self._input_tokens[self._pos]

			if token.type != "enclosed":
				current_block.append(token)
				self._pos += 1
			else:
				token_enclosed_type = _get_enclosed_type(token)

				if start_token is None:
					if token.value == token_enclosed_type[1]:
						error_format(token,"Ending {name} doesn't have a starting match.".format(name=token_enclosed_type[2]))
					else:
						#This is the start of another block.
						self._pos += 1
						new_block = self._generate_blocks(start_token = token)
						current_block.append(new_block)
				else:
					if token.value == start_token_enclosed_type[1]:
						current_block.append(token)
						self._pos += 1
						return current_block
					else:
						if token.value == token_enclosed_type[0]:
							#This is the start of another block.
							self._pos += 1
							new_block = self._generate_blocks(start_token = token)
							current_block.append(new_block)

		if start_token is None:
			self.block = current_block
			self.block.simplify()