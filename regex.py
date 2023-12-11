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

        # rhs = child 0 (>=)
        # lhs = child 1 (always length 1)


        # nfar1 = NFA()
        # nfar2 = NFA()

        # state0r1 = State(0)
        # state1r1 = State(1)
        # nfar1.states = [state0r1, state1r1]
        # nfar1.addTransition(nfar1.states[0], nfar1.states[1], self.children[0])
        # nfar1.is_accepting = {0 : False, 1 : True}
        # nfar1.alphabet = [self.children[0]]
        
        # state0r2 = State(0)
        # state1r2 = State(1)
        # nfar2.states = [state0r2, state1r2]
        # nfar2.addTransition(nfar2.states[0], nfar2.states[1], self.children[1])
        # nfar2.is_accepting = {0 : False, 1 : True}
        # nfar2.alphabet = [self.children[1]]





        return nfa_test

    pass

class StarRegex(Regex):
    def __init__(self, r1):
        self.children=[r1]
        pass
    def __str__(self):
        return "({})*".format(self.children[0])
    def transformToNFA(self):
        # FIXME
        pass
    pass

class OrRegex(Regex):
    def __init__(self, r1, r2):
        self.children=[r1,r2]
        pass
    def __str__(self):
        return "(({})|({}))".format(self.children[0],self.children[1])
    def transformToNFA(self):
        #FIXME
        pass
    pass

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
        nfa.addTransition(nfa.states[0], nfa.states[1], self.sym)

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
        #nfa.alphabet = []

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