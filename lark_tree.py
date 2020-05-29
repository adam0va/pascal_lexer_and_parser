from lark import Lark

def build_AST(filename):
	file = open(filename, 'r')
	text = file.read()

	parser = Lark(open('grammar.lark'))
	print(parser.parse(text).pretty())

