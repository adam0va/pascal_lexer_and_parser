from enum import Enum

class TypeOfLexem(Enum):
	string = 1
	number = 2
	keyword = 3
	identificator = 4

class Lexem:
	def __init__(self, number_of_line_, lexem_string_, type_of_lexem_, **kwagrs):
		self.number_of_line = number_of_line_
		self.lexem_string = lexem_string_
		if 'lexem_int' in kwagrs:
			self.lexem_int = kwagrs['lexem_int']
		else:
			self.lexem_int = 0
		self.type_of_lexem = type_of_lexem_