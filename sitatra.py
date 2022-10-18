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
#

# Declare global variables. Might move these to a module since usage.txt already exists.
gUser = ""
usage_file = open("usage.txt", "r")
usage_msg = usage_file.read()

# Execute appropriate functions and handle all errors
def main():
    try:
        print(f'SImple TAsk TRAcker\n')
        global gUser
        while gUser == "":
            tUser()
        tLoop()
    except FileNotFoundError:
        print('\nNo tasks found for this user.')
        main()
    except Exception as e:
        global usage_msg
        print(e, '\n', '\n\n', usage_msg)

# Determine username for list filename
def tUser():
    msg = "Enter your username: "
    global gUser
    gUser = input(msg)
    if gUser == "":
        msg = "Invalid username\n"
    else:
        msg = f'Welcome, {gUser}'
    print(msg)

# TUI event loop
def tLoop():
    end = False
    task_msg = ["Please select from the following:",
                "1. Add task",
                "2. Remove task",
                "3. List tasks",
                "4. Change user",
                "5. Quit",
                "",
                "Type ? or help at any time to display help followed by this prompt"]
    print()
    for i in task_msg:
        print(i)
        global usage_msg
    print()
    while end is not True:
        match input('sitatra: '):
            case '1':
                tAdd()
            case '2':
                tRemove()
            case '3':
                tList()
            case '4':
                tUser()
            case '5':
                end = True
            case '?':
                print(usage_msg)
                main()
            case 'help':
                print(usage_msg)
                main()
            case _:
                print('Invalid selection, please try again')
                main()

# Add tasks to the user.txt file
def tAdd():
    global gUser
    f = open(gUser + ".txt", "a")
    f.write(input("Input a new task: ") + "\n")
    f.close()

# List all tasks for the current user.txt
def tList():
    global gUser
    f = open(gUser + ".txt", "r")
    list = f.readlines()
    f.close()
    count = 1
    print('All tasks:\n')
    for i in list:
        print(str(count) + ". " + i, end="")
        count += 1
    print()

# Remove tasks from list pulled from user.txt and rewrites user.txt
def tRemove():
    global gUser
    f = open(gUser + ".txt", "r")
    list = f.readlines()
    f.close()
    selRem = int(input('Enter the number for a task to remove: ')) - 1
    try:
        check = input(f'Are you sure you want to remove task {selRem + 1}. {list[selRem]}? (Y/n)')
        match check.lower():
            case "y":
                list.pop(selRem)
            case "yes":
                list.pop(selRem)
            case "":
                list.pop(selRem)
            case "n":
                print('Operation cancelled.')
                main()
            case "no":
                print('Operation cancelled.')
                main()
            case _:
                print('Invalid input')
                main()
    except:
        print('Invalid input')
    f = open(gUser + ".txt", "w")
    f.writelines(list)
    f.close()

# init main() if not being called as a module
if __name__ == '__main__':
    main()
