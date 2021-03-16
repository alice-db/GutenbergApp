from regparser import regextree as rt


def is_valid(regex):
    return len(regex) > 0


def char_to_root(c):
    if c == '(':
        return rt.PARENTHESEOUVRANTE
    if c == ')':
        return rt.PARENTHESEFERMANTE
    if c == '*':
        return rt.ETOILE
    if c == '|':
        return rt.ALTERN


def get_char_or_dot(c):
    if c == ".":
        return rt.DOT
    return c


class Parser(object):
    def __init__(self, regex):
        self.regex = regex
        self.regexTree = None

    def __repr__(self):
        return "Parser"

    def __str__(self):
        return str(self.regexTree)

    def peek_char(self):
        if is_valid(self.regex):
            return self.regex[0]

    def read_char(self):
        if is_valid(self.regex):
            return self.regex.pop(0)

    # RETURN: subtree in parenthesis
    def parse_parenthesis(self):
        if char_to_root(self.read_char()) == rt.PARENTHESEOUVRANTE:
            self.regexTree = self.parse_m()
        if char_to_root(self.read_char()) == rt.PARENTHESEFERMANTE:
            if is_valid(self.regex) and char_to_root(self.peek_char()) == rt.ETOILE:
                self.read_char()
                return rt.RegExTree(rt.ETOILE, [self.regexTree, []])
            else:
                return self.regexTree

    def parse_m(self):
        if is_valid(self.regex):
            self.regexTree = self.parse_char_or_parenthesis()
            return self.parse_main()

    def parse_char_or_parenthesis(self):
        c = self.peek_char()
        if char_to_root(c) == rt.PARENTHESEOUVRANTE:
            expr = self.parse_parenthesis()
            if is_valid(self.regex) and char_to_root(self.peek_char()) == rt.ETOILE:
                self.read_char()
                return rt.RegExTree(rt.ETOILE, [expr, []])
            else:
                return expr
        else:
            self.read_char()
            if is_valid(self.regex) and char_to_root(self.peek_char()) == rt.ETOILE:
                self.read_char()
                return rt.RegExTree(rt.ETOILE, [rt.RegExTree(get_char_or_dot(c), []), []])
            else:
                return rt.RegExTree(get_char_or_dot(c), [])

    def parse_next_altern(self, tree):
        if is_valid(self.regex):
            c = self.peek_char()
            if char_to_root(c) == rt.ALTERN:
                return tree
            if char_to_root(c) == rt.PARENTHESEFERMANTE:
                return tree
            tree = rt.RegExTree(rt.CONCAT, [tree, self.parse_char_or_parenthesis()])
            return self.parse_next_altern(tree)
        else:
            return tree

    def parse_main(self):
        if is_valid(self.regex):
            c = self.peek_char()
            if char_to_root(c) == rt.PARENTHESEOUVRANTE:
                self.regexTree = rt.RegExTree(rt.CONCAT, [self.regexTree, self.parse_parenthesis()])
                return self.parse_main()
            else:
                if char_to_root(c) == rt.ALTERN:
                    self.read_char()
                    self.regexTree = rt.RegExTree(rt.ALTERN, [self.regexTree, self.parse_next_altern(self.parse_char_or_parenthesis())])
                    return self.parse_main()
                else:
                    if char_to_root(c) == rt.PARENTHESEFERMANTE:
                        return self.regexTree
                    else:
                        self.regexTree = rt.RegExTree(rt.CONCAT, [self.regexTree, self.parse_char_or_parenthesis()])
                        return self.parse_main()
        else:
            return self.regexTree

