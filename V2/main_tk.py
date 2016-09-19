import traceback, string

try:
	import Tkinter
	import tkMessageBox
except Exception, e:
	print traceback.format_exc()
	input("Press enter to quit.")


import pancake.compiler, pancake.interpreter
from pancake.constants import *


class Main(object):
	def __init__(self):
		self.top = Tkinter.Tk()

		self.top.option_add("*Font", "Tahoma")
		self.top.option_add("*Font", "Tahoma 18")
		self.top.option_add("*Background", "black")
		self.top.option_add("*Foreground", "white")
		self.top.option_add("*selectBackground", "white")
		self.top.option_add("*selectForeground", "black")

		self.setup_main_gui()

		self.script_name = "lerp.txt"

		f = open(self.script_name)
		self.script = f.read()

		self.set_text(self.script_element, self.script)
		self.compiled_script = pancake.compiler.compile(self.script)

		self.token_elements = []
		self.setup_token_elements()

		self.interpreter = pancake.interpreter.Interpreter(self.compiled_script)

		self.analyze()

		self.top.mainloop()

	def setup_main_gui(self):
		self.main = Tkinter.Frame(self.top)
		self.main.pack(expand=True, fill=Tkinter.BOTH)

		bottom_frame = Tkinter.Frame(self.main)
		bottom_frame.pack(expand=True, fill=Tkinter.BOTH)

		middle_frame = Tkinter.Frame(self.main)
		middle_frame.pack(expand=True, fill=Tkinter.BOTH)

		top_frame = Tkinter.Frame(self.main)
		top_frame.pack(expand=False, fill=Tkinter.BOTH)

		self.next_button = Tkinter.Button(middle_frame, text="NEXT", command=self.do_next)
		self.next_button.pack(side=Tkinter.LEFT)

		self.continue_var = Tkinter.IntVar()
		self.continue_checkbutton = Tkinter.Checkbutton(middle_frame, text="Continue", variable=self.continue_var)
		self.continue_checkbutton.pack(side=Tkinter.LEFT)

		self.fast_var = Tkinter.IntVar()
		self.fast_checkbutton = Tkinter.Checkbutton(middle_frame, text="Fast", variable=self.fast_var)
		self.fast_checkbutton.pack(side=Tkinter.LEFT)

		#w = Tkinter.Label(top_frame, text="SOURCE SCRIPT:")
		#w.pack()

		self.display_element = Tkinter.Text(top_frame)
		self.display_element.config(state=Tkinter.DISABLED)
		self.display_element.pack(expand=True, fill=Tkinter.BOTH)

		left_frame = Tkinter.Frame(bottom_frame)
		left_frame.config()
		left_frame.pack(fill=Tkinter.BOTH)

		middle_frame = Tkinter.Frame(bottom_frame)
		middle_frame.pack(side=Tkinter.LEFT, fill=Tkinter.Y)

		right_frame = Tkinter.Frame(bottom_frame)
		right_frame.pack(side=Tkinter.LEFT, expand=True, fill=Tkinter.BOTH)

		w = Tkinter.Label(middle_frame, text="COMPILED TOKENS:")
		w.pack()

		scrollbar = Tkinter.Scrollbar(middle_frame)
		scrollbar.pack(side=Tkinter.RIGHT, expand=True, fill=Tkinter.Y)

		self.tokens_frame = Tkinter.Listbox(middle_frame, selectmode=Tkinter.SINGLE, yscrollcommand=scrollbar.set)
		self.tokens_frame.pack(expand=True, fill=Tkinter.BOTH)

		scrollbar.config(command=self.tokens_frame.yview)

		w = Tkinter.Label(middle_frame, text="THE STACK:")
		w.pack()

		self.stack_element = Tkinter.Text(middle_frame, width=50, height=STACK_MAX)
		self.stack_element.config()
		self.stack_element.pack()

		w = Tkinter.Label(middle_frame, text="MEMORY:")
		w.pack()

		self.memory_element = Tkinter.Text(middle_frame, width=50, height=VAR_MAX)
		self.memory_element.config()
		self.memory_element.pack()

		self.script_element = Tkinter.Text(right_frame, wrap=Tkinter.NONE)
		self.script_element.config()
		self.script_element.pack(expand=True, fill=Tkinter.BOTH)

	def setup_token_elements(self):
		i = 0
		for token in self.compiled_script.tokens:
			self.tokens_frame.insert(Tkinter.END, str(i) + "      " + str(token))
			i += 1

	def analyze(self):
		#first we highlight the portion of the script being executed.
		self.script_element.tag_delete("highlight")
		if self.interpreter.current_token is not None and self.interpreter.current_token.line_number is not None:
			line_num = self.interpreter.current_token.line_number
			char_num = self.interpreter.current_token.char_number-1
			length = len(str(self.interpreter.current_token.value))
			if self.interpreter.current_token.type == TYPE_STRING:
				length += 2
			self.script_element.see("{line}.{ch}".format(line=line_num, ch=char_num))
			self.script_element.tag_add("highlight",
										"{line}.{ch}".format(line=line_num, ch=char_num),
										"{line}.{ch}".format(line=line_num, ch=char_num+length))
			self.script_element.tag_config("highlight", background="white", foreground="black")

		#next we show which token just ran and which token will run next.
		i = self.interpreter.cursor
		i2 = self.interpreter.next_cursor
		if i is not None:
			self.tokens_frame.see(i)
			self.tokens_frame.selection_clear(0,len(self.compiled_script.tokens))
			self.tokens_frame.selection_set(i)
		if i2 is not None:
			self.tokens_frame.activate(i2)

		#next we set the stack
		stack_text = ""
		for x in self.interpreter.stack:
			stack_text += str(x) + "\n"
		self.set_text(self.stack_element, stack_text)

		# next we set the memory
		stack_text = ""
		for key in self.interpreter.variables:
			stack_text += str(key) + " : " + str(self.interpreter.variables[key]) + "\n"
		self.set_text(self.memory_element, stack_text)

		# next we print
		if len(self.interpreter.print_buffer) > 0:
			self.display_element.config(state=Tkinter.NORMAL)
			for i in xrange(len(self.interpreter.print_buffer)):
				line = self.interpreter.print_buffer[i]
				self.display_element.insert(Tkinter.INSERT, line + "\n")
			self.display_element.see(Tkinter.END)
			self.display_element.config(state=Tkinter.DISABLED)

	def set_text(self, element, text):
		element.config(state=Tkinter.NORMAL)
		element.delete(1.0, Tkinter.END)
		lines = text.split("\n")
		for i in xrange(len(lines)):
			line = lines[i]
			if i != len(lines) - 1:
				line += "\n"
			element.insert(Tkinter.INSERT, line)
		element.config(state=Tkinter.DISABLED)

	def do_next(self):
		self.interpreter.process_one()
		self.analyze()

		if bool(self.continue_var.get()):
			self.next_button.config(state=Tkinter.DISABLED)
			delay = 500
			if bool(self.fast_var.get()):
				delay = 1
			self.top.after(delay, self._continue)

	def _continue(self):
		if bool(self.continue_var.get()):
			self.do_next()
		else:
			self.next_button.config(state=Tkinter.ACTIVE)


try:
	main = Main()
except Exception, e:
	print traceback.format_exc()
	input("Press enter to quit.")