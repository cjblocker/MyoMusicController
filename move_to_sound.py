from __future__ import print_function

import myo as libmyo; libmyo.init()
import time
import sys

import pygame.midi
import time

pygame.midi.init()
player = pygame.midi.Output(0)
player.set_instrument(0)


data_out = open(r'd:\workfile.txt', 'w')

class Listener(libmyo.DeviceListener):
    """
    Listener implementation. Return False from any function to
    stop the Hub.
    """

    interval = 0.1  # Output only 0.05 seconds

    def __init__(self):
        super(Listener, self).__init__()
        self.orientation = None
        self.pose = libmyo.Pose.rest
        self.emg_enabled = False
        self.locked = False
        self.rssi = None
        self.emg = None
        self.last_time = 0

    def output(self):
        ctime = time.time()
        if (ctime - self.last_time) < self.interval:
            return
        self.last_time = ctime

        parts = []
        if self.orientation:
            for comp in self.orientation:
                parts.append(str(comp).ljust(15))
        parts.append(str(self.pose).ljust(10))
        parts.append('E' if self.emg_enabled else ' ')
        parts.append('L' if self.locked else ' ')
        parts.append(self.rssi or 'NORSSI')
        if self.emg:
            for comp in self.emg:
                parts.append(str(comp).ljust(5))
        parse(parts)    
        sys.stdout.flush()

    def on_connect(self, myo, timestamp, firmware_version):
        myo.vibrate('short')
        myo.vibrate('short')
        myo.request_rssi()
        myo.request_battery_level()

    def on_rssi(self, myo, timestamp, rssi):
        self.rssi = rssi
        self.output()

    def on_pose(self, myo, timestamp, pose):
        if pose == libmyo.Pose.double_tap:
            myo.set_stream_emg(libmyo.StreamEmg.enabled)
            self.emg_enabled = True
        elif pose == libmyo.Pose.fingers_spread:
            myo.set_stream_emg(libmyo.StreamEmg.disabled)
            self.emg_enabled = False
            self.emg = None
        self.pose = pose
        self.output()

    def on_orientation_data(self, myo, timestamp, orientation):
        self.orientation = orientation
        self.output()

    def on_accelerometor_data(self, myo, timestamp, acceleration):
        pass

    def on_gyroscope_data(self, myo, timestamp, gyroscope):
        pass

    def on_emg_data(self, myo, timestamp, emg):
        self.emg = emg
        self.output()

    def on_unlock(self, myo, timestamp):
        self.locked = False
        self.output()

    def on_lock(self, myo, timestamp):
        self.locked = True
        self.output()

    def on_event(self, kind, event):
        """
        Called before any of the event callbacks.
        """

    def on_event_finished(self, kind, event):
        """
        Called after the respective event callbacks have been
        invoked. This method is *always* triggered, even if one of
        the callbacks requested the stop of the Hub.
        """

    def on_pair(self, myo, timestamp, firmware_version):
        """
        Called when a Myo armband is paired.
        """

    def on_unpair(self, myo, timestamp):
        """
        Called when a Myo armband is unpaired.
        """

    def on_disconnect(self, myo, timestamp):
        """
        Called when a Myo is disconnected.
        """

    def on_arm_sync(self, myo, timestamp, arm, x_direction, rotation,
                    warmup_state):
        """
        Called when a Myo armband and an arm is synced.
        """

    def on_arm_unsync(self, myo, timestamp):
        """
        Called when a Myo armband and an arm is unsynced.
        """

    def on_battery_level_received(self, myo, timestamp, level):
        """
        Called when the requested battery level received.
        """

    def on_warmup_completed(self, myo, timestamp, warmup_result):
        """
        Called when the warmup completed.
        """
def parse (state):
    length = len(state)
    round_range = 3
    if length > 4:
        x = round(float(state [0]),round_range)
        y = round(float(state [1]),round_range)
        z = round(float(state [2]),round_range)
        w = round(float(state [3]),round_range)
        pose = state [4] [7:-1]
        hk = state [5:]
        
        line = str(x) + '\t'+ str(y) + '\t'+ str(z) + '\t'+ str(w) + '\t' +pose+ '\t'
        data_out.write(line)
        print(line)
        data_out.write('\n')

        TONE = 64 + int (64*x)

        player.note_on(TONE, 127)
        time.sleep(1)
        player.note_off(TONE, 127)
       

        '''if hk:
            for part in hk:
                data_out.write(str(part))
                data_out.write('\t')
                print (str(part))'''
        data_out.write('\n')

def main():
    print("Connecting to Myo ... Use CTRL^C to exit.")
    try:
        hub = libmyo.Hub()
    except MemoryError:
        print("Myo Hub could not be created. Make sure Myo Connect is running.")
        return
    
    hub.set_locking_policy(libmyo.LockingPolicy.none)
    hub.run(1000, Listener())

    # Listen to keyboard interrupts and stop the hub in that case.
    try:
        while hub.running:
            time.sleep(0.25)
    except KeyboardInterrupt:
        print("\nQuitting ...")
    finally:
        print("Shutting down hub...")
        hub.shutdown()
        data_out.close()
        del player
        pygame.midi.quit()

if __name__ == '__main__':
    main()

