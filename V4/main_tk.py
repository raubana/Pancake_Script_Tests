import traceback, string, sys, os, time

try:
	import Tkinter
	import tkMessageBox
except Exception, e:
	print traceback.format_exc()
	input("Press enter to quit.")


import pancake.compiler, pc_code.interpreter
from pancake.compiler.constants import *
from pc_code.constants import *


class Main(object):
	def __init__(self):
		self.top = Tkinter.Tk()

		self.setup_main_gui()

		self.needs_to_compile = True
		self.running = False

		self.script = ""

		self.generated_script = None
		self.compiled_script = None
		self.interpreter = None

		self.last_highlighted_syntax = time.time()
		self.last_script_change = time.time()

		self.top.mainloop()

	def setup_main_gui(self):
		padding = 10

		element_color = "#1a1a1a"
		frame_color = "#4d4d4d"
		label_color = "#808080"

		self.top.option_add("*Font", "Consolas")
		self.top.option_add("*Font", "Consolas 18")
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

		top_frame = Tkinter.Frame(self.main)
		top_frame.pack(expand=False, fill=Tkinter.BOTH)

		middle_frame = Tkinter.Frame(self.main)
		middle_frame.pack(expand=True, fill=Tkinter.BOTH, padx = padding)

		bottom_frame = Tkinter.Frame(self.main)
		bottom_frame.pack(expand=True, fill=Tkinter.BOTH, padx = padding, pady = padding)

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

		self.display_element = Tkinter.Text(bottom_frame)
		self.display_element.config(state=Tkinter.DISABLED)
		self.display_element.pack(expand=True, fill=Tkinter.BOTH)

		left_frame = Tkinter.Frame(top_frame)
		left_frame.pack(side=Tkinter.LEFT, fill=Tkinter.Y, padx = padding, pady = padding)

		center_frame = Tkinter.Frame(top_frame)
		center_frame.pack(side=Tkinter.LEFT, fill=Tkinter.Y, pady = padding)

		right_frame = Tkinter.Frame(top_frame)
		right_frame.pack(side=Tkinter.LEFT, expand=True, fill=Tkinter.BOTH, padx = padding, pady = padding)

		w = Tkinter.Label(center_frame, text="COMPILED TOKENS:")
		w.pack()

		self.tokens_scrollbar = Tkinter.Scrollbar(center_frame)
		self.tokens_scrollbar.pack(side=Tkinter.RIGHT, expand=True, fill=Tkinter.Y, padx = padding)

		self.tokens_element = Tkinter.Text(center_frame, width=25, wrap=Tkinter.NONE, yscrollcommand=self.tokens_scrollbar.set)
		self.tokens_element.config(state=Tkinter.DISABLED)
		self.tokens_element.pack(expand=True, fill=Tkinter.BOTH)

		self.tokens_scrollbar.config(command=self.tokens_element.yview)

		w = Tkinter.Label(left_frame, text="THE STACK:")
		w.pack()

		self.stack_element = Tkinter.Text(left_frame, width=20, height=STACK_SIZE)
		self.stack_element.config(state=Tkinter.DISABLED)
		self.stack_element.pack()

		w = Tkinter.Label(left_frame, text="MEMORY:")
		w.pack()

		self.memory_element = Tkinter.Text(left_frame, width=20, height=MEMORY_SIZE)
		self.memory_element.config(state=Tkinter.DISABLED)
		self.memory_element.pack()

		self.script_scrollbar = Tkinter.Scrollbar(right_frame)
		self.script_scrollbar.pack(side=Tkinter.RIGHT, expand=True, fill=Tkinter.Y, padx=padding)

		self.script_element = Tkinter.Text(right_frame, wrap=Tkinter.NONE, yscrollcommand=self.script_scrollbar.set)
		self.script_element.config()
		self.script_element.pack(expand=True, fill=Tkinter.BOTH)
		self.script_element.bind("<KeyRelease>", self.on_script_change)

		self.script_scrollbar.config(command=self.script_element.yview)



	def on_script_change(self, *args):
		if not self.running:
			new_script = self.get_script_text()
			if new_script != self.script:
				self.last_script_change = time.time()
				self.script = new_script
				self.set_needs_to_compile(True)
				self.highlight_syntax()

	def highlight_syntax(self):
		ti = time.time()
		if ti - self.last_highlighted_syntax > 0.2 and ti - self.last_script_change > 0.2:
			self.last_highlighted_syntax = ti

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
			self.script_element.tag_delete("token_literal")
			self.script_element.tag_delete("token_function")
			self.script_element.tag_delete("token_bad")
			self.script_element.tag_delete("token_comment")

			self.script_element.tag_config("token_term", foreground="#bfbf00")
			self.script_element.tag_config("token_string", foreground="#20bf00")
			self.script_element.tag_config("token_op", foreground="#00afbf")
			self.script_element.tag_config("token_literal", foreground="#bf7000")
			self.script_element.tag_config("token_function", foreground="#00bf50")
			self.script_element.tag_config("token_bad", foreground="#ff0000")
			self.script_element.tag_config("token_comment", foreground="#808080")

			for token in tokenlist.tokens:
				t = token.type
				v = token.value

				tag = None
				start_line = token.line_number
				start_char = token.char_number-1

				if t == TYPE_OPERATOR:
					length = len(v.symbol)
				else:
					length = len(str(v))

				if t == TYPE_TERM:
					tag = "token_term"
				elif t == TYPE_FUNCTION:
					tag = "token_function"
				elif t == TYPE_OPERATOR:
					tag = "token_op"
				elif t == TYPE_STRING:
					tag = "token_string"
					length += 2
				elif t in LITERAL_TYPES:
					tag = "token_literal"
				elif t == TYPE_COMMENT:
					tag = "token_comment"
				elif t == TYPE_NULL:
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
		data = str(self.script_element.get("1.0", Tkinter.END))
		data = data.strip()
		return data

	def setup_token_elements(self):
		self.tokens_element.config(state=Tkinter.NORMAL)
		self.tokens_element.delete("1.0", Tkinter.END)
		i = 0
		for token in string.split( self.generated_script, "\n" ):
			self.tokens_element.insert(Tkinter.END, str(i) + "   " + str(token) + "\n")
			i += 1
		self.tokens_element.config(state=Tkinter.DISABLED)

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
			self.script_element.tag_delete("current_line")
			self.script_element.tag_delete("next_line")
			self.tokens_element.tag_delete("current_line")
			self.tokens_element.tag_delete("next_line")
			self.interpreter = None
			self.set_running(False)

	def compile(self):
		if self.needs_to_compile:
			self.display_element.config(state=Tkinter.NORMAL)
			self.display_element.delete(1.0, Tkinter.END)
			try:
				self.compiled_script = pancake.compiler.compile(self.get_script_text())
				self.generated_script = pancake.compiler.generate(self.compiled_script)
				self.setup_token_elements()
				self.set_needs_to_compile(False)
			except Exception as e:
				if not str(e).startswith("ERROR:"):
					traceback.print_exc()
					self.display_element.insert(Tkinter.END, "Some error occurred. Please see the python console.")
				else:
					self.display_element.insert(Tkinter.END, str(e.message))

			self.display_element.config(state=Tkinter.DISABLED)

	def analyze(self):
		i = self.interpreter.current_line_index
		i2 = self.interpreter.next_line_index


		cur_tok = None
		next_tok = None

		# I'm lazy...
		try: cur_tok = self.compiled_script.tokens[i]
		except: pass
		try: next_tok = self.compiled_script.tokens[i2]
		except: pass

		#first we highlight the portion of the script being executed.
		self.script_element.tag_delete("current_line")
		self.script_element.tag_delete("next_line")
		self.script_element.tag_config("current_line", background="white", foreground="black")
		self.script_element.tag_config("next_line", background="#808080")

		if cur_tok is not None and cur_tok.line_number is not None:
			line_num = cur_tok.line_number
			char_num = cur_tok.char_number-1
			length = 0
			if cur_tok.type == TYPE_ASSIGN:
				length = 1
			elif cur_tok.type == TYPE_BOOLEAN:
				length = len(str(cur_tok.value))
			else:
				length = len(cur_tok.value)
				if cur_tok.type == TYPE_STRING:
					length += 2
			self.script_element.see("{line}.{ch}".format(line=line_num, ch=char_num))
			self.place_tag(self.script_element, "current_line", line_num, char_num, length)

		# Then we highlight the portion of the scrip that will execute next.
		if next_tok is not None and next_tok.line_number is not None:
			line_num = next_tok.line_number
			char_num = next_tok.char_number-1
			length = 0
			if next_tok.type == TYPE_ASSIGN:
				length = 1
			elif next_tok.type == TYPE_BOOLEAN:
				length = len(str(next_tok.value))
			else:
				length = len(next_tok.value)
				if next_tok.type == TYPE_STRING:
					length += 2
			self.script_element.see("{line}.{ch}".format(line=line_num, ch=char_num))
			self.place_tag(self.script_element, "next_line", line_num, char_num, length)

		#next we show which token just ran and which token will run next.
		self.tokens_element.tag_delete("current_line")
		self.tokens_element.tag_delete("next_line")
		self.tokens_element.tag_config("current_line", background="white", foreground="black")
		self.tokens_element.tag_config("next_line", background="#808080")
		if i is not None:
			self.tokens_element.see("{line}.{ch}".format(line=i+1, ch=0))
			self.place_tag(self.tokens_element, "current_line", i+1, 0, 1000)
		if i2 is not None:
			self.place_tag(self.tokens_element, "next_line", i2+1, 0, 1000)

		#next we set the stack
		stack_text = ""
		for x in self.interpreter.stack:
			stack_text += str(x) + "\n"
		self.set_text(self.stack_element, stack_text)

		# next we set the memory
		stack_text = ""
		for key in self.interpreter.memory:
			stack_text += str(key) + " : " + str(self.interpreter.memory[key]) + "\n"
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
			self.interpreter = pc_code.interpreter.Interpreter(self.generated_script)
			self.set_running(True)
			self.display_element.config(state=Tkinter.NORMAL)
			self.display_element.delete(1.0, Tkinter.END)
			self.display_element.config(state=Tkinter.DISABLED)

		if not self.interpreter.running:
			self.stop()
		else:
			try:
				self.interpreter.go_to_next_line()
				self.analyze()
				if self.interpreter.running:
					self.interpreter.process_current_line()
					self.analyze()

					if bool(self.continue_var.get()):
						self.run_button.config(state=Tkinter.DISABLED)
						delay = 500
						if bool(self.fast_var.get()):
							delay = 1
						self.top.after(delay, self._continue)
				else:
					self.stop()
			except Exception as e:
				self.display_element.config(state=Tkinter.NORMAL)
				traceback.print_exc()
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