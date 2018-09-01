import os
from stringRSA import *
from mathRSA import *

def createUser():
    private, public = generateKeys()
    user = {
        'private': private,
        'public': public,
        'contacts': []
    }

    saveUser(user)

    return user

def loadUser():
    try:
        #existing user
        userFile = open("../user/usrInfo.txt", "r")
        user = eval(userFile.readlines()[0])
        userFile.close()
    except:
        user = createUser()
    
    if not('public' in user and 'private' in user and 'contacts' in user):
        user = createUser()

    return user

def saveUser(user):
    f = userFile = open("../user/usrInfo.txt", "w")
    f.write(str(user))
    f.close


def console(user):
    while True:
        inp = input("@enigma > ")
        command = inp.split()

        inp = command[0]

        if inp == "exit":
            os.system("clear")
            return 0
        
        elif inp == "":
            print("", end="")
        
        elif inp == "clear" or inp == "cls":
            os.system("clear")
        
        elif inp == "help":
            f = open("../helpMenu.txt")
            a = f.readlines()
            f.close()
            for i in a:
                print(i[:-1])
        
        elif inp == "myKey":
            print(user['public'])
        
        elif inp == "newKey":
            private, public = generateKeys()
            user['private'] = private
            user['public'] = public
            saveUser(user)
            print(user['public'])

        elif inp == "encrypt":
            text = ""
            for i in range(1, len(command)):
                text += command[i] + " "
            text = text[:-1]
            parsed = getEncryptArgs(text)
            if parsed == -1:
                print('Invalid arguments. Use')
                print('encrypt <key> <message>')
            else:
                print('encryped message:')
                print(transform(parsed[0], parsed[1], True) + 'Ö<---THE MESSAGE ENDS HERE')
                print('\n(end char ("Ö") doesn\'t belong to coded msg)')
        
        elif inp == "decrypt":
            text = ""
            for i in range(1, len(command)):
                text += command[i] + " "
            text = text[:-1]
            print(transform(text, user['private'], False))

        else:
            print("Unknown command. Type help for list of commands.")

def getEncryptArgs(text):
    N, e = 0, 0
    msg = ''
    if text[0] != '(':
        return -1
    i = 1

    # get to first digit
    while text[i] == ' ':
        i += 1
    
    # get first number
    while not(text[i] == ' ' or text[i] == ','):
        # between '0' and '9'
        if not (48 <= ord(text[i]) <= 57):
            return -1
        N = N*10 + int(text[i])
        i += 1
    
    # eat spaces
    while text[i] == ' ':
        i += 1
    
    # check if ','
    if text[i] != ',':
        return -1
    
    i+= 1
    # eat spaces
    while text[i] == ' ':
        i += 1
    
    # get second number
    while not(text[i] == ' ' or text[i] == ')'):
        # between '0' and '9'
        if not (48 <= ord(text[i]) <= 57):
            return -1
        e = e*10 + int(text[i])
        i += 1
    
    # eat spaces
    while text[i] == ' ':
        i += 1
    
    # check if ')'
    if text[i] != ')':
        return -1
    
    i+= 1
    # check if ' '
    if text[i] != ' ':
        return -1
    
    msg = text[i+1: ]
    key = (N, e)
    return(msg, key)


def main():
    os.system("clear")
    user = loadUser()
    console(user)
    return 0

main()