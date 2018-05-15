from subprocess import check_output, CalledProcessError
import time
from datetime import datetime
import json
import sys

host = "8.8.8.8"
time_format = "%H:%M:%S"
timenow = datetime.now().strftime(time_format)

print(f"Start tijd: {timenow}")

results = {
        'ping': [],
        'time': [],
    }

try:   
    while True:
        try:
            raw_response = check_output(['ping', host, '-n', '1'], universal_newlines=True)

            response = "".join(raw_response).split('=')

            results['ping'].append(int(response[2].split(' ')[0]))
            results['time'].append(datetime.now().strftime(time_format))

            print(f"[*] ping: {response[2].split(' ')[0]} ms | Max: {max(results['ping'])} ms | Min: {min(results['ping'])} ms",
                  flush=True, end='\r')

        except CalledProcessError as e:
            # results['ping'].append(0)
            # results['time'].append(datetime.now().strftime(time_format))
            print("Time-out\n")

        time.sleep(1)

except KeyboardInterrupt:
    with open("ping.json", 'w') as pingtest:
        json.dump(results, pingtest)
        print("[*} Klaar")
        print(f"[*] Max: {int(max(results['ping']))}")
        print(f"[*] Min: {int(min(results['ping']))}")
        print(f"[*] Gemiddelde: {int(sum(results['ping']) / len(results['ping']))}")

        input("Druk op enter om het bestand op te slaan.")
