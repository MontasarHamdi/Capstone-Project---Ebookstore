import sqlite3  # import SQL module to work with database
print("\t----- EBOOKSTORE PROGRAM -----")  # NOQA


# Define 4 functions for each menu operation.
def enter_book():
    title = input("Enter the title of the book: ").lower()
    author = input("Enter the author of the book: ").lower()
    quantity = int(input(f"Enter quantity of {title} available: "))
    # No need for ID as it is auto incremented. Use SQL INSERT command to add new values to database.
    cur.execute('INSERT INTO ebookstore (title, author, qty) values (?, ?, ?)', (title, author, quantity))  # NOQA -typo
    db.commit()
    print("**New book has been added to the ebookstore database!**")  # NOQA -TYPO


def update_book():
    try:  # Defensive programming - only enter integer
        id = int(input('Enter the id of book that you want to update: '))
    except ValueError:
        print("Error. Only enter numbers. Try again")
    else:
        title = input('Enter the new title: ')
        author = input('Enter the updated author name: ')
        quantity = int(input('Enter the new quantity: '))
        # Use SQL UPDATE command to update new values in database.
        cur.execute('UPDATE ebookstore SET title=?, author=?, qty=? WHERE id=?', (title, author, quantity, id))  # NOQA -typo
        db.commit()
        print(f"Book ID: {id} has been updated")


def delete_book():
    try:  # Defensive programming
        id = int(input('Enter the book id to delete: '))
    except ValueError:
        print("Only enter numbers. Try again!")
    # Use SQL DELETE command to delete book from database.
    else:
        cur.execute('DELETE FROM ebookstore WHERE id=?', (id,))  # NOQA - TYPO
        db.commit()
        print(f"Book ID: {id} has been deleted!")


def search_book():
    author = input('Input the author name to search book for: ').lower()
    # Use SQL SELECT*FROM command to find book in database based on author entry.
    cur.execute('SELECT * FROM ebookstore where author like ?', (author,))  # NOQA - TYPO
    results = cur.fetchall()  # Fetch all results from above statement
    if results:
        for row in results:  # Use for loop to print requested book
            print("Requested book: ", str(row[0]) + ' | ' + row[1] + ' | ' + row[2] + ' | ' + str(row[3]))
    else:
        print('Books have not been found in ebookstore database.')  # NOQA - TYPO


# In main block, create connection to database bookstore_db file and store in variable db. # NOQA -TYPO
# Learned about autoincrement here: link>>> https://www.w3schools.com/sql/sql_autoincrement.asp
if __name__ == '__main__':
    db = sqlite3.connect('bookstore_db')  # NOQA -TYPO
    cur = db.cursor()  # Create cursor object allowing us to execute SQL.
    cur.execute('DROP TABLE IF EXISTS ebookstore')  # NOQA -TYPO
    # Create table
    table = ''' CREATE TABLE ebookstore  
    (id integer primary key AUTOINCREMENT,
    Title varchar(255),
    Author varchar(30),
    Qty integer);'''  # NOQA - TYPO, use autoincrement for ID so a new ID (+1) is generated for every new book addition.
    cur.execute(table)
    # Insert data into table
    data = [
        (3001, "a tale of two cities", "charles dickens", 30),
        (3002, "harry potter and the philosopher's stone", "j.k. rowling", 40),
        (3003, "the lion, the witch and the wardrobe", "c.s. lewis", 25),
        (3004, "the lord of the rings", "j.r.r tolkein", 37),
        (3005, "alice in wonderland", "lewis carrol", 12)]

    cur.executemany("INSERT INTO ebookstore VALUES(?, ?, ?, ?)", data)  # NOQA - TYPO
    db.commit()

    while True:
        choice = input('''\nTo choose option enter number: 
1. Enter Book\n
2. Update Book\n
3. Delete Book\n
4. Search Book\n
0. Exit: ''')
        if choice == '1':
            enter_book()
        elif choice == '2':
            update_book()
        elif choice == '3':
            delete_book()
        elif choice == '4':
            search_book()
        elif choice == '0':
            break
        else:
            print('Incorrect entry. Try again.')

    print('Thank you for using EBookStore program!')
    db.close()  # When user exits, use close function on connection object db.
