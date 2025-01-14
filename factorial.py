from sm import SM, Cascade, Delay, Feedback, Feedback2
from utils import splitValue, safeAdd, safeMul

class Multiplier(SM):

    def getNextState(self, state, inp):
        (i1, i2) = splitValue(inp)
        return safeMul(i1, i2)

class Increment(SM):

    def __init__(self, incr):
        self.incr = incr

    def getNextState(self, state, inp):
        return safeAdd(inp, self.incr)

def makeCounter(init, step):
    return Feedback(Cascade(Increment(step), Delay(init)))

fact = Cascade(makeCounter(1, 1), Feedback2(Cascade(Multiplier(), Delay(1))))
x = fact.run()

print(x)