from os import system, name
import datetime
import re
import unittest
from unittest import mock

from peewee import *
# import peewee
# print(peewee.__version__)

db = SqliteDatabase('work_logs.db')

class WorkLog(Model):
    name = CharField(max_length=255)
    task_title = CharField(max_length=255)
    minutes = IntegerField(default=0)
    date = DateField(default=datetime.datetime.now)
    notes = CharField(max_length=255)
    show_log = IntegerField(default=0)

    class Meta:
        database = db


def show_menu_header(header):
    # for windows
    if name == 'nt':
        _ = system('cls')
        # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')
    print("______Work Log {}______".format(header))
    return 1


def main_menu():
    # As a user of the script, I should be prompted with a menu to
    # choose whether to add a new entry or lookup previous entries.
    show_menu_header("Main Menu")
    choice = input("""Please enter a letter from the choices below
[A]dd a new entry
[L]ookup previous entries
[Q]uit application
>""").lower()
    return choice


def run_main_menu():
    choice = ''
    while choice != 'q':
        choice = main_menu()
        if choice == 'a':
            print("You chose to add a new entry")
            create_new_entry()
        elif choice == 'l':
            print("You chose to search for entry")
            display_find_menu()
            # display_entries()
        # Menu has a “quit” option to exit the program.
        elif choice == 'q':
            print("We are sorry to see you go, goodbye.")
            exit()
        else:
            print("You did not enter a valid choice, please only enter  "
                  "letters from the list")


def display_find_menu():
    # As a user of the script, if I choose to find a previous entry,
    # I should be presented with four options: find by xxx
    choice = ''
    while choice != 'r':
        show_menu_header("Find Menu")
        choice = input("""Please enter a letter from the choices below (if your
         search returns no value, you will need to search again)
Find by [E]mployee
Find by [D]ate
Find by [T]ime spent
Find by [S]earch Term
[R]eturn to Main Menu
>""").lower()
        if choice == 'e':
            # print("You chose to lookup by employee")
            display_entries("e")
        elif choice == 'd':
            # print("You chose to search by date")
            display_entries("d")
        elif choice == 't':
            # print("You chose to lookup by time spent")
            display_entries("t")
        elif choice == 's':
            # print("You chose to lookup by Search Term")
            display_entries("s")
        elif choice == 'r':
            # print("You chose to return to the main menu")
            run_main_menu()
        else:
            print("You did not enter a valid choice, please only enter "
                  "letters from the list")
    # print("display_find_menu after")


def create_new_entry():
    # As a user of the script, if I choose to enter a new work log, I should
    # be able to provide my name, a task name, a number of
    # minutes spent working on it, and any additional notes I want to record.
    show_menu_header("Add New Entry")
    entry_information = gather_entry_information(False)
    # print(entry_information["name"])
    WorkLog.create(name=entry_information["name"],
                   task_title=entry_information["task_title"],
                   minutes=entry_information["minutes"],
                   notes=entry_information["notes"])
    run_main_menu()
    return 1


def gather_entry_information(include_date):
    date_string = datetime.date.today().strftime("%m/%d/%Y")
    if include_date:
        while True:
            try:
                date_string = input("What is your date?>")
                datetime.datetime.strptime(date_string, '%m/%d/%Y')
            except ValueError:
                print("Incorrect data format, should be MM/DD/YYYY")
                continue
            else:
                break
    # Make sure your script runs without errors. Catch exceptions and report
    # errors to the user in a meaningful way.
    while True:
        full_name = input("What is your name?>")
        if not full_name:
            print("name is not optional, please enter it")
            continue
        else:
            break
    while True:
        task_title = input("What is your task title?>")
        if not task_title:
            print("task title is not optional, please enter it")
            continue
        else:
            break
    while True:
        try:
            minutes_spent = int(input("How many minutes did you spend?>"))
        except ValueError:
            print("Please input an integer amount of minutes")
            continue
        else:
            break
    notes = input("Please enter any optional notes>")
    return {"name": full_name, "date": date_string, "task_title": task_title,
            "minutes": minutes_spent, "notes": notes}


def load_work_log(search_type):
    all_work_logs = WorkLog.select().dicts(True)

    # with open(WORK_LOG_FILE, mode='r') as csv_file:
    #    csv_reader = csv.DictReader(csv_file)
    #    for row in csv_reader:
    #       all_work_logs.append({"date": row["date"], "task_title":
    #                              row["task_title"], "minutes":
    # row["minutes"],
    #                             "notes": row["notes"], "show_log": 1})

    # for log in all_work_logs:
    # print(log)
    if search_type == 'e':
        search_pattern = input("For which employee are you searching?>")
        return all_work_logs.select().where(WorkLog.name.contains
                                            (search_pattern))
    elif search_type == 'd':
        while True:
            try:
                date_str = input("For which MM/DD/YYYY date(s) do you "
                                 "want to "
                                 "search? (enter two separated by a space"
                                 " if you want a range)>")
                split_date_str = date_str.split()
                if len(split_date_str) == 2:
                    date1 = datetime.datetime.strptime(split_date_str[0],
                                                       '%m/%d/%Y')
                    date2 = datetime.datetime.strptime(split_date_str[1],
                                                       '%m/%d/%Y')
                    return all_work_logs.select().where(
                        WorkLog.date >= date1 & WorkLog.date
                        <= date2)
                else:
                    only_date = datetime.datetime.strptime(date_str,
                                                           '%m/%d/%Y')
                    return all_work_logs.select().where(
                        WorkLog.date == only_date)
            except ValueError:
                print("Incorrect data format, should be MM/DD/YYYY")
                continue
            else:
                break
                # for log in all_work_logs:
                # print(log["date"] + " " + str(log["show_log"]))
    elif search_type == 't':
        while True:
            try:
                search_minutes = int(input("For how many minutes do "
                                           "you want "
                                           "to search?>"))
                return all_work_logs.select().where(WorkLog.minutes ==
                                                    search_minutes)
            except ValueError:
                print("Please input an integer amount of minutes")
                continue
            else:
                # for log in all_work_logs:
                #     print(log["minutes"] + " " + str(log["show_log"]))
                break
    elif search_type == 's':
        search_pattern = input("What is your search string?>")
        return all_work_logs.select().where(WorkLog.task_title.contains
                                            (search_pattern)
                                            | WorkLog.notes.contains
                                            (search_pattern))
    # for log in all_work_logs:
    #     print(str(log["name"]) + " " + log["task_title"] + " " + log["notes"]
    #           + " " + str(log["show_log"]))
    # print(all_work_logs.where(WorkLog.show_log == 1).count())
    return all_work_logs


def display_entries(search_type):
    # When displaying the entries, the entries should be displayed in a
    # readable format with the date, task name, time
    # spent, and notes information.
    work_logs = load_work_log(search_type)
    # print(work_logs.count())

    # print("display_entries before" + str(work_logs.count()))
    if work_logs.count() == 0:
        print("Your search returned no values, please try again")
        return

    # for log in work_logs:
    #    print(log["name"] + " " + log["task_title"] + " "
    #          + log["notes"] + " " + str(log["show_log"]))
    choice = ''
    i = 0
    while choice != 'r':
        # print("i: " + str(i))
        log = work_logs[i]
        # Entries are displayed one at a time with the ability to page through
        # records (previous/next/back).
        # print("choice loop" + "," + str(log["show_log"]) + "," + str(
        #    i) + "," + choice + str(work_logs.count()))

        show_menu_header("Display Entries")
        print("Name: {} \nDate: {} \nTask Title: {} \nMinutes Spent: {} "
              "\nNotes(Optional): {}"
              .format(log["name"], log["date"], log["task_title"],
                      str(log["minutes"]),
                      log["notes"]))
        choice = input("""What would like you like to do? [E]dit record /
        [D]elete record / [N]ext record /
        [P]revious record / [R]eturn to Main Menu>""").lower()

        # Entries can be deleted and edited, letting user change the date,
        # task name, time spent, and/or notes.
        if choice == 'e':
            # print("You chose to edit")
            edited_entry_information = gather_entry_information(True)
            # print(log)
            # print(edited_entry_information)
            # for log in work_logs:
            #    print(log)
            q = (WorkLog.
                 update({WorkLog.name: edited_entry_information["name"],
                         WorkLog.date: edited_entry_information["date"],
                         WorkLog.task_title:
                             edited_entry_information["task_title"],
                         WorkLog.minutes:
                             edited_entry_information["minutes"],
                         WorkLog.notes:
                             edited_entry_information["notes"],
                         })
                 .where(WorkLog.name == log["name"],
                        WorkLog.date == log["date"],
                        WorkLog.task_title == log["task_title"],
                        WorkLog.minutes == log["minutes"],
                        WorkLog.notes == log["notes"]))
            q.execute()
            log["name"] = edited_entry_information["name"]
            log["date"] = edited_entry_information["date"]
            log["task_title"] = edited_entry_information["task_title"]
            log["minutes"] = edited_entry_information["minutes"]
            log["notes"] = edited_entry_information["notes"]
            # for log in work_logs:
            #    print(log)
        elif choice == 'd':
            # print("You chose to delete the record")
            # print(log)
            # for log in work_logs:
            #    print(log)
            q = (
                WorkLog.delete()
                .where(WorkLog.name == log["name"],
                       WorkLog.date == log["date"],
                       WorkLog.task_title == log["task_title"],
                       WorkLog.minutes == log["minutes"],
                       WorkLog.notes == log["notes"]))
            q.execute()
            break
        # Entries are displayed one at a time with the ability to page through
        # records (previous/next/back).
        elif choice == 'n':
            print("You chose go to the next record")
            if i == work_logs.count() - 1:
                i = 0
            else:
                i += 1
        elif choice == 'p':
            # print("You chose go to the previous record")
            if i == 0:
                i = work_logs.count() - 1
            else:
                i -= 1
        elif choice == 'r':
            # print("You chose to return to the main menu")
            # overwrite_work_log(work_logs)
            run_main_menu()
            break
        else:
            print("You did not enter a valid choice, please only enter "
                  "letters from the list")


if __name__ == "__main__":
    db.connect()
    # db.drop_tables([WorkLog])
    db.create_tables([WorkLog], safe=True)
    # unittest.main()
    run_main_menu()
    # display_find_menu()
