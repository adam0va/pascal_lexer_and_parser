from lark import Lark

def build_AST():
	file = open('test1.txt', 'r')
	text = file.read()

	parser = Lark(open('grammar.lark'))
	print(parser.parse(text).pretty())

