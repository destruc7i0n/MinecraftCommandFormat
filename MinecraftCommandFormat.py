import sublime
import sublime_plugin

class MinecraftFormatBaseCommand(sublime_plugin.TextCommand):

	""" Base code | Majority is from @TexelElf """

	def indent(self, ct):
		return "".join(["\t" for i in xrange(ct)])

	def strexplode(self, command):
		coms = []
		if not command:
			return coms
		i = 0
		line = ""
		inquote = 0
		for c in xrange(len(command)):
			if command[c] == "{":
				if inquote:
					line += command[c]
				else:
					if line:
						coms.append(self.indent(i)+line+"\n")
						line = ""
					coms.append(self.indent(i)+"{\n")
					i += 1
			elif command[c] == "}":
				if inquote:
					line += command[c]
				else:
					if line:
						coms.append(self.indent(i)+line+"\n")
						line = ""
					i -= 1
					line += command[c]
			elif command[c] == "[":
				if inquote:
					line += command[c]
				else:
					if line:
						coms.append(self.indent(i)+line+"\n")
						line = ""
					coms.append(self.indent(i)+"[\n")
					i += 1
			elif command[c] == "]":
				if inquote:
					line += command[c]
				else:
					if line:
						coms.append(self.indent(i)+line+"\n")
						line = ""
					i -= 1
					line += command[c]
			elif command[c] == '\"':
				if command[c-1] != "\\":
					inquote ^= 1
				line += command[c]
			elif command[c] == ",":
				if inquote:
					line += command[c]
				else:
					coms.append(self.indent(i)+line+",\n")
					line = ""
			else:
				line += command[c]
		else:
			if line:
				coms.append(self.indent(i)+line+"\n")
		return coms


	def strcollapse(self, lines):
		commands = []
		command = ""
		id = ""
		comfound = True
		for l in lines:
			if not l:
				continue
			if l[0] == ";":
				continue
			if comfound:
				comfound = False
				command += l.lstrip().replace("\r\n","").replace("\n","") #+ " "
			else:
				command += l.lstrip().replace("\r\n","").replace("\n","")
		else:
			commands.append((id,command.encode("utf-8", "ignore").decode("unicode-escape","ignore").replace(u"\u00C2","")))
		
			
		return commands
				
class MinecraftFormatCommand(MinecraftFormatBaseCommand):
	
	""" Pretty Print a Minecraft Command """

	def run(self, edit):
		outputlines = []
		for region in self.view.sel():

			# If no selection, use the entire file as the selection
			if region.empty():
				selection = sublime.Region(0, self.view.size())
			else:
				selection = region

			fs = self.view.substr(selection)

			if "{" in fs:
				mdatapos = fs.find("{")
				outputlines.append(fs[:mdatapos]+"\n")
				outputlines+=self.strexplode(fs[mdatapos:])
			else:
				outputlines.append(str(fs)+"\n")
			outputlines.append("\n")		
#			obj = self.strexplode(self.view.substr(selection))
			self.view.replace(edit, selection, ("".join(outputlines)))

class MinecraftUnFormatCommand(MinecraftFormatBaseCommand):

	""" Bring Pretty Printed Command Back To String """

	def run(self, edit):
		for region in self.view.sel():

			# If no selection, use the entire file as the selection
			if region.empty():
				selection = sublime.Region(0, self.view.size())
			else:
				selection = region

			fs = self.view.substr(selection).splitlines(True)
			print fs

			output = self.strcollapse(fs)[0][1]
			print output
			self.view.replace(edit, selection, output)
