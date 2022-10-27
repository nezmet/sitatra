# (si)mple (ta)sk (tra)cker
#
# python 7.1 project - todo list
# 
# need statement:
# - tui to use repl
# - add tasks, delete tasks, list tasks in the order they were inserted
# - persist across runs
# - multiple users with unique lists
# - store data on disk somewhere, human readable
# - no memorization of commands, user friendly prompt interface
#
# new goals:
# - printing list is default behavior
# - no more than 15 items printed at once.
# - save completed tasks
# - show completed tasks with visible delimiting
# - completed tasks at top of list should be deleted
#
# stretch goals:
# - integrate gpg somehow
# - add options to export as csv and other filetypes
# - store timestamps with the tasks and make them show up optionally
# - add a config file
#
#
# sitatra.py

# import elliotquotes.py, a fork from terryt git  miller's elliotquote repository.
import os
from rich import print
from rich.panel import Panel
from elliotquotes import randElliotQuote
from usage import usage_msg

# ugly variables going here:
gUser = ""

def main():
    done = False
    while not done:
        try:
            global gUser
            printTUI()
            if gUser == "":
                getUser()
            else: 
                done = getInput()
        except FileNotFoundError:
            print('No tasks found for this user.')
            with open(gUser + ".txt", "w"):
                pass
        except IndexError:
            print('Invalid task number')
        except Exception as e:
            global usage_msg
            print(e, '\n', '\n\n', usage_msg)

def printTUI():
    clearScreen()
    global gUser
    print(Panel(f'''Current User: {gUser}

Current List: {getList()}
Options:
1. Add
2. Toggle Complete
3. Remove
4. Change User
5. Quit

Type ? or help to display help''', title=f'[green]si[blue]ta[red]tra', subtitle=f'{randElliotQuote()}'))

def getUser():
    global gUser
    while gUser == "":
        gUser = input('Enter your username: ')
        if gUser == "":
            msg = "Invalid username"
        else:
            msg = f'Welcome, {gUser}'
            gUser = gUser.lower()
        print(msg)

def getInput():
    global usage_msg
    global gUser
    check = input(f'Enter an option: ')
    match check.lower():
        case '1' | 'a' | 'add':
            doAdd()
        case '2' | 't' | 'toggle':
            toggleTask()
        case '3' | 'r' | 'rm' | 'remove':
            doRemove()
        case '4' | 'change' | 'user' | 'change user':
            gUser = ""
            getUser()
        case '5' | 'q' | 'quit':
            return True
        case '?' | 'help':
            clearScreen()
            print(Panel(usage_msg))
            input('Press any key to continue...')
        case _:
            print('Invalid selection, please try again')

def getList():
    global gUser
    currentList = "\n"
    if gUser != "":
        with open(gUser + ".txt", "r") as file:
            list = file.readlines()
        count = 1
        for i in list:
            try:
                tmp = list[count - 1].split(';')
                match tmp[1]:
                    case "0\n":
                        tmp = tmp[0] + "\n"
                    case "1\n":
                        tmp = f'[s]{tmp[0]}[/s]\n'
                    case _:
                        tmp = tmp[0] + "\n" 
            except:
                tmp = i

            currentList += (str(count) + ". " + tmp)
            count += 1

    return currentList

def toggleTask():
    global gUser
    taskList = readList()
    toToggle = int(input('Enter a task to toggle: ')) - 1
    
    if taskList[toToggle].split(';')[1] == "0\n":
        taskComplete(taskList, toToggle)
    elif taskList[toToggle].split(';')[1] == "1\n":
        taskIncomplete(taskList, toToggle)

def taskComplete(taskList, task):
    tmp = taskList[task].split(';')
    taskList[task] = tmp[0] + ";1\n"
    writeTask(taskList)

def taskIncomplete(taskList, task):
    tmp = taskList[task].split(';')
    taskList[task] = tmp[0] + ";0\n"
    writeTask(taskList)

def readList():
    global gUser
    with open(gUser + ".txt", 'r') as file:
        taskList = file.readlines()
    return taskList

def writeTask(taskList):
    global gUser
    with open(gUser + ".txt", "w") as file:
        file.writelines(taskList)

def doAdd():
    global gUser
    with open(gUser + ".txt", "a") as file:
        file.write(input("Input a new task: ") + ";0\n")

def doRemove():
    global gUser
    taskList = readList()
    selRem = int(input('Enter the number for a task to remove: ')) - 1
    check = input(f'Are you sure you want to remove task {selRem + 1}? [Y/n]')
    match check.lower():
        case "y" | "yes" | "":
            taskList.pop(selRem)
        case "n" | "no":
            print('Operation cancelled.')
            input('Press any key to continue...')
        case _:
            print('Invalid input')
    writeTask(taskList)

def clearScreen():
    if os.name == 'posix':
        clearCommand = "clear"
    else:
        clearCommand = "cls"

    os.system(clearCommand)

if __name__ == '__main__':
    main()
