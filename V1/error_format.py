
def error_format(token, message):
	if token is None:
		raise Exception("ERROR: {message}".format(message=message))
	raise Exception("ERROR: Line {line}, Char {char}: {message}".format(
			line=token.line_number,
			char=token.char_number,
			message=message
		)
	)