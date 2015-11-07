import pygame.midi as midi
import time

midi.init()
devices = []
for i in range(midi.get_count()):
   devices.append(midi.get_device_info(i))

for i in devices:
    print i

#for i in range(midi.get_count()):
#    print i
#    try:
#        p = midi.Output(i)
#        p.set_instrument(0)
#        p.note_on(69,127)
#        time.sleep(1)
#    except:
#        print "faulty channel. Must be an input not an output"
#

p = midi.Output(6)
p.set_instrument(0)
p.note_on(69,127)
time.sleep(1)


del p

midi.quit()
