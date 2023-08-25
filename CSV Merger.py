#Merge multiple csv files with identical schemas incl. column headers
#Coded to merge cleansed datasets only from https://www.kaggle.com/datasets/adityadesai13/used-car-dataset-ford-and-mercedes
import pandas as pd
import csv
import os
from tabulate import tabulate

path = r"C:\Users\Dan\Desktop\UK Used Car Data Sets"
file_dirs = []
source_details = []
file_count = 0
total_rows = 0
#Adding absolute filepaths to list, files in subdirectories will also be added
for root, dirs, files in os.walk(os.path.abspath(path)):
    for file in files:
        file_dirs.append(os.path.join(root, file))

initial_df = True

#prceding space for values in first column of source csv are removed
#brand value is determined by source csv filename and inserted as first column
for file in file_dirs:
    df = pd.read_csv(file, skipinitialspace = True)
    brand = file[file.rfind("\\") + 1:file.rindex(".")]
    df.insert(0, "brand", brand)
    if initial_df == True:
        df.to_csv(r"C:\Users\Dan\Desktop\All Cars.csv", header=True, index=False, encoding="utf-8")
        initial_df = False
    else:
        df.to_csv(r"C:\Users\Dan\Desktop\All Cars.csv", mode="a", header=False, index=False, encoding="utf-8")

    filename = file[file.rfind("\\") + 1:]
    rows = len(df)
    source_details.append((filename, rows))

    file_count += 1
    total_rows += rows

source_details_col_names = ["Filename", "Rows"]
print(tabulate(source_details, headers=source_details_col_names))

print("")

summary = []
summary.append((file_count, total_rows))
summary_col_names = ["Total Files Read", "Total Rows Read"]
print(tabulate(summary, headers=summary_col_names))

print("")

output_rows = pd.read_csv(r"C:\Users\Dan\Desktop\All Cars.csv")
print("Rows in merged file: ", len(output_rows))