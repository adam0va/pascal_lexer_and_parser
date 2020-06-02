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
		self.print_name_of_functions = False
		self.print_lexem = False

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

	def analyse(self, print_tree):
		minipascal_program = self.program()
		self.ast = tree.AST(minipascal_program)
		if print_tree:
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
			decl_part = self.declarative_part()
		operators = self.operators()
		#return tree.BlockNode(declarative_part = decl_part)
		
		if decl_part:
			return tree.BlockNode(declarative_part = decl_part, operators =operators)
		else:
			return tree.BlockNode(operators=operators)
		

	def declarative_part(self):
		if self.print_name_of_functions:
			print('declarative_part')
		list_of_sections = self.list_of_sections()
		return tree.DeclarativePartNode(list_of_sections)
		# проверка на ";" осуществляется внутри описаний переменных и констант
		'''
		if not self.check_correctness_of_delimiter(';'):
			raise ParserSyntaxError('";" expected after sections with constants and variables')
		'''

	def list_of_sections(self):
		if self.print_name_of_functions:
			print('list_of_sections')
		section = self.section()
		list_of_sections = self.list_of_sections_()
		if list_of_sections:
			return tree.ListOfSectionsNode(section, list_of_sections)
		else:
			return tree.ListOfSectionsNode(section)


	def list_of_sections_(self):
		if self.print_name_of_functions:
			print('list_of_sections_')
		if self.check_correctness_of_keyword('var') or self.check_correctness_of_keyword('const'):
			section = self.section()
			list_of_sections = self.list_of_sections_()
			if list_of_sections:
				return tree.ListOfSectionsNode(section, list_of_sections)
			else:
				return tree.ListOfSectionsNode(section)
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
			section_of_variables = self.section_of_variables()
			return tree.SectionNode(section_of_variables=section_of_variables)
		elif self.check_correctness_of_keyword('const'): 
			section_of_constants = self.section_of_constants()
			return tree.SectionNode(section_of_constants=section_of_constants)
		'''
		if section_of_constants and section_of_variables:
			return tree.SectionNode(section_of_variables=section_of_variables, section_of_constants=\
				section_of_constants)
		elif section_of_constants:
			return tree.SectionNode(section_of_constants=section_of_constants)
		elif section_of_variables:
			return tree.SectionNode(section_of_variables=section_of_variables)
		'''

	# variables declarations
	def section_of_variables(self):
		if self.print_name_of_functions:
			print('section_of_variables')
		if not self.check_correctness_of_keyword('var'):
			raise ParserSyntaxError('"var" expected')
		self.next()
		list_of_variables_description = self.list_of_variables_description()
		return tree.SectionOfVariablesNode(list_of_variables_description)

	def list_of_variables_description(self):
		if self.print_name_of_functions:
			print('list_of_variables_description')
		variables_description = self.variables_description()
		list_of_variables_description = self.list_of_variables_description_()
		if list_of_variables_description:
			return tree.ListOfVarDescriptionsNode(variables_description, list_of_var_descriptions = \
				list_of_variables_description)
		else: 
			return tree.ListOfVarDescriptionsNode(variables_description)

	def list_of_variables_description_(self):
		if self.print_name_of_functions:
			print('list_of_variables_description_')
		if self.check_correctness_of_delimiter(';'):
			self.next()
			# ";" может служить как концом секции объявления переменных и констант,
			# так и концом лишь части их объявлений
			if self.check_correctness_of_keyword('begin') or self.check_correctness_of_keyword('const'):
				return
			variables_description = self.variables_description()
			list_of_variables_description = self.list_of_variables_description_()
			if list_of_variables_description:
				return tree.ListOfVarDescriptionsNode(variables_description, list_of_var_descriptions = \
					list_of_variables_description)
			else: 
				return tree.ListOfVarDescriptionsNode(variables_description)

	def variables_description(self):
		if self.print_name_of_functions:
			print('variables_description')
		list_of_variables = self.list_of_variables()
		if not self.check_correctness_of_delimiter(':'):
			raise ParserSyntaxError('":" expected')
		self.next()
		type = self.type()
		return tree.VarDescriptionNode(list_of_variables, type)

	def list_of_variables(self):
		if self.print_name_of_functions:
			print('list_of_variables')
		variable = self.variable()
		list_of_variables = self.list_of_variables_()
		if list_of_variables:
			return tree.ListOfVariablesNode(variable, list_of_variables=list_of_variables)
		else:
			return tree.ListOfVariablesNode(variable)

	def list_of_variables_(self):
		if self.print_name_of_functions:
			print('list_of_variables_')
		if self.check_correctness_of_delimiter(','):
			self.next()
			variable = self.variable()
			list_of_variables = self.list_of_variables_()
			if list_of_variables:
				return tree.ListOfVariablesNode(variable, list_of_variables=list_of_variables)
			else:
				return tree.ListOfVariablesNode(variable)

	def variable(self):
		if self.print_name_of_functions:
			print('variable')
		if not self.lexems[self.number_of_current_lexem].type_of_lexem == TypeOfLexem.identificator:
			raise ParserSyntaxError('Identificator expected')
		identificator = tree.IdentificatorNode(self.lexems[self.number_of_current_lexem])
		self.next()
		return tree.VariableNode(identificator)

	def type(self):
		if self.print_name_of_functions:
			print('type')
		if not (self.check_correctness_of_keyword('Byte') or self.check_correctness_of_keyword('Word') or \
			self.check_correctness_of_keyword('ShortInt') or self.check_correctness_of_keyword('Integer') or \
			self.check_correctness_of_keyword('LongInt')):
			raise ParserSyntaxError('Type expected')
		keyword = self.lexems[self.number_of_current_lexem]
		self.next()
		return tree.TypeNode(keyword)

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
		operators_sequence = self.operators_sequence()
		if not self.check_correctness_of_keyword('end'):
			raise ParserSyntaxError('"end" expected after operators')
		self.next()
		return tree.OperatorsNode(operators_sequence)

	def operators_sequence(self):
		if self.print_name_of_functions:
			print('operators_sequence')
		operator = self.operator()
		operators_sequence = self.operators_sequence_()
		if operators_sequence:
			return tree.OperatorsSequenceNode(operator=operator, operators_sequence=operators_sequence)
		else:
			return tree.OperatorsSequenceNode(operator=operator)

	def operators_sequence_(self):
		if self.print_name_of_functions:
			print('operators_sequence_')
		if self.check_correctness_of_delimiter(';'):
			self.next()
			if self.check_correctness_of_keyword('end'):
				return
			operator = self.operator()
			operators_sequence = self.operators_sequence_()
			if operators_sequence:
				return tree.OperatorsSequenceNode(operator=operator, operators_sequence=operators_sequence)
			else:
				return tree.OperatorsSequenceNode(operator=operator)

	def operator(self):
		if self.print_name_of_functions:
			print('operator')
		if self.check_correctness_of_keyword('readln'):
			input_operator = self.input_operator()
			return tree.OperatorNode(input_operator=input_operator)
		elif self.check_correctness_of_keyword('writeln'):
			output_operator = self.output_operator()
			return tree.OperatorNode(output_operator=output_operator)
		elif self.lexems[self.number_of_current_lexem].type_of_lexem == TypeOfLexem.identificator:
			operator_of_assignment = self.operator_of_assignment()
			return tree.OperatorNode(operator_of_assignment=operator_of_assignment)

	# input operator
	def input_operator(self):
		if self.print_name_of_functions:
			print('input_operator')
		if not self.check_correctness_of_keyword('readln'):
			raise ParserSyntaxError('Input operator expected')
		self.next()
		if self.check_correctness_of_delimiter('('):
			self.next()
			input_list = self.input_list()
			if not self.check_correctness_of_delimiter(')'):
				raise ParserSyntaxError('")" expected after input list')
			self.next()
			return tree.InputOperatorNode(input_list=input_list)
		else:
			return tree.InputOperatorNode()

	def input_list(self):
		if self.print_name_of_functions:
			print('input_list')
		variable = self.variable()
		list_of_variables = self.list_of_variables_()
		if list_of_variables:
			input_list = tree.ListOfVariablesNode(variable, list_of_variables=list_of_variables)
		else:
			input_list = tree.ListOfVariablesNode(variable)
		return tree.InputListNode(input_list)

	# output operator
	def output_operator(self):
		if self.print_name_of_functions:
			print('output_operator')
		if not self.check_correctness_of_keyword('writeln'):
			raise ParserSyntaxError('Output operator expected')
		self.next()
		if self.check_correctness_of_delimiter('('):
			self.next()
			list_of_expressions = self.list_of_expressions()
			if not self.check_correctness_of_delimiter(')'):
				raise ParserSyntaxError('")" expected after list of expressions for output')
			self.next()
			output_list = tree.OutputListNode(list_of_expressions)

			return tree.OutputOperatorNode(output_list)

	# operator of assignment
	def operator_of_assignment(self):
		if self.print_name_of_functions:
			print('operator_of_assignment')
		if not self.lexems[self.number_of_current_lexem].type_of_lexem == TypeOfLexem.identificator:
			raise ParserSyntaxError('Identificator expected')
		ident = tree.IdentificatorNode(self.lexems[self.number_of_current_lexem])
		self.next()
		if not self.check_correctness_of_assigment_sign(':='):
			raise ParserSyntaxError('Assignment sign expected')
		sign = self.lexems[self.number_of_current_lexem]
		self.next()
		expression = self.expression()
		return tree.OperatorOfAssignmentNode(variable=ident, sign=sign, expression=expression)

	# expressions
	def list_of_expressions(self):
		if self.print_name_of_functions:
			print('list_of_expressions')
		expression = self.expression()
		list_of_expressions = self.list_of_expressions_()

		if list_of_expressions:
			return tree.ListOfExpressionsNode(expression=expression, list_of_expressions=list_of_expressions)
		else:
			return tree.ListOfExpressionsNode(expression=expression)

	def list_of_expressions_(self):
		if self.print_name_of_functions:
			print('list_of_expressions_')
		if self.check_correctness_of_delimiter(','):
			self.next()
			expression = self.expression()
			list_of_expressions = self.list_of_expressions_()
			if list_of_expressions:
				return tree.ListOfExpressionsNode(expression=expression, \
					list_of_expressions=list_of_expressions)
			else:
				return tree.ListOfExpressionsNode(expression=expression)

	def expression(self):
		if self.print_name_of_functions:
			print('expression')

		# если выражение начинается с числа или идентификатора, то это арифметическое выражение
		if self.lexems[self.number_of_current_lexem].type_of_lexem in {TypeOfLexem.number, \
		TypeOfLexem.identificator} or self.lexems[self.number_of_current_lexem].lexem_string in \
		{'+', '-'}:
			arithmetic_expression=self.arithmetic_expression()
			return tree.ExpressionNode(arithmetic_expression=arithmetic_expression)
		# если со строки, то это текстовое выражение
		elif self.lexems[self.number_of_current_lexem].type_of_lexem == TypeOfLexem.string:
			text_const = self.lexems[self.number_of_current_lexem]
			self.next()
			text_expr = tree.TextExpressionNode(text_constant=text_const)
			return tree.ExpressionNode(text_expression=text_expr)
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
			number = self.number()
			arithmetic_expression = self.arithmetic_expression_()
			return tree.ArithmeticExpressionHeadNode(whole_constant=number, arithmetic_expression_tail1=\
				arithmetic_expression)
		elif self.lexems[self.number_of_current_lexem].type_of_lexem == TypeOfLexem.identificator:
			identificator = self.lexems[self.number_of_current_lexem]
			identificator = tree.IdentificatorNode(identificator)
			self.next()
			arithmetic_expression=self.arithmetic_expression_()
			return tree.ArithmeticExpressionHeadNode(variable=identificator, arithmetic_expression_tail2=\
				arithmetic_expression)
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
			sign = self.sign_of_arithmetic_expression()
			arithmetic_expression1 = self.arithmetic_expression()
			arithmetic_expression2 = self.arithmetic_expression_()
			if arithmetic_expression2:
				return tree.ArithmeticExpressionTailNode(sign=sign, arithmetic_expression1=\
					arithmetic_expression1, arithmetic_expression2=arithmetic_expression2)
			else:
				return tree.ArithmeticExpressionTailNode(sign=sign, arithmetic_expression1=\
					arithmetic_expression1)

	def sign_of_arithmetic_expression(self):
		if self.print_name_of_functions:
			print('sign_of_arithmetic_expression')
		if self.check_correctness_of_arithmetic_operation_sign('+'):
			sign = self.lexems[self.number_of_current_lexem]
			self.next()
			return sign
		elif self.check_correctness_of_arithmetic_operation_sign('-'):
			sign = self.lexems[self.number_of_current_lexem]
			self.next()
			return sign
		elif self.check_correctness_of_arithmetic_operation_sign('*'):
			sign = self.lexems[self.number_of_current_lexem]
			self.next()
			return sign
		elif self.check_correctness_of_keyword('div'):
			sign = self.lexems[self.number_of_current_lexem]
			self.next()
			return sign
		elif self.check_correctness_of_keyword('mod'):
			sign = self.lexems[self.number_of_current_lexem]
			self.next()
			return sign
		else:
			raise ParserSyntaxError('Arithmetic operation sign expected')

	def number(self):
		if self.check_correctness_of_arithmetic_operation_sign('+') \
		or self.check_correctness_of_arithmetic_operation_sign('-'):
			sign = self.lexems[self.number_of_current_lexem]
			self.next()
		else:
			sign = None
		if not self.lexems[self.number_of_current_lexem].type_of_lexem == TypeOfLexem.number:
			raise ParserSyntaxError('Number exprected')
		number = self.lexems[self.number_of_current_lexem]
		self.next()
		return tree.WholeConstantNode(sign=sign, number=number)

	def identificator(self):
		if not self.lexems[self.number_of_current_lexem].type_of_lexem == TypeOfLexem.identificator:
			raise ParserSyntaxError('Identificator expected')
		self.next()


def syntatic_analysis(lexems, print_tree):
	parser = Parser(lexems)
	parser.analyse(print_tree)








