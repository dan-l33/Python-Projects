#Fuctionality still to add:
#--> Ability to opt for single run or
#--> for duration & intervals of user's request

import speedtest
from tabulate import tabulate
from datetime import datetime
from time import sleep
import csv

st = speedtest.Speedtest()
data = []
def main():
    now = datetime.now()
    str_time = now.strftime("%Y%m%d_%H%M%S")

    dl = round(st.download()/1024/1024, 1)
    ul = round(st.upload()/1024/1024, 1)
    ping = round(st.results.ping)
    data.append((str_time, dl, ul, ping))

main()

col_names = ["Date_Time", "Download (Mbps)", "Upload (Mbps)", "Ping (ms)"]
print(tabulate(data, headers = col_names))

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