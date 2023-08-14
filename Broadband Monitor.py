# Choose between single run or set custom interval & duration
# Option to export to csv

from datetime import datetime, timedelta
from tabulate import tabulate
from time import sleep
import csv, speedtest
duration = 0
interval = 0
data = []
schedule = []

st = speedtest.Speedtest()

def check():
    global col_names
    now = datetime.now()
    str_time = now.strftime("%Y-%m-%d_%H:%M:%S")

    dl = round(st.download()/1024/1024, 1)
    ul = round(st.upload()/1024/1024, 1)
    ping = round(st.results.ping)
    data.append((str_time, dl, ul, ping))

    col_names = ["Date_Time", "Download (Mbps)", "Upload (Mbps)", "Ping (ms)"]
    print(tabulate(data, headers=col_names))

def scheduler():
    time_from_start = 0
    count = 0
    start = datetime.now()

    while time_from_start < duration:
        time_from_start = interval * count
        inter = start + timedelta(seconds = time_from_start)
        str_inter_time = inter.strftime("%Y-%m-%d_%H:%M:%S")
        schedule.append(str_inter_time)
        count+=1

        while datetime.now().strftime("%Y-%m-%d_%H:%M:%S") < max(schedule):
            if datetime.now().strftime("%Y-%m-%d_%H:%M:%S") in schedule:
                check()
                sleep(1) #needed in case function takes less than a second

def export_csv():
    while True:
        export = input("Export to csv? (Y/N): ")
        if export.lower() == "y":
            file = open(r"C:\Users\Dan\Desktop\Broadband Data.csv", "w", newline="")
            writer = csv.writer(file)
            writer.writerow(col_names)
            writer.writerows(data)
            print("File created")
            exit(0)
        elif export.lower() == "n":
            exit(0)
        else:
            print("Input not recognised")

def time_parameters():
    global duration
    global interval
    while True:
        interval_input = input("Set interval. Follow integer with (s)econds, (m)inutes or (h)ours [e.g. 60m for 60 minutes]: ")
        try:
            int(interval_input[:-1])
            if interval_input[-1].lower() == "s":
                interval = int(interval_input[:-1])
                break
            elif interval_input[-1].lower() == "m":
                interval = int(interval_input[:-1]) * 60
                break
            elif interval_input[-1].lower() == "h":
                interval = int(interval_input[:-1]) * pow(60, 2)
                break
            else:
                print("Input not recognised")
        except:
            print("Input not recognised")

    while True:
        duration_input = input(
            "Set duration. Follow integer with (s)econds, (m)inutes or (h)ours [e.g. 60m for 60 minutes]: ")
        try:
            int(duration_input[:-1])
            if duration_input[-1].lower() == "s":
                duration = int(duration_input[:-1])
                if duration > interval:
                    break
                else:
                    print("Duration cannot be less than interval")
            elif duration_input[-1].lower() == "m":
                duration = int(duration_input[:-1]) * 60
                if duration > interval:
                    break
                else:
                    print("Duration cannot be less than interval")
            elif duration_input[-1].lower() == "h":
                duration = int(duration_input[:-1]) * pow(60, 2)
                if duration > interval:
                    break
                else:
                    print("Duration cannot be less than interval")
            else:
                print("Input not recognised")
        except:
            print("Input not recognised")

while True:
    mode = input("Enter (s) for single run or (c) for custom interval & duration: ")
    if mode.lower() == "s":
        check()
        exit(0)
    elif mode.lower() == "c":
        while True:
            time_parameters()
            scheduler()
            export_csv()
            exit(0)
    else:
        print("Input not recognised")
