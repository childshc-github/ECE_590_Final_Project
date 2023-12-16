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
    
    # for each powerset item, create state + add to DFA
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
            #print(str(k) + " is an accept")
            NFA_accepts.append(k)
    for a in NFA_accepts:
        for d in dfa.states:
            if a in d.descr:
                #print("Update " + str(d.descr) + " to true")
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
    toswap_accept = State(0)
    for g in dfa.states:
        if g.descr == start_eclose:
            toswap = g.id
            toswap_accept = g
    # get accept of start and toswap
    start_accept = False
    swap_accept = False
    for k, v in dfa.is_accepting.items():
        # get start
        if k == 0:
            start_accept = v
        # get swap
        elif k == toswap:
            swap_accept = v
    
    # swap states + update accepts
    dfa.states[0], dfa.states[toswap] = dfa.states[toswap], dfa.states[0]
    dfa.states[0].id = 0
    dfa.states[toswap].id = toswap
    dfa.is_accepting[0] = swap_accept
    dfa.is_accepting[toswap] = start_accept

    #print(dfa)
    return dfa

# You should write this function.
# It takes an DFA and returns a NFA.
def dfaToNFA(dfa):
    # create DFA w/ start state
    ndfa = DFA()
    state0 = State(0)
    ndfa.states = [state0]
    ndfa.is_accepting = {0 : False}

    # merge states + add &
    incr = ndfa.addStatesFrom(dfa)
    ndfa.addTransition(ndfa.states[0], ndfa.states[incr])

    return ndfa

# unions 2 NFAs by add & trans from new start -> beginning of each. Returns 1 object
def NFA_union(nfa1, nfa2):
    # creat new NFA with start
    unfa = NFA()
    state0 = State(0)
    unfa.states = [state0]
    unfa.is_accepting = {0 : False}

    # merge states
    u_to_1 = unfa.addStatesFrom(nfa1)
    u_to_2 = unfa.addStatesFrom(nfa2)

    # add union transition
    unfa.addTransition(unfa.states[0], unfa.states[u_to_1])
    unfa.addTransition(unfa.states[0], unfa.states[u_to_2])

    return unfa

# You should write this function.
# It takes two regular expressions and returns a 
# boolean indicating if they are equivalent
def equivalent(re1, re2):
    # boolean tracker
    are_equiv = False

    # create NFA1
    nfa1 = re1.transformToNFA()

    # create NFA2
    nfa2 = re2.transformToNFA()

    # get complement of nfa1 and nfa2
    dfa1 = nfaToDFA(nfa1)
    cdfa1 = dfa1.complement()
    cnfa1 = dfaToNFA(cdfa1)
    dfa2 = nfaToDFA(nfa2)
    cdfa2 = dfa2.complement()
    cnfa2 = dfaToNFA(cdfa2)

    # union of cNFA1 to NFA2
    union_c1_2 = NFA_union(cnfa1, nfa2)

    # union of NFA1 to cNFA2
    union_1_c2 = NFA_union(nfa1, cnfa2)

    # complement of union cNFA1 to NFA2
    d_c1_2 = nfaToDFA(union_c1_2)
    cd_c1_2 = d_c1_2.complement()

    # complement of union NFA1 to cNFA2
    d_1_c2 = nfaToDFA(union_1_c2)
    cd_1_c2 = nfaToDFA(d_1_c2)
    
    # determine if any string accepts (emptiness)
    answer1 = cd_c1_2.shortestString()
    answer2 = cd_1_c2.shortestString()
    if answer1 == answer2:
        are_equiv = True
    
    return are_equiv



if __name__ == "__main__":
    def testNFA(strRe, s, expected):
        # returns regex object
        re = parse_re(strRe)
        
        # test your nfa conversion
        nfa = re.transformToNFA()
        #print(nfa)
        res = nfa.isStringInLanguage(s)
        if res == expected:
            print(strRe, " gave ",res, " as expected on ", s)
        else:
            print("**** ", strRe, " Gave ", res , " on " , s , " but expected " , expected)
            pass
        pass

    def testDFA(nfa, s, expected):
        dfa = nfaToDFA(nfa)
        #print(dfa)
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

    # # DFA tests
    # # format = testDFA(nfa, s, expected)
    # # testing sym
    # print("Sym DFA Tests:")
    # re = parse_re("a")
    # n = re.transformToNFA()
    # testDFA(n, "a", True)

    # re = parse_re("b")
    # n = re.transformToNFA()
    # testDFA(n, "a", False)

    # # testing Concat
    # print("----")
    # print("Concat DFA Tests: ")
    # re = parse_re("ab")
    # n = re.transformToNFA()
    # testDFA(n, "aa", False)

    # # testing OR
    # print("----")
    # print("Or DFA Tests:")
    # re = parse_re("a|b")
    # n = re.transformToNFA()
    # testDFA(n, "a", True)

    # re = parse_re("a|b")
    # n = re.transformToNFA()
    # testDFA(n, "b", True)

    # re = parse_re("a|b")
    # n = re.transformToNFA()
    # testDFA(n, "aa", False)

    # # testing Star
    # re = parse_re("a*")
    # n = re.transformToNFA()
    # testDFA(n, "", True)

    # re = parse_re("a*")
    # n = re.transformToNFA()
    # testDFA(n, "b", False)

    # # shortest string check
    # # check SYM
    # re1 = parse_re("a")
    # NFA1 = re1.transformToNFA()
    # test = nfaToDFA(NFA1)
    # answer = test.shortestString()
    # print("SS is " + answer + " and should be a")

    # # check OR
    # re1 = parse_re("a|b")
    # NFA1 = re1.transformToNFA()
    # test = nfaToDFA(NFA1)
    # answer = test.shortestString()
    # print("SS is " + answer + " and should be a (b ok too)")

    # # check Star
    # re1 = parse_re("a*")
    # NFA1 = re1.transformToNFA()
    # test = nfaToDFA(NFA1)
    # answer = test.shortestString()
    # print("SS is " + answer + " and should be empty")

    # complement + equivalence DFA tests
    # Sym test
    # NFA1/2 regex = "a" (equiv)
    testEquivalence("a", "a", True)
    


    pass
    
