from lexem import Lexem, TypeOfLexem
from enum import Enum

class State(Enum):
	H = 1
	IDENT = 2
	NUMBER = 3
	STRING = 4
	ERROR = 5
	ASSIGNMENT = 6
	PLUS_MINUS = 7

class Lexer:
	keywords = {'program', 'var', 'Byte', 'Word', 'ShortInt', 'Integer', 'LongInt',\
	'begin', 'end', 'readln', 'writeln', 'div', 'mod', 'const'}
	delimiters = {';', '.', ':', ',', '(', ')', '='}
	arithmetic_operations = {'+', '-', '*'}
	assignment = {':='}
	any_sign = {';', '.', ':', ',', '(', ')', '+', '-', '*', ':=', '='}
	def __init__(self):
		self.state = State.H
		self.current_line = 1
		self.current_lexem = ''
		self.lexems_ready = []

	def take(self, c):
		if c == '\n':
			self.current_line = self.current_line + 1
		print(f'{c} {self.current_line}')

		if self.state == State.H:
			self.state_H(c)
		elif self.state == State.IDENT:
			self.state_IDENT(c)
		elif self.state == State.NUMBER:
			self.state_NUMBER(c)
		elif self.state == State.STRING:
			self.state_STRING(c)
		elif self.state == State.ERROR:
			return
		elif self.state == State.ASSIGNMENT:
			self.state_ASSIGNMENT(c)
		elif self.state == State.PLUS_MINUS:
			self.state_PLUS_MINUS(c)

	def get_lexems(self):
		lexems_to_return = self.lexems_ready
		self.lexems_ready = ''
		return lexems_to_return

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
		elif c in self.any_sign:
			self.handle_signs(c)

	def state_IDENT(self, c):
		if c.isalpha() or c.isnumeric() or c == '_':
			self.current_lexem = self.current_lexem + c
		elif c in self.any_sign:
			self.make_lexem(TypeOfLexem.identificator)
			self.handle_signs(c)
		elif self.__is_space(c):
			self.make_lexem(TypeOfLexem.identificator)
			self.state = State.H
		else:
			self.state = State.ERROR
			print(f'Line {self.current_line}: Unexpected symbol in identificator')

	def state_NUMBER(self, c):
		if c.isnumeric():
			self.current_lexem = self.current_lexem + c
		elif c.isalpha():
			self.state = State.ERROR
			print(f'Line {self.current_line}: Number expected')
		elif c in self.any_sign:
			self.make_lexem(TypeOfLexem.number)
			self.handle_signs(c)
		elif self.__is_space(c):
			self.make_lexem(TypeOfLexem.number)
			self.state = State.H

	def state_STRING(self, c):
		if c == '"':
			self.make_lexem(TypeOfLexem.string)
			self.state = State.H
		else:
			self.current_lexem = self.current_lexem + c

	def state_ASSIGNMENT(self, c):
		if c == '=':
			self.current_lexem = self.current_lexem + c
			self.make_lexem(TypeOfLexem.assignment)
			self.state = State.H
		else: 
			self.make_lexem(TypeOfLexem.delimiter)
			self.state = State.H
			self.state_H(c)

	def state_PLUS_MINUS(self, c):
		# если следующим за знаком +/- автомат получил число, то
		if c.isnumeric():
			# если перед ним распознана переменная или идентификатор, то
			# будем считать, что +/- это знак арифметической операции
			print(f'last type: {self.lexems_ready[-1].type_of_lexem}')
			if self.lexems_ready[-1].type_of_lexem == TypeOfLexem.number or \
			self.lexems_ready[-1].type_of_lexem == TypeOfLexem.identificator:
				self.make_lexem(TypeOfLexem.arithmetic_operation)
				self.state = State.H
				self.state_H(c)
			# если перед ним распознан любой другой знак, то 
			# будем считать, что +/- это знак знакового числа
			else:
				self.current_lexem = self.current_lexem + c
				self.state = State.NUMBER
		# если следующим за знаком +/- автомат получил НЕ число, то
		# будем считать, что +/- это знак арифметической операции
		else:
			self.make_lexem(TypeOfLexem.arithmetic_operation)
			self.state = State.H
			self.state_H(c)

		'''
		if c.isnumeric():
			self.current_lexem = self.current_lexem + c
			self.state = State.NUMBER
		else:
			self.make_lexem(TypeOfLexem.arithmetic_operation)
			self.state = State.H
			self.state_H(c)
		'''

	def handle_delimiter(self, c):
		self.current_lexem = self.current_lexem + c
		if c == ':':
			self.state = State.ASSIGNMENT
		else:
			self.make_lexem(TypeOfLexem.keyword)
			self.state = State.H

	def __is_space(self, c):
		return c in {' ', '\n', '\t'}

	def handle_signs(self, c):
		self.current_lexem = self.current_lexem + c
		if c == ':':
			self.state = State.ASSIGNMENT
		elif c in {'+', '-'}:
			self.state = State.PLUS_MINUS
		elif c == '*':
			self.make_lexem(TypeOfLexem.arithmetic_operation)
		else:
			self.make_lexem(TypeOfLexem.delimiter)
			self.state = State.H
	
def lex_analysis(filename: str):
	with open(filename) as file:
		data = file.read()

	data = list(data)
	print(data)
	lexer = Lexer()
	lexems = []

	for symbol in data:
		lexer.take(symbol)

	lexems = lexems + lexer.lexems_ready

	for lexem in lexems:
		print(f'{lexem.number_of_line}: {lexem.lexem_string} {lexem.type_of_lexem}')

	return lexems











	

