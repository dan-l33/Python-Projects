#Generate a csv listing all files within directory incl. subdirectories
##Rename List.csv to contain {File path} & {New file name} column headers
import os
import csv


def list_files():
    count = 0
    dir = r"C:\Users\Dan\PycharmProjects"
    file = open("File List.csv", "w", newline="")
    writer = csv.writer(file)
    writer.writerow(["File_Location", "File_Name", "File_Extension", "File_Size (KB)"])

    for path, subdirs, files in os.walk(dir):
        for name in files:
            count += 1
            fs = round(os.path.getsize(os.path.join(path, name)) / 1024)
            try:
                writer.writerow([path + "\\", name, name[name.rindex(".") + 1:], fs])
            except:
                writer.writerow([path + "\\", name, "", fs])

    file.close()
    print("Done: ", count, " files have been listed.")

fpath = r"C:\Users\Dan\Desktop\Test\Rename List.csv"

def rename():
    count = 0
    missing = []
    #with open(r"C:\Users\Dan\Desktop\Test\Rename List.csv") as file_obj:
    with open(fpath, "r", newline="") as file_obj:
        reader_obj = csv.reader(file_obj)
        next(reader_obj, None)
        for row in reader_obj:
            path = str(row[0])
            dir = path[:path.rfind("\\")+1]
            #old_name = path[path.rfind("\\")+1:]
            new_name = dir + str(row[1])
            try:
                os.rename(path, new_name)
                count += 1
            except:
                missing.append(path)

    if len(missing) > 0:
        print("[PARTIALLY COMPLETED] " + str(count) + " file(s) renamed")
        print("[SKIPPED FILE(S)] ", len(missing))
        for i in missing:
            print(i)
    else:
        print("[SUCCESSFULLY COMPLETED] " + str(count) + " file(s) renamed")

def repeated_output_check():
    #global file_obj
    outputs = []
    duplicate_outputs = []
    #with open(r"C:\Users\Dan\Desktop\Test\Rename List.csv") as file_obj:
    with open(fpath, "r", newline="") as file_obj:
        reader_obj = csv.reader(file_obj)
        next(reader_obj, None)
        for row in reader_obj:
            path = str(row[0])
            dir = path[:path.rfind("\\") + 1]
            new_name = dir + str(row[1])
            if new_name not in outputs:
                outputs.append(new_name)
            elif new_name not in duplicate_outputs:
                duplicate_outputs.append(new_name)

    if len(duplicate_outputs) > 0:
        print("[PROCESS TERMINATED] Output(s) repeated")
        for i in duplicate_outputs:
            print(i)
        file_obj.close()
        exit(1)
    else:
        print("No output repetitions")

def repeated_sources_check():
    #global file_obj
    sources = []
    duplicate_sources = []
    #with open(r"C:\Users\Dan\Desktop\Test\Rename List.csv") as file_obj:
    with open(fpath, "r", newline = "") as file_obj:
        reader_obj = csv.reader(file_obj)
        next(reader_obj, None)
        for row in reader_obj:
            if row[0] not in sources:
                sources.append(row[0])
            elif row[0] not in duplicate_sources:
                duplicate_sources.append(row[0])

    if len(duplicate_sources) > 0:
        print("[PROCESS TERMINATED] Source(s) repeated")
        for i in duplicate_sources:
            print(i)
        file_obj.close()
        exit(1)
    else:
        print("No source repetitions")

repeated_sources_check()
repeated_output_check()
rename()