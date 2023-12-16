import copy
from state import *

# DFA is a class with four fields:
# -states = a list of states in the DFA
#  Note that the start state is always state 0
# -accepting = A dictionary, the key is the state id 
#  and value is a boolean indicating which states are acceping
# -alphabet = a list of symbols in the alphabet of the regular language.
#  Note that & can not be included because we use it as epsilon
# -startS = it is the start state id which we assume it is always 0
class DFA:
    def __init__(self):
        self.states = []
        self.is_accepting= dict()
        self.alphabet = []
        self.startS = 0
        pass

    # def __str__(self):
    #     pass  

    def __str__(self):
        a = []
        for k, v in self.is_accepting.items():
            if v == True:
                a.append(k)
        hold = "------------" + "\n"
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
    # It takes two states and a symbol/char. It adds a transition from 
    # the first state of the DFA to the other input state of the DFA.
    def addTransition(self, s1, s2, sym='&'):
        # if sym already in dict, append s2 to list
        for k, v in s1.transition.items():
            if k == sym:
                v.append(s2)
                s1.transition[k] = v
                return
            
        # else, add trans from s1 -> s2 State (dict)
        s1.transition[sym] = [s2]
        pass

    def addStatesFrom(self, nfa):
        # find length of nfa
        incr = len(self.states)
        newStates = []

        # update states + trans w/ new incremented IDs
        for s in nfa.states:
            newState = s
            newState.id = newState.id + incr
            newState.descr = []
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
    # It returns a DFA that is the complement of this DFA
    def complement(self):
        cdfa = copy.deepcopy(self)
        for k, v in cdfa.is_accepting.items():
            if v == True:
                cdfa.is_accepting[k] = False
            elif v == False:
                cdfa.is_accepting[k] = True
        return cdfa

    # You should write this function.
    # It takes a string and returns True if the string is in the language of this DFA
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
                #for n in self.epsilonClose([currS]):
                    #queue.append((n, pos))
                continue
            for s in self.states:
                if s.id == currS.id:
                    if string[pos] in s.transition:
                        stats = s.transition[string[pos]]
                        for stat in stats:
                            queue.extend([(stat,pos+1)])
                            #queue.extend([(s,pos+1) for s in self.epsilonClose([stat])])
                    #else:
                        #for n in self.epsilonClose([currS]):
                            #queue.append((n, pos))
                    break
        if pos == len(string):
            return currS.id in self.is_accepting and self.is_accepting[currS.id]
        else:
            return False
    pass

    # You should write this function.
    # It runs BFS on this DFA and returns the shortest string accepted by it
    def shortestString(self):
        # tracker
        at_accept = False

        # create list of accept IDs
        accepts = []
        for k, v in self.is_accepting.items():
            if v == True:
                accepts.append(k)
        
        # if start node is accept, ss = "" FIXME
        

        # start by putting start state + empty path in queue
        queue = [[self.states[0], ""]]
        visited = []

        # until reach an accept state, find shortest string
        while at_accept == False:
            # get current node
            curr, path = queue[0]

            # update queue
            queue.pop(0)
            #print("Checking " + str(curr.descr))
            #print("Path is " + path)

            # if current is an accept, don't loop again
            if curr.id in accepts:
                at_accept = True
                return path

            # for all edges on curr, add to queue
            if not curr in visited:
                visited.append(curr)
                for k, v in curr.transition.items():
                    for v2 in v:
                        new_path = path + k
                        queue.append([v2, new_path])


    pass