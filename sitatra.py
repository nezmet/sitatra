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

import os
from rich import print
from rich.panel import Panel
from elliotquotes import randElliotQuote
from usage import usage_msg

gUser = ""
currentPage = 0
taskPerPage = 10

def main():
    done = False
    while not done:
        try:
            global gUser
            delFirstComplete()
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
1. [bright_blue]A[/bright_blue]dd
2. [bright_blue]T[/bright_blue]oggle Complete
3. [bright_blue]R[/bright_blue]emove
4. [bright_blue]C[/bright_blue]hange User
5. [bright_blue]N[/bright_blue]ext page
6. [bright_blue]P[/bright_blue]revious page
7. [bright_blue]Q[/bright_blue]uit

Type [bright_blue]?[/bright_blue] or [bright_blue]help[/bright_blue] to display help''', title=f'[green]si[blue]ta[red]tra', subtitle=f'{randElliotQuote()}'))

def getUser():
    global gUser
    while gUser == "":
        gUser = input('\nEnter your username: ')
        if gUser == "":
            print("Invalid username")
        else:
            gUser = gUser.lower()

def getInput():
    global usage_msg
    check = input(f'\nEnter an option: ')
    match check.lower():
        case '1' | 'a' | 'add':
            doAdd()
        case '2' | 't' | 'toggle':
            toggleTask()
        case '3' | 'r' | 'rm' | 'remove':
            promptRemove()
        case '4' | 'change' | 'user' | 'c':
            global gUser
            gUser = ""
            getUser()
        case '5' | 'n' | 'next':
            pass
        case '6' | 'p' | 'previous':
            pass
        case '7' | 'q' | 'quit':
            return True
        case '?' | 'help':
            clearScreen()
            print(Panel(usage_msg))
            input('Press any key to continue...')
        case _:
            print('Invalid selection, please try again')

def getList():
    currentList = "\n"
    if gUser != "":
        taskList = readList()
        count = 1
        for i in taskList:
            try:
                tmp = taskList[count - 1].split(';')
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

def delFirstComplete():
    taskList = readList()
    if len(taskList) > 0:
        while taskList[0].split(';')[1] == '1\n':
            doRemove(0)
            taskList = readList()

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
    with open(gUser + ".txt", 'r') as file:
        taskList = file.readlines()

    return taskList

def writeTask(taskList):
    with open(gUser + ".txt", "w") as file:
        file.writelines(taskList)

def doAdd():
    with open(gUser + ".txt", "a") as file:
        file.write(input("Input a new task: ") + ";0\n")

def promptRemove():
    selRem = int(input('Enter the number for a task to remove: ')) - 1
    check = input(f'Are you sure you want to remove task {selRem + 1}? [Y/n]')

    match check.lower():
        case "y" | "yes" | "":
            doRemove(selRem)
        case "n" | "no":
            print('Operation cancelled.')
            input('Press any key to continue...')
        case _:
            print('Invalid input. Operation Cancelled.')
            input('Press any key to continue...')

def doRemove(toRemove):
    taskList = readList()
    taskList.pop(toRemove)
    writeTask(taskList)

def clearScreen():
    if os.name == 'posix':
        clearCommand = "clear"
    else:
        clearCommand = "cls"

    os.system(clearCommand)

if __name__ == '__main__':
    main()
