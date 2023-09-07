from database.db import Base, engine, Session
import click
from models import User, Book, BorrowedBook, Fines
import datetime


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
    click.echo("5. List of books")
    click.echo("6. Buy a book")
    click.echo(f"{TextStyle.RED}7. Quit" + TextStyle.RESET)

    print_separator()

    option = click.prompt("Enter an option number")
    while True:
        execute_option(option)
        if option == "7":
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


# Define the 'list-books' command
@cli.command()
def list_books():
    """List all the books in the system"""

    db = Session()
    books = db.query(Book).all()

    # Check if there are no books in the system
    if not books:
        # If there are no books, display a message indicating that no books were found
        click.echo(f"{TextStyle.YELLOW}No books found." + TextStyle.RESET)
    else:
        # If there are books in the system, display a header indicating "Books:"
        click.echo(f"{TextStyle.CYAN}Books:")

        # Iterate over each book in the list of books
        for book in books:
            # Determine the status of the book (Borrowed or Available)
            status = "Borrowed" if not book.status else "Available"

            # Display information about the book, including its title, author, status, and inventory
            click.echo(
                f"{TextStyle.BOLD} {TextStyle.CYAN}- {book.title} by {book.author} ({status}) || {book.inventory} books remaining."
                + TextStyle.RESET
            )


# Helper function to execute chosen options
def execute_option(option):
    while option not in ["1", "2", "3", "4", "5", "6", "7"]:
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
        list_books()
    elif option == "7":
        click.echo(
            f"{TextStyle.YELLOW} Thank you for choosing this bookstore!"
            + TextStyle.RESET
        )


cli.add_command(menu)

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    while True:
        menu()