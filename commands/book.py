from database.db import Session
import click
from models import User, Book, BorrowedBook, Fines, Sales
from datetime import datetime, timedelta


# Define ANSI codes for formatting
class TextStyle:
    BOLD = "\x1b[1m"
    RESET = "\x1b[0m"
    RED = "\x1b[31m"
    GREEN = "\x1b[32m"
    YELLOW = "\x1b[33m"
    CYAN = "\x1b[36m"


@click.group()
def book_commands():
    pass


# Dictionary to store book data
books = {}


# Define the 'add-book' command
@book_commands.command()
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
@book_commands.command()
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
    return_date = datetime.now() + timedelta(days=2)

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
@book_commands.command()
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
        current_date = datetime.now()

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

        # Update the arrears status for the user
        user_id = borrowed_book.user_id
        user = db.query(User).filter(User.id == user_id).first()
        fines = (
            db.query(Fines)
            .filter(Fines.user_id == user_id, Fines.arrears == False)
            .all()
        )
        user_arrears = any(fine.arrears for fine in fines)
        user.arrears = user_arrears

        db.commit()
        db.close()

        # Display a message indicating that the book has been returned successfully
        click.echo(
            f"{TextStyle.GREEN}Book '{book_title}' returned successfully."
            + TextStyle.RESET
        )


# Define the 'buy-book' command
@book_commands.command()
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


# Define the 'delete-book' command
@book_commands.command()
@click.option(
    "--title",
    prompt="Enter the title of the book to delete",
    help="Enter the title of the book to delete",
)
def delete_book(title):
    """Delete a book from the system"""

    db = Session()

    book = db.query(Book).filter(Book.title == title).first()

    if book is None:
        db.close()
        click.echo(f"{TextStyle.RED}Book '{title}' not found." + TextStyle.RESET)
        return

    # Check if the book is currently borrowed
    borrowed_book = (
        db.query(BorrowedBook).filter(BorrowedBook.book_id == book.id).first()
    )

    if borrowed_book:
        db.close()
        click.echo(
            f"{TextStyle.RED}Cannot delete book '{title}' as it is currently borrowed."
            + TextStyle.RESET
        )
        return

    # Delete the book from the database
    db.delete(book)
    db.commit()
    db.close()

    # Remove the book from the 'books' dictionary
    del books[title]

    click.echo(
        f"{TextStyle.GREEN}Book '{title}' has been deleted from the system."
        + TextStyle.RESET
    )

    # Define the 'update' command with subcommands


@book_commands.command()
@click.option(
    "--title",
    prompt="Enter the title of the existing book",
    help="Enter the title of the existing book",
)
@click.option(
    "--quantity",
    prompt="Enter the quantity to add",
    help="Enter the quantity to add",
)
@click.option(
    "--price",
    prompt="Enter the new price of the book",
    help="Enter the new price of the book",
)
def update_book(title, quantity, price):
    """Add more existing books to the system and update the price"""

    db = Session()

    book = db.query(Book).filter(Book.title == title).first()

    if book is None:
        db.close()
        click.echo(f"{TextStyle.RED} {title} not found." + TextStyle.RESET)
        return

    # Check if there are enough books in the inventory to add
    try:
        quantity = int(quantity)
    except ValueError:
        db.close()
        click.echo(
            f"{TextStyle.RED} Invalid Quantity. Please enter a valid number"
            + TextStyle.RESET
        )
        return

    # Update the existing book's quantity and price
    book.inventory += quantity
    book.price = float(price)

    db.commit()
    db.close()

    click.echo(
        f"{TextStyle.GREEN} {quantity} more '{title}' books added successfully. "
        f"New price: Ksh.{price}." + TextStyle.RESET
    )
