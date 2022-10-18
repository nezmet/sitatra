# (SI)mple (TA)sk (TRA)cker

# Global user variable
gUser = ""
usage_file = open("usage.txt", "r")
usage_msg = usage_file.read()

def main():
    try:
        print(f'SImple TAsk TRAcker\n')
        tUser()
        tLoop()

    except FileNotFoundError:
        print('No tasks for this user.')
        tLoop()
    except Exception as e:
        global usage_msg
        print(e, '\n', '\n\n', usage_msg)

def tUser():
    msg = "Enter your username: "
    global gUser
    gUser = input(msg)
    print(f'\nWelcome {gUser}.\n')

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
    for i in task_msg:
        print(i)
        global usage_msg
    while end is not True:
        match input('sitatra: '):
            case '1':
                tAdd()
            case '2':
                tRem()
            case '3':
                tLi()
            case '4':
                tUser()
            case '5':
                end = True
            case '?':
                print(usage_msg)
            case 'help':
                print(usage_msg)
            case _:
                print('Invalid selection, please try again')
                tLoop()


def tAdd():
    global gUser
    f = open(gUser + ".txt", "a")
    f.write(input("Input a new task: ") + "\n")
    f.close()

def tLi():
    global gUser
    f = open(gUser + ".txt", "r")
    list = f.readlines()
    f.close()
    count = 1
    print('All tasks:\n')
    for i in list:
        print(str(count) + ". " + i, end="")
        count += 1

def tRem():
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
                tLoop()
            case "no":
                print('Operation cancelled.')
                tLoop()
            case _:
                print('Invalid input')
                tLoop()
    except:
        print('Invalid input')
    f = open(gUser + ".txt", "w")
    f.writelines(list)
    f.close()

if __name__ == '__main__':
    main()
