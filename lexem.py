from enum import Enum

class Type_of_Lexem(Enum):
	string = 1
	number = 2
	keyword = 3
	identificator = 4

class Lexem:
	def __init__(self, number_of_line_, lexem_string_, type_of_lexem_):
		number_of_line = number_of_line_
		lexem_string = lexem_string_
		type_of_lexem = type_of_lexem_