from database.db import Base, engine, Session
import click
from models import User, Book


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

#Dictionary to store book data
books = {}

#Define the 'add-book' command
@cli.command()
@click.option("--title", prompt = "Enter the title of the book", help = "Enter the title of the book")
@click.option("--author", prompt = "Enter the author of the book", help = "Enter the author of the book")
@click.option("--quantity", prompt = "Enter the number of books", help = "Enter the number of books")
@click.option("--price", prompt = "Enter the price of one unit item", help = "Enter the price of one unit item")
def add_book(title, author, quantity, price):
    """Add a book to the system"""

    db = Session()
    book = Book(title = title, author = author, status = True, inventory = quantity, price = price) 

    db.add(book)
    db.commit()
    db.close()

    #Update the books dictionary with book information
    books[title] = {
        "author": author,
        "status": True,
        "quantity": int(quantity),
        "price": float(price),
    }

    click.echo(f"{TextStyle.GREEN} {title} by {author} has been added successfully.")


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