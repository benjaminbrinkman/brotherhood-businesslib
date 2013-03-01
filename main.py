#!/usr/bin/env python2

from pymongo import MongoClient
import contacts
import tasks

DATABASE_NAME="brotherhood"

def main():
    run = True
    connection = MongoClient()
    database = connection[DATABASE_NAME]
    menu = """
Main Menu
-[T]asks
-([C]ontacts) WARNING: Not yet implemented!
-[Q]uit
Please enter the square bracketed letter of the menu option you wish to use [T]:  """
    while run == True:
        currentMenu = raw_input(menu)
        if currentMenu == "":
            currentMenu = "T"
        if currentMenu.upper().startswith("C"):
            contacts.main(database.contacts)
        elif currentMenu.upper().startswith("T"):
            tasks.main(database.tasks)
        elif currentMenu.upper().startswith("Q"):
            run = False


if __name__ == "__main__":
    main()
