import pancake.compiler
import string, time

def tabify(s):
	l = string.split(s,"\n")
	for x in xrange(len(l)):
		l[x] = "\t"+l[x]
	return string.join(l,"\n")


DEBUG_PROCESS = True
DEBUG_PAUSE = True

f = open("../tests/0_test.txt")
script = f.read()

print "INPUT SOURCE SCRIPT:"
print
print script
print
"""print
print "COMPILED OUTPUT:"
print"""
compiled_script = pancake.compiler.compile(script)
"""lines = string.split(str(compiled_script),"\n")
for x in xrange(len(lines)):
	lines[x] = str(x) + "\t" + lines[x]
print string.join(lines,"\n")
print"""
print
print "PC CODE OUTPUT:"
print
generated_script = pancake.compiler.generate(compiled_script)
lines = string.split(str(generated_script),"\n")
for x in xrange(len(lines)):
	lines[x] = str(x) + "\t" + lines[x]
print string.join(lines,"\n")
print


"""
print
print "BEGIN EXECUTION:"
print
iteration = 0
interpreter = pancake.interpreter.Interpreter(compiled_script)
while not interpreter.eof:
	interpreter.process_one()
	if not interpreter.eof:
		if DEBUG_PROCESS:
			print "======================================================="
			print " EXEC "+str(iteration)
			print
			print "TOK:",interpreter.current_token
			print "CRS:",interpreter.cursor
			print "NXT:",interpreter.next_cursor
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
			#raw_input("")
			time.sleep(0.2)
		iteration += 1
if DEBUG_PROCESS:
	print " ======================================================= "
	print "EOF."
"""