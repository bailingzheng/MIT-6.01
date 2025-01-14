class SM():
    """We can specify a transducer (a process that takes as input a sequence of values which serve as inputs to the state machine, 
    and returns as ouput the set of outputs of the machine for each input) as a state machine (SM) by specifying:
    - a set of states, S,
    - a set of inputs, I, also called the input vocabulary,
    - a set of outputs, O, also called the output vocabulary,
    - a next-state function, n(i[t], s[t]) -> s[t+1], that maps the input at time t and the state at time t to
    the state at time t + 1,
    - an output function, o(i[t], s[t]) -> o[t], that maps the input at time t and the state at time t to the
    output at time t; and
    - an initial state, s[0], which is the state at time 0.
    """

    startState = None
    
    def start(self):
        self.state = self.startState

    def step(self, inp):
        (s, o) = self.getNextValues(self.state, inp)
        self.state = s
        return o

    def transduce(self, inputs):
        self.start()
        return [self.step(inp) for inp in inputs]

    def run(self, n = 10):
        return self.transduce([None] * n)

    def getNextValues(self, state, inp):
        nextState = self.getNextState(state, inp)
        return (nextState, nextState)

class Delay(SM):
    """An even simpler machine just takes the input and passes it through to the output, but with one step of delay, 
    so the kth element of the input sequence will be the k + 1st element of the output sequence.
    """

    def __init__(self, v0):
        self.startState = v0

    def getNextValues(self, state, inp):
        return (inp, state)

class Parallel(SM):
    """In parallel composition, we take two machines and run them “side by side”. They both take the same input, 
    and the output of the composite machine is the pair of outputs of the individual machines. 
    """

    def __init__(self, sm1, sm2):
        self.m1 = sm1
        self.m2 = sm2
        self.startState = (sm1.startState, sm2.startState)

    def getNextValues(self, state, inp):
        (s1, s2) = state
        (newS1, o1) = self.m1.getNextValues(s1, inp)
        (newS2, o2) = self.m2.getNextValues(s2, inp)
        return ((newS1, newS2), (o1, o2))

class Cascade(SM):
    """In cascade composition, we take two machines and use the output of the first one as the input to the second.
    """

    def __init__(self, sm1, sm2):
        self.m1 = sm1
        self.m2 = sm2
        self.startState = (sm1.startState, sm2.startState)

    def getNextValues(self, state, inp):
        (s1, s2) = state
        (newS1, o1) = self.m1.getNextValues(s1, inp)
        (newS2, o2) = self.m2.getNextValues(s2, o1)
        return ((newS1, newS2), o2)

class Feedback(SM):
    """Another important means of combination that we will use frequently is the feedback combinator, in which 
    the output of a machine is fed back to be the input of the same machine at the next step
    """

    def __init__(self, sm):
        self.m = sm
        self.startState = sm.startState

    def getNextValues(self, state, inp):
        (_, o) = self.m.getNextValues(state, 'undefined')
        (newS, _) = self.m.getNextValues(state, o)
        return (newS, o)


class Feedback2(Feedback):
    """Feedback2 is very similar to the basic feedback combinator, but it gives, as input to the constituent
    machine, the pair of the input to the machine and the feedback value.
    """

    def getNextValues(self, state, inp):
        (_, o) = self.m.getNextValues(state, (inp, 'undefined'))
        (newS, _) = self.m.getNextValues(state, (inp, o))
        return (newS, o)