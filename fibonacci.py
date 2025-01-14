class SM():

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

    def __init__(self, v0):
        self.startState = v0

    def getNextValues(self, state, inp):
        return (inp, state)

class Parallel(SM):

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

    def __init__(self, sm):
        self.m = sm
        self.startState = sm.startState

    def getNextValues(self, state, inp):
        (_, o) = self.m.getNextValues(state, 'undefined')
        (newS, _) = self.m.getNextValues(state, o)
        return (newS, o)

def splitValue(v):
    if v == 'undefined':
        return ('undefined', 'undefined')
    else:
        return v

def safeAdd(v1, v2):
    if v1 == 'undefined' or v2 == 'undefined':
        return 'undefined'
    else:
        return v1 + v2

class Adder(SM):

    def getNextState(self, state, inp):
        (i1, i2) = splitValue(inp)
        return safeAdd(i1, i2)

fib = Cascade(Feedback(Cascade(Parallel(Delay(1), Cascade(Delay(1), \
    Delay(0))), Adder())), Delay(1))

x = fib.run()
print(x)