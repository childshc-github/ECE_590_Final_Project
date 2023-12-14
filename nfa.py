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
        pass

    # You should write this function.
    # It takes two states (object!) and a symbol. It adds a transition from 
    # the first state of the NFA to the other input state of the NFA.
    # need for transformation of ConcatRegex and OrRegex (regex.py) to NFA
    def addTransition(self, s1, s2, sym = '&'):
        # if sym already in dict, append s2 to set
        for k, v in s1.transition.items():
            if k == sym:
                v.append(s2)
                return
            
        # else, add trans from s1 -> s2 State (dict)
        s1.transition[sym] = [s2]
        pass

    # You should write this function.
    # It takes an nfa, adds all the states from that nfa and returns a 
    # mapping of (state number in old NFA -> state number in this NFA) as a dictionary.
    # need for transformation of ConcatRegex and OrRegex (regex.py) to NFA
    def addStatesFrom(self, nfa):
        # find length of nfa + increment new NFA ids in dict
        incr = len(self.states)
        new_dict = dict()

        # create copy NFA w/ new IDs - avoid memory + overlap ID issues
        cnfa = NFA()
        # update states w/ new incremented IDs
        for s in nfa.states:
            new_id = s.id + incr
            new_dict[s.id] = new_id
            newS = State(new_id)
            newS.transition = s.transition.copy()
            cnfa.states.append(newS)
        # update accepting
        for k, v in nfa.is_accepting.items():
            newk = k + incr
            newv = v
            self.is_accepting[newk] = newv
        # update dictionary
        for a in nfa.alphabet:
            self.alphabet.append(a)

        # append cNFA to self
        for s in cnfa.states:
            self.states.append(s)

        return new_dict

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

    # def isStringInLanguage(self, string):
    #     queue = [(self.states[0], 0)]
    #     currS = self.states[0]
    #     pos = 0
    #     visited = []
    #     while queue:
    #         currS, pos = queue.pop()
    #         print(f"Processing state {currS.id} at position {pos}")
    #         if pos == len(string):
    #             if currS.id in self.is_accepting and self.is_accepting[currS.id]:
    #                 return self.is_accepting[currS.id]
    #             for n in self.epsilonClose([currS]):
    #                 queue.append((n, pos))
    #             continue
    #         for s in self.states:
    #             if s.id == currS.id:
    #                 if string[pos] in s.transition:
    #                     stats = s.transition[string[pos]]
    #                     for stat in stats:
    #                         queue.extend([(stat, pos + 1)])
    #                         queue.extend([(s, pos + 1) for s in self.epsilonClose([stat])])
    #                 else:
    #                     print(f"Error: No transition for symbol {string[pos]} at state {currS.id}")
    #                     for n in self.epsilonClose([currS]):
    #                         queue.append((n, pos))
    #                 break
    #     if pos == len(string):
    #         return currS.id in self.is_accepting and self.is_accepting[currS.id]
    #     else:
    #         return False

