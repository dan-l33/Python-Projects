import pandas as pd
from tabulate import tabulate

pd.set_option("display.max_colwidth", 500)

table = pd.read_csv("https://raw.githubusercontent.com/dan-l33/SQL/main/Hackerrank%20MySQL%20Solutions.csv", encoding = "cp1252")

def main():
    print(tabulate(table[["Ref#", "Challenge Name"]], showindex=False, headers = ["Ref#", "Challenge Name"], numalign="left"))

    while True:
        request = input("Enter the Ref#: ")
        if request in table["Ref#"].values:
            request_check = "pass"
            break
        else:
            print("Ref# not recognised.")

    request_challenge_name = table.loc[table["Ref#"] == request, "Challenge Name"].to_string(index=False)
    raw_output = table.loc[table["Ref#"] == request, "Solution"].to_string(index=False)
    print("Dan's solution to " + request + " - "  + request_challenge_name + ": \n\n" + raw_output.replace("\\n", "\n") + "\n")

main()

while True:
    a = input("Enter y/n to continue searching: ")
    if a=="y":
        main()
    elif a=="n":
        print("Good Luck!")
        break
    else:
        print("Enter either y/n: ")