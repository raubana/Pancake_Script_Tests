"""
The purpose of the first tokenizer is to take the source code of a script and break it down into a simple list of
tokens.
"""


import string


ENCLOSED_TOKENS = "()[]{}"


class Token(object):
	def __init__(self, type, value, line_number, char_number):
		self.type = type
		self.value = value
		self.line_number = line_number
		self.char_number = char_number

	def __str__(self):
		return "T({type}, {value}, {line}, {char})".format(
			type=self.type,
			value=repr(self.value),
			line=self.line_number,
			char=self.char_number
		)

	def __repr__(self):
		return self.__str__()


class FirstTokenizer(object):
	def __init__(self, text):
		self.text = text
		self._pos = 0
		self._line_number = 1
		self._char_number = 1
		self._current_token = None

		self.tokens = []

		self._tokenize_script()

	def _finish_token(self, sub=True, push=True):
		if push:
			self.tokens.append(self._current_token)
		self._current_token = None
		if sub:
			self._pos -= 1
			self._char_number -= 1

	def _tokenize_script(self):
		self._line_number = 1
		self._char_number = 1

		while self._pos < len(self.text):
			ch = self.text[self._pos]

			curtok = self._current_token

			# START OF A TOKEN
			if curtok == None:
				if ch == "#":
					self._current_token = Token("comment",str(ch),self._line_number,self._char_number)
				elif ch in string.ascii_letters + "_":
					self._current_token = Token("term",str(ch),self._line_number,self._char_number)
				elif ch in string.digits + ".":
					self._current_token = Token("number",str(ch),self._line_number,self._char_number)
				elif ch == '"':
					self._current_token = Token("string","",self._line_number,self._char_number)
				elif ch == ';':
					self.tokens.append(Token("EOL",None,self._line_number,self._char_number))
				elif ch == ',':
					self.tokens.append(Token("separator",str(ch),self._line_number,self._char_number))
				elif ch in string.whitespace:
					self._current_token = Token("whitespace",str(ch),self._line_number,self._char_number)
					if ch == '\n':
						self._line_number += 1
						self._char_number = 0
				elif ch in ENCLOSED_TOKENS:
					self.tokens.append(Token("enclosed",str(ch),self._line_number,self._char_number))
				else:
					self._current_token = Token("other",str(ch),self._line_number,self._char_number)

			#CONTINUATION/ENDING OF A TOKEN
			else:
				if curtok.type == "comment":
					if ch == '\n':
						self._finish_token(False,False)
					else:
						curtok.value += ch
				elif curtok.type == "term":
					if ch in string.ascii_letters + "_" or ch in string.digits:
						curtok.value += ch
					else:
						self._finish_token()
				elif curtok.type == "number":
					if ch in string.digits + ".":
						curtok.value += ch
					else:
						self._finish_token()
				elif curtok.type == "whitespace":
					if ch in string.whitespace:
						curtok.value += ch
					else:
						self._finish_token(True,False)
				elif curtok.type == "string":
					if ch == '"':
						self._finish_token(False)
					else:
						curtok.value += ch
				elif curtok.type == "other":
					if ch in string.ascii_letters + "_" or ch in string.digits or ch in string.whitespace or \
						ch in ENCLOSED_TOKENS:
						self._finish_token()
					else:
						curtok.value += ch

			self._char_number += 1
			self._pos += 1

		if self._current_token != None:
			self._finish_token()