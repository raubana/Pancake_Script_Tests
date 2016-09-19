from constants import *


def error_format(token, message):
	if token is None:
		raise Exception("ERROR: {message}".format(message=message))
	line_number = token.line_number
	char_number = token.char_number
	if token.type == TYPE_CALL:
		line_number = token.value[1].line_number
		char_number = token.value[1].char_number
	raise Exception("ERROR: Line {line}, Char {char}: {message}".format(
			line=line_number,
			char=char_number,
			message=message
		)
	)