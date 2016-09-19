
import string
from firsttokenizer import FirstTokenizer
from blocker import Blocker
from line_blocker import LineBlocker
from opfinder import OpFinder
from fncfinder import FncFinder
from shunter import Shunter
from gotoifyer import GoToIfyer


class Compiler(object):
	@staticmethod
	def compile_script(script):
		first_tokenizer = FirstTokenizer(script)
		OpFinder(first_tokenizer.tokens)

		blocker = Blocker(first_tokenizer.tokens)
		line_blocker = LineBlocker(blocker.block)

		FncFinder(line_blocker.output_block.tokens)
		shunter = Shunter(line_blocker.output_block)

		GoToIfyer(shunter.output_block)

		return shunter.output_block