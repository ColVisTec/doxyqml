import logging
import re

TYPE_RX = "(?P<prefix>\s+type:)(?P<type>[\w.<>|]+)"

def post_process_type(rx, text, type):
    match = rx.search(text)
    if match:
        type = match.group("type")
        text = text[:match.start("prefix")] + text[match.end("type"):]
    return text, type

class QmlClass(object):
    SINGLETON_COMMENT = "/** @remark This component is a singleton */"
    VERSION_COMMENT = "/** @since %s */"

    def __init__(self, name, version = None):
        self.name = name
        self.base_name = ""
        self.header_comments = []
        self.footer_comments = []
        self.elements = []
        self.imports = []
        self.top_level = True

        if version:
            self.header_comments.append(QmlClass.VERSION_COMMENT % version)


    def get_attributes(self):
        return [x for x in self.elements if isinstance(x, QmlAttribute)]

    def get_properties(self):
        return [x for x in self.elements if isinstance(x, QmlProperty)]

    def get_functions(self):
        return [x for x in self.elements if isinstance(x, QmlFunction)]

    def get_signals(self):
        return [x for x in self.elements if isinstance(x, QmlSignal)]

    def add_element(self, element):
        self.elements.append(element)

    def add_header_comment(self, obj):
        self.header_comments.append(obj)

    def add_footer_comment(self, obj):
        self.footer_comments.append(obj)

    def add_import(self, decl):
        module = decl.split()[1]
        if module[0] == '"':
            # Ignore directory or javascript imports for now
            return
        self.imports.append(module)

    def add_pragma(self, decl):
        args = decl.split(' ', 2)[1].strip()

        if args.lower() == "singleton":
            self.header_comments.append(QmlClass.SINGLETON_COMMENT)

    def __str__(self):
        name = self.name.split('.')

        lst = []
        if self.top_level:
            for module in self.imports:
                lst.append("using namespace %s;" % module.replace('.', '::'))
            if len(name) > 1:
                lst.append("namespace %s {" % '::'.join(name[:-1]))

        lst.extend([str(x) for x in self.header_comments])

        # Either the top level component, or a (grand)child component with ID.
        # Do not show child objects without IDs.
        show_object = True
        if not self.top_level:
            show_object = False
            for attr in self.get_attributes():
                if attr.name == "id":
                    if self.comment is not None:
                        lst.append(self.comment);
                    lst.append("%s %s;" % (name[-1], attr.value));
                    show_object = True
                    break

        # For child objects with IDs, associate the object with the top-level
        # object. This avoids very deep nesting in the generated documentation.
        if show_object:
            class_decl = "class " + name[-1]
            if len(self.base_name) > 0:
                class_decl += " : public " + self.base_name

            class_decl += " {"
            lst.append(class_decl)
            lst.append("public:")
            if self.top_level:
                lst.extend([str(x) for x in self.elements])
            else:
                for x in self.elements:
                    if not isinstance(x, QmlClass):
                        lst.append(str(x))

            lst.append("};")

        if not self.top_level:
            for x in self.elements:
                if isinstance(x, QmlClass):
                    lst.append(str(x))

        lst.extend([str(x) for x in self.footer_comments])
        if self.top_level and len(name) > 1:
            lst.append("}")

        return "\n".join(lst)


class QmlArgument(object):
    def __init__(self, name):
        self.type = ""
        self.name = name

    def __str__(self):
        if self.type == "":
            return self.name
        else:
            return self.type + " " + self.name


class QmlAttribute(object):
    def __init__(self):
        self.name = ""
        self.value = ""
        self.type = "var"
        self.doc = ""

    def __str__(self):
        if self.name != "id":
            lst = []
            if len(self.doc) > 0:
                lst.append(self.doc)
            lst.append(self.type + " " + self.name + ";")
            return "\n".join(lst)
        else:
            return ""


class QmlProperty(object):
    type_rx = re.compile(TYPE_RX)

    DEFAULT_PROPERTY_COMMENT = "/** @remark This is the default property */"
    READONLY_PROPERTY_COMMENT = "/** @remark This property is read-only */"

    def __init__(self):
        self.type = ""
        self.is_default = False
        self.is_readonly = False
        self.name = ""
        self.doc = ""
        self.doc_is_inline = False

    def __str__(self):
        self.post_process_doc()
        lst = []
        if not self.doc_is_inline:
            lst.append(self.doc + "\n")
        if self.is_default:
            lst.append(self.DEFAULT_PROPERTY_COMMENT + "\n")
        elif self.is_readonly:
            lst.append(self.READONLY_PROPERTY_COMMENT + "\n")
        lst.append("Q_PROPERTY(%s %s)" % (self.type, self.name))
        if self.doc_is_inline:
            lst.append(" " + self.doc)
        return "".join(lst)

    def post_process_doc(self):
        self.doc, self.type = post_process_type(self.type_rx, self.doc, self.type)


class QmlFunction(object):
    doc_arg_rx = re.compile(r"[@\\]param" + TYPE_RX + "\s+(?P<name>\w+)")
    return_rx = re.compile(r"[@\\]returns?" + TYPE_RX)
    def __init__(self):
        self.type = "void"
        self.name = ""
        self.doc = ""
        self.doc_is_inline = False
        self.args = []

    def __str__(self):
        self.post_process_doc()
        arg_string = ", ".join([str(x) for x in self.args])
        lst = []
        if not self.doc_is_inline:
            lst.append(self.doc + "\n")
        lst.append("%s %s(%s);" % (self.type, self.name, arg_string))
        if self.doc_is_inline:
            lst.append(" " + self.doc)
        return "".join(lst)

    def post_process_doc(self):
        def repl(match):
            # For each argument with a specified type, update arg.type and return a typeless @param line
            type = match.group("type")
            name = match.group("name")
            for arg in self.args:
                if arg.name == name:
                    arg.type = type
                    break
            else:
                logging.warning("In function %s(): Unknown argument %s" % (self.name, name))
            return "@param %s" % name

        self.doc = self.doc_arg_rx.sub(repl, self.doc)
        self.doc, self.type = post_process_type(self.return_rx, self.doc, self.type)


class QmlSignal(object):
    def __init__(self):
        self.name = ""
        self.doc = ""
        self.doc_is_inline = False
        self.args = []

    def __str__(self):
        arg_string = ", ".join([str(x) for x in self.args])
        lst = []
        if not self.doc_is_inline:
            lst.append(self.doc + "\n")
        lst.append("Q_SIGNALS: void %s(%s); " % (self.name, arg_string))
        if self.doc_is_inline:
            lst.append(self.doc + "\n")
        # Appending "public:" here makes it possible to declare a signal without
        # turning all functions defined after into signals.
        # It could be replaced with the use of Q_SIGNAL, but my version of
        # Doxygen (1.8.4) does not support it
        lst.append("public:")
        return "".join(lst)
