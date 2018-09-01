import threading
import os

Primes = []
firstNewPos = 0
stopFlag = False

helpMenu = "\n\
--------help menu--------\n\
clear\t\t|clear screen\n\
exit\t\t|ends program\n\
help\t\t|show this menu\n\
lastPrime\t|show biggest prime found\n\
primes\t\t|show list of primes\n\
-------------------------\n"

# load primes from file
def getPrimes(file):
    primes = []
    ReadFile = file.readlines()
    print("@primeGen: Loading primes...")
    for line in ReadFile:
        # convert str to int
        lineNum, char = 0, 0
        while (ord("0") <=  ord(line[char]) <= ord("9")):
            lineNum = lineNum*10 + int(line[char])
            char += 1

        primes += [lineNum]

    print("@primeGen: Done Loading.")
    return primes

# save primes in file
def savePrimes(file, primeList, primeInd):
    for i in range(primeInd, len(primeList)):
        file.write(str(primeList[i]) + "\n")
    return

# interactive UI
def console():
    global stopFlag
    global Primes
    while True:
        inp = input("@primeGen > ")

        if inp == "exit":
            #kills PrimeCrunch thread
            stopFlag = True
            return 0

        elif inp == "lastPrime":
            print(Primes[len(Primes)-1])

        elif inp == "primes":
            print(Primes)

        elif inp == "help":
            print(helpMenu)

        elif inp == "clear":
            os.system("clear")

        elif inp == "":
            print("", end="")

        else:
            print("Unknown command. Type help for list of commands.")

# prime finder algorithm
def primeCrunch():
    global Primes
    global stopFlag
    global firstNewPos


    primeFile = open("primes.txt", "a")
    test = Primes[firstNewPos - 1] + 2
    while (not stopFlag):
        divFlag = False
        for prime in Primes:
            if test%prime == 0:
                divFlag = True
                break

        if (not divFlag):
            Primes += [test]
            primeFile.write(str(test) + "\n")

        test += 2

    primeFile.close()

    return 0

# distributor
def main():
    global Primes
    global stopFlag
    global firstNewPos

    os.system("clear")
    a = threading.Thread(target = console, args = ())


    primeFile = open("primes.txt", "r")
    Primes = getPrimes(primeFile)
    primeFile.close()

    a.start()

    firstNewPos = len(Primes)

    b = threading.Thread(target = primeCrunch, args = ())
    b.start()

    return 0

# main()
