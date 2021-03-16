
class Reader:

    def __init__(self, dfa):
        # Read file
        file = open("gutenberg.txt", encoding="utf-8")
        text = file.read()
        tinput = text.split("\n")
        id_line = 0
        res = set()
        self.lines = set()
        # for each lines from gutenberg.txt
        for line in tinput:
            if read_line(line.split(), dfa):
                res.add(id_line)
                self.lines.add(line)
            id_line += 1
        self.lines_ids = res


def read_line(line, dfa):
    next_state = 0
    for word in line:
        for i in range(len(word)):
            previous_state = next_state
            transitions = dfa.get(next_state)
            for transition in transitions:
                # handle dot transitions
                if transition == word[i] or transition == ".":
                    next_state = transitions.get(transition)
                    break
            # TODO: change by giving a token for ending states
            # final state condition
            if len(dfa.get(next_state)) == 1:
                return True
            # if no transition is char go to init state
            if next_state == previous_state:
                next_state = 0
        next_state = 0
    return False



