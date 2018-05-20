import time
from datetime import datetime
import json
import os
import lib.utils as utils

time_format = "%H:%M:%S"

app = utils.Ping(host="8.8.8.8")

results = {
        "ping": [],
        "time": [],
        "time-out": [],
    }

utils.start_message()

print(f"[*] Start tijd: {datetime.now().strftime(time_format)}\n")

try:   
    while True:
        response = app.get_ping()

        if response == "time-out":
            print(f"Time-out | {datetime.now().strftime(time_format)}....", flush=True, end="\r")
            results["time-out"].append(0)

        else:
            results["ping"].append(int(response))
            results["time"].append(datetime.now().strftime(time_format))

            print(f"[*] {datetime.now().strftime(time_format)} | ping: {response} ms | Min: {min(results['ping'])} ms | Max: {max(results['ping'])} ms | Time-outs: {len(results['time-out'])}   ",
                  flush=True, end="\r")

        time.sleep(1)

except KeyboardInterrupt:
    utils.eind_message(results)

    if not os.path.exists("data"):
        os.mkdir("data")
    with open("data\\ping.json", "w") as pingtest:
        json.dump(results, pingtest)
        input("\nDruk op enter om het bestand op te slaan.")
    