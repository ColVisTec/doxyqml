from collections import namedtuple
import re


COMMENT = "comment"
ICOMMENT = "inline_comment"
STRING = "string"
ELEMENT = "element"
BLOCK_START = "block_start"
BLOCK_END = "block_end"
ARRAY_START = "array_start"
ARRAY_END = "array_end"
CHAR = "char"
KEYWORD = "keyword"
IMPORT = "import"
PRAGMA = "pragma"
COMPONENT = "component"
ICOMPONENT = "inline_component"
ATTRIBUTE = "attribute"
ELLIPSES = "ellipses"

# not a doxy comment
PLAIN_COMMENT_RX = re.compile("/[/*][^/!*]")


def is_doxy_comment_token(token):
    return token.type == COMMENT and not PLAIN_COMMENT_RX.match(token.value)


class LexerError(Exception):
    def __init__(self, msg, idx):
        Exception.__init__(self, msg)
        self.idx = idx


Token = namedtuple("Token", ["type", "value", "idx", "column"])


class Tokenizer(object):
    def __init__(self, token_type, rx):
        self.token_type = token_type
        self.rx = rx

    def __call__(self, lexer, matched_str):
        lexer.append_token(self.token_type, matched_str)


class Lexer(object):
    def __init__(self, text):
        # Tokens that start at the first non-whitespace character in a line
        self.tokenizers_newline = [
            Tokenizer(ICOMPONENT, re.compile(r"component ([-\w\.]+)\s*")),  # an inline component
            Tokenizer(COMPONENT, re.compile(r"([-\w\.]+)\s*{")),  # a component
            Tokenizer(ATTRIBUTE, re.compile(r"([-\w\.]+)\s*:")),  # an attribute
            ]

        self.tokenizers = [
            Tokenizer(ICOMMENT, re.compile(r"/\*[!*]<.*?\*/", re.DOTALL)),
            Tokenizer(ICOMMENT, re.compile(r"//[/!]<[^\n]*(?:\n[ \t]*//[/!]<[^\n]*)*")),
            Tokenizer(COMMENT, re.compile(r"/\*.*?\*/", re.DOTALL)),
            Tokenizer(COMMENT, re.compile(r"//[^\n]*(?:\n[ \t]*//[^\n]*)*")),
            # A double/single quote or backtick, then either:
            # - anything but a matching quote or a backslash
            # - an escaped char (\n, \t...)
            # then a matching quote
            Tokenizer(STRING, re.compile(r'("([^\\"]|(\\.))*"|\'([^\\\']|(\\.))*\'|`([^\\`]|(\\.))*`)')),
            Tokenizer(BLOCK_START, re.compile("(?<!')\{(?!')")),
            Tokenizer(BLOCK_END, re.compile("(?<!')\}(?!')")),
            Tokenizer(ARRAY_START, re.compile("\[")),
            Tokenizer(ARRAY_END, re.compile("\]")),
            Tokenizer(IMPORT, re.compile(r"import\s+.*")),
            Tokenizer(PRAGMA, re.compile(r"pragma\s+\w.*")),
            Tokenizer(KEYWORD, re.compile(r"(default\s+property|property|readonly\s+property|signal|enum)\s+")),
            Tokenizer(KEYWORD, re.compile(r"(function)\s+[^(]")),  # a named function
            Tokenizer(ELLIPSES, re.compile(r"\.\.\.")),
            Tokenizer(ELEMENT, re.compile(r"\w[\w.<>]*")),
            Tokenizer(CHAR, re.compile(".")),
            ]
        self.text = text.replace('\\\n', '\n')
        self.idx = 0
        self.column = 0
        self.newline = False
        self.tokens = []

    def tokenize(self):
        while True:
            self.advance()
            if self.idx == len(self.text):
                break
            self.apply_tokenizers()
        self.fixup_tokens()

    def advance(self):
        self.newline = False
        if self.idx == 0:
            # Process start-of-file as newline.
            self.newline = True

        while self.idx < len(self.text):
            if self.text[self.idx] == '\n':
                self.newline = True
                self.idx += 1
                self.column = 0
            elif self.text[self.idx].isspace():
                self.idx += 1
                self.column += 1
            else:
                break

    def apply_tokenizers(self):
        if self.newline:
            for tokenizer in self.tokenizers_newline:
                match = tokenizer.rx.match(self.text, self.idx)

                if not match:
                    continue

                if len(match.groups()) > 0:
                    tokenizer(self, match.group(1))
                    self.set_position(match.end(1))
                    return
                else:
                    tokenizer(self, match.group(0))
                    self.set_position(match.end(0))
                    return

        for tokenizer in self.tokenizers:
            match = tokenizer.rx.match(self.text, self.idx)

            if not match:
                continue

            if len(match.groups()) > 0:
                tokenizer(self, match.group(1))
                self.set_position(match.end(1))
                return
            else:
                tokenizer(self, match.group(0))
                self.set_position(match.end(0))
                return

        raise LexerError("No lexer matched", self.idx)

    def fixup_tokens(self):
        for idx, token in enumerate(self.tokens):
            # Fix tokenization of a property named "property". For example:
            #   property string property: "foo"
            if (token.type == KEYWORD and token.value == "property" and idx > 1 and
                    self.tokens[idx - 1].type == ELEMENT and
                    self.tokens[idx - 2].type == KEYWORD and self.tokens[idx - 2].value.endswith("property")):
                self.tokens[idx] = Token(ELEMENT, token.value, token.idx, token.column)
            if token.type == COMMENT or token.type == ICOMMENT:
                self.left_shift_comment(idx)
            if token.type == ICOMMENT and idx > 1:
                self.move_inline_comments(idx)

    def left_shift_comment(self, idx):
        """
        Change the value of multiline-tokens so they look like they were
        defined on column 1 instead of wherever they were.
        """
        token = self.tokens.pop(idx)
        if token.column < 1:
            self.tokens.insert(idx, token)
            return
        rx = re.compile(r"^[ \t]{{{}}}".format(token.column), re.MULTILINE)
        newval = rx.sub("", token.value)
        self.tokens.insert(idx, Token(token.type, newval, token.idx, token.column))

    def move_inline_comments(self, start_idx):
        """
        Move inline comments ahead of their parent KEYWORD. This way they get
        properly handed over to the Qml* object type handlers which can do with
        them as they wish.
        """
        # Iterate backwards looking for a KEYWORD. As a sanity measure we only
        # search back up to 20 tokens or until an "invalid" token is found.
        end_idx = max(start_idx - 20, 0)
        for idx, token in enumerate(self.tokens[start_idx - 1:end_idx:-1]):
            if token.type == KEYWORD:
                ins_idx = start_idx - idx - 1
                if ins_idx <= 0:
                    return
                break
            if token.type in (COMMENT, ICOMMENT, IMPORT, PRAGMA):
                return

        # Final sanity check for a misplaced inline comment
        previous_token = self.tokens[ins_idx - 1]
        if previous_token.type == ICOMMENT or is_doxy_comment_token(previous_token):
            return

        self.tokens.insert(ins_idx, self.tokens.pop(start_idx))

    def append_token(self, type, value):
        self.tokens.append(Token(type, value, self.idx, self.column))

    def set_position(self, idx):
        self.idx = idx
        newline = self.text.rfind("\n", 0, idx)
        if newline == -1:
            self.column = idx
        else:
            self.column = idx - newline - 1
