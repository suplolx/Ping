from subprocess import check_output, CalledProcessError


class Ping(object):

    def __init__(self, host="8.8.8.8"):
        self.host = host
    
    def get_ping(self):
        try:
            raw_response = check_output(['ping', self.host, '-n', '1'], universal_newlines=True)
            response = "".join(raw_response).replace("<", "=").split("=")
        except CalledProcessError:
            response = "time-out"
        return response[2].split('ms')[0].strip('<')


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
