# (SI)mple (TA)sk (TRA)cker
#
# Python 7.1 Project - TODO List
# 
# Need statement:
# - TUI to use REPL
# - Add tasks, Delete tasks, List tasks in the order they were inserted
# - Persist across runs
# - Multiple users with unique lists
# - Store data on disk somewhere, human readable
# - No memorization of commands, user friendly prompt interface
# 
# Stretch Goals:
# - Integrate gpg somehow
# - Add options to export as csv and other filetypes
# - Store timestamps with the tasks and make them show up optionally
# - Add a config file
#
#
# sitatra.py

# Import elliotquotes.py, a fork from Terry Miller's elliotquote repository.
from elliotquotes import randElliotQuote

# Declare global variables. Might move these to a module since usage.txt already exists.
gUser = ""
usage_file = open("usage.txt", "r")
usage_msg = usage_file.read()

# Execute appropriate functions and handle all errors
def main():
    print(f'SImple TAsk TRAcker\n\n{randElliotQuote()}\n')
    global gUser
    while gUser == "":
        tUser()
    showTUI()
    done = False
    while not done:
        try:
            done = getInput()
        except FileNotFoundError:
            print('No tasks found for this user.')
        except IndexError:
            print('Invalid task number')
        except Exception as e:
            global usage_msg
            print(e, '\n', '\n\n', usage_msg)

# Determine username for list filename
def tUser():
    msg = "Enter your username: "
    global gUser
    while gUser == "":
        gUser = input(msg)
        if gUser == "":
            msg = "Invalid username\n"
        else:
            msg = f'Welcome, {gUser}'
            gUser = gUser.lower()
        print(msg)

# TUI event loop
def showTUI():
    tui = ["Please select from the following:",
                "1. Add task",
                "2. Remove task",
                "3. List tasks",
                "4. Change user",
                "5. Quit",
                "",
                "Type ? or help at any time to display help followed by this prompt"]
    for i in tui:
        print(i)
    print()

def getInput():
    global usage_msg
    global gUser
    check = input(f'sitatra:{gUser}$ ')
    match check.lower():
        case '1' | 'a' | 'add':
            tAdd()
        case '2' | 'r' | 'rm' | 'remove':
            tRemove()
        case '3' | 'l' | 'list':
            tList()
        case '4' | 'change' | 'user' | 'change user':
            gUser = ""
            tUser()
        case '5' | 'q' | 'quit':
            return True
        case '?' | 'help':
            print(usage_msg)
            showTUI()
        case _:
            print('Invalid selection, please try again')

# Add tasks to the user.txt file
def tAdd():
    global gUser
    with open(gUser + ".txt", "a") as file:
        file.write(input("Input a new task: ") + "\n")

# List all tasks for the current user.txt
def tList():
    global gUser
    with open(gUser + ".txt", "r") as file:
        list = file.readlines()
    count = 1
    print('All tasks:\n')
    for i in list:
        print(str(count) + ". " + i, end="")
        count += 1
    print()

# Remove tasks from list pulled from user.txt and rewrites user.txt
def tRemove():
    global gUser
    with open(gUser + ".txt", "r") as file:
        list = file.readlines()
    selRem = int(input('Enter the number for a task to remove: ')) - 1
    check = input(f'Are you sure you want to remove task {selRem + 1}? [Y/n]')
    match check.lower():
        case "y" | "yes" | "":
            list.pop(selRem)
        case "n" | "no":
            print('Operation cancelled.')
        case _:
            print('Invalid input')
    with open(gUser + ".txt", "w") as file:
        file.writelines(list)

# init main() if not being called as a module
if __name__ == '__main__':
    main()
