CONCAT = 0xC04CA7
ETOILE = 0xE7011E
ALTERN = 0xA17E54
PARENTHESEOUVRANTE = 0x16641664
PARENTHESEFERMANTE = 0x51515151
DOT = 0xD07


class RegExTree(object):

    def __init__(self, root, subtrees):
        self.root = root
        self.subTrees = subtrees

    def __repr__(self):
        return "RegExTree"

    def __str__(self):
        if not self.subTrees:
            return self.str_root()
        return self.str_root() + self.str_children()

    def str_children(self):
        if not self.get_sbtree_l():
            return "(" + str(self.get_sbtree_r()) + ")"
        if not self.get_sbtree_r():
            return "(" + str(self.get_sbtree_l()) + ")"
        return "(" + str(self.get_sbtree_l()) + "," + str(self.get_sbtree_r()) + ")"

    def str_root(self):
        if self.root == PARENTHESEOUVRANTE:
            return "("
        if self.root == PARENTHESEFERMANTE:
            return ")"
        if self.root == CONCAT:
            return "."
        if self.root == ALTERN:
            return "|"
        if self.root == ETOILE:
            return "*"
        if self.root == DOT:
            return "."
        return str(self.root)

    def get_sbtree_l(self):
        if self.subTrees:
            return self.subTrees[0]
        return None

    def get_sbtree_r(self):
        if self.subTrees:
          return self.subTrees[1]
        return None

    def set_sbtree_l(self, tree):
        if self.subTrees:
            self.subTrees[0] = tree

    def set_sbtree_r(self, tree):
        if self.subTrees:
            self.subTrees[1] = tree

    def str_ascii(self):
        if not self.subTrees:
            return str(ord(self.root)) + ", " + self.str_ascii()

    def postfix(self):
        print(self.str_root())
        if self.get_sbtree_l():
            self.get_sbtree_l().postfix()
        if self.get_sbtree_r():
            self.get_sbtree_r().postfix()

