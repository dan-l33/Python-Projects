#Generate a csv listing all files whithin directory incl. subdirectories

import os
import csv

count = 0
dir = r"C:\Users\Dan\PycharmProjects"
file =  open("File List.csv", "w", newline="")
writer = csv.writer(file)
writer.writerow(["File_Location","File_Name", "File_Extension", "File_Size (KB)"])

for path, subdirs, files in os.walk(dir):
    for name in files:
        count += 1
        fs = round(os.path.getsize(os.path.join(path,name))/1024)
        try:
            writer.writerow([path+"\\", name, name[name.rindex('.')+1:], fs])
        except:
            writer.writerow([path+"\\", name, "", fs])

file.close()
print("Done: ", count, " files have been listed.")