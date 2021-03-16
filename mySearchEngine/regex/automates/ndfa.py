from regparser import regextree as rt

EPSILON = "eps"
DOT = '.'


def epsilon_transition(to_state):
    return {EPSILON: to_state}


def dot_transition(to_state):
    return {DOT: to_state}


class NDFA(rt.RegExTree):

    ndfa_graph = {}
    nb_states = 0

    def __init__(self, regextree):
        if regextree:
            super().__init__(regextree.root, regextree.subTrees)

    def __repr__(self):
        return "NDFA"

    def __str__(self):
        return str(NDFA.ndfa_graph)

    def concat(self):

        NDFA(self.get_sbtree_l()).construct()
        NDFA.ndfa_graph.update({
            NDFA.nb_states - 1: epsilon_transition({NDFA.nb_states}),
        })

        NDFA(self.get_sbtree_r()).construct()

    def altern(self):
        deb = NDFA.nb_states
        debr1 = NDFA.nb_states + 1
        # R1
        NDFA.nb_states += 1
        NDFA(self.get_sbtree_l()).construct()
        finr1 = NDFA.nb_states - 1

        NDFA.ndfa_graph.update({
            deb: epsilon_transition({debr1, NDFA.nb_states}),
        })

        NDFA(self.get_sbtree_r()).construct()
        NDFA.ndfa_graph.update({
            NDFA.nb_states - 1: epsilon_transition({NDFA.nb_states}),
            finr1: epsilon_transition({NDFA.nb_states}),
        })
        NDFA.nb_states += 1

    def etoile(self):

        state1 = NDFA.nb_states
        state2 = NDFA.nb_states + 1

        NDFA.ndfa_graph.update({
            state1: epsilon_transition({state2})
        })
        NDFA.nb_states += 1
        NDFA(self.get_sbtree_l()).construct()

        NDFA.ndfa_graph.update({
            NDFA.nb_states - 1: epsilon_transition({state2, NDFA.nb_states}),
            state1: epsilon_transition({state2, NDFA.nb_states})
        })
        NDFA.nb_states += 1

    def char(self):
        NDFA.ndfa_graph.update({
            NDFA.nb_states: {self.root: {NDFA.nb_states + 1}},
        })
        NDFA.nb_states += 2

    def dot(self):
        NDFA.ndfa_graph.update({
            NDFA.nb_states: dot_transition({NDFA.nb_states + 1}),
        })
        NDFA.nb_states += 2

    def construct(self):
        if self.root == rt.ETOILE:
            self.etoile()
        else:
            if self.root == rt.CONCAT:
                self.concat()
            else:
                if self.root == rt.ALTERN:
                    self.altern()
                else:
                    if self.root == rt.DOT:
                        self.dot()
                    else:
                        self.char()


