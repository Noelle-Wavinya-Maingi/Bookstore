from database.db import Base, engine, Session
import click
from models import User, Book, BorrowedBook, Fines, Sales
from datetime import datetime


# Define ANSI codes for formatting
class TextStyle:
    BOLD = "\x1b[1m"
    RESET = "\x1b[0m"
    RED = "\x1b[31m"
    GREEN = "\x1b[32m"
    YELLOW = "\x1b[33m"
    CYAN = "\x1b[36m"


# Define a CLI group
@click.group()
def cli():
    pass


# Helper function to print a separator
def print_separator():
    print(TextStyle.BOLD + "*" * 70 + TextStyle.RESET)


# Define the main menu command
@cli.command()
def menu():
    """Main Menu - Choose an option"""

    print_separator()

    click.echo(TextStyle.CYAN + "Choose an option:")
    click.echo(f"{TextStyle.BOLD}1. Add a user")
    click.echo("2. Add a book")
    click.echo("3. Borrow a book")
    click.echo("4. Return a book")
    click.echo("5. Buy a book")
    click.echo("6. List all books")
    click.echo("7. List all users")
    click.echo("8. List of Borrowed Books")
    click.echo("9. Search")
    click.echo("10. Update records")
    click.echo(f"{TextStyle.RED}11. Quit" + TextStyle.RESET)

    print_separator()

    option = click.prompt("Enter an option number")
    while True:
        execute_option(option)
        if option == "11":
            break


# Set to store unique usernames
unique_usernames = set()


# Define the 'add-user' command
@cli.command()
@click.option("--username", prompt="Add a username", help="Enter the username")
def add_user(username):
    """
    Add a user to the system
    """
    db = Session()
    existing_user = db.query(User).filter(User.username == username).first()

    if existing_user:
        db.close()
        click.echo(f"{TextStyle.RED} {username} already exists.")
        return

    user = User(username=username)
    db.add(user)
    db.commit()
    db.close()
    unique_usernames.add(username)
    click.echo(f"{TextStyle.GREEN} {username} added successfully.")


# Dictionary to store book data
books = {}


# Define the 'add-book' command
@cli.command()
@click.option(
    "--title", prompt="Enter the title of the book", help="Enter the title of the book"
)
@click.option(
    "--author",
    prompt="Enter the author of the book",
    help="Enter the author of the book",
)
@click.option(
    "--quantity", prompt="Enter the number of books", help="Enter the number of books"
)
@click.option(
    "--price",
    prompt="Enter the price of one unit item",
    help="Enter the price of one unit item",
)
def add_book(title, author, quantity, price):
    """Add a book to the system"""

    db = Session()
    book = Book(
        title=title, author=author, status=True, inventory=quantity, price=price
    )

    db.add(book)
    db.commit()
    db.close()

    # Update the books dictionary with book information
    books[title] = {
        "author": author,
        "status": True,
        "quantity": int(quantity),
        "price": float(price),
    }

    click.echo(f"{TextStyle.GREEN} {title} by {author} has been added successfully.")


# Define the 'borrow-book' command
@cli.command()
@click.option("--user_name", prompt="Enter the username", help="Enter the username")
def borrow_book(user_name):
    """
    Borrow a book from the system
    """
    db = Session()

    user = db.query(User).filter(User.username == user_name).first()

    if user is None:
        db.close()
        click.echo(f"{TextStyle.RED}{user_name} not found." + TextStyle.RESET)
        return

    # Check if the user already has a book borrowed
    if db.query(BorrowedBook).filter(BorrowedBook.user_id == user.id).first():
        db.close()
        click.echo(
            f"{TextStyle.RED}{user_name} already has a book borrowed. "
            " Please return your borrowed book before borrowing another."
            + TextStyle.RESET
        )
        return

    book_title = click.prompt("Enter the book title")

    book = db.query(Book).filter(Book.title == book_title).first()

    if book is None:
        db.close()
        click.echo(f"{TextStyle.RED}{book_title} not found." + TextStyle.RESET)
        return

    # Check if the book is already borrowed
    if db.query(BorrowedBook).filter(BorrowedBook.book_id == book.id).first():
        db.close()
        click.echo(
            f"{TextStyle.RED}Book '{book_title}' is already borrowed." + TextStyle.RESET
        )
        return

    # Calculate the return date as two days from the current date
    return_date = datetime.datetime.now() + datetime.timedelta(days=2)

    # Create a new BorrowedBook entry with the user's ID, book's ID, and return date
    borrow_book = BorrowedBook(
        user_id=user.id, book_id=book.id, return_date=return_date
    )
    db.add(borrow_book)

    # Update the book status to False (indicating it's borrowed)
    book.status = False

    db.commit()
    db.close()

    click.echo(
        f"{TextStyle.GREEN}{user_name} has borrowed '{book_title}' successfully."
        + TextStyle.RESET
    )


# Define the 'return-book' command
@cli.command()
@click.option(
    "--book_title", prompt="Enter the book title", help="Enter the book title to return"
)
def return_book(book_title):
    """
    Return a book to the system
    """
    db = Session()

    # Find the borrowed book entry based on the book title
    borrowed_book = (
        db.query(BorrowedBook).join(Book).filter(Book.title == book_title).first()
    )

    # Check if the book has not been borrowed
    if not borrowed_book:
        # If the book has not been borrowed, close the database session
        db.close()

        # Display a message indicating that the book was not found in the borrowed books
        click.echo(
            f"{TextStyle.RED}Book '{book_title}' not found in the borrowed books."
            + TextStyle.RESET
        )
    else:
        # If the book has been borrowed, proceed with returning the book

        # Get the return date of the borrowed book and the current date
        return_date = borrowed_book.return_date
        current_date = datetime.datetime.now()

        # Check if the book is returned late (current date is greater than return date)
        if current_date > return_date:
            # Calculate the number of days late
            days_late = (current_date - return_date).days

            # Calculate the late fee based on the number of days late
            late_fee = days_late * 200

            # Display a message indicating that the book is returned late and the late fee
            click.echo(
                f"{TextStyle.RED}{book_title} returned late by {days_late} days."
                f" You are charged Ksh.{late_fee} as a late fee." + TextStyle.RESET
            )

            # Get the user ID associated with the borrowed book
            user_id = borrowed_book.user_id

            # Create a fine entry with the user's ID and the calculated late fee
            fine_entry = Fines(user_id=user_id, amount=late_fee)

            # Add the fine entry to the database
            db.add(fine_entry)
        else:
            # If the book is returned on time, display a success message
            click.echo(
                f"{TextStyle.GREEN}{book_title} returned successfully."
                + TextStyle.RESET
            )

        # Set the status of the book back to "Available"
        borrowed_book.book.status = True

        # Delete the borrowed book entry from the database
        db.delete(borrowed_book)
        db.commit()
        db.close()

        # Display a message indicating that the book has been returned successfully
        click.echo(
            f"{TextStyle.GREEN}Book '{book_title}' returned successfully."
            + TextStyle.RESET
        )


# Define the 'buy-book' command
@cli.command()
@click.option(
    "--book_title", prompt="Enter the book title", help="Enter the book title"
)
@click.option(
    "--quantity",
    prompt="Enter the number of books you want to purchase",
    help="Enter the number of books you want to purchase",
)
def buy_book(book_title, quantity):
    """Buy a book from the system"""

    db = Session()

    book = db.query(Book).filter(Book.title == book_title).first()

    if book is None:
        db.close()
        click.echo(f"{TextStyle.RED} {book_title} not found." + TextStyle.RESET)
        return

    # Check if there are enough books in the inventory to sell
    try:
        quantity = int(quantity)
    except ValueError:
        db.close()
        click.echo(
            f"{TextStyle.RED} Invalid Quantity. Please enter a valid number"
            + TextStyle.RESET
        )
        return

    if book.inventory < quantity:
        db.close()
        click.echo(
            f"{TextStyle.RED} Sorry, there are only {book.inventory} {book_title}books available."
            + TextStyle.RESET
        )
        return

    # Calculate the total amount for the sale
    total_amount = float(quantity) * book.price

    # Confirm the purchase with the user
    click.echo(
        f"{TextStyle.CYAN} You are about to purchase {quantity} {book_title} books for a total of Ksh.{total_amount}."
        + TextStyle.RESET
    )
    confirmation = click.prompt("Are you sure you want to proceed? (yes/no)")

    if confirmation.lower() != "yes":
        db.close()
        click.echo(f"{TextStyle.YELLOW} Purchase Cancelled." + TextStyle.RESET)
        return

    # Get the current date and time
    purchase_time = datetime.now()

    # Update the book's sales records with the purchase date and time
    sale = Sales(
        book_id=book.id,
        quantity=quantity,
        total_amount=total_amount,
        purchase_time=purchase_time,
    )

    # Update the book's inventory and total sales amount
    book.inventory -= quantity
    book.total_sales += total_amount

    db.add(sale)
    db.commit()
    db.close()

    click.echo(
        f"{TextStyle.GREEN} {quantity} '{book_title}' books purchased successfully for a total of Ksh.{total_amount}."
        + TextStyle.RESET
    )

    # Define the 'list-books' command


@cli.command()
def list_books():
    """List all the books in the system"""

    db = Session()

    # Query the Sales table and join it with the Book table to get sales data with book titles
    sales = (
        db.query(Sales, Book)
        .join(Book, Sales.book_id == Book.id)
        .order_by(Sales.purchase_time.desc())
        .all()
    )

    # Check if there are no sales records
    if not sales:
        # If there are no sales, display a message indicating that no sales were found
        db.close()
        click.echo(f"{TextStyle.YELLOW}No sales found." + TextStyle.RESET)
        return

    # If there are sales records, display a header indicating "Sales:"
    click.echo(f"{TextStyle.CYAN}Books:")

    # Iterate over each sale and display the sale information, including the book title
    for sale, book in sales:
        purchase_time = sale.purchase_time.strftime("%Y-%m-%d %H:%M:%S")
        click.echo(
            f"{TextStyle.BOLD} {TextStyle.CYAN}- Book: {book.title} |Author: {book.author} |Status: {book.status} |Inventory: {book.inventory} | Quantity: {sale.quantity} | Total Amount: Ksh.{sale.total_amount} | Purchase Time: {purchase_time}"
            + TextStyle.RESET
        )

    db.close()


# Add a new command to list all users and their fine information
@cli.command()
def list_users():
    """List all users and their fine information"""

    db = Session()

    # Query the User and Fines tables to get user details and fines
    users_with_fines = (
        db.query(User, Fines).outerjoin(Fines, User.id == Fines.user_id).all()
    )

    # Check if there are no users in the system
    if not users_with_fines:
        # If there are no users, display a message indicating that no users were found
        db.close()
        click.echo(f"{TextStyle.YELLOW}No users found." + TextStyle.RESET)
        return

    # If there are users, display a header indicating "Users:"
    click.echo(f"{TextStyle.CYAN}Users:")

    # Iterate over each user and display their details, including fines
    for user, fine in users_with_fines:
        # Determine if the user has fines and get the fine amount
        if fine is None:
            fine_amount = 0
        else:
            fine_amount = fine.amount

        click.echo(
            f"{TextStyle.BOLD} {TextStyle.CYAN}- Username: {user.username} | Fine Amount: Ksh.{fine_amount}"
            + TextStyle.RESET
        )

    db.close()


# List books borrowed by users and their return dates
@cli.command()
def list_borrowed_books():
    """List books borrowed by users and their return dates"""

    db = Session()

    # Query BorrowedBook table and join it with User and Book table
    borrowed_books = (
        db.query(BorrowedBook, User, Book)
        .join(User, BorrowedBook.user_id == User.id)
        .join(Book, BorrowedBook.book_id == Book.id)
        .all()
    )

    # Check if there are no borrowed books, if not display a message
    if not borrowed_books:
        db.close()
        click.echo(
            f"{TextStyle.YELLOW} No books are currently borrowed." + TextStyle.RESET
        )
        return

    # If there are borrowed books, display a header indicating "Borrowed Books:"
    click.echo(f"{TextStyle.CYAN}Borrowed Books: ")

    # Iterate ober each borrowed book and display the book title, user and return date
    for borrowed_book, user, book in borrowed_books:
        return_date = borrowed_book.return_date.strftime("%Y-%m-%d %H:%M:%S")
        click.echo(
            f"{TextStyle.BOLD} {TextStyle.CYAN}- Book Title: {book.title} | Borrower: {user.username} | Return Date: {return_date}"
            + TextStyle.RESET
        )

        db.close()


# Add search for users or books
@cli.command()
@click.option("--query", prompt="Enter a search term", help="Enter a search term")
def search(query):
    """Search for users or books"""

    db = Session()

    # Query the User table to search for matching usernames
    matching_users = db.query(User).filter(User.username.ilike(f"%{query}%")).all()

    # Query the Book table to search for matching book titles or authors
    matching_books = (
        db.query(Book)
        .filter(Book.title.ilike(f"%{query}%") | Book.author.ilike(f"%{query}%"))
        .all()
    )

    db.close()

    # Check if there are no matching users or books, if not display a message indicating that no results were found
    if not matching_users and not matching_books:
        click.echo(
            f"{TextStyle.YELLOW}No matching users or books found." + TextStyle.RESET
        )
        return

    # If there are matching users, display a header and list the matching users
    if matching_users:
        click.echo(f"{TextStyle.CYAN}Matching Users")
        for user in matching_users:
            click.echo(
                f"{TextStyle.BOLD} {TextStyle.CYAN}- Username: {user.username}"
                + TextStyle.RESET
            )

    # If there are matching books, display a header and list the matching books
    if matching_books:
        click.echo(f"{TextStyle.CYAN}Matching Books")
        for book in matching_books:
            click.echo(
                f"{TextStyle.BOLD} {TextStyle.CYAN}- Title: {book.title} | Author: {book.author}"
                + TextStyle.RESET
            )


# Define the 'update' command with subcommands
@cli.command()
@click.option(
    "--record_type",
    type=click.Choice(["sales", "fines", "users", "books"]),
    prompt="Enter the record type",
    help="Enter the record type to update (sales, fines, users, books)",
)
def update(record_type):
    """Update records in the database"""

    if record_type == "sales":
        update_sales()

    elif record_type == "fines":
        update_fine()

    elif record_type == "users":
        update_users()

    elif record_type == "books":
        update_books()


# Define subcommands for sales records
def update_sales():
    pass


def update_fine():
    pass


def update_users():
    pass


def update_books():
    pass


# Helper function to execute chosen options
def execute_option(option):
    while option not in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"]:
        click.echo(
            f"{TextStyle.RED}Invalid option. Please choose a valid option."
            + TextStyle.RESET
        )
        option = click.prompt("Enter a valid option")

    if option == "1":
        add_user()
    elif option == "2":
        add_book()
    elif option == "3":
        borrow_book()
    elif option == "4":
        return_book()
    elif option == "5":
        buy_book()
    elif option == "6":
        list_books()
    elif option == "7":
        list_users()
    elif option == "8":
        list_borrowed_books()
    elif option == "9":
        search()
    elif option == "10":
        update()
    elif option == "11":
        click.echo(
            f"{TextStyle.YELLOW} Thank you for choosing this bookstore!"
            + TextStyle.RESET
        )


cli.add_command(menu)

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    while True:
        menu()
