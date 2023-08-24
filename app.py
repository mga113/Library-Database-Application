import datetime
import random
import sqlite3

conn = sqlite3.connect('library.db')
cursor = conn.cursor()
cursor.execute("PRAGMA foreign_keys = ON;")  # Enforce foreign key constraints.
print("Opened database successfully")

def borrow_item(cursor, item_id: int, patron_id: int) -> None:
    borrow_date = datetime.date.today()
    due_date = borrow_date + datetime.timedelta(weeks=2)
    cursor.execute("INSERT INTO Borrows (item_id, patron_id, borrow_date, due_date) VALUES (?, ?, ?, ?);",
                   (item_id, patron_id, borrow_date, due_date))
    conn.commit()
    print()
    print("Your item is checked out.")
    print("Please keep your item id when returning:", item_id)
    print("Due date:", due_date)

def return_item(cursor, item_id: int) -> None:
    library_id = random.randint(1, 10)
    cursor.execute("INSERT INTO Availability (library_id, item_id) VALUES (?, ?);",
                   (library_id, item_id))
    conn.commit()
    print()
    print("Item returned successfully.")
    print("Please check your current balance for any late fines.")

def donate_item(cursor, title: str, author: str, pub_date: str, item_type: str, isbn: int) -> None:
    cursor.execute("INSERT INTO Items (title, author, pub_date, type, isbn) VALUES (?, ?, ?, ?, ?);",
                   (title, author, pub_date, item_type, isbn))
    cursor.execute("INSERT INTO Availability (library_id, item_id) VALUES (?, (SELECT MAX(item_id) FROM Items));",
                   (random.randint(1, 10),))
    conn.commit()
    print()
    print("Item added to collections.")
    print("Thank you for your contributions!")

def register_event(cursor, event_id: int, patron_id: int) -> None:
    cursor.execute("INSERT INTO Registers (event_id, patron_id) VALUES (?, ?);", (event_id, patron_id))
    conn.commit()
    print()
    print("You are registered for the event.")
    print("See you soon.")

def volunteer(cursor, name: str, address: str, dob: str) -> None:
    cursor.execute("INSERT INTO Personnel (library_id, name, address, position, dob) VALUES (?, ?, ?, ?, ?);",
                   (random.randint(1, 10), name, address, "Volunteer", dob))
    conn.commit()
    print()
    print("Welcome to the team.")
    print("Thank you for volunteering!")

def ask_librarian(cursor) -> None:
    print()
    print("Available librarians:")
    print()
    all_librarians = cursor.execute("SELECT personnel_id, name, position FROM Personnel WHERE position LIKE ?;",
                                    ("%Librarian%",)).fetchall()
    prettyprint(all_librarians)
    if all_librarians:
        librarian_id = input("Enter the id (1st number) of the librarian you would like to ask for help: ")
        print()
        assert(int(librarian_id) in [librarian[0] for librarian in all_librarians])
        print(f"Your request has been assigned to librarian {librarian_id}.\nPlease monitor your inbox for replies.")

def prettyprint(tuples: list[tuple]) -> None:
    if tuples:
        for tuple in tuples:
            print(tuple)
        print()
    else:
        print("No records found.")

# Constants for menu options
OPTION_EXIT = '0'
OPTION_FIND_ITEM = '1'
OPTION_BORROW_ITEM = '2'
OPTION_RETURN_ITEM = '3'
OPTION_DONATE_ITEM = '4'
OPTION_FIND_EVENT = '5'
OPTION_REGISTER_EVENT = '6'
OPTION_VOLUNTEER = '7'
OPTION_ASK_LIBRARIAN = '8'

def get_main_menu() -> str:
    print()
    print('Select one of the following options.')
    print()
    print('1: Find an item in the library')
    print('2: Borrow an item from the library')
    print('3: Return a borrowed item')
    print('4: Donate an item to the library ')
    print('5: Find an event in the library')
    print('6: Register for an event in the library')
    print('7: Volunteer for the library')
    print('8: Ask for help from a librarian')
    print('0: Exit')
    return input('-> ')

def find_records_by_field(cursor, table: str, field: str, value: str, is_string: bool) -> list[tuple]:
    if is_string:
        # e.g. WHERE title LIKE "%ar%"
        where_clause = f"WHERE {field} LIKE \"%{value}%\""
    else:
        # e.g. WHERE ISBN = 90238098240
        where_clause = f"WHERE {field} = {value}"
    query = f"SELECT * FROM {table} {where_clause};"
    return cursor.execute(query).fetchall()

def get_item_search_menu() -> str:
    print()
    print('Search items with one of the following options.')
    print()
    print('1: title')
    print('2: author')
    print('3: publisher')
    print('4: type ')
    print('5: publication date')
    print('6: ISBN')
    print('0: Exit')
    return input('-> ')

def find_items_by_field(cursor, field: str, value: str, is_string: bool) -> list[tuple]:
    return find_records_by_field(cursor, 'Items', field, value, is_string)

def input_items_to_find(find_item_option: str) -> list[tuple]:
    match find_item_option:
        case '1':
            # Find by title
            search_value = input("Enter item's title to search: ")
            return find_items_by_field(cursor, "title", search_value, True)
        case '2':
            # Find by author
            search_value = input("Enter item's author to search: ")
            return find_items_by_field(cursor, "author", search_value, True)
        case '3':
            # Find by publisher
            search_value = input("Enter item's publisher to search: ")
            return find_items_by_field(cursor, "publisher", search_value, True)
        case '4':
            # Find by type
            search_value = input("Enter item's type to search: ")
            return find_items_by_field(cursor, "type", search_value, True)
        case '5':
            # Find by pub_date
            search_value = input("Enter item's publishing date to search: ")
            return find_items_by_field(cursor, "pub_date", search_value, True)
        case '6':
            # Find by ISBN
            search_value = input("Enter item's ISBN to search: ")
            return find_items_by_field(cursor, "ISBN", search_value, False)

def quote(str: str) -> str:
    return "\"" + str + "\""

def get_event_search_menu() -> str:
    print()
    print('Search events with one of the following options.')
    print()
    print('1: event id')
    print('2: name')
    print('3: event type')
    print('4: date')
    print('5: room number')
    print('6: target audience')
    print('0: Exit')
    return input('-> ')

def find_events_by_field(cursor, field: str, value: str) -> list[tuple]:
    return find_records_by_field(cursor, 'Events', field, value, field != 'event_id')

def input_events_to_find(find_event_option: str) -> list[tuple]:
    match find_event_option:
        case '1':
            # Find by event id
            search_value = input("Enter event id to search: ")
            return find_events_by_field(cursor, "event_id", search_value)
        case '2':
            # Find by name
            search_value = input("Enter event name to search: ")
            return find_events_by_field(cursor, "name", search_value)
        case '3':
            # Find by event type
            search_value = input("Enter event type to search: ")
            return find_events_by_field(cursor, "type", search_value)
        case '4':
            # Find by date
            search_value = input("Enter event's date to search: ")
            return find_events_by_field(cursor, "time", search_value)
        case '5':
            # Find by room number
            search_value = input("Enter room number to search: ")
            return find_events_by_field(cursor, "room_no", search_value)
        case '6':
            # Find by target audience
            search_value = input("Enter target audience to search: ")
            return find_events_by_field(cursor, "target_audience", search_value)

def main() -> None:
    '''Main loop'''
    while True:
        main_menu_option = get_main_menu()

        if main_menu_option == OPTION_EXIT:
            break

        elif main_menu_option == OPTION_FIND_ITEM:
            # Find items.
            items = input_items_to_find(get_item_search_menu())
            prettyprint(items)

        elif main_menu_option == OPTION_BORROW_ITEM:
            # Borrow an item.
            items = input_items_to_find(get_item_search_menu())
            prettyprint(items)
            if items:
                # Borrow this item.
                item_id = input("Enter the id (1st number) of the item you want to borrow: ")
                patron_id = input("Enter your account number / patron id (1-10): ")
                borrow_item(cursor, item_id, patron_id)

        elif main_menu_option == OPTION_RETURN_ITEM:
            # Return a borrowed item
            item_id = input("Please enter the id of the item you are returning: ")
            return_item(cursor, item_id)

        elif main_menu_option == OPTION_DONATE_ITEM:
            # Donate an item to the library
            title = input('Please enter the title: ')
            author = input('Please enter the author: ')
            pub_date = input('Please enter the publication date: ')
            item_type = input('Please enter the item type: ')
            isbn = input('Please enter a 13-digit ISBN number: ')
            donate_item(cursor, title, author, pub_date, item_type, isbn)

        elif main_menu_option == OPTION_FIND_EVENT:
            # Find an event in the library
            events = input_events_to_find(get_event_search_menu())
            prettyprint(events)

        elif main_menu_option == OPTION_REGISTER_EVENT:
            # Register for an event in the library
            events = input_events_to_find(get_event_search_menu())
            prettyprint(events)
            if events:
                # Register for this event.
                event_id = input("Enter the id (1st number) of the event you want to register: ")
                patron_id = input("Enter your account number / patron id (1-10): ")
                register_event(cursor, event_id, patron_id)

        elif main_menu_option == OPTION_VOLUNTEER:
            # Volunteer for the library
            name = input('Please enter your name: ')
            address = input('Please enter your address: ')
            dob = input('Please enter your date of birth: ')
            volunteer(cursor, name, address, dob)

        elif main_menu_option == OPTION_ASK_LIBRARIAN:
            # Ask for help from a librarian
            ask_librarian(cursor)

if __name__ == "__main__":
    main()

conn.close()
