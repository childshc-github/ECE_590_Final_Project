from nfa import *
from state import *

# used to build up tree. Transform regex -> NFA.

class Regex:
    # converts printable object to string
    def __repr__(self):
        ans=str(type(self))+"("
        sep=""
        for i in self.children:
            ans = ans + sep + repr(i)
            sep=", "
            pass
        ans=ans+")"
        return ans

    def transformToNFA(self):
        # FIXME - should create new object and return it
        pass
    pass

class ConcatRegex(Regex):
    def __init__(self, r1, r2):
        self.children=[r1,r2]
        pass
    def __str__(self):
        return "{}{}".format(self.children[0],self.children[1])
    def transformToNFA(self):
        # transform regex -> NFAs
        nfa1 = self.children[0].transformToNFA()
        nfa2 = self.children[1].transformToNFA()
        
        # update NFA1 accepts
        NFA1_astates = []
        for k, v in nfa1.is_accepting.items():
            if v == True:
                NFA1_astates.append(k)
                nfa1.is_accepting[k] = False
        
        # add NFA2 to NFA1
        new_map = nfa1.addStatesFrom(nfa2)

        # add trans based on map
        for a in NFA1_astates:
            for k in new_map.keys():
                if a == k:
                    nfa1.addTransition(nfa1.states[k], nfa2.states[0])
        
        return nfa1

class StarRegex(Regex):
    def __init__(self, r1):
        self.children=[r1]
        pass
    def __str__(self):
        return "({})*".format(self.children[0])
    def transformToNFA(self):
        # transform to NFA
        nfa = self.children[0].transformToNFA()

        # update transition
        nfa.addTransition(nfa.states[1], nfa.states[1], str(self.children[0]))
        
        # update alphabet
        nfa.alphabet = [str(self.children[0])]

        # update accepting
        nfa.is_accepting = {0 : True, 1 : True}

        return nfa
        
    pass

class OrRegex(Regex):
    def __init__(self, r1, r2):
        self.children=[r1,r2]
        pass
    def __str__(self):
        return "(({})|({}))".format(self.children[0],self.children[1])
    def transformToNFA(self):
        # create new start node NFA
        state0 = State(0)
        nfa0 = NFA()
        nfa0.states = [state0]
        nfa0.is_accepting = {0 : False}

        # transform both to NFA
        nfa1 = self.children[0].transformToNFA()
        nfa2 = self.children[1].transformToNFA()

        # add & trans from start NFA to both NFAs
        nfa0.addTransition(nfa0.states[0], nfa1.states[0])
        nfa0.addTransition(nfa0.states[0], nfa2.states[0])
        print(nfa0.states[0].transition)

        # add NFA1 and NFA2 to NFA0
        hold1 = nfa0.addStatesFrom(nfa1)
        hold2 = nfa0.addStatesFrom(nfa2)
        
        return nfa0

# Sym=symbol
class SymRegex(Regex):
    def __init__(self, sym):
        self.sym=sym
        pass
    def __str__(self):
        return self.sym
    def __repr__(self):
        return self.sym
    def transformToNFA(self):
        nfa = NFA()
        state0 = State(0)
        state1 = State(1)

        nfa.states = [state0, state1]
        nfa.is_accepting = {0 : False, 1 : True}
        nfa.alphabet = [self.sym]
        nfa.addTransition(state0, state1, str(self.sym))

        return nfa
    pass

class EpsilonRegex(Regex):
    def __init__(self):
        pass
    def __str__(self):
        return '&'
    def __repr__(self):
        return '&'
    def transformToNFA(self):
        nfa = NFA()
        state = State(0)

        nfa.states = [state]
        nfa.is_accepting = {0 : True}

        return nfa
    pass

class ReInput:
    def __init__(self,s):
        self.str=s
        self.pos=0
        pass
    def peek(self):
        if (self.pos < len(self.str)):
            return self.str[self.pos]
        return None
    def get(self):
        ans = self.peek()
        self.pos +=1
        return ans
    def eat(self,c):
        ans = self.get()
        if (ans != c):
            raise ValueError("Expected " + str(c) + " but found " + str(ans)+
                             " at position " + str(self.pos-1) + " of  " + self.str)
        return c
    def unget(self):
        if (self.pos > 0):
            self.pos -=1
            pass
        pass
    pass

# R -> C rtail
# rtail -> OR C rtail | eps
# C -> S ctail
# ctail -> S ctail | eps
# S -> atom stars
# atom -> (R) | sym | &
# stars -> * stars | eps

#It gets a regular expression string and returns a Regex object. 
def parse_re(s):
    inp=ReInput(s)
    def parseR():
        return rtail(parseC())
    def parseC():
        return ctail(parseS())
    def parseS():
        return stars(parseA())
    def parseA():
        c=inp.get()
        if c == '(':
            ans=parseR()
            inp.eat(')')
            return ans
        if c == '&':
            return EpsilonRegex()
        if c in ')|*':
            inp.unget()
            inp.fail("Expected open paren, symbol, or epsilon")
            pass
        return SymRegex(c)
    def rtail(lhs):
        if (inp.peek()=='|'):
            inp.get()
            x = parseC()
            return rtail(OrRegex(lhs,x))
        return lhs
    def ctail(lhs):
        if(inp.peek() is not None and inp.peek() not in '|*)'):
            temp=parseS()
            return ctail(ConcatRegex(lhs,temp))
        return lhs
    def stars(lhs):
        while(inp.peek()=='*'):
            inp.eat('*')
            lhs=StarRegex(lhs)
            pass
        return lhs
    return parseR()