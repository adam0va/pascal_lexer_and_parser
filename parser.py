from lexem import TypeOfLexem, Lexem
from lark import Lark
import tree

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
		self.print_name_of_functions = True
		self.print_lexem = True


	def next(self):
		self.number_of_current_lexem += 1

		self.current_lexem = self.lexems[self.number_of_current_lexem]
		if self.print_lexem:
			print(f'Currently examining lexem  "{self.current_lexem.lexem_string}"')

	def check_correctness_of_keyword(self, keyword: str):
		if self.lexems[self.number_of_current_lexem].type_of_lexem != TypeOfLexem.keyword:
			return False
		return self.lexems[self.number_of_current_lexem].lexem_string == keyword

	def check_correctness_of_delimiter(self, keyword: str):
		if self.lexems[self.number_of_current_lexem].type_of_lexem != TypeOfLexem.delimiter:
			return False
		return self.lexems[self.number_of_current_lexem].lexem_string == keyword

	def check_correctness_of_assigment_sign(self, keyword: str):
		if self.lexems[self.number_of_current_lexem].type_of_lexem != TypeOfLexem.assignment:
			return False
		return self.lexems[self.number_of_current_lexem].lexem_string == keyword

	def check_correctness_of_arithmetic_operation_sign(self, keyword: str):
		if self.lexems[self.number_of_current_lexem].type_of_lexem != TypeOfLexem.arithmetic_operation:
			return False
		return self.lexems[self.number_of_current_lexem].lexem_string == keyword

	def analyse(self):
		minipascal_program = self.program()
		self.ast = tree.AST(minipascal_program)
		self.ast.print_tree()

	def program(self):
		if self.print_name_of_functions:
			print('program')
		head = self.head_of_the_program()
		if not self.check_correctness_of_delimiter(';'):
			raise ParserSyntaxError('";" expected between head of the program and block')
		self.next()
		block = self.block()
		if not self.check_correctness_of_delimiter('.'):
			raise ParserSyntaxError('"." expected in the end of the program')
		return tree.MinipascalProgramNode(head, block)

	def head_of_the_program(self):
		if self.print_name_of_functions:
			print('head_of_the_program')
		if not self.check_correctness_of_keyword('program'):
			raise ParserSyntaxError('"program" expected in the beginning of the program')
		self.next()
		if not self.lexems[self.number_of_current_lexem].type_of_lexem == TypeOfLexem.identificator:
			raise ParserSyntaxError('Identificator expected')
		identificator = tree.IdentificatorNode(self.lexems[self.number_of_current_lexem])
		name_of_the_program = tree.NameOfTheProgramNode(identificator)
		head_of_the_program = tree.HeadOfTheProgramNode(name_of_the_program)
		self.next()
		return head_of_the_program

	def block(self):
		if self.print_name_of_functions:
			print('block')
		if self.check_correctness_of_keyword('var') or self.check_correctness_of_keyword('const'):
			self.declarative_part()
		self.operators()

	def declarative_part(self):
		if self.print_name_of_functions:
			print('declarative_part')
		self.list_of_sections()
		# проверка на ";" осуществляется внутри описаний переменных и констант
		'''
		if not self.check_correctness_of_delimiter(';'):
			raise ParserSyntaxError('";" expected after sections with constants and variables')
		'''

	def list_of_sections(self):
		if self.print_name_of_functions:
			print('list_of_sections')
		self.section()
		self.list_of_sections_()

	def list_of_sections_(self):
		if self.print_name_of_functions:
			print('list_of_sections_')
		if self.check_correctness_of_keyword('var') or self.check_correctness_of_keyword('const'):
			self.section()
			self.list_of_sections_()
		'''
		if self.check_correctness_of_delimiter(';'):
			self.next()
			self.section()
			self.list_of_sections_()
		'''

	def section(self):
		if self.print_name_of_functions:
			print('section')
		if self.check_correctness_of_keyword('var'):
			self.section_of_variables()
		if self.check_correctness_of_keyword('const'): 
			self.section_of_constants()

	# variables declarations
	def section_of_variables(self):
		if self.print_name_of_functions:
			print('section_of_variables')
		if not self.check_correctness_of_keyword('var'):
			raise ParserSyntaxError('"var" expected')
		self.next()
		self.list_of_variables_description()

	def list_of_variables_description(self):
		if self.print_name_of_functions:
			print('list_of_variables_description')
		self.variables_description()
		self.list_of_variables_description_()

	def list_of_variables_description_(self):
		if self.print_name_of_functions:
			print('list_of_variables_description_')
		if self.check_correctness_of_delimiter(';'):
			self.next()
			# ";" может служить как концом секции объявления переменных и констант,
			# так и концом лишь части их объявлений
			if self.check_correctness_of_keyword('begin') or self.check_correctness_of_keyword('const'):
				return
			self.variables_description()
			self.list_of_variables_description_()

	def variables_description(self):
		if self.print_name_of_functions:
			print('variables_description')
		self.list_of_variables()
		if not self.check_correctness_of_delimiter(':'):
			raise ParserSyntaxError('":" expected')
		self.next()
		self.type()

	def list_of_variables(self):
		if self.print_name_of_functions:
			print('list_of_variables')
		self.variable()
		self.list_of_variables_()

	def list_of_variables_(self):
		if self.print_name_of_functions:
			print('list_of_variables_')
		if self.check_correctness_of_delimiter(','):
			self.next()
			self.variable()
			self.list_of_variables_()

	def variable(self):
		if self.print_name_of_functions:
			print('variable')
		if not self.lexems[self.number_of_current_lexem].type_of_lexem == TypeOfLexem.identificator:
			raise ParserSyntaxError('Identificator expected')
		self.next()

	def type(self):
		if self.print_name_of_functions:
			print('type')
		if not (self.check_correctness_of_keyword('Byte') or self.check_correctness_of_keyword('Word') or \
			self.check_correctness_of_keyword('ShortInt') or self.check_correctness_of_keyword('Integer') or \
			self.check_correctness_of_keyword('LongInt')):
			raise ParserSyntaxError('Type expected')
		self.next()

	# constants declarations
	def section_of_constants(self):
		if self.print_name_of_functions:
			print('section_of_constants')
		if not self.check_correctness_of_keyword('const'):
			raise ParserSyntaxError('"const" expected before constants description')
		self.next()
		self.list_of_constants_declaration()

	def list_of_constants_declaration(self):
		if self.print_name_of_functions:
			print('list_of_constants_declaration')
		self.constant_declaration()
		self.list_of_constants_declaration_()

	def list_of_constants_declaration_(self):
		if self.print_name_of_functions:
			print('list_of_constants_declaration_')
		if self.check_correctness_of_delimiter(';'):
			self.next()
			# ";" может служить как концом секции объявления переменных и констант,
			# так и концом лишь части их объявления
			if self.check_correctness_of_keyword('begin') or self.check_correctness_of_keyword('var'):
				return
			self.constant_declaration()
			self.list_of_constants_declaration_()

	def constant_declaration(self):
		if self.print_name_of_functions:
			print('constant_declaration')
		self.name_of_constant()
		if not self.check_correctness_of_delimiter('='):
			raise ParserSyntaxError('"=" expected in constant declaration')
		self.next()
		self.constant()

	def name_of_constant(self):
		if self.print_name_of_functions:
			print('name_of_constant')
		if not self.lexems[self.number_of_current_lexem].type_of_lexem == TypeOfLexem.identificator:
			raise ParserSyntaxError('Identificator expected')
		self.next()

	def constant(self):
		if self.print_name_of_functions:
			print('constant')
		if not self.lexems[self.number_of_current_lexem].type_of_lexem in {TypeOfLexem.number, \
		TypeOfLexem.string}:
			raise ParserSyntaxError('Constant expected')
		self.next()

	# operators
	def operators(self):
		if self.print_name_of_functions:
			print('operators')
		print('!')
		if not self.check_correctness_of_keyword('begin'):
			raise ParserSyntaxError('"begin" expected before operators')
		self.next()
		self.operators_sequence()
		if not self.check_correctness_of_keyword('end'):
			raise ParserSyntaxError('"end" expected after operators')
		self.next()

	def operators_sequence(self):
		if self.print_name_of_functions:
			print('operators_sequence')
		self.operator()
		self.operators_sequence_()

	def operators_sequence_(self):
		if self.print_name_of_functions:
			print('operators_sequence_')
		if self.check_correctness_of_delimiter(';'):
			self.next()
			if self.check_correctness_of_keyword('end'):
				return
			self.operator()
			self.operators_sequence_()

	def operator(self):
		if self.print_name_of_functions:
			print('operator')
		if self.check_correctness_of_keyword('readln'):
			self.input_operator()
		elif self.check_correctness_of_keyword('writeln'):
			self.output_operator()
		elif self.lexems[self.number_of_current_lexem].type_of_lexem == TypeOfLexem.identificator:
			self.operator_of_assignment()

	# input operator
	def input_operator(self):
		if self.print_name_of_functions:
			print('input_operator')
		if not self.check_correctness_of_keyword('readln'):
			raise ParserSyntaxError('Input operator expected')
		self.next()
		if self.check_correctness_of_delimiter('('):
			self.next()
			self.input_list()
			if not self.check_correctness_of_delimiter(')'):
				raise ParserSyntaxError('")" expected after input list')
			self.next()

	def input_list(self):
		if self.print_name_of_functions:
			print('input_list')
		self.variable()
		self.list_of_variables_()

	# output operator
	def output_operator(self):
		if self.print_name_of_functions:
			print('output_operator')
		if not self.check_correctness_of_keyword('writeln'):
			raise ParserSyntaxError('Output operator expected')
		self.next()
		if self.check_correctness_of_delimiter('('):
			self.next()
			self.list_of_expressions()
			if not self.check_correctness_of_delimiter(')'):
				raise ParserSyntaxError('")" expected after list of expressions for output')
			self.next()

	# operator of assignment
	def operator_of_assignment(self):
		if self.print_name_of_functions:
			print('operator_of_assignment')
		if not self.lexems[self.number_of_current_lexem].type_of_lexem == TypeOfLexem.identificator:
			raise ParserSyntaxError('Identificator expected')
		self.next()
		if not self.check_correctness_of_assigment_sign(':='):
			raise ParserSyntaxError('Assignment sign expected')
		self.next()
		self.expression()

	# expressions
	def list_of_expressions(self):
		if self.print_name_of_functions:
			print('list_of_expressions')
		self.expression()
		self.list_of_expressions_()

	def list_of_expressions_(self):
		if self.print_name_of_functions:
			print('list_of_expressions_')
		if self.check_correctness_of_delimiter(','):
			self.next()
			self.expression()
			self.list_of_expressions_()

	def expression(self):
		if self.print_name_of_functions:
			print('expression')

		if self.lexems[self.number_of_current_lexem].type_of_lexem in {TypeOfLexem.number, \
		TypeOfLexem.identificator} or self.lexems[self.number_of_current_lexem].lexem_string in \
		{'+', '-'}:
			self.arithmetic_expression()
		elif self.lexems[self.number_of_current_lexem].type_of_lexem == TypeOfLexem.string:
			self.next()
		else:
			raise ParserSyntaxError('Expression expected')
		'''
		if self.lexems[self.number_of_current_lexem].type_of_lexem in {TypeOfLexem.number, \
		TypeOfLexem.identificator}:
			self.arithmetic_expression()
		elif self.lexems[self.number_of_current_lexem].type_of_lexem == TypeOfLexem.string:
			self.next()
		else:
			raise ParserSyntaxError('Expression expected')
		'''

	def arithmetic_expression(self):
		if self.print_name_of_functions:
			print('arithmetic_expression')
		if self.lexems[self.number_of_current_lexem].type_of_lexem == TypeOfLexem.number or \
		self.lexems[self.number_of_current_lexem].lexem_string in {'+', '-'}:
			self.number()
			self.arithmetic_expression_()
		elif self.lexems[self.number_of_current_lexem].type_of_lexem == TypeOfLexem.identificator:
			self.next()
			self.arithmetic_expression_()
		'''
		if self.lexems[self.number_of_current_lexem].type_of_lexem == TypeOfLexem.number or \
		self.lexems[self.number_of_current_lexem].type_of_lexem == TypeOfLexem.identificator:
			self.next()
			self.arithmetic_expression_()
		'''

	def arithmetic_expression_(self):
		if self.print_name_of_functions:
			print('arithmetic_expression_')
		if self.lexems[self.number_of_current_lexem].lexem_string in ('+', '-', '*', 'div', 'mod'):
			self.sign_of_arithmetic_expression()
			self.arithmetic_expression()
			self.arithmetic_expression_()

	def sign_of_arithmetic_expression(self):
		if self.print_name_of_functions:
			print('sign_of_arithmetic_expression')
		if self.check_correctness_of_arithmetic_operation_sign('+'):
			self.next()
		elif self.check_correctness_of_arithmetic_operation_sign('-'):
			self.next()
		elif self.check_correctness_of_arithmetic_operation_sign('*'):
			self.next()
		elif self.check_correctness_of_keyword('div'):
			self.next()
		elif self.check_correctness_of_keyword('mod'):
			self.next()
		else:
			raise ParserSyntaxError('Arithmetic operation sign expected')

	def number(self):
		if self.check_correctness_of_arithmetic_operation_sign('+') \
		or self.check_correctness_of_arithmetic_operation_sign('-'):
			self.next()
		if not self.lexems[self.number_of_current_lexem].type_of_lexem == TypeOfLexem.number:
			raise ParserSyntaxError('Number exprected')
		self.next()

	def identificator(self):
		if not self.lexems[self.number_of_current_lexem].type_of_lexem == TypeOfLexem.identificator:
			raise ParserSyntaxError('Identificator expected')
		self.next()


def syntatic_analysis(lexems):
	parser = Parser(lexems)
	parser.analyse()








