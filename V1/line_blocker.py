"""
The purpose of the line blocker is to take the tokens from the blocker and move each "line" into their own block.
"""

from error_format import error_format
from blocker import Block

class LineBlocker(object):
	def __init__(self, block):
		self.output_block = self._block_off_lines(block)

	def _block_off_lines(self, input_block):
		output_block = Block()
		output_block.enclosed_type = input_block.enclosed_type

		current_block = Block()

		for token in input_block.tokens:
			if token.type == "EOL":
				output_block.append(current_block)
				current_block = Block()
			elif token.type == "block":
				current_block.append(self._block_off_lines(token))
			else:
				current_block.append(token)

		if len(current_block.tokens) > 0:
			output_block.append(current_block)

		return output_block