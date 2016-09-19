import string, time
from compiler import Compiler
from interpreter import Interpreter

def tabify(s):
	l = string.split(s,"\n")
	for x in xrange(len(l)):
		l[x] = "\t"+l[x]
	return string.join(l,"\n")

DEBUG_PROCESS = False
DEBUG_PAUSE = False

f = open("../8_while.txt")
script = f.read()

print "INPUT SOURCE SCRIPT:"
print
print tabify(script)
print
print
print "PARSED OUTPUT:"
print

compiled = Compiler.compile_script(script)
print tabify(str(compiled))
print


#"""
print
print "BEGIN EXECUTION:"
print
iteration = 0
interpreter = Interpreter(compiled)
while not interpreter.eof:
	interpreter.process_one()
	if not interpreter.eof:
		if DEBUG_PROCESS:
			print "======================================================="
			print " EXEC "+str(iteration)
			print
			print "TOK:",interpreter.current_token
			print "CRS:",interpreter.current_index
			print "MEM:",interpreter.variables
			print "STC:",interpreter.stack
		if len(interpreter.print_buffer) > 0:
			if DEBUG_PROCESS:
				print
				print "OUTPUT:"
			print string.join(interpreter.print_buffer,"\n")
		if DEBUG_PROCESS:
			print
			print("EOL.")
		if DEBUG_PAUSE:
			raw_input("")
		iteration += 1
if DEBUG_PROCESS:
	print " ======================================================= "
	print "EOF."
#"""