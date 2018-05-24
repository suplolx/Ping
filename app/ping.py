import time
from datetime import datetime
import json
import os
import lib.utils as utils

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
time_format = "%H:%M:%S"

app = utils.Ping(host="8.8.8.8")
speed_test = utils.NetSpeed()

results = {
        "ping": [],
        "time": [],
        "time-out": [],
    }

utils.start_message()

print(f"[*] Start tijd: {datetime.now().strftime(time_format)}\n")

try:   
    while True:
        try:
            response = app.get_ping()
        except ValueError:
            print(response)

        if response == "time-out":
            print(f"Time-out | {datetime.now().strftime(time_format)}....", flush=True, end="\r")
            results["time-out"].append(0)

        else:
            results["ping"].append(int(response[2].split('ms')[0].strip('<')))
            results["time"].append(datetime.now().strftime(time_format))

            print(f"[*] {datetime.now().strftime(time_format)} | ping: {response[2].split('ms')[0].strip('<')} ms | Min: {min(results['ping'])} ms | Max: {max(results['ping'])} ms | Time-outs: {len(results['time-out'])} | Down: {speed_test.download_speed()}mb/s | Up: {speed_test.upload_speed()}mb/s    ",
                  flush=True, end="\r")

        time.sleep(1)

except KeyboardInterrupt:
    utils.eind_message(results)

    if not os.path.exists(os.path.join(base_dir, "app", "data")):
        os.mkdir("data")
    with open(os.path.join(base_dir, "app", "data", "ping.json"), "w") as pingtest:
        json.dump(results, pingtest)
        input("\nDruk op enter om het bestand op te slaan.")
