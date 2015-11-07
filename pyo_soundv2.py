from pyo import *
import time

F1 = 440
F2= 553
F3 = 660

def init():
	global server, s, f1, f2, f3
	server = Server(audio='jack')
	s = server.boot()
	f1 = Sine(F1).out()
	f2 = Sine(F2).out()
	f3 = Sine(F3).out()
	s.start()

def play_sound(a,b,c):
    f1.setFreq(F1+a)
    f2.setFreq(F2+b)
    f3.setFreq(F3+b)  
    time.sleep(.1)

def close():
	s.stop()
	s.close()
	server.close()
