"""
import os
os.system('cls')

while check == "fail":
    guess = input("Enter a value between " + str(min_val) + " and " + str(max_val) + ": ")
    valid_guess(guess)
    if check == "pass":
        guess_count =+ 1
        break

def guess_loop():
    global guess
    global first_guess
    while check == "fail":
        guess = input("Enter a value between " + str(min_val) + " and " + str(max_val) + ":")
        valid_guess(guess)

"""
check = "fail"
difficulty = ""
guess_count = 0
max_val = 10
min_val = 0

print("Welcome to Dan's Number Guessing Game!")

from time import sleep
sleep(0.75)

while difficulty not in ("E", "e", "M", "m", "H", "h"):
    difficulty = input('[Set your difficulty] Enter "e" for easy, "m" for medium or "h" for hard: ')
    if  difficulty in ("E", "e"):
        #max_val = 10
        break
    elif  difficulty in ("M", "m"):
        max_val = 20
        break
    elif difficulty in ("H", "h"):
        max_val = 50
        break
    else:
        print("INVALID INPUT")
        sleep(0.5)

import random
x = random.randint(1, max_val)

print("Let's go!")
sleep(0.5)

def valid_guess(guess):
    global check
    global guess_count
    if str(guess).isdigit():
        if min_val < int(guess) < max_val:
            check = "pass"
            guess_count += 1
        else:
            print("Number not within range. Attempt not counted.")
            check = "fail"
    else:
        print("Number not recognised. Attempt not counted.")
        check = "fail"

def game_over():
    sleep(0.5)
    print("Gimme: Answer is " + str(x))
    sleep(0.5)
    print("You had " + str(guess_count) + " attemps.")
    sleep(0.5)
    print("GAME OVER")

while check == "fail" or int(guess) != x:
    guess = input("Enter a value between " + str(min_val) + " and " + str(max_val) + ": ")
    valid_guess(guess)
    if check == "pass" and int(guess) == x:
        sleep(0.5)
        print("You won with " + str(guess_count) + " attemps!")
        break
    elif check == "pass" and x > int(guess):
        min_val = int(guess)
        if int(max_val) - int(min_val) == 2:
            game_over()
            break
        else:
            sleep(0.5)
            print("Too low. Try again.")
            sleep(0.5)
    elif check == "pass" and x < int(guess):
        max_val = int(guess)
        if int(max_val) - int(min_val) == 2:
            game_over()
            break
        else:
            sleep(0.5)
            print("Too high. Try again.")
            sleep(0.5)