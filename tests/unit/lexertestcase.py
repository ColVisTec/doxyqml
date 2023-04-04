from unittest import TestCase

from doxyqml.lexer import Lexer, Token, IMPORT, PRAGMA, STRING, COMMENT, KEYWORD, ELEMENT, \
    BLOCK_START, BLOCK_END, COMPONENT, CHAR


class LexerTestCase(TestCase):
    def test_import(self):
        src = "import foo\n import bar"
        lexer = Lexer(src)
        lexer.tokenize()
        self.assertEqual(lexer.tokens[0], Token(IMPORT, "import foo", 0, 0))
        self.assertEqual(lexer.tokens[1], Token(IMPORT, "import bar", 12, 1))

    def test_pragma(self):
        src = "pragma foo\n pragma bar"
        lexer = Lexer(src)
        lexer.tokenize()
        self.assertEqual(lexer.tokens[0], Token(PRAGMA, "pragma foo", 0, 0))
        self.assertEqual(lexer.tokens[1], Token(PRAGMA, "pragma bar", 12, 1))

    def test_string(self):
        src = r'"hello" "world!" "new\nline" "qu\"ote"'
        lexer = Lexer(src)
        lexer.tokenize()
        self.assertEqual(lexer.tokens[0], Token(STRING, '"hello"', 0, 0))
        self.assertEqual(lexer.tokens[1], Token(STRING, '"world!"', 8, 8))
        self.assertEqual(lexer.tokens[2], Token(STRING, r'"new\nline"', 17, 17))
        self.assertEqual(lexer.tokens[3], Token(STRING, r'"qu\"ote"', 29, 29))

    def test_single_line_comment(self):
        src = "// hello\nimport bob"
        lexer = Lexer(src)
        lexer.tokenize()
        self.assertEqual(lexer.tokens[0], Token(COMMENT, '// hello', 0, 0))
        self.assertEqual(lexer.tokens[1], Token(IMPORT, 'import bob', 9, 0))

    def test_multi_line_comment(self):
        src = "/* hello\nworld *//* good bye\nworld */"
        lexer = Lexer(src)
        lexer.tokenize()
        self.assertEqual(lexer.tokens[0], Token(COMMENT, '/* hello\nworld */', 0, 0))
        self.assertEqual(lexer.tokens[1], Token(COMMENT, '/* good bye\nworld */', 17, 8))

    def test_property_named_property(self):
        src = "Item { property var property }"
        lexer = Lexer(src)
        lexer.tokenize()
        self.assertEqual(lexer.tokens[0], Token(COMPONENT, 'Item', 0, 0))
        self.assertEqual(lexer.tokens[1], Token(BLOCK_START, '{', 5, 5))
        self.assertEqual(lexer.tokens[2], Token(KEYWORD, 'property', 7, 7))
        self.assertEqual(lexer.tokens[3], Token(ELEMENT, 'var', 16, 16))
        self.assertEqual(lexer.tokens[4], Token(ELEMENT, 'property', 20, 20))

    def test_curly_brackets_in_function(self):
        src = "function foo(){ var bar = ' }' }"
        lexer = Lexer(src)
        lexer.tokenize()
        self.assertEqual(lexer.tokens[9], Token(CHAR, '}', 28, 28))
