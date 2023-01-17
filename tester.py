import sys
from time import sleep
#-----------------------------#
sys.path.append("./Minienv")
#-----------------------------#
import subprocess
import re
#-----------------------------#

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

file_path = 'logs'
command = "../minishell"

def remove_blank_lines(lines):
    cleaned_lines = []
    for line in lines:
        if line != '\n' and line.strip():
            cleaned_lines.append(line)
    return cleaned_lines

def remove_sequence(lines, sequence):
    cleaned_lines = []
    for line in lines:
        cleaned_lines.append(line.replace(sequence, ""))
    return cleaned_lines

def remove_even_lines(lines):
    cleaned_lines = []
    for i, line in enumerate(lines):
        if i % 2 != 0:
            cleaned_lines.append(line)
    return cleaned_lines

def read_quoted_characters(file_path):
    with open(file_path, 'r') as file:
        characters = file.read().replace('\n','').replace('"','')
    return characters

class Tests():
	def __init__(self, string, commands):
		self.commands = list(commands)
		self.string = str(string)
		self.commands.append('\n')
		self.score = 0
		self.questions = 0
		self.output_bash = []
		self.output_minishell = []
		self.output_bash, self.output_minishell = self.get_output()
		self.prompt = ""
		self.prompt = read_quoted_characters("prompt.txt")
		self.output_bash = remove_blank_lines(self.output_bash)
		self.output_minishell = remove_sequence(self.output_minishell, self.prompt)
		self.output_minishell = remove_blank_lines(self.output_minishell) 
		self.output_minishell = remove_even_lines(self.output_minishell)

	def	get_output(self):
		output = []
		with open(file_path, 'w') as f:
			process = subprocess.Popen('bash', stdout=f, stdin=subprocess.PIPE, stderr=f)
			input_str = "\n\n".join(self.commands)
			process.communicate(input=input_str.encode(), timeout=5)
		with open(file_path, "r", encoding='utf-8-sig') as f:
			bash_output= f.read()
			output.append(bash_output.splitlines(True))
		try:
			with open(file_path, 'w') as f:
				process = subprocess.Popen(command, stdout=f, stdin=subprocess.PIPE, stderr=f)
				input_str = "\n".join(self.commands)
				process.communicate(input=input_str.encode(), timeout=5)
		except:
			print(bcolors.FAIL+"\n[¬º-°]¬		TIMEOUT	"+bcolors.ENDC)
			return
		with open(file_path, "r", encoding='utf-8-sig') as f:
			minishell_output= f.read()
			output.append(minishell_output.splitlines(True))
		f = lambda x: x.replace("$ ▶ ", "")
		list(map(f, output[1]))
		output[1] = list(filter(None, output[1]))
		return (output[0], output[1])

	def get_comparison(self):
		error_pattern = r"(bash:)"
		print(f"\n\n{bcolors.HEADER} - {self.string} - {bcolors.ENDC}\n")
		self.questions = len(self.output_minishell)
		for i in range(max(len(self.output_bash), len(self.output_minishell))):
			try:
				if re.findall(error_pattern, self.output_bash[i]):
					self.questions = self.questions - 1
					print(bcolors.FAIL+"Error detected.\nNot adding to score \n"+bcolors.ENDC)
				elif self.output_bash[i] == self.output_minishell[i]:
					self.score = self.score + 1
					print(bcolors.OKGREEN+"\nSUCESS\n"+bcolors.ENDC)
				else:
					print(bcolors.FAIL+"\nFAILURE\n"+bcolors.ENDC)
			except IndexError:
				print(bcolors.FAIL+'Out of range.'+bcolors.ENDC)
				break
			try:
				print(bcolors.OKBLUE+"MINISHELL:"+bcolors.ENDC)
				print(f'{self.output_minishell[i]}')
			except IndexError:
				for j in range(i, len(self.output_minishell)):
					print(bcolors.OKBLUE+"MINISHELL:"+bcolors.ENDC)
					print(f'{self.output_minishell[j]}')
				break
			try:
				print(bcolors.OKCYAN+"BASH:"+bcolors.ENDC)
				print(f'{self.output_bash[i]}')
			except IndexError:
				for j in range(i, len(self.output_bash)):
					print(bcolors.OKCYAN+"BASH:"+bcolors.ENDC)
					print(f'{self.output_bash[j]}')
				break
		try:
			score = (self.score * 100) / self.questions
			print(f"{bcolors.WARNING}You got {score}%!\n{self.score} out of {self.questions} questions\n{bcolors.ENDC}")
		except:
			print(bcolors.FAIL+'Invalid Score.'+bcolors.ENDC)

	def	get_output_2(self, flag):
		print(f"\n\n{bcolors.HEADER} - {self.string} - {bcolors.ENDC}\n")
		if flag == 1:
			for i in range(max(len(self.output_bash), len(self.output_minishell))):
				try:
					print(bcolors.OKBLUE+"MINISHELL:"+bcolors.ENDC)
					print(f'{self.output_minishell[i]}')
				except IndexError:
					for j in range(i, len(self.output_minishell)):
						print(bcolors.OKBLUE+"MINISHELL:"+bcolors.ENDC)
						print(f'{self.output_minishell[j]}')
					break
				try:
					print(bcolors.OKCYAN+"BASH:"+bcolors.ENDC)
					print(f'{self.output_bash[i]}')
				except IndexError:
					for j in range(i, len(self.output_bash)):
						print(bcolors.OKCYAN+"BASH:"+bcolors.ENDC)
						print(f'{self.output_bash[j]}')
					break
		elif flag == 0:
			for i in range(len(self.output_minishell)):
				print(bcolors.OKBLUE+"MINISHELL:"+bcolors.ENDC)
				print(self.output_minishell[i])
				print("\n")


def create_tests_from_file(file_path):
	tests = []
	try:
		with open(file_path, 'r') as file:
			lines = file.readlines()
			i = 0
			while i < len(lines):
				try:
					string = lines[i].strip()
					commands = [x.strip() for x in lines[i + 1].strip().split(',')]
					tests.append(Tests(string, commands))
					i += 3
				except:
					break
	except:
		print(bcolors.FAIL+'\n\nInvalid File...'+bcolors.ENDC)
		exit
	return tests


tests = create_tests_from_file('tests.txt')

def print_menu():
	print(f"{bcolors.BOLD}\n\n\n(-(-_-(-_(-_(-_-)_-)-_-)_-)_-)-)\n	MINISHELL TESTER	\n(-(-_-(-_(-_(-_-)_-)-_-)_-)_-)-)\n{bcolors.ENDC}")
	print(f"{bcolors.OKBLUE}1. Print Minishell Output {bcolors.ENDC}")
	print(f"{bcolors.OKBLUE}2. Print Bash Output and Minishell Output {bcolors.ENDC}")
	print(f"{bcolors.OKBLUE}3. Run Comparison between Bash and Minishell (Beta){bcolors.ENDC}")
	print(f"{bcolors.FAIL}4. Exit{bcolors.ENDC}")
	print("\n\nEnter your choice:")

def option_1():
	for test in tests:
		test.get_output_2(0)

def option_2():
	for test in tests:
		test.get_output_2(1)


def	option_3():
	for test in tests:
		test.get_comparison()

while True:
    print_menu()
    choice = input()
    if choice == '1':
        option_1()
    elif choice == '2':
        option_2()
    elif choice == '3':
        option_3()
    elif choice == '4':
        break
    else:
        print("Invalid choice, please try again")



print(bcolors.WARNING+"DONT FORGET TO TEST /BIN/LS & LS & ENV & EXPORT & signals...."+bcolors.ENDC)