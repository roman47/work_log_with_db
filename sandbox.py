


"""from collections import OrderedDict
import datetime
import sys
import os

from peewee import *
db = SqliteDatabase('students.db')


class Student(Model):
    username = CharField(max_length=255, unique=True)
    points = IntegerField(default=0)

    class Meta:
        database = db

def menu_loop():
    choice = None
    while choice != 'q':
        clear()
        print ("enter q to quit.")
        for key,value in menu.items():
            print('{}) {}'.format(key,value.__doc__))
        choice = input('Action: ').lower().strip()
        if choice in menu:
            clear()
            menu[choice]()

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


menu = OrderedDict([('a', add_entry),
                    ('v', view_entry),
                    ('s', view_entry),
                    ])

def add_entry():
    print('enter your entry. Please ')
    data = sys.stdin.read().strip()

    if data:
        if input('Save entry? [Y/n/ ').lower() != 'n':
            Entry.create(content=data)
            print("Saved successfully!")

def view_entries(search_query=None):
    entries = Entry.select().order_by(Entry.timestamp.desc())
    if search_query:
        entries = entries.where(Entry.content.contains(search_query))

    for entry in entries:
        timestamp = entry.timestamp.strftime('%A %B %d, %Y %I:%M%p')
        clear()
        print(timestamp)
        print("="*len(timestamp))
        print(entry.content)
        print("\n\n" + "="*len(timestamp))
        print("N) next entry")
        print("q) return to main menu")

        next_action = input('Action: [Nq] ').lower().strip()
        if next_action == 'q':
            break

def search_entries():
    view_entries(input('Search query:'))

def delete_entry(entry):
    if input("Are you sure [yN] ").lower() == 'y':
        entry.delete_instance()
        print("Entry Deleted!")

if __name__ == '__main__':
    db.connect()
    db.create_tables([Student], safe=True)
"""

