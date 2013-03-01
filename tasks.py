import datetime

def main(collection):
    menu = """
Task Menu
-[A]dd Task
-[L]ist Tasks
-[M]ain Menu
-[Q]uit
Please enter the square bracketed letter of the menu option you wish to use [A]:  """
    tasks_run = True
    while tasks_run == True:
        currentMenu = raw_input(menu)
        if currentMenu == "":
            # set default item
            currentMenu = "A"
        if currentMenu.upper().startswith("A"):
            # add task
            title = raw_input("Title:  ")
            info = raw_input("Text about task:  ")
            add_task(collection, title, info)
        elif currentMenu.upper().startswith("L"):
            # query and list tasks
            ui_list_tasks(collection)
        elif currentMenu.upper().startswith("M"):
            tasks_run = False
        elif currentMenu.upper().startswith("Q"):
            quit()

def add_task(collection, title, info):
    collection.insert({"title": title, "info": info, "priority": 2, "client_name": "Brotherhood User", "start_date": str(datetime.date(year=datetime.datetime.now().year, month=datetime.datetime.now().month, day=datetime.datetime.now().day)), "start_time": str(datetime.time(hour=datetime.datetime.now().hour, minute=datetime.datetime.now().minute)), "completion": 0})
    
def all_tasks(collection):
    result = []
    for task in collection.find():
        result.append(task["title"])
    return result
    
def tasks_by_due_date(collection, due_date):
    result = []
    for task in collection.find({"due_date": datetime.datetime(year=due_date.year, month=due_date.month, day=due_date.day)}):
        result.append(task["title"])
    return result
    
def tasks_by_start_date(collection, start_date):
    result = []
    for task in collection.find({"start_date": start_date}):
        result.append(task["title"])
    return result
    
def incomplete_tasks(collection):
    result = []
    for task in collection.find():
        if task["completion"] < 100:
            result.append(task["title"])
    return result

def tasks_by_title(collection, title):
    result = []
    for task in collection.find({"title": title}):
        result.append(task["title"])
    return result
    
def ui_generate_datetime():
    year = raw_input("Please enter the year [" + str(datetime.datetime.now().year) + "]:  ")
    if year == "":
        year = datetime.datetime.now().year
    month = raw_input("Please enter the month [" + str(datetime.datetime.now().month) + "]:  ")
    if month == "":
        month = datetime.datetime.now().month
    date = raw_input("Please enter the date [" + str(datetime.datetime.now().day) + "]:  ")
    if date == "":
        date = datetime.datetime.now().day
    time_deadline = raw_input("Is there a specific time you need? (Y/N) [N]:  ")
    if time_deadline == "":
        time_deadline = "N"
    if time_deadline.upper().startswith("Y"):
        hour = raw_input("Please enter the hour (00-23) [" + str(datetime.datetime.now().hour) + "]:  ")
        if hour == "":
            hour = datetime.datetime.now().hour
        else:
            hour = int(hour)
        minute = raw_input("Please enter the minute (00-59) [" + str(datetime.datetime.now().minute) + "]:  ")
        if minute == "":
            minute = datetime.datetime.now().minute
        else:
            minute = int(minute)
        result = datetime.datetime(year=year, month=month, day=date, hour=hour, minute=minute)
    else:
        result = datetime.datetime(year=year, month=month, day=date)
    return result

def ui_task_operations(collection, tasks, selection):
    task_title = tasks[selection - 1]
    task = collection.find_one(title=task_title)
    info = """
You have selected:
%s: %s

""" % (str(selection), task["title"])
    try:
        info += """Which was started on %s at %s
For %s
With %s percent completion and Level %s priority
""" % (str(task["start_date"]), str(task["start_time"]), str(task["client_name"]), str(task["completion"]), str(task["priority"]))
    except KeyError:
        pass    
    info += """
You must do the following:
%s
""" % (task["info"],)
    try:
        info += "It must be done by %s at %s" % (str(task["due_date"]), str(task["due_time"]))
    except KeyError:
        pass
    
    operations_menu = """
Task Operations Menu
-Set a [d]ue date
-Set percentage of [c]ompletion
-Set [p]riority
-(Set [a]ssociated client from contacts list) WARNING: Not yet implemented!
-Go [B]ack
-[Q]uit
Please state your preferred operation [B]:  """
    display = True
    while display == True:
        print info
        currentMenu = raw_input(operations_menu)
        if currentMenu == "":
            # set default item
            currentMenu = "B"
        if currentMenu.lower().startswith("d"):
            result = ui_generate_datetime()
            collection.update({"title": task_title}, {"$set": {"due_date": result.date, "due_time": result.time}})
        elif currentMenu.lower().startswith("c"):
            result = raw_input("Percentage of completion (0-100) [" + str(task["completion"]) + "]:  ")
            collection.update({"title": task_title}, {"$set": {"completion": int(result)}})
        elif currentMenu.lower().startswith("p"):
            result = int(raw_input("Please enter the level of priority (1-7) [" + int(task["priority"]) + "]:  "))
            collection.update({"title": task_title}, {"$set": {"priority": int(result)}})
        elif currentMenu.upper().startswith("B"):
            display = False
        elif currentMenu.upper().startswith("Q"):
            quit()
    
def ui_list_tasks(collection):
    query_menu = """
Task Query Menu
Display:
-[A]ll tasks
-[I]ncomplete tasks
-Tasks by [t]itle
-Tasks by [d]ue date
-Tasks by [s]tart date
-Go [B]ack
-[Q]uit
Please state your query method [I]:  """
    display = True
    while display == True:
        currentMenu = raw_input(query_menu)
        if currentMenu == "":
            # set default item
            currentMenu = "I"
        if currentMenu.upper().startswith("A"):
            # list all tasks
            tasks = all_tasks(collection)
            ui_select_task(collection, tasks)
        elif currentMenu.upper().startswith("I"):
            tasks = incomplete_tasks(collection)
            ui_select_task(collection, tasks)
        elif currentMenu.lower().startswith("t"):
            title = raw_input("Please enter the title to query:  ")
            tasks = tasks_by_title(collection, title)
            ui_select_task(collection, tasks)
        elif currentMenu.lower().startswith("d"):
            due_date = ui_generate_datetime()
            tasks = tasks_by_due_date(collection, due_date)
            ui_select_task(collection, tasks)
        elif currentMenu.lower().startswith("s"):
            start_date = ui_generate_datetime()
            tasks = tasks_by_start_date(collection, start_date)
            ui_select_task(collection, tasks)
        elif currentMenu.upper().startswith("B"):
            display = False
        elif currentMenu.upper().startswith("Q"):
            quit()

def ui_select_task(collection, tasks):
    task_ops = True
    while task_ops == True:
        i = 1
        for task in tasks:
            print
            print str(i) + ": " + task
            i += 1
        print
        selection = raw_input("Using the numbers that correspond to each task, select a task to operate on, or enter B to go back [B]:  ")
        if selection == "":
            selection = "B"
        if selection.upper().startswith("B"):
            task_ops = False
        else:
            try:
                selection = int(selection)
            except ValueError:
                print
                print "Please use a number to proceed, or the letter B to go back."
                print
            ui_task_operations(collection, tasks, selection)

if __name__ == "__main__":
    main()
