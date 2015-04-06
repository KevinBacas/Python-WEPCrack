import os
import subprocess
import threading
import time


class WEP_thread(threading.Thread):
    def __init__(self, name='WEP_thread', box, datafile_path):
        self.pid = -1
        self._continue = True
        self._stopevent = threading.Event()
        self._sleepperiod = 1.0
        threading.Thread.__init__(self, name=name)
        self.box = box
        self.path = datafile_path

    def run(self) :
        key_file_name = self.box.ESSID + ".result"
        KEY = ""
        while KEY == "" && self._continue == True :
            logging.warning("%s n'a pas reussi à lancer Aircrack-ng", path)
            print 'Lancement de aircrack-ng'
            pid = aircrack_final_wep(self.path)
            KEY = get_key(key_file_name)
            time.sleep(5)
        if KEY != "":
            cmd = "echo \" WEP_box_path : " + path + " with key " + KEY + "\" >> key.result"
            FNULL = open(os.devnull, 'w')
            subprocess.Popen(cmd, stdout=FNULL, shell=True, stderr=subprocess.STDOUT, preexec_fn=os.setsid)
        os.killpg(self.pid,SIGKILL)
 

    def stop(self, timeout=None):
        _continue = True

    def join(self, timeout=None):
        self._stopevent.set()
        threading.Thread.join(self, timeout)
    
