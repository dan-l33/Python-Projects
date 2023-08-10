#delete_fileless_branches() = deletes earliest ancestor directory containing zero files within itself incl. subfolders
#list_files() = Generate a csv listing all files within directory incl. subdirectories
#delete()/rename() = to complete their actions via their respective csv lists
    ##Rename List.csv first row to have {File path} & {New file name} column headers
    ##Delete List.csv first row to have {File path} column header
#unique_output_check() = checks outputs filepath (incl. file name) are unique
#unique_sources_check() = checks sources filepath (incl. file name) are unique

import os
import csv
import shutil

def delete_fileless_branches():
    path = r"C:\Users\Dan\Desktop\New Folder"
    empty = []
    #identify empty folders and add folderpath to list
    for root, dirs, files in os.walk(path):
        if not len(dirs) and not len(files):
            if root == path:
                print("Path is empty")
                exit(0)
            else:
                empty.append(root)

    if len(empty) == 0:
        print("No empty folders were found")
    else:
        #for each item in empty list
        #find earliest ancestor containing zero files within itself incl. subfolders
        #then add folderpath to second list
        fileless_branch = []
        for empty_dir in empty:
            parent_dir = empty_dir[:empty_dir.rfind("\\")]
            while sum([len(files) for r, d, files in os.walk(parent_dir)]) ==0:
                empty_dir = parent_dir
                parent_dir = empty_dir[:empty_dir.rfind("\\")]
                if parent_dir == path:
                    break

            if empty_dir not in fileless_branch:
                fileless_branch.append(empty_dir)

        for i in empty:
            print("empty: ", i)
        for i in fileless_branch:
            print("fileless_branch: ", i)
        #Functionality to delete folderpaths in fileless_branch to be added
        while True:
            delete_confirm = input("Confirm deletion of fileless branches y/n: ")
            if delete_confirm.lower() == "y":
                for i in fileless_branch:
                    shutil.rmtree(i)
                print("Branches deleted")
                break
            elif delete_confirm.lower() == "n":
                print("no")
                break
            else:
                print("Input not recognised")

delete_fileless_branches()
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

#fpath = r"C:\Users\Dan\Desktop\Test\Rename List.csv"
#fpath = r"C:\Users\Dan\Desktop\Test\Delete List.csv"


def completion_message():
    if len(missing) > 0:
        print("[PARTIALLY COMPLETED] " + str(count) + " file(s) " + mode)
        print("[SKIPPED FILE(S)] ", len(missing))
        for i in missing:
            print(i)
    else:
        print("[SUCCESSFULLY COMPLETED] " + str(count) + " file(s) " + mode)

#delete() & rename() to be merged
def delete():
    global count
    global missing
    global mode
    count = 0
    missing = []
    mode = "deleted"
    #with open(r"C:\Users\Dan\Desktop\Test\Rename List.csv") as file_obj:
    with open(fpath, "r", newline="") as file_obj:
        reader_obj = csv.reader(file_obj)
        next(reader_obj, None)
        for row in reader_obj:
            path = str(row[0])
            if os.path.exists(path):
                os.remove(path)
                count += 1
            else:
                missing.append(path)

    completion_message()

def rename():
    global count
    global missing
    global mode
    count = 0
    missing = []
    mode = "renamed"
    #with open(r"C:\Users\Dan\Desktop\Test\Rename List.csv") as file_obj:
    with open(fpath, "r", newline="") as file_obj:
        reader_obj = csv.reader(file_obj)
        next(reader_obj, None)
        for row in reader_obj:
            path = str(row[0])
            dir = path[:path.rfind("\\")+1]
            #old_name = path[path.rfind("\\")+1:]
            new_name = dir + str(row[1])
            if os.path.exists(path):
                os.rename(path, new_name)
                count += 1
            else:
                missing.append(path)

    completion_message()

def unique_output_check():
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

def unique_sources_check():
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

def batch_rename():
    unique_sources_check()
    unique_output_check()
    rename()

def batch_delete():
    unique_sources_check()
    delete()
