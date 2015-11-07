F1 = 440
F2= 553
F3 = 660

f1 = Sine(F1).out()
f2 = Sine(F2).out()
f3 = Sine(F3).out()

def play_sound(a,b,c):
    f1.setFreq(F1+a)
    f2.setFreq(F2+b)
    f3.setFreq(F3+b)
