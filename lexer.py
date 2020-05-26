import lexem
from enum import Enum

class State(Enum):
	H = 1
	IDENT = 2
	NUMBER = 3
	STRING = 4
	ERROR = 5

class Lexer:
	keywords = {'program', 'var', 'Byte', 'Word', 'ShortInt', 'Integer', 'LongInt',\
	'begin', 'end', 'readln', 'writeln', 'div', 'mod', 'const'}
	delimiters = {';', '.', ':', ',', '(', ')', '+', '-', '*', ':='}
	def __init__(self):
		self.state = State.H
		self.current_line = 1

	def take(c):
		if c == '\n':
			self.current_line = self.current_line + 1

		if self.state == State.H:
			self.state_H
		elif self.state == State.IDENT:
			self.state_IDENT
		elif self.state == State.NUMBER:
			self.state_NUMBER
		elif self.state == State.STRING:
			self.state_STRING
		elif self.state == State.ERROR:
			self.state_ERROR

	def state_H(self):
		pass

	def state_IDENT(self):
		pass

	def state_NUMBER(self):
		pass

	def state_STRING(self):
		pass

	def state_ERROR(self):
		pass


	
def lex_analysis(filename: str):
	with open(filename) as file:
		data = file.read()

	lexer = Lexer()

	for symbol in data:
		lexer.take(symbol)
	

