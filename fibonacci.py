from sm import SM, Cascade, Feedback, Parallel, Delay
from utils import splitValue, safeAdd

class Adder(SM):

    def getNextState(self, state, inp):
        (i1, i2) = splitValue(inp)
        return safeAdd(i1, i2)

fib = Cascade(Feedback(Cascade(Parallel(Delay(1), Cascade(Delay(1), Delay(0))), Adder())), Delay(1))

x = fib.run()
print(x)