import RPi.GPIO as GPIO
import threading

# import time
import pandas as pd
import numpy as np
import serial
import matplotlib.pyplot as plt

# import matplotlib.dates as md
# from datetime import datetime
# from PIL import Image
import json

# import matplotlib
# matplotlib.use('GTKAgg')

pd.options.mode.chained_assignment = None


AC_PIN = 32
SOLAR_PIN = 37

# ratio = 0
ratios = [0, 0, 0, 0, 0, 0]

outJSON = {
    "ac_electricity": 0.0,
    "ac_usage": 0.0,
    "ac_abnormal": 0,
    "solar_electricity": 0,
    "solar_usage": 0,
    "solar_abnormal": 0,
    "predfee": 0,
    "aclimit": False,
}


def setup():
    GPIO.setwarnings(True)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(AC_PIN, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(SOLAR_PIN, GPIO.OUT, initial=GPIO.HIGH)
    ac = GPIO.PWM(AC_PIN, 2000)
    ac.start(50)
    return ac


class arduinoReader(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.ser = serial.Serial("/dev/ttyUSB0", 9600, timeout=1)
        self.ser.reset_input_buffer()

    def run(self):
        global ratios
        while True:
            if self.ser.in_waiting > 0:
                line = self.ser.readline().decode("utf-8").strip("\r")

                try:
                    line = line.split(",")
                    id = int(line[0])
                    value = float(line[1]) / 512
                    if value < 0.1:
                        value = 0
                    if value > 1.9:
                        value = 2
                    ratios[id] = value
                    # print(id, value)
                except:
                    pass


if __name__ == "__main__":
    ac = setup()
    reader = arduinoReader()
    reader.start()
    allData = pd.read_csv("ele_sun.csv", header=0)

    usageRecord = [[] for _ in range(3)]
    electricityRecord = [[] for _ in range(3)]
    electricity = [0, 0, 0]
    usage = [0, 0, 0]
    date = []
    corrcoef = [0, 0, 0]
    predfee = 0
    count = 0
    daily_usage = 0
    daily_limit = 10

    fig, ax = plt.subplots(figsize=(8, 4))
    daySep = []

    noise = np.random.normal(1, scale=0.3, size=48)

    devices = ["ac", "solar", "total"]
    columnMap = {
        "ac": "E_instanceElectricity",
        "solar": "instanceElectricityIN",
        "total": "add",
    }

    for index, row in allData.iterrows():
        if count % 24 == 0:
            daySep.append(count)

        date.append(row["time"])
        for i, device in enumerate(devices):
            column = columnMap[device]
            data = allData[["time", column]]
            if count % 24 == 0 and count:
                old = np.array(data.iloc[index - 24 : index, 1])
                new = np.array(electricityRecord[i][-24:])
                print(old.shape, new.shape)
                corrcoef[i] = np.corrcoef(new, old)[0, 1]
                print(corrcoef)
                daily_usage = 0

            ratio = ratios[i]
            print(ratios)
            print(f"daily_usage:{daily_usage}")

            instanceElectricity = row[column]
            # dt = datetime.fromtimestamp(row["time"] + 1643587200).strftime("%m/%d %H:%M")

            if i != 2:
                electricity[i] = instanceElectricity * ratio
            else:
                electricity[2] = electricity[0] * ratios[0] - electricity[1] * ratios[1]
                daily_usage += electricity[2] / 1000
            electricityRecord[i].append(electricity[i])
            usage[i] = electricity[i] / 1000
            if count:
                usageRecord[i].append((usageRecord[i][-1] + usage[i]))
            else:
                usageRecord[i].append(usage[i])
            # print(f"{ratio:.2f}, {power:.2f}, {row['time']}, {electricity[i]:.2f}")

            # GPIO.cleanup()
            if electricity[1] > 0:
                print("sun")
                GPIO.output(SOLAR_PIN, GPIO.HIGH)
            else:
                print("no sun")
                GPIO.output(SOLAR_PIN, GPIO.LOW)

            outJSON[f"{device}_electricity"] = round(electricity[i], 2)
            outJSON[f"{device}_usage"] = round(usage[i], 2)
            outJSON[f"{device}_abnormal"] = bool(corrcoef[i] < 0.7)
            outJSON_str = json.dumps(outJSON)

            if device == "ac":
                if daily_usage > daily_limit:
                    power = 0
                    ac.stop()
                    outJSON["aclimit"] = True
                else:
                    power = max(min(electricity[i] / 50, 100), 0)
                    outJSON["aclimit"] = False

                ac.ChangeDutyCycle(power)

            if count % 3 == 0:
                pred_len = 48
                if i < 2:
                    pred = data.iloc[count : count + pred_len, :]
                    pred[column] = pred[column] * ratio
                else:
                    pred = allData.iloc[count : count + pred_len, :]
                    pred[column] = pred["E_instanceElectricity"] * ratios[0] - pred["instanceElectricityIN"] * ratios[1]
                pred[column] = pred[column].multiply(noise, axis=0)
                pred.iloc[0, -1] = electricity[i]

                if i == 2:
                    predfee = pred["add"].sum() / 1000 * 15
                    outJSON["predfee"] = round(predfee*3, 2)

                # Plot
                ax.plot(date, usageRecord[i], color="b")

                for sep in daySep:
                    ax.axvline(x=sep, color="k", linestyle="--")

                tmp = count // 10 + 1
                xticks = date[::tmp]
                ax.set_xticks(xticks)

                fig.autofmt_xdate()
                plt.xlabel("Time", fontsize=12)
                plt.ylabel("Usage (kWh)", fontsize=12)
                plt.grid(linestyle="dotted", linewidth=1)
                plt.savefig(f"output/{device}_usage.png", dpi=100, bbox_inches="tight")

                plt.cla()

                ax.plot(date, electricityRecord[i], color="r")
                ax.plot(
                    pred["time"],
                    pred[column],
                    color="tab:orange",
                    linestyle="--",
                )

                for sep in daySep:
                    ax.axvline(x=sep, color="k", linestyle="--")

                tmp = (count + pred_len) // 10 + 1
                xticks = date[::tmp]
                ax.set_xticks(xticks)

                fig.autofmt_xdate()
                plt.xlabel("Time", fontsize=12)
                plt.ylabel("Power (W)", fontsize=12)
                plt.grid(linestyle="dotted", linewidth=1)

                plt.savefig(
                    f"output/{device}_electricity.png", dpi=100, bbox_inches="tight"
                )

                plt.cla()

            with open("output/out.json", "w") as f:
                f.write(outJSON_str)
            print(outJSON_str)

        count += 1
