from utils import utils
import time
from datetime import datetime
import json


time_format = "%H:%M:%S"
timenow = datetime.now().strftime(time_format)

app = utils.Ping(host="8.8.8.8")

results = {
        'ping': [],
        'time': [],
        'time-out': [],
    }

print(f"Start tijd: {timenow}")

try:   
    while True:
        response = app.get_ping()

        if response == "time-out":
            print(f"Time-out | {datetime.now().strftime(time_format)}....", flush=True, end='\r')
            results['time-out'].append(0)

        else:
            results['ping'].append(int(response[2].split('ms')[0]))
            results['time'].append(datetime.now().strftime(time_format))

            print(f"[*] {datetime.now().strftime(time_format)} | ping: {response[2].split('ms')[0]} ms | Min: {min(results['ping'])} ms | Max: {max(results['ping'])} ms | Time-outs: {len(results['time-out'])}   ",
                  flush=True, end='\r')

        time.sleep(1)

except KeyboardInterrupt:
    with open("data\\ping.json", 'w') as pingtest:
        json.dump(results, pingtest)
        print("\n")
        print("[*} Klaar")
        print(f"[*] Max: {int(max(results['ping']))}")
        print(f"[*] Min: {int(min(results['ping']))}")
        print(f"[*] Gemiddelde: {int(sum(results['ping']) / len(results['ping']))}")
        print(f"[*] Time-outs: {len(results['time-out'])}")

        input("Druk op enter om het bestand op te slaan.")
