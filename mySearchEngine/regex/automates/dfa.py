from automates import ndfa

# all letters other than recognized language
ALL = "all"


# find transition associated with ndfa_state
def find_transition(ndfa_state, transitions):
    if transitions is not None:
        for key in transitions.keys():
            for state in transitions.get(key):
                if state == ndfa_state:
                    return key


class DFA:

    def __init__(self, ndfa_automaton):
        self.ndfa = ndfa_automaton
        self.dfa = {0: {ALL: 0}}
        self.map_states = {0: {0}}
        self.reachability = {}
        self.dfa_states = set()
        self.transitions_dfa = {}

    def __repr__(self):
        return "DFA"

    def __str__(self):
        return str(self.dfa)

    def find_dfa_states(self, ndfa_states):
        res = set()
        for ndfa_state in ndfa_states:
            # pour chaque etat du dfa
            for dfa_state in self.map_states.keys():
                # pour chaque etat du ndfa correspondant
                for state in self.map_states.get(dfa_state):
                    # s'il existe deja un etat du ndfa enregistre dans le dfa
                    if state == ndfa_state or dfa_state == ndfa_state:
                        res.add(dfa_state)
        return res

    def find_dfa_state(self, ndfa_states):
        for ndfa_state in ndfa_states:
            # pour chaque etat du dfa
            for dfa_state in self.map_states.keys():
                # pour chaque etat du ndfa correspondant
                for state in self.map_states.get(dfa_state):
                    # s'il existe deja un etat du ndfa enregistre dans le dfa
                    if state == ndfa_state or dfa_state == ndfa_state:
                        return dfa_state

    # main function
    def construct(self):
        # construct set of dfa states and remove labelled transitions
        self.parcours_ndfa_set(0)
        # add the initial state
        self.dfa_states.add(0)

        # for each dfa state set the reached states from epsilon transitions
        for s in self.dfa_states:
            self.map_states.update({s: self.parcours_ndfa_construct(s, set())})
        # add transition to initial state for each other letters than transitions
        for state in self.map_states.keys():
            self.dfa.update({state: {ALL: 0}})
        # add labelled transitions to dfa
        self.add_transitions()

    # update reachables ndfa states for a given dfa state
    def update_reachability(self, current_state, ndfa_states):
        maps = self.reachability.get(current_state)
        if maps is not None:
            self.reachability.get(current_state).update(ndfa_states)
        else:
            self.reachability.update({current_state: ndfa_states})

    # add labelled transitions in dfa
    def add_transitions(self):
        for ndfa_state in self.transitions_dfa.keys():
            for transition in self.transitions_dfa.get(ndfa_state).keys():
                for state in self.find_dfa_states({ndfa_state}):
                    self.dfa.get(state).update({
                        transition: self.find_dfa_state(self.transitions_dfa.get(ndfa_state).get(transition))
                    })

    # choose dfa states from ndfa automaton and remove labelled transitions
    def parcours_ndfa_set(self, ndfa_state):
        transitions = self.ndfa.get(ndfa_state)
        if transitions is not None:
            # pour chaque transition du ndfa
            for transition in transitions.copy().keys():
                states = set(transitions.get(transition))
                if transition == ndfa.EPSILON:
                    self.update_reachability(ndfa_state, states.copy())
                else:
                    # update dfa states
                    self.dfa_states = self.dfa_states.union(states)
                    self.transitions_dfa.update({ndfa_state: {transition: states}})
                    # remove labelled transition
                    self.ndfa.get(ndfa_state).pop(transition)
                # continue with out states
                for s in states.copy():
                    self.parcours_ndfa_set(s)

    # return set of reacheable ndfa states with epsilon transitions
    def parcours_ndfa_construct(self, ndfa_state, res):
        transitions = self.ndfa.get(ndfa_state)
        if transitions is not None:
            res.add(ndfa_state)
            # pour chaque transition du ndfa
            for transition in transitions.copy().keys():
                states = set(transitions.get(transition))
                for s in states.copy():
                    res = res.union(self.parcours_ndfa_construct(s, res))
            return res
        else:
            return {ndfa_state + 1}


