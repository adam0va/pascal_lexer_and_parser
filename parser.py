class ParserSyntaxError(Exception):
	def __init__(self, *args):
		if args:
			self.message = args[0]
		else:
			self.message = None

	def __str__(self):
		if self.message:
			return f'ParserSyntaxError: {self.message}'
		else:
			return f'ParserSyntaxError was raised'

class Parser:
	def __init__(self, lexems):
		self.lexems = lexems
		self.number_of_current_lexem = 0
		self.length_of_list = len(self.lexems)
		self.current_lexem = self.lexems[self.number_of_current_lexem]
		self.print_name_of_functions = False
		self.print_lexem = False

	def next(self):
		self.number_of_current_lexem += 1

		self.current_lexem = self.lexems[self.number_of_current_lexem]
		if self.print_lexem:
			print(f'Currently examining lexem  "{self.current_lexem}"')

	def check_correctness_of_the_keyword(self, keyword: str):
		if self.lexems[self.number_of_current_lexem].type_of_lexem != TypeOfLexem.keyword:
			return False
		return self.lexems[self.number_of_current_lexem] == keyword

	def analyse(self):
		self.program()

	def program(self):
		self.head_of_the_program()
		if not check_correctness_of_the_keyword(';'):
			raise ParserSyntaxError('";" expected between head of the program and block')
		self.next()
		self.block()
		if not check_correctness_of_the_keyword('.'):
			raise ParserSyntaxError('"." expected in the end of the program')

	def head_of_the_program(self):
		if not check_correctness_of_the_keyword('program'):
			raise ParserSyntaxError('"program" expected in the beginning of the program')
		self.next()
		if not self.lexems[self.number_of_current_lexem].type_of_lexem == TypeOfLexem.identificator:
			raise ParserSyntaxError('Identificator expected')
		self.next()

	def block(self):
		if check_correctness_of_the_keyword('var') or check_correctness_of_the_keyword('const'):
			self.declarative_part()
		self.operators()

	def declarative_part(self):
		self.list_of_sections()
		if not check_correctness_of_the_keyword(';'):
			raise ParserSyntaxError('";" expected after sections with constants and variables')

	def list_of_sections(self):
		self.section()
		self.list_of_sections_()

	def list_of_sections_(self):
		if check_correctness_of_the_keyword(';'):
			self.next()
			self.section()
			self.list_of_sections_()

	def section(self):
		if check_correctness_of_the_keyword('var'):
			self.section_of_variables()
		elif if check_correctness_of_the_keyword('const'): 
			self.section_of_constants()

	def section_of_variables(self):
		if not check_correctness_of_the_keyword('var'):
			raise ParserSyntaxError('"var" expected')
		self.next()
		self.list_of_variables_description()

	def list_of_variables_description(self):
		self.variables_description()
		self.list_of_variables_description_()

	def list_of_variables_description_(self):
		if check_correctness_of_the_keyword(';'):
			self.variables_description()
			self.list_of_variables_description_()

	def variables_description(self):
		self.list_of_variables()
		if not check_correctness_of_the_keyword(':'):
			raise ParserSyntaxError('":" expected')
		self.next()
		self.type()

	def list_of_variables(self):
		self.variables()
		self.list_of_variables_()

	def list_of_variables_(self):
		if check_correctness_of_the_keyword(','):
			self.variable()
			self.list_of_variables_()

	def variable(self):
		if not self.lexems[self.number_of_current_lexem].type_of_lexem == TypeOfLexem.identificator:
			raise ParserSyntaxError('Identificator expected')
		self.next()

	def type(self):
		if not (self.check_correctness_of_the_keyword('Byte') or self.check_correctness_of_the_keyword('Word') or \
			self.check_correctness_of_the_keyword('ShortInt') or self.check_correctness_of_the_keyword('Integer') or \
			self.check_correctness_of_the_keyword('LongInt')):
			raise ParserSyntaxError('Type expected')
		self.next()

	
















