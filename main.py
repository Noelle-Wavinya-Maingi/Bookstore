from database.db import Base, engine
import click
from commands.book import (
    TextStyle,
    add_book,
    delete_book,
    return_book,
    borrow_book,
    buy_book,
    update_book,
)
from commands.user import add_user, delete_user, list_users
from commands.fines import pay_fine
from commands.lists import list_books, list_borrowed_books, search


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
    click.echo("10. Update Book Records")
    click.echo("11. Delete User Records")
    click.echo("12. Delete Book Records")
    click.echo("13. Pay Fines")
    click.echo(f"{TextStyle.RED}14. Quit" + TextStyle.RESET)

    print_separator()

    option = click.prompt("Enter an option number")
    while True:
        execute_option(option)
        if option == "14":
            break


# Helper function to execute chosen options
def execute_option(option):
    while option not in [
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "10",
        "11",
        "12",
        "13",
        "14",
    ]:
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
        update_book()
    elif option == "11":
        delete_user()
    elif option == "12":
        delete_book()
    elif option == "13":
        pay_fine()
    elif option == "14":
        click.echo(
            f"{TextStyle.YELLOW} Thank you for choosing this bookstore!"
            + TextStyle.RESET
        )
    else:
        execute_option(option)


cli.add_command(menu)


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    while True:
        menu()
