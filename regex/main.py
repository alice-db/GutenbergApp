from regparser import regex_parser
from automates import ndfa, dfa
from reader import read


def read_input():
    regex = input("Entrer une RegExpr: ")

    if not regex_parser.is_valid(regex):
        raise Exception("Entree invalide: " + regex)

    parsed_regex = regex_parser.Parser(list(regex))
    parsed_regex.parse_m()
    # print("Tree format RegExpr: " + str(parsed_regex))

    ndfa_graph = ndfa.NDFA(parsed_regex.regexTree)
    ndfa_graph.construct()
    # print("ndfa graph: " + str(ndfa_graph))

    dfa_graph = dfa.DFA(ndfa.NDFA.ndfa_graph)
    dfa_graph.construct()
    # print("dfa graph: " + str(dfa_graph))

    result = read.Reader(dfa_graph.dfa)

    for line in result.lines:
        print(str(line))


if __name__ == '__main__':
    read_input()
