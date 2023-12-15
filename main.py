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

    # add self-loops for empty set + update dfa alphabet
    for a in nfa.alphabet:
        dfa.alphabet.append(a)
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
                
    # add trans NFA -> DFA
    for d in dfa.states:
        # get DFA node name
        actual = d.descr
        # print("actual is : " + str(actual))
        # evaluate each node in node name relative to alphabet (skip empty set)
        if len(actual) > 0:
            for a in nfa.alphabet:
                # print("sym is " + str(a))
                ends_on = []
                for t in actual:
                    # print("current state in actual is " + str(t))
                    # find trans + update ends_on
                    for k, v in nfa.states[t].transition.items():
                        # print("Key is " + str(k))
                        if a == k:
                            # print("key match!")
                            for v2 in v:
                                ends_on.append(v2.id)
                # use goal descr name + sym to make transition in DFA
                # print("Sym " + a + " leads to " + str(ends_on))
                if len(ends_on) > 0:
                    for f in dfa.states:
                        if f.descr == ends_on:
                            end_state = f
                    dfa.addTransition(d, end_state, a)
                    # print("new transition from " + str(d.descr) + " to " + str(end_state.descr))
            # print("-------")
    
    # if no trans addded for an alphabet sym, add trans to empty set
    for r in dfa.states:
        # if no transitions, add to empty
        if len(r.transition) == 0:
            for q in dfa.alphabet:
                dfa.addTransition(r, dfa.states[0], q)
        # if some added, add missing alphabet -> empty
        else:
            toadd = []
            for k, v in r.transition.items():
                if not k in dfa.alphabet:
                    toadd.append(k)
            for t in toadd:
                dfa.addTransition(r, dfa.states[0], t)

                        
    
    # adjust start state (descr w/ eps trans)
    # find eps close
    start_eclose = [0]
    for k, v in nfa.states[0].transition.items():
        if k == '&':
            for v2 in v:
                start_eclose.append(v2.id)
    # find index of start_eclose and swap states
    toswap = 1
    for g in dfa.states:
        if g.descr == start_eclose:
            toswap = g.id
    dfa.states[0], dfa.states[toswap] = dfa.states[toswap], dfa.states[0]
    dfa.states[0].id = 0
    dfa.states[toswap].id = toswap

    #print(dfa)
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
            print("gave ",res, " as expected on ", s)
            #print(strRe, " gave ",res, " as expected on ", s)
        else:
            print("**** Gave", res , " on " , s , " but expected " , expected)
            #print("**** ", strRe, " Gave ", res , " on " , s , " but expected " , expected)
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


    # DFA tests
    # format = testDFA(nfa, s, expected)
    # testing sym
    print("Sym DFA Tests:")
    re = parse_re("a")
    n = re.transformToNFA()
    testDFA(n, "a", True)

    re = parse_re("b")
    n = re.transformToNFA()
    testDFA(n, "a", False)

    # testing Concat
    print("----")
    print("Concat DFA Tests: ")
    re = parse_re("ab")
    n = re.transformToNFA()
    testDFA(n, "ab", True)

    re = parse_re("ab")
    n = re.transformToNFA()
    testDFA(n, "aa", False)

    # testing OR
    print("----")
    print("Or DFA Tests:")
    re = parse_re("a|b")
    n = re.transformToNFA()
    testDFA(n, "a", True)

    re = parse_re("a|b")
    n = re.transformToNFA()
    testDFA(n, "b", True)

    re = parse_re("a|b")
    n = re.transformToNFA()
    testDFA(n, "aa", False)

    # testing Star
    print("----")
    print("Star DFA Tests: ")
    re = parse_re("a*")
    n = re.transformToNFA()
    testDFA(n, "aa", True)

    re = parse_re("a*")
    n = re.transformToNFA()
    testDFA(n, "", True)

    re = parse_re("a*")
    n = re.transformToNFA()
    testDFA(n, "b", False)
    pass
    
