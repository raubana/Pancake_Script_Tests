import traceback, string, sys, os, time

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

		self.setup_main_gui()

		self.needs_to_compile = True
		self.running = False

		self.script = ""

		self.compiled_script = None#pancake.compiler.compile(self.script)
		self.interpreter = None#pancake.interpreter.Interpreter(self.compiled_script)

		self.last_highlighted_syntax = time.time()
		self.last_script_change = time.time()

		self.top.mainloop()

	def setup_main_gui(self):
		padding = 10

		element_color = "#1a1a1a"
		frame_color = "#4d4d4d"
		label_color = "#808080"

		self.top.option_add("*Font", "Tahoma")
		self.top.option_add("*Font", "Tahoma 16")
		self.top.option_add("*Background", element_color)
		self.top.option_add("*Frame.Background", frame_color)
		self.top.option_add("*Label.Background", frame_color)
		self.top.option_add("*Label.Foreground", label_color)
		self.top.option_add("*Checkbutton.Background", frame_color)
		self.top.option_add("*Button.Background", frame_color)
		self.top.option_add("*Foreground", "white")
		self.top.option_add("*selectBackground", "white")
		self.top.option_add("*selectForeground", "black")

		self.main = Tkinter.Frame(self.top)
		self.main.pack(expand=True, fill=Tkinter.BOTH)

		bottom_frame = Tkinter.Frame(self.main)
		bottom_frame.pack(expand=True, fill=Tkinter.BOTH)

		middle_frame = Tkinter.Frame(self.main)
		middle_frame.pack(expand=True, fill=Tkinter.BOTH, padx = padding)

		top_frame = Tkinter.Frame(self.main)
		top_frame.pack(expand=False, fill=Tkinter.BOTH, padx = padding, pady = padding)

		self.compile_button = Tkinter.Button(middle_frame, text="COMPILE", command=self.compile)
		self.compile_button.pack(side=Tkinter.LEFT)

		self.run_button = Tkinter.Button(middle_frame, text="RUN", command=self.do_next)
		self.run_button.config(state=Tkinter.DISABLED)
		self.run_button.pack(side=Tkinter.LEFT)

		self.continue_var = Tkinter.IntVar()
		self.continue_checkbutton = Tkinter.Checkbutton(middle_frame, text="Continue", variable=self.continue_var)
		self.continue_checkbutton.pack(side=Tkinter.LEFT)

		self.fast_var = Tkinter.IntVar()
		self.fast_checkbutton = Tkinter.Checkbutton(middle_frame, text="Fast", variable=self.fast_var)
		self.fast_checkbutton.pack(side=Tkinter.LEFT)

		self.stop_button = Tkinter.Button(middle_frame, text="STOP", command=self.stop)
		self.stop_button.config(state=Tkinter.DISABLED)
		self.stop_button.pack(side=Tkinter.LEFT)

		self.display_element = Tkinter.Text(top_frame)
		self.display_element.config(state=Tkinter.DISABLED)
		self.display_element.pack(expand=True, fill=Tkinter.BOTH)

		left_frame = Tkinter.Frame(bottom_frame)
		left_frame.config()
		left_frame.pack(fill=Tkinter.BOTH)

		middle_frame = Tkinter.Frame(bottom_frame)
		middle_frame.pack(side=Tkinter.LEFT, fill=Tkinter.Y, padx = padding, pady = padding)

		right_frame = Tkinter.Frame(bottom_frame)
		right_frame.pack(side=Tkinter.LEFT, expand=True, fill=Tkinter.BOTH, padx = padding, pady = padding)

		w = Tkinter.Label(middle_frame, text="COMPILED TOKENS:")
		w.pack()

		scrollbar = Tkinter.Scrollbar(middle_frame)
		scrollbar.pack(side=Tkinter.RIGHT, expand=True, fill=Tkinter.Y, padx = padding)

		self.tokens_frame = Tkinter.Listbox(middle_frame, selectmode=Tkinter.SINGLE, yscrollcommand=scrollbar.set)
		self.tokens_frame.pack(expand=True, fill=Tkinter.BOTH)

		scrollbar.config(command=self.tokens_frame.yview)

		w = Tkinter.Label(middle_frame, text="THE STACK:")
		w.pack()

		self.stack_element = Tkinter.Text(middle_frame, width=50, height=STACK_MAX)
		self.stack_element.config(state=Tkinter.DISABLED)
		self.stack_element.pack()

		w = Tkinter.Label(middle_frame, text="MEMORY:")
		w.pack()

		self.memory_element = Tkinter.Text(middle_frame, width=50, height=VAR_MAX)
		self.memory_element.config(state=Tkinter.DISABLED)
		self.memory_element.pack()

		self.script_element = Tkinter.Text(right_frame, wrap=Tkinter.NONE)
		self.script_element.config()
		self.script_element.pack(expand=True, fill=Tkinter.BOTH)
		self.script_element.bind("<KeyRelease>", self.on_script_change)

	def on_script_change(self, *args):
		if not self.running:
			new_script = self.get_script_text()
			if new_script != self.script:
				self.last_script_change = time.time()
				self.script = new_script
				self.set_needs_to_compile(True)
				self.highlight_syntax()

	def highlight_syntax(self):
		t = time.time()
		if t - self.last_highlighted_syntax > 0.2 and t - self.last_script_change > 0.2:
			self.last_highlighted_syntax = t

			tokenlist = pancake.compiler.tokenizer.tokenize(self.get_script_text(), True)
			try:
				pancake.compiler.op_finder.process(tokenlist, True)
				pancake.compiler.blocker.process(tokenlist)
				pancake.compiler.fnc_finder.process(tokenlist)
			except:
				pass

			self.script_element.tag_delete("token_term")
			self.script_element.tag_delete("token_string")
			self.script_element.tag_delete("token_op")
			self.script_element.tag_delete("token_number")
			self.script_element.tag_delete("token_function")
			self.script_element.tag_delete("token_bad")
			self.script_element.tag_delete("token_comment")

			self.script_element.tag_config("token_term", foreground="#bfbf00")
			self.script_element.tag_config("token_string", foreground="#20bf00")
			self.script_element.tag_config("token_op", foreground="#00afbf")
			self.script_element.tag_config("token_number", foreground="#bf7000")
			self.script_element.tag_config("token_function", foreground="#00bf50")
			self.script_element.tag_config("token_bad", foreground="#ff0000")
			self.script_element.tag_config("token_comment", foreground="#808080")

			for token in tokenlist.tokens:
				tag = None
				start_line = token.line_number
				start_char = token.char_number-1
				length = len(token.value) or 0
				if token.type == TYPE_TERM:
					tag = "token_term"
				elif token.type == TYPE_FUNCTION:
					tag = "token_function"
				elif token.type == TYPE_OPERATOR:
					tag = "token_op"
				elif token.type == TYPE_NUMBER:
					tag = "token_number"
				elif token.type == TYPE_STRING:
					tag = "token_string"
					length += 2
				elif token.type == TYPE_COMMENT:
					tag = "token_comment"
				elif token.type == TYPE_NULL:
					tag = "token_bad"

				if tag is not None:
					self.place_tag(self.script_element, tag, start_line, start_char, length)
		else:
			self.top.after(50, self.highlight_syntax)

	def place_tag(self, element, tag_name, line_number, char_number, length):
		element.tag_add(tag_name,
									"{line}.{ch}".format(line=line_number, ch=char_number),
									"{line}.{ch}".format(line=line_number, ch=char_number + length))

	def get_script_text(self):
		data = str(self.script_element.get("1.0", "1000000000.0"))
		data = data.strip()
		return data

	def setup_token_elements(self):
		self.tokens_frame.delete(0,Tkinter.END)
		i = 0
		for token in self.compiled_script.tokens:
			self.tokens_frame.insert(Tkinter.END, str(i) + "   " + str(token))
			i += 1

	def set_needs_to_compile(self, state):
		if state != self.needs_to_compile:
			self.needs_to_compile = state
			if state:
				self.compile_button.config(state=Tkinter.NORMAL)
				self.run_button.config(state=Tkinter.DISABLED)
			else:
				self.compile_button.config(state=Tkinter.DISABLED)
				self.run_button.config(state=Tkinter.NORMAL)

	def set_running(self, state):
		if state != self.running:
			self.running = state
			if state:
				self.script_element.config(state=Tkinter.DISABLED)
				self.stop_button.config(state=Tkinter.NORMAL)
				if self.continue_var.get():
					self.run_button.config(state=Tkinter.DISABLED)
			else:
				self.script_element.config(state=Tkinter.NORMAL)
				self.stop_button.config(state=Tkinter.DISABLED)
				self.run_button.config(state=Tkinter.NORMAL)

	def stop(self):
		if self.running:
			self.script_element.tag_delete("highlight")
			self.interpreter = None
			self.set_running(False)

	def compile(self):
		if self.needs_to_compile:
			self.display_element.config(state=Tkinter.NORMAL)
			self.display_element.delete(1.0, Tkinter.END)
			try:
				self.compiled_script = pancake.compiler.compile(self.get_script_text())
				self.setup_token_elements()
				self.set_needs_to_compile(False)
			except Exception as e:
				if not str(e).startswith("ERROR:"):
					traceback.print_exc()
					self.display_element.insert(Tkinter.END, "Some error occured. Please see the python console.")
				else:
					self.display_element.insert(Tkinter.END, str(e.message))

			self.display_element.config(state=Tkinter.DISABLED)

	def analyze(self):
		cur_tok = self.interpreter.current_token
		if cur_tok is not None:
			if cur_tok.type == TYPE_CALL:
				cur_tok = cur_tok.value[1]

		#first we highlight the portion of the script being executed.
		self.script_element.tag_delete("highlight")
		if cur_tok is not None and cur_tok.line_number is not None:
			line_num = cur_tok.line_number
			char_num = cur_tok.char_number-1
			length = len(cur_tok.value)
			if cur_tok.type == TYPE_STRING:
				length += 2
			self.script_element.see("{line}.{ch}".format(line=line_num, ch=char_num))
			self.place_tag(self.script_element, "highlight", line_num, char_num, length)
			self.script_element.tag_config("highlight", background="yellow", foreground="black")

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
		if self.interpreter is None:
			self.interpreter = pancake.interpreter.Interpreter(self.compiled_script)
			self.set_running(True)
			self.display_element.config(state=Tkinter.NORMAL)
			self.display_element.delete(1.0, Tkinter.END)
			self.display_element.config(state=Tkinter.DISABLED)

		if self.interpreter.eof:
			self.stop()
		else:
			try:
				self.interpreter.process_one()
				self.analyze()

				if bool(self.continue_var.get()):
					self.run_button.config(state=Tkinter.DISABLED)
					delay = 500
					if bool(self.fast_var.get()):
						delay = 1
					self.top.after(delay, self._continue)
			except Exception as e:
				self.display_element.config(state=Tkinter.NORMAL)
				if not str(e).startswith("ERROR:"):
					traceback.print_exc()
					self.display_element.insert(Tkinter.END, "Some error occured. Please see the python console.")
				else:
					self.display_element.insert(Tkinter.END, str(e.message))
				self.display_element.config(state=Tkinter.DISABLED)

				self.stop()

	def _continue(self):
		if bool(self.continue_var.get()) and self.running:
			self.do_next()
		else:
			self.run_button.config(state=Tkinter.NORMAL)


try:
	main = Main()
except Exception, e:
	print traceback.format_exc()
	input("Press enter to quit.")