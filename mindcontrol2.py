from liblo import *
import sys 
import time
import pyo_soundv2 as sound

class MuseServer(ServerThread):
    #listen for messages on port 5001
    def __init__(self):
        ServerThread.__init__(self, 5001)
        self.baseX = None
        self.baseY = None
        self.baseZ = None
        sound.init()


    #receive accelrometer data
    @make_method('/muse/acc', 'fff')
    def acc_callback(self, path, args):
        if not self.baseZ or not self.baseY or not self.baseX:
            self.baseX, self.baseY, self.baseZ = args
        acc_x, acc_y, acc_z = args
        acc_x -= self.baseX
        acc_y -= self.baseY
        acc_z -= self.baseZ
        sound.play_sound(acc_x, acc_y, acc_z)
        print "%f %f %f\n" % (acc_x, acc_y, acc_z)


    #receive EEG data
    @make_method('/muse/eeg', 'ffff')
    def eeg_callback(self, path, args):
        l_ear, l_forehead, r_forehead, r_ear = args
        pass


    #handle unexpected messages
    @make_method(None, None)
    def fallback(self, path, args, types, src):
        pass
        # print "Unknown message \
        # \n\t Source: '%s' \
        # \n\t Address: '%s' \
        # \n\t Types: '%s ' \
        # \n\t Payload: '%s'" \
        # % (src.url, path, types, args)



try:
    server = MuseServer()
except ServerError, err:
    print str(err)
    sys.exit()



server.start()



if __name__ == "__main__":
    while 1:
        time.sleep(1)