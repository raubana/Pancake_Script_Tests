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
		self.root = Tkinter.Tk()
		self.root.wm_title("Pancake Script Editor")

		self.setup_main_gui()

		self.needs_to_compile = True
		self.running = False

		self.speed = 0

		self.script = ""

		self.generated_script = None
		self.compiled_script = None
		self.interpreter = None

		self.last_highlighted_syntax = time.time()
		self.last_script_change = time.time()

		self.root.mainloop()

	def create_scrollable_text_element(self, label, parent, column, row, columnspan=1, rowspan=1):
		frame = Tkinter.LabelFrame(parent, text=label, bg=self.frame_color, padx=10, pady=10, borderwidth=0)
		frame.grid(column=column, row=row, columnspan=columnspan, rowspan=rowspan, sticky=Tkinter.W+Tkinter.E+Tkinter.N+Tkinter.S)

		frame.columnconfigure(0, weight=1)
		frame.columnconfigure(1, weight=0)

		frame.rowconfigure(0, weight=1)
		frame.rowconfigure(1, weight=0)

		text_element = Tkinter.Text(frame, state=Tkinter.DISABLED, wrap=Tkinter.NONE, width=0, height=0)
		xscrollbar = Tkinter.Scrollbar(frame, orient=Tkinter.HORIZONTAL)
		yscrollbar = Tkinter.Scrollbar(frame)

		text_element.config(
			xscrollcommand=xscrollbar.set,
			yscrollcommand=yscrollbar.set
		)

		xscrollbar.config(command=text_element.xview)
		yscrollbar.config(command=text_element.yview)

		text_element.grid(column=0, row=0, sticky=Tkinter.W+Tkinter.E+Tkinter.N+Tkinter.S)
		xscrollbar.grid(column=0, row=1, sticky=Tkinter.W+Tkinter.E)
		yscrollbar.grid(column=1, row=0, sticky=Tkinter.N+Tkinter.S)

		return text_element

	def setup_main_gui(self):
		padding = 10

		self.element_color = "#1a1a1a"
		self.frame_color = "#4d4d4d"
		self.label_color = "#808080"

		self.root.option_add("*Font", "Consolas")
		self.root.option_add("*Font", "Consolas 12 bold")
		self.root.option_add("*Background", self.element_color)
		self.root.option_add("*Frame.Background", self.frame_color)
		self.root.option_add("*Label.Background", self.frame_color)
		self.root.option_add("*Label.Foreground", self.label_color)
		self.root.option_add("*Checkbutton.Background", self.frame_color)
		self.root.option_add("*Button.Background", self.frame_color)
		self.root.option_add("*Foreground", "white")
		self.root.option_add("*selectBackground", "white")
		self.root.option_add("*selectForeground", "black")

		self.root.config(padx=10, pady=10, bg=self.frame_color)

		self.root.columnconfigure(0, weight=3, pad=10)
		self.root.columnconfigure(1, weight=1, pad=10)
		self.root.columnconfigure(2, weight=1, pad=10)

		self.root.rowconfigure(0, weight=1)
		self.root.rowconfigure(1, weight=1)
		self.root.rowconfigure(2, weight=0)
		self.root.rowconfigure(3, weight=0)
		self.root.rowconfigure(4, weight=1)

		self.script_element = self.create_scrollable_text_element("Editor", self.root, 0, 0, 1, 3)
		self.script_element.config(state=Tkinter.NORMAL)
		self.script_element.bind("<KeyRelease>", self.on_script_change)

		self.tokens_element = self.create_scrollable_text_element("Tokens", self.root, 1, 0, 1, 3)

		self.stack_element = self.create_scrollable_text_element("Stack", self.root, 2, 0, 1, 1)

		self.ram_element = self.create_scrollable_text_element("RAM", self.root, 2, 1, 1, 1)

		self.memory_frame = Tkinter.LabelFrame(self.root, text="Memory", bg=self.frame_color, borderwidth=0)
		self.memory_frame.grid(column=2, row=2, sticky=Tkinter.W+Tkinter.E+Tkinter.N+Tkinter.S)

		self.memory_frame.columnconfigure(0, weight=1)
		self.memory_frame.rowconfigure(0, weight=1)

		if True:
			self.memory_label_text = Tkinter.StringVar()
			self.memory_label = Tkinter.Label(self.memory_frame, textvariable=self.memory_label_text, width=20)
			self.memory_label_text.set("0/" + str(MEMORY_SIZE) + " bytes")
			self.memory_label.grid(sticky=Tkinter.W+Tkinter.E+Tkinter.N+Tkinter.S)

		self.buttons_frame = Tkinter.Frame(self.root, bg=self.frame_color)
		self.buttons_frame.grid(column=0, row=3, columnspan=3, sticky=Tkinter.W+Tkinter.E+Tkinter.N+Tkinter.S)

		if True:
			self.compile_button = Tkinter.Button(self.buttons_frame, text="COMPILE", command=self.compile)
			self.compile_button.grid(column=0, row=0, padx=5)

			self.run_button = Tkinter.Button(self.buttons_frame, text="RUN", command=self.do_next)
			self.run_button.config(state=Tkinter.DISABLED)
			self.run_button.grid(column=1, row=0, padx=5)

			self.continue_var = Tkinter.IntVar()
			self.continue_checkbutton = Tkinter.Checkbutton(self.buttons_frame, text="Continue", variable=self.continue_var)
			self.continue_checkbutton.grid(column=2, row=0, padx=5)

			self.slower_button = Tkinter.Button(self.buttons_frame, text="<", command=self.slower)
			self.slower_button.grid(column=3, row=0, padx=5)

			self.speed_label = Tkinter.Label(self.buttons_frame, text="0")
			self.speed_label.grid(column=4, row=0, padx=5)

			self.faster_button = Tkinter.Button(self.buttons_frame, text=">", command=self.faster)
			self.faster_button.grid(column=5, row=0, padx=5)

			self.stop_button = Tkinter.Button(self.buttons_frame, text="STOP", command=self.stop)
			self.stop_button.config(state=Tkinter.DISABLED)
			self.stop_button.grid(column=6, row=0, padx=50)

		self.output_element = self.create_scrollable_text_element("Output", self.root, 0, 4, 3, 1)

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
				pancake.compiler.blocker.process(tokenlist)
				pancake.compiler.fnc_finder.process(tokenlist)
				pancake.compiler.op_finder.process(tokenlist, True)
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

				length = token.length

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
			self.root.after(50, self.highlight_syntax)

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
				self.run_button.config(state=Tkinter.DISABLED, bg=self.frame_color)
			else:
				self.compile_button.config(state=Tkinter.DISABLED)
				self.run_button.config(state=Tkinter.NORMAL, bg="dark green")

	def set_running(self, state):
		if state != self.running:
			self.running = state
			if state:
				self.script_element.config(state=Tkinter.DISABLED)
				self.stop_button.config(state=Tkinter.NORMAL, bg="dark red")
				if self.continue_var.get():
					self.run_button.config(state=Tkinter.DISABLED)
			else:
				self.script_element.config(state=Tkinter.NORMAL)
				self.stop_button.config(state=Tkinter.DISABLED, bg=self.frame_color)
				self.run_button.config(state=Tkinter.NORMAL)

	def faster(self):
		self.speed = min(self.speed+1,16)
		self.update_speed_label()

	def slower(self):
		self.speed = max(self.speed-1,0)
		self.update_speed_label()

	def update_speed_label(self):
		self.speed_label.config(text = str(self.speed))

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
			self.output_element.config(state=Tkinter.NORMAL)
			self.output_element.delete(1.0, Tkinter.END)
			try:
				self.compiled_script = pancake.compiler.compile(self.get_script_text())
				self.generated_script = pancake.compiler.generate(self.compiled_script)
				self.setup_token_elements()
				self.set_needs_to_compile(False)
			except Exception as e:
				if not str(e).startswith("ERROR:"):
					traceback.print_exc()
					self.output_element.insert(Tkinter.END, "Some error occurred. Please see the python console.")
				else:
					self.output_element.insert(Tkinter.END, str(e.message))

			self.output_element.config(state=Tkinter.DISABLED)

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
			length = cur_tok.length
			if cur_tok.type == TYPE_STRING:
				length += 2
			self.script_element.see("{line}.{ch}".format(line=line_num, ch=char_num))
			self.place_tag(self.script_element, "current_line", line_num, char_num, length)

		# Then we highlight the portion of the scrip that will execute next.
		if next_tok is not None and next_tok.line_number is not None:
			line_num = next_tok.line_number
			char_num = next_tok.char_number-1
			length = next_tok.length
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
			stack_text += repr(x) + "\n"
		self.set_text(self.stack_element, stack_text)

		# next we set the ram
		stack_text = ""
		for key in self.interpreter.ram:
			stack_text += str(key) + " : " + repr(self.interpreter.ram[key]) + "\n"
		self.set_text(self.ram_element, stack_text)

		# next we set the memory
		self.memory_label_text.set(str(self.interpreter.memory)+"/"+str(MEMORY_SIZE)+" bytes")

	def analyze_output(self):
		# next we print
		if len(self.interpreter.print_buffer) > 0:
			self.output_element.config(state=Tkinter.NORMAL)
			for i in xrange(len(self.interpreter.print_buffer)):
				line = self.interpreter.print_buffer[i]
				self.output_element.insert(Tkinter.INSERT, line + "\n")
			self.output_element.see(Tkinter.END)
			self.output_element.config(state=Tkinter.DISABLED)

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
			self.output_element.config(state=Tkinter.NORMAL)
			self.output_element.delete(1.0, Tkinter.END)
			self.output_element.config(state=Tkinter.DISABLED)

		iterations = 2.0 ** (self.speed - 10)
		delay = max(int(1.0 / iterations),1)
		iterations = max(int(iterations),1)

		if not bool(self.continue_var.get()):
			iterations = 1

		while self.interpreter is not None and self.interpreter.running and iterations > 0:
			try:
				self.interpreter.go_to_next_line()
				self.analyze_output()
				self.analyze()
				if self.interpreter.running:
					self.interpreter.process_current_line()
					self.analyze_output()

					iterations -= 1
					if iterations <= 0:
						self.analyze()
				else:
					self.stop()
			except Exception as e:
				self.output_element.config(state=Tkinter.NORMAL)
				traceback.print_exc()
				self.output_element.insert(Tkinter.END, str(e.message))
				self.output_element.config(state=Tkinter.DISABLED)

				self.analyze()
				self.analyze_output()
				self.stop()

		if self.interpreter is not None and self.interpreter.running:
			if bool(self.continue_var.get()):
				self.run_button.config(state=Tkinter.DISABLED)
				self.root.after(delay, self._continue)
		else:
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