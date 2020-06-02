import lexer
import parser
import lark_tree

if __name__ == "__main__":
	filename = 'test2.txt'
	lexems = lexer.lex_analysis(filename)

	parser.syntatic_analysis(lexems, print_tree=True)

	#lark_tree.build_AST(filename)


	