from database.db import Session
import click
from models import User, Book, BorrowedBook, Sales
from commands.book import TextStyle


@click.group()
def list_commands():
    pass


# Define the 'list-books' command
@list_commands.command()
def list_books():
    """List all the books in the system"""

    db = Session()

    try:
        # Query the Book table to get all books
        books = db.query(Book).all()

        # Check if there are no books in the system
        if not books:
            click.echo(f"{TextStyle.YELLOW}No books found in the system." + TextStyle.RESET)
            return

        # If there are books, display a header indicating "Books:"
        click.echo(f"{TextStyle.CYAN}Books:")

        # Iterate over each book and display its details
        for book in books:
            click.echo(
                f"{TextStyle.BOLD} {TextStyle.CYAN}- Title: {book.title} | Author: {book.author} | Status: {book.status} | Inventory: {book.inventory} | Total Sales Amount: {book.total_sales}"
                + TextStyle.RESET
            )

    except Exception as e:
        # Handle any exceptions related to database access
        click.echo(f"{TextStyle.RED}Error accessing the database: {str(e)}" + TextStyle.RESET)
        db.close()



# List books borrowed by users and their return dates
@list_commands.command()
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
@list_commands.command()
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
