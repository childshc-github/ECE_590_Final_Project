from state import *
import regex
import copy


class NFA:
    def __init__(self):
        # -states = a list of states (object! - state.py) in the NFA
        self.states = []

        # -accepting = A dictionary, the key is the state id and value is a boolean indicating which states are acceping
        self.is_accepting = dict()

        # -alphabet = a list of symbols in the alphabet of the regular language. Note that & can not be included because we use it as epsilon
        self.alphabet = []

        #  Note that the start state is always state 0. -startS = it is the start state id which we assume it is always 0
        self.startS = 0
        pass
    def __str__(self):
        a = []
        for k, v in self.is_accepting.items():
            if v == True:
                a.append(k)
        hold = ""
        for s in self.states:
            n = s.print_state()
            hold = hold + n
            for i in a:
                if s.id == i:
                    hold = hold + " This node (" + str(i) + ") accepts"
            hold = hold + "\n"
        hold = hold + "Alphabet: " + str(self.alphabet)
        return hold

    # You should write this function.
    # It takes two states (object!) and a symbol. It adds a transition from 
    # the first state of the NFA to the other input state of the NFA.
    # need for transformation of ConcatRegex and OrRegex (regex.py) to NFA
    def addTransition(self, s1, s2, sym = '&'):
        # if sym already in dict, append s2 to list
        for k, v in s1.transition.items():
            if k == sym:
                v.append(s2)
                s1.transition[k] = v
                return
            
        # else, add trans from s1 -> s2 State (dict)
        s1.transition[sym] = [s2]
        pass

    # You should write this function.
    # It takes an nfa, adds all the states from that nfa and returns a 
    # mapping of (state number in old NFA -> state number in this NFA) as a dictionary.
    # need for transformation of ConcatRegex and OrRegex (regex.py) to NFA
    # NOW RETURNS INCREMENT
    def addStatesFrom(self, nfa):
        # find length of nfa
        incr = len(self.states)
        newStates = []

        # update states + trans w/ new incremented IDs
        for s in nfa.states:
            newState = copy.deepcopy(s)
            newState.id = newState.id + incr
            for k, v in newState.transition.items():
                for v2 in v:
                    v2.id = v2.id + incr
            newStates.append(newState)
        self.states = self.states + newStates

        # update accepting
        for k, v in nfa.is_accepting.items():
            newk = k + incr
            self.is_accepting[newk] = v
        # update dictionary
        for a in nfa.alphabet:
            self.alphabet.append(a)

        return incr

    # You should write this function.
    # It takes a (actually list of) state and returns the epsilon closure of that state 
    # which is a set of states which are reachable from this state 
    #on epsilon transitions.
    def epsilonClose(self, ns):
        states = []
        for n in ns:
            for sym, nn in self.states[n.id].transition.items():  
                if sym == '&':
                    for s in nn:
                        states.append(s)
        return states

    # It takes a string and returns True if the string is in the language of this NFA
    def isStringInLanguage(self, string):
        queue = [(self.states[0], 0)]
        currS = self.states[0]
        pos = 0
        visited = []
        while queue:
            currS, pos = queue.pop()
            if pos == len(string):
                if currS.id in self.is_accepting and self.is_accepting[currS.id]:
                    return self.is_accepting[currS.id]
                for n in self.epsilonClose([currS]):
                    queue.append((n, pos))
                continue
            for s in self.states:
                if s.id == currS.id:
                    if string[pos] in s.transition:
                        stats = s.transition[string[pos]]
                        for stat in stats:
                            queue.extend([(stat,pos+1)])
                            queue.extend([(s,pos+1) for s in self.epsilonClose([stat])])
                    else:
                        for n in self.epsilonClose([currS]):
                            queue.append((n, pos))
                    break
        if pos == len(string):
            return currS.id in self.is_accepting and self.is_accepting[currS.id]
        else:
            return False
    pass

