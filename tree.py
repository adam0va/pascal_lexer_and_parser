from lexem import Lexem


class AST:
	def __init__(self, minipascal_program):
		self.minipascal_program = minipascal_program

	def print_tree(self):
		self.minipascal_program.print_tree(indent=0)

class MinipascalProgramNode(AST):
	def __init__(self, left, right):
	 	self.head_of_the_program = left # head_of_the_program
	 	self.block = right # block

	def print_tree(self, indent):
		print(f'{" "*indent}minipascal_program')
		self.head_of_the_program.print_tree(indent=indent+2)
		self.block.print_tree(indent=indent+2)

class HeadOfTheProgramNode(AST):
	def __init__(self, name_of_the_program):
		self.name_of_the_program = name_of_the_program

	def print_tree(self, indent):
		print(f'{" "*indent}head_of_the_program')
		self.name_of_the_program.print_tree(indent=indent+2)

class NameOfTheProgramNode(AST):
	def __init__(self, identificator):
		self.name_of_the_program = identificator

	def print_tree(self, indent):
		print(f'{" "*indent}name_of_the_program')
		self.name_of_the_program.print_tree(indent=indent+2)

class IdentificatorNode(AST):
	def __init__(self, lexem: Lexem):
		self.identificator = lexem

	def print_tree(self, indent):
		print(f'{" "*indent}identificator\t{self.identificator.lexem_string}')

class BlockNode(AST):
	'''
	def __init__(self, declarative_part):
		self.declarative_part = declarative_part

	def print_tree(self, indent):
		print(f'{" "*indent}block')
		self.declarative_part.print_tree(indent=indent+2)
	'''
	def __init__(self, operators, **kwargs):
		if 'declarative_part' in kwargs:
			self.declarative_part = kwargs['declarative_part']
		self.operators = operators

	def print_tree(self, indent):
		print(f'{" "*indent}block')
		if self.declarative_part:
			self.declarative_part.print_tree(indent=indent+2)
			self.operators.print_tree(indent=indent+2)

class DeclarativePartNode(AST):
	def __init__(self, list_of_sections):
		self.list_of_sections = list_of_sections

	def print_tree(self, indent):
		print(f'{" "*indent}declarative_part')
		self.list_of_sections.print_tree(indent=indent+2)

class ListOfSectionsNode(AST):
	def __init__(self, section, **kwargs):
		self.section = section
		if 'list_of_sections' in kwargs:
			self.list_of_sections = kwargs['list_of_sections']
		else:
			self.list_of_sections = None

	def print_tree(self, indent):
		print(f'{" "*indent}list_of_sections')
		self.section.print_tree(indent=indent+2)
		if self.list_of_sections:
			self.list_of_sections.print_tree(indent=indent+2)

class SectionNode(AST):
	def __init__(self, **kwargs):
		if 'section_of_variables' in kwargs:
			self.section_of_variables = kwargs['section_of_variables']
		else:
			self.section_of_variables = None
		
		if 'section_of_constants' in kwargs:
			self.section_of_constants = kwargs['section_of_constants']
		else:
			self.section_of_constants = None

	def print_tree(self, indent):
		print(f'{" "*indent}section')
		if self.section_of_variables:
			self.section_of_variables.print_tree(indent=indent+2)
			
		if self.section_of_constants:
			self.section_of_constants.print_tree(indent=indent+2)
			

class SectionOfVariablesNode(AST):
	def __init__(self, list_of_var_descriptions):
		self.list_of_var_descriptions = list_of_var_descriptions

	def print_tree(self, indent):
		print(f'{" "*indent}section_of_variables')
		self.list_of_var_descriptions.print_tree(indent=indent+2)

class ListOfVarDescriptionsNode(AST):
	def __init__(self, var_description, **kwargs):
		self.var_description = var_description
		if 'list_of_var_descriptions' in kwargs:
			self.list_of_var_descriptions = kwargs['list_of_var_descriptions']
		else:
			self.list_of_var_descriptions = None

	def print_tree(self, indent):
		print(f'{" "*indent}list_of_var_descriptions')
		self.var_description.print_tree(indent=indent+2)
		if self.list_of_var_descriptions:
			self.list_of_var_descriptions.print_tree(indent=indent+2)


class VarDescriptionNode(AST):
	def __init__(self, list_of_variables, type: Lexem):
		self.list_of_variables = list_of_variables
		self.type = type

	def print_tree(self, indent):
		print(f'{" "*indent}var_description')
		self.list_of_variables.print_tree(indent=indent+2)
		self.type.print_tree(indent=indent+2)


class ListOfVariablesNode(AST):
	def __init__(self, variable, **kwargs):
		self.variable = variable
		if 'list_of_variables' in kwargs:
			self.list_of_variables = kwargs['list_of_variables']
		else:
			self.list_of_variables = None

	def print_tree(self, indent):
		print(f'{" "*indent}list_of_variables')
		self.variable.print_tree(indent=indent+2)
		if self.list_of_variables:
			self.list_of_variables.print_tree(indent=indent+2)

class VariableNode(AST):
	def __init__(self, identificator: Lexem):
		self.variable = identificator

	def print_tree(self, indent):
		print(f'{" "*indent}variable')
		self.variable.print_tree(indent=indent+2)

class TypeNode(AST):
	def __init__(self, keyword: Lexem):
		self.type = keyword

	def print_tree(self, indent):
		print(f'{" "*indent}type\t{self.type.lexem_string}')

class OperatorsNode(AST):
	def __init__(self, operators_sequence):
		self.operators_sequence = operators_sequence

	def print_tree(self, indent):
		print(f'{" "*indent}operators')
		self.operators_sequence.print_tree(indent=indent+2)

class OperatorsSequenceNode(AST):
	def __init__(self, operator, **kwargs):
		self.operator = operator
		if 'operators_sequence' in kwargs:
			self.operators_sequence = kwargs['operators_sequence']
		else:
			self.operators_sequence = None

	def print_tree(self, indent):
		print(f'{" "*indent}operators_sequence')
		self.operator.print_tree(indent=indent+2)
		if self.operators_sequence:
			self.operators_sequence.print_tree(indent=indent+2)


class OperatorNode(AST):
	def __init__(self, **kwargs):
		if 'input_operator' in kwargs:
			self.input_operator = kwargs['input_operator']
		else:
			self.input_operator = None
		if 'output_operator' in kwargs:
			self.output_operator = kwargs['output_operator']
		else:
			self.output_operator = None
		if 'operator_of_assignment' in kwargs:
			self.operator_of_assignment = kwargs['operator_of_assignment']
		else:
			self.operator_of_assignment = None
		if 'if_operator' in kwargs:
			self.if_operator = kwargs['if_operator']
		else:
			self.if_operator = None
		if 'empty_operator' in kwargs:
			self.empty_operator = ['empty_operator']
		else:
			self.empty_operator = None

	def print_tree(self, indent):
		print(f'{" "*indent}operator')
		if self.input_operator:
			self.input_operator.print_tree(indent=indent+2)
		elif self.output_operator:
			self.output_operator.print_tree(indent=indent+2)
		elif self.operator_of_assignment:
			self.operator_of_assignment.print_tree(indent=indent+2)
		elif self.if_operator:
			self.if_operator.print_tree(indent=indent+2)
		elif self.empty_operator:
			self.empty_operator.print_tree(indent=indent+2)

class IfOperatorNode(AST):
	def __init__(self, logic_expression, operator, **kwargs):
		self.logic_expression = logic_expression
		self.operator = operator

	def print_tree(self, indent):
		print(f'{" "*indent}if_operator')
		print(f'{" "*(indent+2)}logic_expression\t{self.logic_expression.lexem_string}')
		self.operator.print_tree(indent=indent+2)

class InputOperatorNode(AST):
	def __init__(self, **kwagrs):
		if 'input_list' in kwagrs:
			self.input_list = kwagrs['input_list']
		else:
			self.input_list = None

	def print_tree(self, indent):
		print(f'{" "*indent}input_operator')
		if self.input_list:
			self.input_list.print_tree(indent=indent+2)

class InputListNode(AST):
	def __init__(self, input_list):
		self.input_list = input_list

	def print_tree(self, indent):
		print(f'{" "*indent}input_list')
		self.input_list.print_tree(indent=indent+2)		

class OutputOperatorNode(AST):
	def __init__(self, output_list):
		self.output_list = output_list

	def print_tree(self, indent):
		print(f'{" "*indent}output_operator')
		self.output_list.print_tree(indent=indent+2)

class OutputListNode(AST):
	def __init__(self, list_of_expressions):
		self.list_of_expressions = list_of_expressions

	def print_tree(self, indent):
		print(f'{" "*indent}output_list')
		self.list_of_expressions.print_tree(indent=indent+2)

class ListOfExpressionsNode(AST):
	def __init__(self, expression, **kwargs):
		self.expression = expression
		if 'list_of_expressions' in kwargs:
			self.list_of_expressions = kwargs['list_of_expressions']
		else:
			self.list_of_expressions = None

	def print_tree(self, indent):
		print(f'{" "*indent}list_of_expressions')
		self.expression.print_tree(indent=indent+2)
		if self.list_of_expressions:
			self.list_of_expressions.print_tree(indent=indent+2)

class ExpressionNode(AST):
	def __init__(self, **kwargs):
		if 'arithmetic_expression' in kwargs:
			self.arithmetic_expression = kwargs['arithmetic_expression']
		else:
			self.arithmetic_expression = None
		if 'text_expression' in kwargs:
			self.text_expression = kwargs['text_expression']
		else:
			self.text_expression = None

	def print_tree(self, indent):
		print(f'{" "*indent}expression')
		if self.arithmetic_expression:
			self.arithmetic_expression.print_tree(indent=indent+2)
		elif self.text_expression:
			self.text_expression.print_tree(indent=indent+2)

class ArithmeticExpressionHeadNode(AST):
	def __init__(self, **kwargs):
		if 'whole_constant' in kwargs and 'arithmetic_expression_tail1' in kwargs:
			self.whole_constant = kwargs['whole_constant']
			self.arithmetic_expression_tail1 = kwargs['arithmetic_expression_tail1']
		else:
			self.whole_constant = None
			self.arithmetic_expression_tail1 = None
		if 'variable' in kwargs and 'arithmetic_expression_tail2' in kwargs:
			self.variable = kwargs['variable']
			self.arithmetic_expression_tail2 = kwargs['arithmetic_expression_tail2']
		else:
			self.variable = None
			self.arithmetic_expression_tail2 = None

	def print_tree(self, indent):
		print(f'{" "*indent}arithmetic_expression_head')
		if self.whole_constant:
			self.whole_constant.print_tree(indent=indent+2)
			if self.arithmetic_expression_tail1: 
				self.arithmetic_expression_tail1.print_tree(indent=indent+2)
		elif self.variable:
			self.variable.print_tree(indent=indent+2)
			if self.arithmetic_expression_tail2:
				self.arithmetic_expression_tail2.print_tree(indent=indent+2)

class ArithmeticExpressionTailNode(AST):
	def __init__(self, sign, arithmetic_expression1, **kwargs):
		self.sign = sign
		self.arithmetic_expression1 = arithmetic_expression1
		if 'arithmetic_expression2' in kwargs:
			self.arithmetic_expression2 = kwargs['arithmetic_expression2']
		else:
			self.arithmetic_expression2 = None

	def print_tree(self, indent):
		print(f'{" "*indent}arithmetic_expression_tail')
		print(f'{" "*(indent+2)}sign\t{self.sign.lexem_string}')
		# self.sign.print_tree(indent=indent+2)
		if self.arithmetic_expression1:
			self.arithmetic_expression1.print_tree(indent=indent+2)
		if self.arithmetic_expression2:
			self.arithmetic_expression2.print_tree(indent=indent+2)

class TextExpressionNode(AST):
	def __init__(self, text_constant):
		self.text_constant = text_constant

	def print_tree(self, indent):
		print(f'{" "*indent}text_expression\t{self.text_constant.lexem_string}')

class OperatorOfAssignmentNode(AST):
	def __init__(self, variable, sign, expression):
		self.variable = variable
		self.sign_of_assignment = sign
		self.expression = expression

	def print_tree(self, indent):
		print(f'{" "*indent}operator_of_assignment')
		self.variable.print_tree(indent=indent+2)
		print(f'{" "*(indent+2)}sign_of_assignment\t{self.sign_of_assignment.lexem_string}')
		self.expression.print_tree(indent=indent+2)

class EmptyOperator(AST):
	def __init__(self):
		pass

	def print_tree(self, indent):
		print(f'{" "*indent}empty_operator')

class WholeConstantNode(AST):
	def __init__(self, sign, number):
		self.sign = sign
		self.number = number

	def print_tree(self, indent):
		print(f'{" "*indent}whole_constant')
		if self.sign:
			print(f'{" "*(indent+2)}{self.sign.lexem_string}{self.number.lexem_string}')
		else:
			print(f'{" "*(indent+2)}{self.number.lexem_string}')

class SectionOfConstantsNode(AST):
	def __init__(self, list_of_const_declarations):
		self.list_of_const_declarations = list_of_const_declarations

	def print_tree(self, indent):
		print(f'{" "*indent}section_of_constants')
		self.list_of_const_declarations.print_tree(indent=indent+2)

class ListOfConstantsDeclarationsNode(AST):
	def __init__(self, const_declaration, **kwargs):
		self.const_declaration = const_declaration
		if 'list_of_const_declarations' in kwargs:
			self.list_of_const_declarations = kwargs['list_of_const_declarations']
		else:
			self.list_of_const_declarations = None

	def print_tree(self, indent):
		print(f'{" "*indent}list_of_const_declarations')
		self.const_declaration.print_tree(indent=indent+2)
		if self.list_of_const_declarations:
			self.list_of_const_declarations.print_tree(indent=indent+2)

class ConstantDeclarationNode(AST):
	def __init__(self, name_of_constant, constant):
		self.name_of_constant = name_of_constant
		self.constant = constant

	def print_tree(self, indent):
		print(f'{" "*indent}constant_declaration')
		self.name_of_constant.print_tree(indent=indent+2)
		self.constant.print_tree(indent=indent+2)

class ConstantNode(AST):
	def __init__(self, **kwargs):
		if 'text_constant' in kwargs:
			self.text_constant = kwargs['text_constant']
		else:
			self.text_constant = None
		if 'whole_constant' in kwargs:
			self.whole_constant = kwargs['whole_constant']
		else:
			self.whole_constant = None

	def print_tree(self, indent):
		print(f'{" "*indent}constant')
		if self.text_constant:
			print(f'{" "*(indent+2)}text_constant\t{self.text_constant.lexem_string}')
		if self.whole_constant:
			self.whole_constant.print_tree(indent=indent+2)




		















