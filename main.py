import copy
from regex import *
from state import * 
from nfa import *
from dfa import *
from itertools import chain, combinations

# powerset fxn
def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

# You should write this function.
# It takes an NFA and returns a DFA (new object!)
def nfaToDFA(nfa):
    # storage
    dfa = DFA()
    IDs = []

    # create all possible states
    # get IDs
    for i in nfa.states:
        IDs.append(i.id)
    pIDs = list(powerset(IDs))
    
    # for each powerset item, create state
    track = 0
    while track < len(pIDs):
        newState = State(track)
        newState.descr = list(pIDs[track])
        dfa.states.append(newState)
        track = track + 1

    # add self-loops for empty set
    for a in nfa.alphabet:
        dfa.addTransition(dfa.states[0], dfa.states[0], a)
        
    # determine accepts from NFA + adjust DFA
    NFA_accepts = []
    for k, v in nfa.is_accepting.items():
        if v == True:
            NFA_accepts.append(k)
    for a in NFA_accepts:
        for d in dfa.states:
            if a in d.descr:
                dfa.is_accepting[d.id] = True



    print(dfa)
    return dfa

# You should write this function.
# It takes an DFA and returns a NFA.
def dfaToNFA(dfa):
    pass

# You should write this function.
# It takes two regular expressions and returns a 
# boolean indicating if they are equivalent
def equivalent(re1, re2):
    pass



if __name__ == "__main__":
    def testNFA(strRe, s, expected):
        # returns regex object
        re = parse_re(strRe)
        
        # test your nfa conversion
        nfa = re.transformToNFA()
        res = nfa.isStringInLanguage(s)
        if res == expected:
            print(strRe, " gave ",res, " as expected on ", s)
        else:
            print("**** ", strRe, " Gave ", res , " on " , s , " but expected " , expected)
            pass
        pass

    def testDFA(nfa, s, expected):
        # test your dfa conversion
        dfa = nfaToDFA(nfa)
        res = dfa.isStringInLanguage(s)
        if res == expected:
            print(strRe, " gave ",res, " as expected on ", s)
        else:
            print("**** ", strRe, " Gave ", res , " on " , s , " but expected " , expected)
            pass
        pass

    def testEquivalence(strRe1, strRe2, expected):
        re1 = parse_re(strRe1)
        re2 = parse_re(strRe2)
        
        res = equivalent(re1, re2)
        if res == expected:
            print("Equivalence(", strRe1, ", ",strRe2, ") = ", res, " as expected.")
        else:
            print("Equivalence(", strRe1, ", ",strRe2, ") = ", res, " but expected " , expected)
            pass
        pass

    def pp(r):
        print()
        print("Starting on " +str(r))
        re=parse_re(r)
        print(repr(re))
        print(str(re))
        pass

    #test your NFA:
    # format = testNFA(RE, input string, expected)

    # my NFA
    # EpsilonRegex testing transformtoNFA
    # testNFA('&', '', True)
    # testNFA('&', 'a', False)
    # testNFA('&', ' ', False)
    # testNFA('&', 'ab', False)

    # SymRegex testing transformtoNFA
    # testNFA('a', 'a', True)
    # testNFA('b', 'b', True)
    # testNFA('a', 'b', False)
    # testNFA('a', 'ab', False)

    # ConcatRegex testing transformtoNFA
    # testNFA('ab', '', False)
    # testNFA('aba', '', False)
    # testNFA('ab', 'ab', True)
    # testNFA('ab', 'a', False)
    # testNFA('ab', 'b', False)
    # testNFA('aba', 'aba', True)
    # testNFA('aba', 'ab', False)
    # testNFA('abaa', 'ba', False)
    # testNFA('abaa', 'abaa', True)

    # StarRegex testing transformtoNFA
    # testNFA('a*', '', True)
    # testNFA('a*', 'b', False)
    # testNFA('a*', 'a', True)
    # testNFA('a*', 'aa', True)
    # testNFA('a*', 'aaa', True)
    # testNFA('a*', 'aba', False)

    # OrRegex testing transformtoNFA
    # testNFA('a|b', 'a', True)
    # testNFA('a|b', 'b', True)
    # testNFA('a|b', '', False)
    # testNFA('a|b', 'c', False)
    
    # mixed transformtoNFA tests
    # testNFA('cd*', 'cddddddd', True)
    # testNFA('a', '', False)
    # testNFA('a', 'a', True)
    # testNFA('a', 'ab', False)
    # testNFA('a*', '', True)
    # testNFA('a*', 'a', True)
    # testNFA('a*', 'aaa', True)
    # testNFA('a|b', '', False)
    # testNFA('a|b', 'a', True)
    # testNFA('a|b', 'b', True)
    # testNFA('a|b', 'ab', False)
    # testNFA('ab|cd', '', False)
    # testNFA('ab|cd', 'ab', True)
    # testNFA('ab|cd', 'cd', True)
    # testNFA('ab|cd*', '', False)
    # testNFA('ab|cd*', 'c', True)
    # testNFA('ab|cd*', 'cd', True)
    # testNFA('ab|cd*', 'cddddddd', True)
    # testNFA('ab|cd*', 'ab', True)
    # testNFA('((ab)|(cd))*', '', True)
    # testNFA('((ab)|(cd))*', 'ab', True)
    # testNFA('((ab)|(cd))*', 'cd', True)
    # testNFA('((ab)|(cd))*', 'abab', True)
    # testNFA('((ab)|(cd))*', 'abcd', True)
    # testNFA('((ab)|(cd))*', 'cdcdabcd', True)
    # testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', '', True)
    # testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'ab', True)
    # testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'abcd', True)
    # testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'cd', True)
    # testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'dfgab', True)
    # testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'defg', True)
    # testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'deeefg', True)
    # testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'hkln', True)
    # testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'q', True)
    # testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'hijijkln', True)
    # testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'hijijklmmmmmmmmmmn', True)





    # DFA test
    # format = testDFA(nfa, s, expected)
    re = parse_re("a")
    n = re.transformToNFA()
    d = nfaToDFA(n)
    pass
    
