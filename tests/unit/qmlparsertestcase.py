from unittest import TestCase

from doxyqml.lexer import Lexer
from doxyqml.qmlclass import QmlClass
from doxyqml import qmlparser


class QmlParserTestCase(TestCase):
    def test(self):
        src = "Item { function foo() {} function bar() {} }"
        lexer = Lexer(src)
        lexer.tokenize()
        qmlclass = QmlClass("Foo")
        qmlparser.parse(lexer.tokens, qmlclass)

        self.assertEqual(qmlclass.base_name, "Item")

        functions = qmlclass.get_functions()
        self.assertEqual(len(functions), 2)
        self.assertEqual(functions[0].name, "foo")
        self.assertEqual(functions[1].name, "bar")

    def test_default_property(self):
        src = """Item {
            /// v1 doc
            default property int v1
            /// v2 doc
            property int v2
            }"""
        lexer = Lexer(src)
        lexer.tokenize()
        qmlclass = QmlClass("Foo")
        qmlparser.parse(lexer.tokens, qmlclass)

        properties = qmlclass.get_properties()
        self.assertEqual(len(properties), 2)
        self.assertEqual(properties[0].name, "v1")
        self.assertEqual(properties[0].type, "int")
        self.assertEqual(properties[0].doc, "/// v1 doc")
        self.assertTrue(properties[0].is_default)

        self.assertEqual(properties[1].name, "v2")
        self.assertEqual(properties[1].type, "int")
        self.assertEqual(properties[1].doc, "/// v2 doc")
        self.assertFalse(properties[1].is_default)

    def test_readonly_property(self):
        src = """Item {
            /// v1 doc
            readonly property int v1
            /// v2 doc
            property int v2
            }"""
        lexer = Lexer(src)
        lexer.tokenize()
        qmlclass = QmlClass("Foo")
        qmlparser.parse(lexer.tokens, qmlclass)

        properties = qmlclass.get_properties()
        self.assertEqual(len(properties), 2)
        self.assertEqual(properties[0].name, "v1")
        self.assertEqual(properties[0].type, "int")
        self.assertEqual(properties[0].doc, "/// v1 doc")
        self.assertTrue(properties[0].is_readonly)

        self.assertEqual(properties[1].name, "v2")
        self.assertEqual(properties[1].type, "int")
        self.assertEqual(properties[1].doc, "/// v2 doc")
        self.assertFalse(properties[1].is_readonly)

    def test_var_property(self):
        src = """Item {
            property var varProperty: { "key1": "value1", "key2": "value2" }
            }"""

        lexer = Lexer(src)
        lexer.tokenize()
        qmlclass = QmlClass("Foo")
        qmlparser.parse(lexer.tokens, qmlclass)

        properties = qmlclass.get_properties()
        self.assertEqual(len(properties), 1)
        self.assertEqual(properties[0].name, "varProperty")
        self.assertEqual(properties[0].type, "var")

    def test_function_property(self):
        src = """Item {
            property var fnProperty: function (arg1, arg2) { return arg1 + arg2; }
            }"""

        lexer = Lexer(src)
        lexer.tokenize()
        qmlclass = QmlClass("Foo")
        qmlparser.parse(lexer.tokens, qmlclass)

        properties = qmlclass.get_properties()
        self.assertEqual(len(properties), 1)
        self.assertEqual(properties[0].name, "fnProperty")
        self.assertEqual(properties[0].type, "var")

    def test_multiline_string(self):
        src = """Item {
            prop1: "A string that spans \\
            multiple lines"
            /// prop2 doc
            property string prop2: "bar"
            }"""

        lexer = Lexer(src)
        lexer.tokenize()
        qmlclass = QmlClass("Foo")
        qmlparser.parse(lexer.tokens, qmlclass)

        properties = qmlclass.get_properties()
        self.assertEqual(len(properties), 1)
        self.assertEqual(properties[0].name, "prop2")
        self.assertEqual(properties[0].type, "string")
        self.assertEqual(properties[0].doc, "/// prop2 doc")

    def test_normal_arguments(self):
        src = """Item {
                     function foo(arg1, arg2) {
                         return arg1 + arg2;
                     }
                 }"""

        lexer = Lexer(src)
        lexer.tokenize()
        qmlclass = QmlClass("Foo")
        qmlparser.parse(lexer.tokens, qmlclass)

        functions = qmlclass.get_functions()
        self.assertEqual(len(functions), 1)
        self.assertEqual(functions[0].name, "foo")
        self.assertEqual(functions[0].type, "void")

    def test_keyword_arguments(self):
        src = """Item {
                     function foo(propertyArgument, signalArgument) {
                         return propertyArgument + signalArgument;
                     }
                 }"""

        lexer = Lexer(src)
        lexer.tokenize()
        qmlclass = QmlClass("Foo")
        qmlparser.parse(lexer.tokens, qmlclass)

        functions = qmlclass.get_functions()
        self.assertEqual(len(functions), 1)
        self.assertEqual(functions[0].name, "foo")
        self.assertEqual(functions[0].type, "void")

    def test_signals(self):
        src = """Item {
                     signal userAdded(string username, int age)
                 }"""

        lexer = Lexer(src)
        lexer.tokenize()
        qmlclass = QmlClass("Foo")
        qmlparser.parse(lexer.tokens, qmlclass)

        signals = qmlclass.get_signals()
        self.assertEqual(len(signals), 1)
        signal = signals[0]
        self.assertEqual(signal.name, "userAdded")

        self.assertEqual(len(signal.args), 2)
        self.assertEqual(signal.args[0].name, "username")
        self.assertEqual(signal.args[0].type, "string")
        self.assertEqual(signal.args[1].name, "age")
        self.assertEqual(signal.args[1].type, "int")

    def test_functions(self):
        src = """Item {
                    function scale(aspect = 4.0 / 3.0) {}
                 }"""
        lexer = Lexer(src)
        lexer.tokenize()
        qmlclass = QmlClass("Foo")
        qmlparser.parse(lexer.tokens, qmlclass)
        functions = qmlclass.get_functions()
        self.assertEqual(len(functions), 1)
        self.assertEqual(functions[0].args[0].name, "aspect")
        self.assertEqual(functions[0].args[0].default_value, "4.0/3.0")
