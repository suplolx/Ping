from subprocess import check_output, CalledProcessError
from collections import deque
import psutil



class Ping(object):

    def __init__(self, host="8.8.8.8"):
        self.host = host
    
    def get_ping(self):
        try:
            raw_response = check_output(['ping', self.host, '-n', '1'], universal_newlines=True)
            response = "".join(raw_response).replace("<", "=").split("=")
        except CalledProcessError:
            response = "time-out"
        return response



class NetSpeed(object):

    bytes_recv = deque(maxlen=20)
    bytes_sent = deque(maxlen=20)
    bytes_recv.append(psutil.net_io_counters().bytes_recv)
    bytes_sent.append(psutil.net_io_counters().bytes_sent)
    
    def download_speed(self):
        bytes_recv_start = psutil.net_io_counters().bytes_recv
        bps_recv = bytes_recv_start - self.bytes_recv[-1]
        self.bytes_recv.append(bytes_recv_start)
        return round(bps_recv / 2**20, 2)
    
    def upload_speed(self):
        bytes_sent_start = psutil.net_io_counters().bytes_sent
        bps_sent = bytes_sent_start - self.bytes_sent[-1]
        self.bytes_sent.append(bytes_sent_start)
        return round(bps_sent / 2**20, 2)



def start_message():
    print("\n\t\t\t##############################")
    print("\t\t\t#                            #")
    print("\t\t\t#        PINGTEST V1.0       #")
    print("\t\t\t#                            #")
    print("\t\t\t# Druk op Ctrl+C om de test  #")
    print("\t\t\t# te beëindigen              #")
    print("\t\t\t#                            #")
    print("\t\t\t##############################\n")


def eind_message(results):
    print("\n")
    print("[*} Klaar")
    print(f"[*] Max: {int(max(results['ping']))}")
    print(f"[*] Min: {int(min(results['ping']))}")
    print(f"[*] Gemiddelde: {int(sum(results['ping']) / len(results['ping']))}")
    print(f"[*] Time-outs: {len(results['time-out'])}")
