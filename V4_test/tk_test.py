import traceback, string, sys, os, time

try:
	import Tkinter
	import tkMessageBox
except Exception, e:
	print traceback.format_exc()
	input("Press enter to quit.")


from interpreter import *


class Main(object):
	def __init__(self):
		self.top = Tkinter.Tk()

		self.setup_main_gui()

		self.running = False

		self.script = ""

		self.interpreter = None

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

		self.run_button = Tkinter.Button(middle_frame, text="RUN", command=self.do_next)
		self.run_button.config(state=Tkinter.NORMAL)
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

		w = Tkinter.Label(middle_frame, text="THE STACK:")
		w.pack()

		self.stack_element = Tkinter.Text(middle_frame, width=50, height=STACK_SIZE)
		self.stack_element.config(state=Tkinter.DISABLED)
		self.stack_element.pack()

		w = Tkinter.Label(middle_frame, text="MEMORY:")
		w.pack()

		self.memory_element = Tkinter.Text(middle_frame, width=50, height=MEMORY_SIZE)
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

	def place_tag(self, element, tag_name, line_number, char_number, length):
		element.tag_add(tag_name,
									"{line}.{ch}".format(line=line_number, ch=char_number),
									"{line}.{ch}".format(line=line_number, ch=char_number + length))

	def get_script_text(self):
		data = str(self.script_element.get("1.0", "1000000000.0"))
		data = data.strip()
		return data

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
			self.script_element.tag_delete("running")
			self.script_element.tag_delete("next_to_run")
			self.interpreter = None
			self.set_running(False)

	def analyze(self):
		#first we highlight the portion of the script being executed.
		self.script_element.tag_delete("running")
		line_num = self.interpreter.current_line_index
		if line_num is not None and line_num >= 0 and line_num < len(self.interpreter.script):
			current_line = self.interpreter.script[line_num]
			line_length = len(current_line)

			self.script_element.see("{line}.{ch}".format(line=line_num + 1, ch=0))
			self.place_tag(self.script_element, "running", line_num + 1, 0, line_length)
			self.script_element.tag_config("running", background="WHITE", foreground="black")

		# then we highlight the portion of the script to execute next, if there is one.
		self.script_element.tag_delete("next_to_run")
		line_num = self.interpreter.next_line_index
		if line_num is not None and line_num >= 0 and line_num < len(self.interpreter.script):
			next_line = self.interpreter.script[line_num]
			line_length = len(next_line)

			self.script_element.see("{line}.{ch}".format(line=line_num + 1, ch=0))
			self.place_tag(self.script_element, "next_to_run", line_num + 1, 0, line_length)
			self.script_element.tag_config("next_to_run", background="#555555")

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
			self.interpreter = Interpreter(self.script)
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