from lark.indenter import Indenter #, DedentError
from lark import Lark, Token



class TreeIndenter(Indenter):
    # Deprecated
    NL_type = '_NL'
    OPEN_PAREN_types = []
    CLOSE_PAREN_types = []
    INDENT_type = '_INDENT'
    DEDENT_type = '_DEDENT'
    tab_len = 8
    

class WittyIndenter(Indenter):
    """
    Ignores indentation under selected tags
    for the sake of separate parsing
    """
    NL_type = '_NL'
    OPEN_PAREN_types = []
    CLOSE_PAREN_types = []
    INDENT_type = '_INDENT'
    DEDENT_type = '_DEDENT'
    tab_len = 8
    
    def __init__(self, ignored_types=["_SCRIPT", "_PATTERNS"]):
        super(WittyIndenter, self).__init__()
        self.ignored_types = ignored_types
        self.enabled = True
        self.expect_indent = False
        
    def handle_NL(self, token):
        if self.paren_level > 0:
            return
        yield token
        
        #print(self.expect_indent)
        indent_str = token.rsplit('\n', 1)[1] # Tabs and spaces
        indent = indent_str.count(' ') + indent_str.count('\t') * self.tab_len
        if indent > self.indent_level[-1]: 
            if self.expect_indent:
                self.enabled, self.expect_indent = False, False
                self.indent_level.append(indent)
                yield Token.new_borrow_pos(self.INDENT_type, indent_str, token)
            else:                
                if self.enabled:     
                    self.indent_level.append(indent)
                    yield Token.new_borrow_pos(self.INDENT_type, indent_str, token)
                else:
                    yield token
        else:
            while indent < self.indent_level[-1]:
                self.indent_level.pop()
                self.enabled, self.expect_indent = True, False
                yield Token.new_borrow_pos(self.DEDENT_type, indent_str, token)
                
            #print(self.indent_level)
#            if indent != self.indent_level[-1]:
#                raise DedentError('Unexpected dedent to column %s. Expected dedent to %s' % (indent, self.indent_level[-1]))
        
    def _process(self, stream):
        for token in stream:
            if token.type in self.ignored_types:
                self.expect_indent = True
                
            if token.type == self.NL_type:
                for t in self.handle_NL(token):
                    yield t
            else:
                yield token

            if token.type in self.OPEN_PAREN_types:
                self.paren_level += 1
            elif token.type in self.CLOSE_PAREN_types:
                self.paren_level -= 1
                assert self.paren_level >= 0

        while len(self.indent_level) > 1:
            self.indent_level.pop()
            yield Token(self.DEDENT_type, '')
            
        assert self.indent_level == [0], self.indent_level
        self.enabled, self.expect_indent = True, False


class ScenarioParser:
    def __init__(self, grammar):
        self.parse_scripts = False
        self.parser = Lark.open(grammar, parser = "lalr", 
                                lexer = "contextual", postlex = WittyIndenter(), 
                                debug = True)
    
    def ignore_indentation_in_scripts(self, error):
        print(error.puppet.parser_state.value_stack)
        return False
    
    def parse(self, sc):
        return self.parser.parse(sc, on_error = self.ignore_indentation_in_scripts)