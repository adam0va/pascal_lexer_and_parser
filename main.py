import lexer
import parser
#import lark_tree
import sys

if __name__ == "__main__":
	filename = 'test3.txt'
	if len (sys.argv) == 1:
		filename = 'test3.txt'
		lexems = lexer.lex_analysis(filename)

		parser.syntatic_analysis(lexems, print_tree=True)
	elif len(sys.argv) == 2:
		filename = sys.argv[1]
		lexems = lexer.lex_analysis(filename)

		parser.syntatic_analysis(lexems, print_tree=True)
	else:
		print('Too many parameters')
		

	

	#lark_tree.build_AST(filename)


	