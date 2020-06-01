from lexem import Lexem


class AST:
	def __init__(self, minipascal_program):
		self.minipascal_program = minipascal_program

	def print_tree(self):
		self.minipascal_program.print_tree(indent=0)

class MinipascalProgramNode(AST):
	def __init__(self, left, right):
	 	self.head_of_the_program = left # head_of_the_program
	 	#self.block = right # block

	def print_tree(self, indent):
		indent_string = ''
		indent_string.join(' ' for x in range(indent))
		print(f'{" "*indent}minipascal_program')
		self.head_of_the_program.print_tree(indent=indent+2)
		#self.block.print_tree(indent=indent+2)

class HeadOfTheProgramNode(AST):
	def __init__(self, name_of_the_program):
		self.name_of_the_program = name_of_the_program

	def print_tree(self, indent):
		indent_string = ''
		indent_string.join(' ' for x in range(indent))
		print(f'{" "*indent}head_of_the_program')
		self.name_of_the_program.print_tree(indent=indent+2)

class NameOfTheProgramNode(AST):
	def __init__(self, identificator):
		self.name_of_the_program = identificator

	def print_tree(self, indent):
		indent_string = ''
		indent_string.join(' ' for x in range(indent))
		print(f'{" "*indent}name_of_the_program')
		self.name_of_the_program.print_tree(indent=indent+2)

class IdentificatorNode(AST):
	def __init__(self, lexem: Lexem):
		self.identificator = lexem

	def print_tree(self, indent):
		indent_string = ''
		indent_string.join(' ' for x in range(indent))
		print(f'{" "*indent}identificator\t{self.identificator.lexem_string}')

class BlockNode(AST):
	def __init__(self, operators, **kwargs):
		if 'declarative_part' in kwargs:
			self.declarative_part = kwargs['declarative_part']
		self.operators = right

	def print__tree(indent):
		indent_string = ''
		indent_string.join(' ' for x in range(indent))
		print(f'{indent_string}block')
		if self.declarative_part:
			self.declarative_part.print_tree(indent=indent+2)
			self.operators.print_tree(indent=indent+2)

class DeclarativePartNode(AST):
	def __init__(self, list_of_sections):
		self.list_of_sections = list_of_sections

class ListOfSectionsNode(AST):
	def __init__(self, section, list_of_sections):
		self.section = section
		self.list_of_sections = list_of_sections

class SectionNode(AST):
	def __init__(self, **kwargs):
		if 'section_of_variables' in kwargs:
			self.declarative_part = kwargs['section_of_variables']
		if 'section_of_constants' in kwargs:
			self.declarative_part = kwargs['section_of_constants']

class SectionOfVariablesNode(AST):
	def __init__(self, list_of_var_descriptions):
		self.list_of_var_descriptions = list_of_var_descriptions

class ListOfVarDescriptionsNode(AST):
	def __init__(self, var_description, **kwargs):
		self.var_description = var_description
		if 'list_of_var_descriptions' in kwargs:
			self.list_of_var_descriptions = kwargs['list_of_var_descriptions']

class VarDescriptionNode(AST):
	def __init__(self, list_of_variables, type: Lexem):
		self.list_of_variables = list_of_variables
		self.type = type

class ListOfVariablesNode(AST):
	def __init__(self, variable, **kwargs):
		self.variable = variable
		if 'list_of_variables' in kwargs:
			self.list_of_variables = kwargs['list_of_variables']













