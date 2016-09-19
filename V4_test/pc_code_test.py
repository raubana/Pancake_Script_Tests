import time
from interpreter import *

DEBUG_PROCESS = True
ITERATIONS_PER_SECOND = 0.25#100

source_file = open("1_test.txt")
source_code = source_file.read()

print "INPUT SOURCE SCRIPT:"
print
print source_code
print

interpreter = Interpreter(source_code)

print
print "BEGIN EXECUTION:"
print
iteration = 0
while interpreter.running:
	interpreter.go_to_next_line()

	if DEBUG_PROCESS:
		print "======================================================="
		print " EXEC " + str(iteration)
		print

		print "IND:", interpreter.current_line_index
		print "NXT:", interpreter.next_line_index
		print "MEM:", interpreter.memory
		print "STC:", interpreter.stack
		print

	time.sleep(1.0/(ITERATIONS_PER_SECOND*4))

	if interpreter.running:
		if DEBUG_PROCESS:
			print "TOK:", interpreter.script[interpreter.current_line_index]
			print

		time.sleep(1.0 / (ITERATIONS_PER_SECOND * 4))

		interpreter.process_current_line()

		if DEBUG_PROCESS:
			print "IND:", interpreter.current_line_index
			print "NXT:", interpreter.next_line_index
			print "MEM:", interpreter.memory
			print "STC:", interpreter.stack
			print

		time.sleep(1.0 / (ITERATIONS_PER_SECOND * 2))

		iteration += 1

if DEBUG_PROCESS:
	print " ======================================================= "
	print "EOF."

