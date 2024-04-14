import os
import sys
import json
from datetime import datetime
import re

def find_tasks():

    '''
    # 1. view of all tasks that are:
            - due today
            - not completed

    # 2. view of all tasks that are:
            - due in three days
            - not completed
    '''

    # get home directory
    home = os.environ["HOME"]

    # retrieve current master directory
    master_dir = ""
    with open(f'{home}/.jafr/user-settings.json', 'r+') as f:
        curr_master = json.load(f)
        master_dir = curr_master["master"]
    
    today = datetime.today().date()
    task_string = "Due: "

    isdir = os.path.isdir(master_dir)
    if isdir == False:
        return -2

    master_dir = master_dir + "/tasks.md"

    try:
        task_file = open(master_dir, 'r')
    except:
        return -1
    task_lines = task_file.readlines()

    for i in task_lines:
        i = i.strip()

    task_found_index = [0 for i in range(len(task_lines))]

    for i in range (0, len(task_lines)):
        for j in task_lines[i]:
            task_found_index[i] = task_lines[i].find(task_string)

    # save task descriptions
    task_descriptions = [0 for i in range(len(task_lines))]
    for i in range (0, len(task_found_index)):
        if (task_found_index[i] != -1):
            task_start_index = task_lines[i].find("-")
            task_descriptions[i] = task_lines[i][(task_start_index + 2):(task_found_index[i] - 1)]

    # check due date and completion status
    task_due_dates = [0 for i in range(len(task_lines))]
    task_status = [0 for i in range(len(task_lines))]
    for i in range (0, len(task_descriptions)):
        if (task_descriptions[i] != 0):
            task_due_dates[i] = task_lines[i][(task_found_index[i] + 5) : (task_found_index[i] + 13)]
            temp_status = task_lines[i][(task_found_index[i] + 14):]
            if("not" in temp_status):
                task_status[i] = 'N'
            else:
                task_status[i] = 'Y'

    # retrieve today's date
    today_date = today.strftime("%d/%m/%y")
    date_left = ['-1' for i in range(len(task_lines))]

    # consider invalid date -> needs to be skipped
    for i in range (0, len(task_descriptions)):
        if (task_descriptions[i] != 0):
            temp_date = task_due_dates[i]
            try:
                d1 = datetime.strptime(temp_date, "%d/%m/%y")
                d2 = datetime.strptime(today_date, "%d/%m/%y")
                date_left[i] = (d1 - d2).days
            except:
                date_left[i] = -1
    
    return date_left, task_status, task_descriptions, task_due_dates


def modify_tasks(new_task_status):

    tasks_found = find_tasks()
    task_descriptions = tasks_found[2]
    task_due_dates = tasks_found[3]
    task_status = tasks_found[1]

    # find and modify task status
    # get home directory
    home = os.environ["HOME"]

    # retrieve current master directory
    master_dir = ""
    with open(f'{home}/.jafr/user-settings.json', 'r+') as f:
        curr_master = json.load(f)
        master_dir = curr_master["master"]

    master_dir = master_dir + "/tasks.md"
    with open(master_dir,'r+') as file:
        data = file.readlines()

        task_found_index = [0 for i in range(len(task_descriptions))]
        for i in range(len(task_descriptions)):
            for j in data[i]:
                task_found_index[i] = data[i].find("Due: ")
        
        for i in range (len(data)):
            if (new_task_status[i] == "Y" and task_descriptions[i] != 0):
                task_lines_start = data[i][:(task_found_index[i] + 14)]
                task_lines_end = "complete\n"
                data[i] = task_lines_start + task_lines_end

        file.seek(0)
        file.truncate()
        file.writelines(data)
        file.close()


def find_meetings():
    
    '''
    # 1. view of all meetings that are:
            - scheduled today

    # 2. view of all meetings that are:
            - scheduled in 7 days
    '''

    # retrieve current master directory
    master_dir = ""
    home = os.environ["HOME"]
    with open(f'{home}/.jafr/user-settings.json', 'r+') as f:
        curr_master = json.load(f)
        master_dir = curr_master["master"]

    today = datetime.today().date()
    meeting_string = "Scheduled: "
    master_dir = master_dir + "/meetings.md"
    try:
        meeting_file = open(master_dir, 'r')
    except:
        return -1
    meeting_lines = meeting_file.readlines()

    meeting_found_index = [0 for i in range(len(meeting_lines))]

    for i in range (0, len(meeting_lines)):
        for j in meeting_lines[i]:
            meeting_found_index[i] = meeting_lines[i].find(meeting_string)

    # save meeting descriptions
    meeting_descriptions = [0 for i in range(len(meeting_lines))]
    for i in range (0, len(meeting_found_index)):
        if (meeting_found_index[i] != -1):
            meeting_start_index = meeting_lines[i].find("-")
            meeting_descriptions[i] = meeting_lines[i][(meeting_start_index + 2):(meeting_found_index[i] - 1)]
    
    # check scheduled time
    meeting_times = [0 for i in range(len(meeting_lines))]
    for i in range (0, len(meeting_descriptions)):
        if (meeting_descriptions[i] != 0):
            meeting_times[i] = meeting_lines[i][(meeting_found_index[i] + 11):(meeting_found_index[i] + 16)]

    # check scheduled date
    meeting_dates = [0 for i in range(len(meeting_lines))]
    for i in range (0, len(meeting_descriptions)):
        if (meeting_descriptions[i] != 0):
            meeting_dates[i] = meeting_lines[i][(meeting_found_index[i] + 17):(meeting_found_index[i] + 25)]

    # retrieve today's date
    today_date = today.strftime("%d/%m/%y")

    date_left = ['-1' for i in range(len(meeting_lines))]

    for i in range (0, len(meeting_descriptions)):
        if (meeting_descriptions[i] != 0):
            temp_date = meeting_dates[i]
            try:
                d1 = datetime.strptime(temp_date, "%d/%m/%y")
                d2 = datetime.strptime(today_date, "%d/%m/%y")
                date_left[i] = (d1 - d2).days
            except:
                date_left[i] = -1

    return date_left, meeting_descriptions, meeting_dates, meeting_times


def initial_display():

    tasks_display = find_tasks()
    if tasks_display == -1:
        return -1
    elif tasks_display == -2:
        return -2
    
    task_date_left = tasks_display[0]
    task_status = tasks_display[1]
    task_descriptions = tasks_display[2]
    task_due_date = tasks_display[3]

    meetings_display = find_meetings()
    if meetings_display == -1:
        return -1
    meeting_date_left = meetings_display[0]
    meeting_descriptions = meetings_display[1]
    meeting_date = meetings_display[2]
    meeting_time = meetings_display[3]
    
    print("Just a friendly reminder! \
You have these tasks to finish today.")
    for i in range (0, len(task_date_left)):
        if (int(task_date_left[i]) == 0 and task_status[i] == 'N'):
            print("-", task_descriptions[i])

    print()

    print("These tasks need to be finished \
in the next three days!")
    for i in range (0, len(task_date_left)):
        if (int(task_date_left[i]) <= 3 \
        and int(task_date_left[i]) > 0 \
        and task_status[i] == 'N'):
            print("-", task_descriptions[i], "by", task_due_date[i])
    print()
    
    print("You have the following meetings today!")
    for i in range (0, len(meeting_date)):
        if (int(meeting_date_left[i]) == 0):
            print("-", meeting_descriptions[i],\
            "at", meeting_time[i])
    print()

    print("You have the following meetings scheduled over the next week!")
    
    for i in range (0, len(meeting_date_left)):
        if (int(meeting_date_left[i]) <= 7 \
        and int(meeting_date_left[i]) > 0):
            print("-", meeting_descriptions[i],\
            "on", meeting_date[i], "at",\
            meeting_time[i])
    
    print()

def complete_tasks():

    tasks_display = find_tasks()
    if tasks_display == -1:
        return
    
    task_date_left = tasks_display[0]
    task_status = tasks_display[1]
    task_descriptions = tasks_display[2]
    task_due_dates = tasks_display[3]
    task_incomplete_index = [0 for i in range(len(task_descriptions))]

    # find tasks that are not completed
    # all tasks that are marked "N" in task_status.
    counter = 0
    for i in range (0, len(task_status)):
        if task_status[i] == "N":
            task_incomplete_index[counter] = i
            counter = counter + 1

    if all(item == 0 for item in task_incomplete_index):
        print("No tasks to complete!")
        return

    
    print("Which task(s) would you like to mark as completed?")
    counter = 0
    for i in range (len(task_status)):
        if task_status[i] == "N":
            print(f"{counter + 1}. {task_descriptions[i]} by {task_due_dates[i]}")
            #task_incomplete_index[counter] = i
            counter = counter + 1
    
    possible_task_nums = [0 for i in range(counter)]
    for i in range(counter):
        possible_task_nums[i] = i + 1


    while True:
        task_nums = input().strip()
        task_nums_split = task_nums.split(" ")
        task_nums_int = []
        try:
            for num in task_nums_split:
                num_int = int(num)
                if num_int in possible_task_nums:
                    task_nums_int.append(num_int)
                else:
                    print("Invalid task number. Please type again.")
                    break
            else:
                break
        except ValueError:
            print("Invalid input. Please type valid numbers separated by spaces.") 

    for i in range(len(task_incomplete_index)):
        if (i + 1) in task_nums_int:
            index = task_nums_int.index(i + 1)
            task_status[task_incomplete_index[task_nums_int[index] - 1]] = "Y"

    # modify the task file
    modify_tasks(task_status)

    print("Marked as complete.")


def add_meeting(passwd_path):
    while True:
        meeting_description = input("Please enter a meeting description:\n")
        if meeting_description == "":
            print("Please enter a valid meeting description.", end = "")
        else:
            break

    
    while True:
        meeting_date = input("Please enter a date:\n")
        try:
            temp = meeting_date.split("/")
            if len(temp[0]) == 2 and len(temp[1]) == 2 and len(temp[2]) == 2:
                if 0 < int(temp[0]) <= 31 and 0 < int(temp[1]) <= 12:
                    date = datetime.strptime(meeting_date, "%d/%m/%y")
                    break
                else:
                    print("Not in valid format. Should be dd/mm/yy", end="")
            else:
                print("Not in valid format. Should be dd/mm/yy", end = "")
        except:
            print("Not in valid format. Should be dd/mm/yy", end = "")

    while True:
        meeting_time = input("Please enter a time:\n")
        try:
            time = meeting_time.split(":")
            if len(time) == 2 and int(time[0]) <= 24 and int(time[0]) <= 60:
                break
            else:
                print("Not in valid format. Should be hh:mm", end = "")
        except:
            print("Not in valid format. Should be hh:mm", end = "")

    new_meeting = f"{meeting_description} on {meeting_date} at {meeting_time}"

    print(f"Ok, I have added {new_meeting}.")

    # modify information on file
    home = os.environ["HOME"]
    with open(f'{home}/.jafr/user-settings.json', 'r+') as f:
        curr_master = json.load(f)
        master_dir = curr_master["master"]
    f.close()

    master_dir = master_dir + "/meetings.md"
    try:
        curr_file = open(master_dir, 'a')
    except:
        return -1
    curr_file.write("\n##### added by you\n")

    new_meeting_formatted = f"{meeting_description} Scheduled: {meeting_time} {meeting_date}"
    curr_file.write(f"- {new_meeting_formatted}\n")
    curr_file.close()

    updated_meetings = find_meetings()
    if updated_meetings == -1:
        return -1
    new_meeting_description = updated_meetings[1]

    meeting_num = 0
    for i in range(len(new_meeting_description)):
        if new_meeting_description[i] != 0:
            meeting_num = meeting_num + 1

    answer_1 = input("Would you like to share this meeting? [y/n]: ")
    if answer_1 == "y":
        sub_share_meetings(meeting_num, passwd_path)
        

def add_shared_task(home_dir, task_description, task_due_date, completion, username):
    # now modify the files in the retrieved directories.
    target_file = "tasks.md"
    for item in os.scandir(home_dir):
        if item.is_dir():
            add_shared_task(item.path, task_description, task_due_date, completion, username)
        elif item.is_file() and item.name == target_file:
            with open(item.path, "r+") as f:
                content = f.read()
                f.write(f"\n##### shared by {username}")
                new_task_formatted = f"{task_description} Due: {task_due_date} {completion}"
                f.write(f"\n- {new_task_formatted}\n")
                f.close()

def share_task(passwd_path):

    tasks_display = find_tasks()
    if tasks_display == -1:
        return
    
    task_status = tasks_display[1]
    task_descriptions = tasks_display[2]
    task_due_dates = tasks_display[3]

    print("Which task would you like to share?")

    j = 0
    for i in range (len(task_descriptions)):
        if task_descriptions[i] != 0 and task_due_dates != 0:
            print(f"{j + 1}. {task_descriptions[i]} by {task_due_dates[i]}")
            j = j + 1

    # do error handling here
    while True:
        task_input = input()
        try:
            task_nums = int(task_input)
            if task_nums <= len(task_descriptions) and task_nums >= 0:
                break
            else:
                print("Invalid task number. Please choose again.")
        except:
            print("Invalid task number. Please choose again.")

    sub_share_tasks(task_nums, passwd_path)


def sub_share_tasks(task_nums, passwd_path):
    tasks_display = find_tasks()
    if tasks_display == -1:
        return
    task_status = tasks_display[1]
    task_descriptions = tasks_display[2]
    task_due_dates = tasks_display[3]

    print("Who would you like to share with?")

    # current user and current home
    username = os.environ['USER']
    home_dir = os.environ['HOME']

    passwd_file = open(f'{passwd_path}', 'r')
    passwd_lines = passwd_file.readlines()

    # make arrays of usernames and IDs
    passwd_usernames = [0 for i in range(len(passwd_lines) - 1)]
    passwd_userID = [0 for i in range(len(passwd_lines) - 1)]
    passwd_hd = [0 for i in range(len(passwd_lines) - 1)]

    counting = 0
    for lines in passwd_lines:
        lines_split = lines.split(":")
        if (lines_split[0] != username):
            passwd_usernames[counting] = lines_split[0]
            passwd_userID[counting] = lines_split[2]
            passwd_hd[counting] = lines_split[5]
            counting = counting + 1

    for i in range(len(passwd_userID)):
        print(f"{passwd_userID[i]} {passwd_usernames[i]}")

    while True:
        ID_input_list = input()
        ID_input_split = ID_input_list.split(" ")
        ID_input_array = []

        for ID in ID_input_split:
            if ID in passwd_userID:
                ID_input_array.append(ID)
            else:
                print("Invalid user ID. Please type again.")
                break
        else:
            break

    selected_hd = [0 for i in range(len(passwd_lines) - 1)]
    # all inputs are validified
    for i in range(len(ID_input_array)):
        # get the ID
        # find it in the passwd_userID array
        # get the home directory of the user of the ID.
        temp_index = passwd_userID.index(ID_input_split[i])
        selected_hd[i] = passwd_hd[temp_index]

    i = 0
    j = 0
    while i < task_nums:
        if task_descriptions[j] != 0 and task_due_dates[j] != 0:
            i = i + 1
        j = j + 1

    task_share_description = task_descriptions[j - 1]
    task_share_due = task_due_dates[j - 1]
    task_share_status = task_status[j - 1]

    task_completion = ""
    if task_share_status == "Y":
        task_completion = "complete"
    if task_share_status == "N":
        task_completion = "not complete"

    i = 0
    while selected_hd[i] != 0:
        add_shared_task(selected_hd[i], task_share_description, task_share_due, task_completion, username)
        i = i + 1
    print("Task shared.")


def add_shared_meeting(home_dir, meeting_description, meeting_time, meeting_date, username):
    # now modify the files in the retrieved directories.
    target_file = "meetings.md"
    for item in os.scandir(home_dir):
        if item.is_dir():
            add_shared_meeting(item.path, meeting_description, meeting_time, meeting_date, username)
        elif item.is_file() and item.name == target_file:
            with open(item.path, "r+") as f:
                content = f.read()
                f.write(f"\n##### shared by {username}")
                new_task_formatted = f"{meeting_description} Scheduled: {meeting_time} {meeting_date}"
                f.write(f"\n- {new_task_formatted}\n")
                f.close()

def sub_share_meetings(meeting_num, passwd_path):
    meetings_display = find_meetings()
    if meetings_display == -1:
        return -1
    
    meeting_descriptions = meetings_display[1]
    meeting_date = meetings_display[2]
    meeting_time = meetings_display[3]

    print("Who would you like to share with?")

    username = os.environ['USER']
    home_dir = os.environ['HOME']

    passwd_file = open(f'{passwd_path}', 'r')
    passwd_lines = passwd_file.readlines()

    # make arrays of usernames and IDs
    passwd_usernames = [0 for i in range(len(passwd_lines) - 1)]
    passwd_userID = [0 for i in range(len(passwd_lines) - 1)]
    passwd_hd = [0 for i in range(len(passwd_lines) - 1)]
    counting = 0

    for lines in passwd_lines:
        lines_split = lines.split(":")
        if (lines_split[0] != username):
            passwd_usernames[counting] = lines_split[0]
            passwd_userID[counting] = lines_split[2]
            passwd_hd[counting] = lines_split[5]
            counting = counting + 1

    for i in range(len(passwd_userID)):
        print(f"{passwd_userID[i]} {passwd_usernames[i]}")

    ID_input_list = input()
    ID_input_split = ID_input_list.split(" ")

    for i in range(len(ID_input_split)):
        # perform error handling
        while ID_input_split[i] not in passwd_userID:
            print("invalid user ID. Please select a valid user ID.")
            ID_input_list = input()
            ID_input_split = ID_input_list.split(" ")

    selected_hd = [0 for i in range(len(passwd_lines) - 1)]
    # all inputs are validified
    for i in range(len(ID_input_split)):
        # get the ID
        # find it in the passwd_userID array
        # get the home directory of the user of the ID.
        temp_index = passwd_userID.index(ID_input_split[i])
        selected_hd[i] = passwd_hd[temp_index]

    i = 0
    j = 0
    while i < meeting_num:
        if meeting_descriptions[j] != 0:
            i = i + 1
        j = j + 1

    meeting_share_description = meeting_descriptions[j - 1]
    meeting_share_time = meeting_time[j - 1]
    meeting_share_date = meeting_date[j - 1]

    i = 0
    while selected_hd[i] != 0:
        add_shared_meeting(selected_hd[i], meeting_share_description, meeting_share_time, meeting_share_date, username)
        i = i + 1
    print("Meeting shared.")

def share_meeting(passwd_path):

    meetings_display = find_meetings()
    if meetings_display == -1:
        return -1
    
    meeting_descriptions = meetings_display[1]
    meeting_date = meetings_display[2]
    meeting_time = meetings_display[3]

    print("Which meeting would you like to share?")

    j = 0
    for i in range (len(meeting_descriptions)):
        if meeting_descriptions[i] != 0:
            print(f"{j + 1}. {meeting_descriptions[i]} on {meeting_date[i]} at {meeting_time[i]}")
            j = j + 1

    # do error handling here
    while True:
        meeting_input = input()
        try:
            meeting_num = int(meeting_input)
            if meeting_num <= len(meeting_descriptions) and meeting_num >= 0:
                break
            else:
                print("Invalid meeting number. Please choose again.")
        except:
            print("Invalid meeting number. Please choose again.")

    sub_share_meetings(meeting_num, passwd_path)

def change_dir():

    print("Which directory would you like Jafr to use?")
    new_master = input()
    home = os.environ["HOME"]
    with open(f'{home}/.jafr/user-settings.json', 'r+') as f:
        
        old_master = json.load(f)
        f.seek(0)
        f.truncate()

        old_master["master"] = new_master

        json.dump(old_master, f, indent=4)

        print(f"Master directory changed to {new_master}.")

def exit_jafr():

    return 1

def main():

    existing = initial_display()
    exit_code = 0

    passwd_provided = len(sys.argv)
    if passwd_provided == 2:
        passwd_path = sys.argv[1]

    if existing == -1:
        print("Missing tasks.md or meetings.md file.", file = sys.stderr)
        return
    elif existing == -2:
        print("Jafr's chosen master directory does not exist.", file = sys.stderr)
        return

    while(exit_code != 1):

        # prompts the user
        print("What would you like to do?")
        print("1. Complete tasks")
        print("2. Add a new meeting.")
        print("3. Share a task.")
        print("4. Share a meeting.")
        print("5. Change Jafr's master directory.")
        print("6. Exit")

        option_str = input()

        try:
            chosen_int = int(option_str)
        except:
            print("Please enter a number.", file=sys.stderr)
            option_str = input()

            try:
                chosen_int = int(option_str)
            except:
                return

        if(chosen_int == 1):
            complete_tasks()
        elif(chosen_int == 2):
            add_meeting(passwd_path)
        elif(chosen_int == 3):
            share_task(passwd_path)
        elif(chosen_int == 4):
            share_meeting(passwd_path)
        elif(chosen_int == 5):
            change_dir()
        elif(chosen_int == 6):
            exit_code = exit_jafr()
        else:
            print("Number out of range.")
            return


if __name__ == '__main__':
    main()
