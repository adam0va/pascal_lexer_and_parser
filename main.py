import lexer
import parser

if __name__ == "__main__":
	filename = 'test1.txt'
	lexems = lexer.lex_analysis(filename)

	parser.syntatic_analysis(lexems)


	