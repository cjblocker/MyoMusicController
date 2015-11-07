import pygame.midi as midi
import time


def parse(fin):
    line = fin.readline().rstrip().split('\t')
    for i in range(4):
        line[i] = float(line[i])
    return line


def main():

    fin = open("workfile2.txt",'r')

    midi.init()
    p1 = midi.Output(2)
    instrument = 0
    count = 0
    while (count < 50):
        line = parse(fin)
        x = line[0]
        v = line[1]
        if (line[-1] == 'fist'):
            instrument = 41
        elif (line[-1] == 'wave_out'):
            instrument = 31
        elif (line[-1] == 'rest'):
            instrument = 1
        elif (line[-1] == 'wave_in'):
            instrument = 59
        else:
            intrument = 67

        p1.set_instrument(instrument)
        print line
        NOTE = 64.0 + 64.0*x
        VOLUME = 64.0 + 64.0*v
        p1.note_on(int(NOTE),int(VOLUME))
        time.sleep(0.25)
        p1.note_off(int(NOTE),int(VOLUME))
        count += 1
    del p1
    midi.quit()
    fin.close()

main()
