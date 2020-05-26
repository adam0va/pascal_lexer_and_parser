from lexem import Lexem, TypeOfLexem
from enum import Enum

class State(Enum):
	H = 1
	IDENT = 2
	NUMBER = 3
	STRING = 4
	ERROR = 5
	ASSIGNMENT = 6

class Lexer:
	keywords = {'program', 'var', 'Byte', 'Word', 'ShortInt', 'Integer', 'LongInt',\
	'begin', 'end', 'readln', 'writeln', 'div', 'mod', 'const'}
	delimiters = {';', '.', ':', ',', '(', ')', '+', '-', '*', ':='}
	def __init__(self):
		self.state = State.H
		self.current_line = 1
		self.current_lexem = ''
		self.lexems_ready = []

	def take(self, c):
		if c == '\n':
			self.current_line = self.current_line + 1

		if self.state == State.H:
			self.state_H(c)
		elif self.state == State.IDENT:
			self.state_IDENT(c)
		elif self.state == State.NUMBER:
			self.state_NUMBER(c)
		elif self.state == State.STRING:
			self.state_STRING(c)
		elif self.state == State.ERROR:
			print(f'Error occured')
			return
		elif self.state == State.ASSIGNMENT:
			self.state_ASSIGNMENT(c)

	def get_lexem(self):
		if self.lexems_ready:
			lexem_to_return = self.lexems_ready[0]
			self.lexems_ready = self.lexems_ready[1:]
			return lexem_to_return

	def make_lexem(self, type_of_lexem_):
		new_lexem = Lexem(self.current_line, self.current_lexem, type_of_lexem_)
		if type_of_lexem_ == TypeOfLexem.identificator and self.current_lexem in self.keywords:
			new_lexem.type_of_lexem = TypeOfLexem.keyword
		elif type_of_lexem_ == TypeOfLexem.number:
			new_lexem.lexem_int = int(self.current_line)
		self.lexems_ready.append(new_lexem)
		self.current_lexem = ''

	def state_H(self, c):
		if c == ' ':
			return
		elif c.isalpha():
			self.current_lexem = self.current_lexem + c
			self.state = State.IDENT
		elif c.isnumeric():
			self.current_lexem = self.current_lexem + c
			self.state = State.NUMBER
		elif c == '"':
			self.state = State.STRING
		elif c in self.delimiters:
			self.handle_delimiter(c)

	def state_IDENT(self, c):
		if c.isalpha() or c.isnumeric():
			self.current_lexem = self.current_lexem + c
		elif c in self.delimiters:
			self.make_lexem(TypeOfLexem.identificator)
			self.handle_delimiter(c)
		elif self.__is_space(c):
			self.make_lexem(TypeOfLexem.identificator)
			self.state = State.H

	def state_NUMBER(self, c):
		if c.isnumeric():
			self.current_lexem = self.current_lexem + c
		elif c.isalpha():
			self.state = State.ERROR
		elif c in self.delimiters:
			self.make_lexem(TypeOfLexem.number)
			self.handle_delimiter(c)
		elif self.__is_space(c):
			self.make_lexem(TypeOfLexem.number)
			self.state = State.H

	def state_STRING(self, c):
		if c == '"':
			self.make_lexem(TypeOfLexem.string)
		else:
			self.current_lexem = self.current_lexem + c

	def state_ASSIGNMENT(self, c):
		if c == '=':
			self.make_lexem(TypeOfLexem.keyword)
			self.state = State.H

	def handle_delimiter(self, c):
		self.current_lexem = self.current_lexem + c
		if c == ':':
			self.state = State.ASSIGNMENT
		else:
			self.make_lexem(TypeOfLexem.keyword)
			self.state = State.H

	def __is_space(self, c):
		return c in {' ', '\n', '\t'}
	
def lex_analysis(filename: str):
	with open(filename) as file:
		data = file.read()

	lexer = Lexer()
	print(lexer.lexems_ready)
	lexems = []

	for symbol in data:
		lexer.take(symbol)
		'''new_lexem = lexer.get_lexem()
		if new_lexem:
			lexems.append(new_lexem)'''

	lexems = lexer.lexems_ready

	for lexem in lexems:
		print(f'{lexem.number_of_line}: {lexem.lexem_string} {lexem.type_of_lexem}')











	

