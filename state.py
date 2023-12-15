import copy

# State is a class with two fields
class State:
    def __init__(self,id):
        # -id = an integer which is used as the unique identifier of the state 
        self.id = id
        # -transition = a dictionary mapping from (char/symbol + epsilon ) to a set (really mean list) of states (object!)
        self.transition = dict()
        pass

    def copy(self, s):
        self.id = s.id
        self.transition = copy.deepcopy(s.transition)
    def __str__(self):
        ans = self.id
    def print_state(self):
        toprint = "ID: "
        # print start node
        toprint = toprint + str(self.id)
        # print K:V transitions
        for k, v in self.transition.items():
            toprint = toprint + " {" + str(k) + ", "
            for t in v:
                toprint = toprint + str(t.id) + "}, "
        return toprint
    pass